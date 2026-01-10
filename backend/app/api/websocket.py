from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Set, Optional
import json
from datetime import datetime
import uuid

from ..database import get_async_session
from ..models.chat_message import ChatMessage
from ..models.character import Character
from ..models.game_session import GameSession

router = APIRouter()


class UserConnection:
    """Represents a user's WebSocket connection"""
    def __init__(self, websocket: WebSocket, user_id: str, username: str, character_id: str = None, character_name: str = None):
        self.websocket = websocket
        self.user_id = user_id
        self.username = username
        self.character_id = character_id
        self.character_name = character_name
        self.connected_at = datetime.utcnow()


class ConnectionManager:
    """Manages WebSocket connections for chronicles"""

    def __init__(self):
        # chronicle_id -> set of UserConnection
        self.active_connections: Dict[str, Set[UserConnection]] = {}

    async def connect(self, websocket: WebSocket, chronicle_id: str, user_id: str, username: str,
                      character_id: str = None, character_name: str = None) -> UserConnection:
        await websocket.accept()
        if chronicle_id not in self.active_connections:
            self.active_connections[chronicle_id] = set()

        user_conn = UserConnection(websocket, user_id, username, character_id, character_name)
        self.active_connections[chronicle_id].add(user_conn)
        return user_conn

    def disconnect(self, user_conn: UserConnection, chronicle_id: str):
        if chronicle_id in self.active_connections:
            self.active_connections[chronicle_id].discard(user_conn)
            if not self.active_connections[chronicle_id]:
                del self.active_connections[chronicle_id]

    def get_online_users(self, chronicle_id: str) -> list:
        """Get list of online users in a chronicle"""
        if chronicle_id not in self.active_connections:
            return []
        return [
            {
                "user_id": conn.user_id,
                "username": conn.username,
                "character_id": conn.character_id,
                "character_name": conn.character_name
            }
            for conn in self.active_connections[chronicle_id]
        ]

    def get_user_connection(self, chronicle_id: str, user_id: str) -> Optional[UserConnection]:
        """Get a specific user's connection"""
        if chronicle_id not in self.active_connections:
            return None
        for conn in self.active_connections[chronicle_id]:
            if conn.user_id == user_id:
                return conn
        return None

    async def broadcast(self, chronicle_id: str, message: dict, exclude: UserConnection = None):
        """Broadcast message to all connections in a chronicle"""
        if chronicle_id not in self.active_connections:
            return

        disconnected = set()
        for conn in self.active_connections[chronicle_id]:
            if exclude and conn == exclude:
                continue
            try:
                await conn.websocket.send_json(message)
            except:
                disconnected.add(conn)

        # Clean up disconnected clients
        for conn in disconnected:
            self.active_connections[chronicle_id].discard(conn)

    async def send_personal(self, user_conn: UserConnection, message: dict):
        """Send message to a specific connection"""
        try:
            await user_conn.websocket.send_json(message)
        except:
            pass

    async def send_to_user(self, chronicle_id: str, user_id: str, message: dict):
        """Send message to a specific user in a chronicle"""
        conn = self.get_user_connection(chronicle_id, user_id)
        if conn:
            await self.send_personal(conn, message)


manager = ConnectionManager()


