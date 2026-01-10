import { useQuery } from '@tanstack/react-query'
import { sessionsApi } from '@/lib/api'
import { formatDistanceToNow, format } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import { Calendar, Clock, Users, Award } from 'lucide-react'

interface Session {
  id: string
  name: string
  number: number
  started_at: string
  ended_at: string | null
  is_active: boolean
  xp_awarded: number
  started_by_name?: string
  participant_count: number
  // participants is only available when fetching single session, not list
  participants?: Array<{
    id: string
    character_name: string
    username: string
    xp_received: number
  }>
}

interface SessionHistoryProps {
  chronicleId: string
}

export function SessionHistory({ chronicleId }: SessionHistoryProps) {
  const { data: sessions = [], isLoading } = useQuery({
    queryKey: ['sessions', chronicleId],
    queryFn: async () => {
      const response = await sessionsApi.list(chronicleId)
      return response.data as Session[]
    },
  })

  const pastSessions = sessions.filter(s => !s.is_active)

  if (isLoading) {
    return (
      <div className="text-midnight-400 text-center py-4">
        Carregando historico...
      </div>
    )
  }

  if (pastSessions.length === 0) {
    return (
      <div className="text-midnight-400 text-center py-8">
        <Calendar className="w-12 h-12 mx-auto mb-2 opacity-50" />
        <p>Nenhuma sessao anterior registrada</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h3 className="font-gothic text-lg text-bone-100">Historico de Sessoes</h3>

      <div className="space-y-3">
        {pastSessions.map(session => (
          <div
            key={session.id}
            className="bg-midnight-800/50 rounded-lg p-4 border border-midnight-700"
          >
            <div className="flex items-start justify-between mb-2">
              <div>
                <h4 className="text-bone-100 font-medium">
                  {session.name || `Sessao ${session.number}`}
                </h4>
                <p className="text-midnight-400 text-sm">
                  Rodada {session.number}
                </p>
              </div>
              {session.xp_awarded > 0 && (
                <div className="flex items-center gap-1 text-amber-400 text-sm">
                  <Award className="w-4 h-4" />
                  <span>{session.xp_awarded} XP</span>
                </div>
              )}
            </div>

            <div className="flex flex-wrap gap-4 text-sm text-midnight-400 mb-3">
              <div className="flex items-center gap-1">
                <Calendar className="w-4 h-4" />
                <span>
                  {session.started_at && format(new Date(session.started_at), "dd/MM/yyyy", { locale: ptBR })}
                </span>
              </div>
              {session.ended_at && (
                <div className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  <span>
                    {formatDistanceToNow(new Date(session.started_at), { locale: ptBR })} atras
                  </span>
                </div>
              )}
              <div className="flex items-center gap-1">
                <Users className="w-4 h-4" />
                <span>{session.participant_count} participantes</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
