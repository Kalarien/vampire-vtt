"""Gameplay features - Sessions, XP, Chat, Initiative

Revision ID: 002
Revises: 001
Create Date: 2026-01-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add missing columns to chronicles
    op.add_column('chronicles', sa.Column('starting_xp', sa.Integer, server_default='0'))
    op.add_column('chronicles', sa.Column('invite_code', sa.String(20), unique=True))
    op.add_column('chronicles', sa.Column('is_active', sa.Boolean, server_default='true'))

    # Add missing columns to characters
    op.add_column('characters', sa.Column('concept', sa.String(255), nullable=True))
    op.add_column('characters', sa.Column('clan', sa.String(100), nullable=True))
    op.add_column('characters', sa.Column('generation', sa.Integer, nullable=True))
    op.add_column('characters', sa.Column('predator_type', sa.String(100), nullable=True))
    op.add_column('characters', sa.Column('nature', sa.String(100), nullable=True))
    op.add_column('characters', sa.Column('demeanor', sa.String(100), nullable=True))
    op.add_column('characters', sa.Column('is_npc', sa.Boolean, server_default='false'))
    op.add_column('characters', sa.Column('portrait_url', sa.Text, nullable=True))

    # Add image_url to scenes
    op.add_column('scenes', sa.Column('image_url', sa.Text, nullable=True))

    # Game Sessions table
    op.create_table(
        'game_sessions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('chronicle_id', sa.String(36), sa.ForeignKey('chronicles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('number', sa.Integer, nullable=True),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('active_scene_id', sa.String(36), sa.ForeignKey('scenes.id', ondelete='SET NULL'), nullable=True),
        sa.Column('xp_awarded', sa.Integer, server_default='0'),
        sa.Column('started_by_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('ix_game_sessions_chronicle_id', 'game_sessions', ['chronicle_id'])
    op.create_index('ix_game_sessions_is_active', 'game_sessions', ['is_active'])

    # Session Participants table
    op.create_table(
        'session_participants',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('session_id', sa.String(36), sa.ForeignKey('game_sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('character_id', sa.String(36), sa.ForeignKey('characters.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('joined_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('left_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('xp_received', sa.Integer, server_default='0'),
    )
    op.create_index('ix_session_participants_session_id', 'session_participants', ['session_id'])
    op.create_index('ix_session_participants_character_id', 'session_participants', ['character_id'])

    # XP Requests table
    op.create_table(
        'xp_requests',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('chronicle_id', sa.String(36), sa.ForeignKey('chronicles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('character_id', sa.String(36), sa.ForeignKey('characters.id', ondelete='CASCADE'), nullable=False),
        sa.Column('requester_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('trait_type', sa.String(50), nullable=False),
        sa.Column('trait_name', sa.String(100), nullable=False),
        sa.Column('trait_category', sa.String(50), nullable=True),
        sa.Column('current_value', sa.Integer, server_default='0'),
        sa.Column('requested_value', sa.Integer, nullable=False),
        sa.Column('xp_cost', sa.Integer, nullable=False),
        sa.Column('justification', sa.Text, nullable=True),
        sa.Column('status', sa.String(20), server_default='pending'),
        sa.Column('storyteller_message', sa.Text, nullable=True),
        sa.Column('reviewed_by_id', sa.String(36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_xp_requests_chronicle_id', 'xp_requests', ['chronicle_id'])
    op.create_index('ix_xp_requests_character_id', 'xp_requests', ['character_id'])
    op.create_index('ix_xp_requests_status', 'xp_requests', ['status'])

    # XP Logs table
    op.create_table(
        'xp_logs',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('character_id', sa.String(36), sa.ForeignKey('characters.id', ondelete='CASCADE'), nullable=False),
        sa.Column('chronicle_id', sa.String(36), sa.ForeignKey('chronicles.id', ondelete='SET NULL'), nullable=True),
        sa.Column('session_id', sa.String(36), sa.ForeignKey('game_sessions.id', ondelete='SET NULL'), nullable=True),
        sa.Column('change_type', sa.String(20), nullable=False),
        sa.Column('amount', sa.Integer, nullable=False),
        sa.Column('previous_total', sa.Integer, nullable=False),
        sa.Column('new_total', sa.Integer, nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('trait_affected', sa.String(100), nullable=True),
        sa.Column('xp_request_id', sa.String(36), sa.ForeignKey('xp_requests.id', ondelete='SET NULL'), nullable=True),
        sa.Column('performed_by_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_xp_logs_character_id', 'xp_logs', ['character_id'])
    op.create_index('ix_xp_logs_session_id', 'xp_logs', ['session_id'])

    # Chat Messages table
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('chronicle_id', sa.String(36), sa.ForeignKey('chronicles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('session_id', sa.String(36), sa.ForeignKey('game_sessions.id', ondelete='SET NULL'), nullable=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('character_id', sa.String(36), sa.ForeignKey('characters.id', ondelete='SET NULL'), nullable=True),
        sa.Column('message_type', sa.String(20), server_default='chat'),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('recipient_id', sa.String(36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('sender_name', sa.String(255), nullable=True),
        sa.Column('character_name', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_chat_messages_chronicle_id', 'chat_messages', ['chronicle_id'])
    op.create_index('ix_chat_messages_session_id', 'chat_messages', ['session_id'])
    op.create_index('ix_chat_messages_created_at', 'chat_messages', ['created_at'])

    # Initiative Orders table
    op.create_table(
        'initiative_orders',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('session_id', sa.String(36), sa.ForeignKey('game_sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('current_round', sa.Integer, server_default='1'),
        sa.Column('current_turn_index', sa.Integer, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_initiative_orders_session_id', 'initiative_orders', ['session_id'])

    # Initiative Entries table
    op.create_table(
        'initiative_entries',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('order_id', sa.String(36), sa.ForeignKey('initiative_orders.id', ondelete='CASCADE'), nullable=False),
        sa.Column('character_id', sa.String(36), sa.ForeignKey('characters.id', ondelete='SET NULL'), nullable=True),
        sa.Column('character_name', sa.String(255), nullable=False),
        sa.Column('initiative_value', sa.Integer, server_default='0'),
        sa.Column('initiative_modifier', sa.Integer, server_default='0'),
        sa.Column('is_npc', sa.Boolean, server_default='false'),
        sa.Column('has_acted', sa.Boolean, server_default='false'),
        sa.Column('is_delayed', sa.Boolean, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_initiative_entries_order_id', 'initiative_entries', ['order_id'])


def downgrade() -> None:
    op.drop_table('initiative_entries')
    op.drop_table('initiative_orders')
    op.drop_table('chat_messages')
    op.drop_table('xp_logs')
    op.drop_table('xp_requests')
    op.drop_table('session_participants')
    op.drop_table('game_sessions')

    op.drop_column('scenes', 'image_url')

    op.drop_column('characters', 'portrait_url')
    op.drop_column('characters', 'is_npc')
    op.drop_column('characters', 'demeanor')
    op.drop_column('characters', 'nature')
    op.drop_column('characters', 'predator_type')
    op.drop_column('characters', 'generation')
    op.drop_column('characters', 'clan')
    op.drop_column('characters', 'concept')

    op.drop_column('chronicles', 'is_active')
    op.drop_column('chronicles', 'invite_code')
    op.drop_column('chronicles', 'starting_xp')
