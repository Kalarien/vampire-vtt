import { useState, useEffect, useRef } from 'react'
import { chatApi } from '../../lib/api'

interface ChatMessage {
  id: string
  content: string
  message_type: string
  user_id: string
  username: string
  character_id?: string
  character_name?: string
  recipient_id?: string
  timestamp: string
}

interface ChatPanelProps {
  chronicleId: string
  userId: string
  username: string
  characterId?: string
  characterName?: string
  websocket?: WebSocket | null
}

export function ChatPanel({
  chronicleId,
  userId,
  username: _username,
  characterId,
  characterName,
  websocket
}: ChatPanelProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [newMessage, setNewMessage] = useState('')
  const [messageType, setMessageType] = useState('chat')
  const [isLoading, setIsLoading] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  // Load initial messages
  useEffect(() => {
    const loadMessages = async () => {
      try {
        const response = await chatApi.getRecent(chronicleId, 50)
        setMessages(response.data)
      } catch (error) {
        console.error('Error loading chat:', error)
      } finally {
        setIsLoading(false)
      }
    }
    loadMessages()
  }, [chronicleId])

  // Handle WebSocket messages
  useEffect(() => {
    if (!websocket) return

    const handleMessage = (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'chat_message') {
          const newMsg: ChatMessage = {
            id: data.data?.id || Date.now().toString(),
            content: data.data?.content || data.message,
            message_type: data.data?.message_type || 'chat',
            user_id: data.user_id,
            username: data.username,
            character_id: data.data?.character_id,
            character_name: data.data?.character_name,
            recipient_id: data.data?.recipient_id,
            timestamp: data.timestamp,
          }
          setMessages(prev => [...prev, newMsg])
        }
      } catch (e) {
        console.error('Error parsing message:', e)
      }
    }

    websocket.addEventListener('message', handleMessage)
    return () => websocket.removeEventListener('message', handleMessage)
  }, [websocket])

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = () => {
    if (!newMessage.trim() || !websocket) return

    const msgData = {
      type: 'chat_message',
      data: {
        content: newMessage,
        message_type: messageType,
        character_id: characterId,
        character_name: characterName,
      }
    }

    websocket.send(JSON.stringify(msgData))
    setNewMessage('')
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
  }

  const getMessageStyle = (msg: ChatMessage) => {
    const isOwnMessage = msg.user_id === userId

    switch (msg.message_type) {
      case 'action':
        return 'italic text-yellow-400'
      case 'whisper':
        return 'text-purple-400'
      case 'ooc':
        return 'text-gray-400'
      case 'system':
        return 'text-blue-400 text-center text-sm'
      default:
        return isOwnMessage ? 'text-green-300' : 'text-white'
    }
  }

  return (
    <div className="flex flex-col h-full bg-gray-800 rounded-lg">
      <div className="p-3 border-b border-gray-700">
        <h3 className="text-lg font-semibold text-white">Chat</h3>
      </div>

      <div className="flex-1 overflow-y-auto p-3 space-y-2 min-h-0">
        {isLoading ? (
          <p className="text-gray-400 text-center">Carregando...</p>
        ) : messages.length === 0 ? (
          <p className="text-gray-400 text-center">Nenhuma mensagem ainda</p>
        ) : (
          messages.map((msg) => (
            <div key={msg.id} className="group">
              <div className="flex items-start gap-2">
                <div className="flex-1 min-w-0">
                  <div className="flex items-baseline gap-2">
                    <span className="font-medium text-red-400 truncate">
                      {msg.character_name || msg.username}
                    </span>
                    {msg.message_type === 'whisper' && (
                      <span className="text-xs text-purple-400">[Sussurro]</span>
                    )}
                    {msg.message_type === 'ooc' && (
                      <span className="text-xs text-gray-500">[OOC]</span>
                    )}
                    {msg.message_type === 'action' && (
                      <span className="text-xs text-yellow-500">[Acao]</span>
                    )}
                    <span className="text-xs text-gray-500 opacity-0 group-hover:opacity-100">
                      {formatTime(msg.timestamp)}
                    </span>
                  </div>
                  <p className={`break-words ${getMessageStyle(msg)}`}>
                    {msg.message_type === 'action' ? `*${msg.content}*` : msg.content}
                  </p>
                </div>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-3 border-t border-gray-700">
        <div className="flex gap-2 mb-2">
          <select
            value={messageType}
            onChange={(e) => setMessageType(e.target.value)}
            className="px-2 py-1 bg-gray-700 border border-gray-600 rounded text-sm text-white"
          >
            <option value="chat">Chat</option>
            <option value="action">Acao</option>
            <option value="ooc">OOC</option>
          </select>
        </div>
        <div className="flex gap-2">
          <textarea
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={messageType === 'action' ? 'Descreva a acao...' : 'Digite sua mensagem...'}
            rows={2}
            className="flex-1 px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 resize-none"
          />
          <button
            onClick={sendMessage}
            disabled={!newMessage.trim() || !websocket}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Enviar
          </button>
        </div>
      </div>
    </div>
  )
}
