import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { charactersApi } from '@/lib/api'
import { Bell, X, Check } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import { ptBR } from 'date-fns/locale'

interface Notification {
  id: string
  changes: Record<string, any>
  reason: string
  storyteller_name: string
  created_at: string
}

interface SheetChangeNotificationProps {
  characterId: string
}

export function SheetChangeNotification({ characterId }: SheetChangeNotificationProps) {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()

  const { data: notifications = [], isLoading } = useQuery({
    queryKey: ['character-notifications', characterId],
    queryFn: async () => {
      const response = await charactersApi.getNotifications(characterId)
      return response.data as Notification[]
    },
    refetchInterval: 30000, // Check every 30 seconds
  })

  const markSeenMutation = useMutation({
    mutationFn: () => charactersApi.markNotificationsSeen(characterId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['character-notifications', characterId] })
      setIsOpen(false)
    },
  })

  if (isLoading || notifications.length === 0) {
    return null
  }

  const formatChanges = (changes: Record<string, any>): string => {
    const parts: string[] = []
    for (const [key, value] of Object.entries(changes)) {
      if (typeof value === 'object' && value !== null) {
        parts.push(`${key}: ${JSON.stringify(value)}`)
      } else {
        parts.push(`${key}: ${value}`)
      }
    }
    return parts.join(', ')
  }

  return (
    <div className="relative">
      {/* Notification Bell */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 rounded-lg bg-blood-700/50 hover:bg-blood-700
                   text-bone-100 transition-colors"
      >
        <Bell className="w-5 h-5" />
        <span className="absolute -top-1 -right-1 w-5 h-5 bg-blood-500 rounded-full
                        text-xs flex items-center justify-center animate-pulse">
          {notifications.length}
        </span>
      </button>

      {/* Notification Panel */}
      {isOpen && (
        <div className="absolute right-0 top-12 w-96 max-h-96 overflow-y-auto
                       bg-midnight-900 border border-blood-700/50 rounded-lg shadow-xl z-50">
          <div className="p-4 border-b border-midnight-700 flex items-center justify-between">
            <h3 className="font-gothic text-bone-100">
              Alteracoes do Narrador
            </h3>
            <button
              onClick={() => setIsOpen(false)}
              className="text-midnight-400 hover:text-bone-100"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="divide-y divide-midnight-700">
            {notifications.map((notification) => (
              <div key={notification.id} className="p-4">
                <div className="flex items-start justify-between mb-2">
                  <span className="text-blood-400 text-sm font-medium">
                    {notification.storyteller_name}
                  </span>
                  <span className="text-midnight-500 text-xs">
                    {notification.created_at && formatDistanceToNow(
                      new Date(notification.created_at),
                      { addSuffix: true, locale: ptBR }
                    )}
                  </span>
                </div>
                <p className="text-bone-300 text-sm mb-2">
                  {notification.reason}
                </p>
                <div className="text-midnight-400 text-xs bg-midnight-800 p-2 rounded">
                  {formatChanges(notification.changes)}
                </div>
              </div>
            ))}
          </div>

          <div className="p-4 border-t border-midnight-700">
            <button
              onClick={() => markSeenMutation.mutate()}
              disabled={markSeenMutation.isPending}
              className="w-full flex items-center justify-center gap-2 px-4 py-2
                        bg-blood-700 hover:bg-blood-600 text-bone-100 rounded-lg
                        transition-colors disabled:opacity-50"
            >
              <Check className="w-4 h-4" />
              {markSeenMutation.isPending ? 'Marcando...' : 'Marcar como visto'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