@router.websocket("/chronicle/{chronicle_id}")
async def chronicle_websocket(websocket: WebSocket, chronicle_id: str):
    """WebSocket endpoint for real-time chronicle updates"""

    # Get user info from query params
    user_id = websocket.query_params.get("user_id", "unknown")
    username = websocket.query_params.get("username", "Anonimo")
    character_id = websocket.query_params.get("character_id")
    character_name = websocket.query_params.get("character_name")

    user_conn = await manager.connect(websocket, chronicle_id, user_id, username, character_id, character_name)

    try:
        # Send connection confirmation with online users
        await manager.send_personal(user_conn, {
            "type": "connected",
            "chronicle_id": chronicle_id,
            "online_users": manager.get_online_users(chronicle_id)
        })

        # Notify others that user joined
        await manager.broadcast(chronicle_id, {
            "type": "user_joined",
            "user_id": user_id,
            "username": username,
            "character_id": character_id,
            "character_name": character_name,
            "online_users": manager.get_online_users(chronicle_id)
        }, exclude=user_conn)

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            message_type = message.get("type")
            timestamp = datetime.utcnow().isoformat()

            # ============== CHAT MESSAGES ==============
            if message_type == "chat_message":
                msg_data = message.get("data", {})
                content = msg_data.get("content", message.get("message", ""))
                msg_type = msg_data.get("message_type", "chat")
                recipient_id = msg_data.get("recipient_id")
                char_id = msg_data.get("character_id", character_id)
                char_name = msg_data.get("character_name", character_name)

                # Save to database
                async for db in get_async_session():
                    # Get active session if any
                    session_result = await db.execute(
                        select(GameSession)
                        .where(GameSession.chronicle_id == chronicle_id)
                        .where(GameSession.is_active == True)
                    )
                    active_session = session_result.scalar_one_or_none()

                    chat_msg = ChatMessage(
                        id=str(uuid.uuid4()),
                        chronicle_id=chronicle_id,
                        session_id=active_session.id if active_session else None,
                        user_id=user_id,
                        character_id=char_id,
                        message_type=msg_type,
                        content=content,
                        recipient_id=recipient_id,
                        sender_name=username,
                        character_name=char_name,
                    )
                    db.add(chat_msg)
                    await db.commit()
                    await db.refresh(chat_msg)

                    response = {
                        "type": "chat_message",
                        "data": {
                            "id": chat_msg.id,
                            "content": content,
                            "message_type": msg_type,
                            "character_id": char_id,
                            "character_name": char_name,
                            "recipient_id": recipient_id,
                        },
                        "user_id": user_id,
                        "username": username,
                        "timestamp": timestamp
                    }

                    if msg_type == "whisper" and recipient_id:
                        # Send only to sender and recipient
                        await manager.send_personal(user_conn, response)
                        await manager.send_to_user(chronicle_id, recipient_id, response)
                    else:
                        # Broadcast to everyone
                        await manager.broadcast(chronicle_id, response)
                    break

            # ============== DICE ROLLS ==============
            elif message_type == "dice_roll":
                roll_data = message.get("data", {})
                is_secret = roll_data.get("is_secret", False)

                response = {
                    "type": "dice_roll",
                    "data": roll_data,
                    "user_id": user_id,
                    "username": username,
                    "character_id": character_id,
                    "character_name": character_name,
                    "is_secret": is_secret,
                    "timestamp": timestamp
                }

                if is_secret:
                    # Secret roll - only send to roller (and storyteller in future)
                    await manager.send_personal(user_conn, response)
                else:
                    # Public roll - broadcast to everyone
                    await manager.broadcast(chronicle_id, response)

            # ============== SESSION EVENTS ==============
            elif message_type == "session_started":
                await manager.broadcast(chronicle_id, {
                    "type": "session_started",
                    "data": message.get("data", {}),
                    "user_id": user_id,
                    "username": username,
                    "timestamp": timestamp
                })

            elif message_type == "session_ended":
                await manager.broadcast(chronicle_id, {
                    "type": "session_ended",
                    "data": message.get("data", {}),
                    "user_id": user_id,
                    "username": username,
                    "timestamp": timestamp
                })

            elif message_type == "participant_joined":
                await manager.broadcast(chronicle_id, {
                    "type": "participant_joined",
                    "data": message.get("data", {}),
                    "user_id": user_id,
                    "username": username,
                    "timestamp": timestamp
                })

            elif message_type == "participant_left":
                await manager.broadcast(chronicle_id, {
                    "type": "participant_left",
                    "data": message.get("data", {}),
                    "user_id": user_id,
                    "username": username,
                    "timestamp": timestamp
                })

            # ============== XP EVENTS ==============
            elif message_type == "xp_request_created":
                await manager.broadcast(chronicle_id, {
                    "type": "xp_request_created",
                    "data": message.get("data", {}),
                    "user_id": user_id,
                    "username": username,
                    "timestamp": timestamp
                })

            elif message_type == "xp_request_updated":
                request_data = message.get("data", {})
                requester_id = request_data.get("requester_id")
                # Notify the requester specifically
                if requester_id:
                    await manager.send_to_user(chronicle_id, requester_id, {
                        "type": "xp_request_updated",
                        "data": request_data,
                        "timestamp": timestamp
                    })
                # Also broadcast to storyteller view
                await manager.broadcast(chronicle_id, {
                    "type": "xp_request_updated",
                    "data": request_data,
                    "timestamp": timestamp
                })

            elif message_type == "xp_awarded":
                await manager.broadcast(chronicle_id, {
                    "type": "xp_awarded",
                    "data": message.get("data", {}),
                    "user_id": user_id,
                    "username": username,
                    "timestamp": timestamp
                })

            # ============== INITIATIVE EVENTS ==============
            elif message_type == "combat_started":
                await manager.broadcast(chronicle_id, {
                    "type": "combat_started",
                    "data": message.get("data", {}),
                    "user_id": user_id,
                    "username": username,
                    "timestamp": timestamp
                })

            elif message_type == "combat_ended":
                await manager.broadcast(chronicle_id, {
                    "type": "combat_ended",
                    "data": message.get("data", {}),
                    "user_id": user_id,
                    "username": username,
                    "timestamp": timestamp
                })

            elif message_type == "initiative_updated":
                await manager.broadcast(chronicle_id, {
                    "type": "initiative_updated",
                    "data": message.get("data", {}),
                    "timestamp": timestamp
                })

            elif message_type == "turn_advanced":
                await manager.broadcast(chronicle_id, {
                    "type": "turn_advanced",
                    "data": message.get("data", {}),
                    "timestamp": timestamp
                })

            # ============== SCENE EVENTS ==============
            elif message_type == "scene_change":
                await manager.broadcast(chronicle_id, {
                    "type": "scene_change",
                    "scene_id": message.get("scene_id"),
                    "scene_name": message.get("scene_name"),
                    "user_id": user_id,
                    "username": username,
                    "timestamp": timestamp
                })

            elif message_type == "scene_updated":
                await manager.broadcast(chronicle_id, {
                    "type": "scene_updated",
                    "data": message.get("data", {}),
                    "timestamp": timestamp
                })

            # ============== CHARACTER EVENTS ==============
            elif message_type == "character_update":
                await manager.broadcast(chronicle_id, {
                    "type": "character_update",
                    "character_id": message.get("character_id"),
                    "character_name": message.get("character_name"),
                    "data": message.get("data"),
                    "timestamp": timestamp
                })

            # ============== UTILITY ==============
            elif message_type == "typing":
                await manager.broadcast(chronicle_id, {
                    "type": "typing",
                    "user_id": user_id,
                    "username": username,
                    "character_name": character_name,
                    "is_typing": message.get("is_typing", False)
                }, exclude=user_conn)

            elif message_type == "ping":
                await manager.send_personal(user_conn, {"type": "pong"})

            elif message_type == "update_character":
                # Update user's active character
                user_conn.character_id = message.get("character_id")
                user_conn.character_name = message.get("character_name")
                await manager.broadcast(chronicle_id, {
                    "type": "user_character_changed",
                    "user_id": user_id,
                    "username": username,
                    "character_id": user_conn.character_id,
                    "character_name": user_conn.character_name,
                    "online_users": manager.get_online_users(chronicle_id)
                })

    except WebSocketDisconnect:
        manager.disconnect(user_conn, chronicle_id)
        await manager.broadcast(chronicle_id, {
            "type": "user_left",
            "user_id": user_id,
            "username": username,
            "online_users": manager.get_online_users(chronicle_id)
        })
    except Exception as e:
        manager.disconnect(user_conn, chronicle_id)
        await manager.broadcast(chronicle_id, {
            "type": "user_left",
            "user_id": user_id,
            "username": username,
            "online_users": manager.get_online_users(chronicle_id)
        })
