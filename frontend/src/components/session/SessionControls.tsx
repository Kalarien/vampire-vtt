import { useState, useEffect } from 'react'
import { useSessionStore } from '../../stores/sessionStore'
import { EndSessionModal } from './EndSessionModal'
import { sessionsApi } from '../../lib/api'

interface SessionControlsProps {
  chronicleId: string
  isStoryteller: boolean
  userCharacters?: Array<{ id: string; name: string }>
  chronicleCharacters?: Array<{ id: string; name: string; clan?: string; owner_name?: string }>
}

export function SessionControls({
  chronicleId,
  isStoryteller,
  userCharacters = [],
  chronicleCharacters = []
}: SessionControlsProps) {
  const {
    activeSession,
    isLoading,
    error,
    fetchActiveSession,
    startSession,
    joinSession,
    leaveSession,
    clearError
  } = useSessionStore()

  const [showStartModal, setShowStartModal] = useState(false)
  const [showEndModal, setShowEndModal] = useState(false)
  const [sessionName, setSessionName] = useState('')
  const [sessionNotes, setSessionNotes] = useState('')
  const [selectedCharacter, setSelectedCharacter] = useState('')

  useEffect(() => {
    fetchActiveSession(chronicleId)
  }, [chronicleId])

  const handleStartSession = async () => {
    try {
      await startSession(chronicleId, sessionName || undefined, sessionNotes || undefined)
      setShowStartModal(false)
      setSessionName('')
      setSessionNotes('')
    } catch (e) {
      // Error is handled by store
    }
  }

  const handleEndSession = async (_xpData: { character_id: string; amount: number }[], notes: string) => {
    if (!activeSession) return
    try {
      // End session without auto-awarding XP (we already awarded it in the modal)
      await sessionsApi.end(activeSession.id, {
        notes: notes,
        xp_amount: 0,
        xp_description: 'XP concedido individualmente'
      })
      setShowEndModal(false)
      fetchActiveSession(chronicleId)
    } catch (e) {
      console.error('Erro ao encerrar sessao:', e)
    }
  }

  const handleJoin = async () => {
    if (!activeSession || !selectedCharacter) return
    try {
      await joinSession(activeSession.id, selectedCharacter)
      setSelectedCharacter('')
    } catch (e) {
      // Error is handled by store
    }
  }

  const handleLeave = async (characterId: string) => {
    if (!activeSession) return
    try {
      await leaveSession(activeSession.id, characterId)
    } catch (e) {
      // Error is handled by store
    }
  }

  const myParticipant = activeSession?.participants.find(
    p => userCharacters.some(c => c.id === p.character_id) && !p.left_at
  )

  return (
    <div className="bg-gray-800 rounded-lg p-4">
      <h3 className="text-lg font-semibold text-white mb-4">Sessao de Jogo</h3>

      {error && (
        <div className="mb-4 p-3 bg-red-900/50 border border-red-700 rounded text-red-200 text-sm flex justify-between">
          <span>{error}</span>
          <button onClick={clearError} className="text-red-400 hover:text-white">&times;</button>
        </div>
      )}

      {activeSession ? (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Sessao Ativa
              </span>
              <h4 className="mt-1 text-white font-medium">{activeSession.name}</h4>
              <p className="text-sm text-gray-400">
                Rodada {activeSession.number} - Iniciada por {activeSession.started_by_name}
              </p>
            </div>
            {isStoryteller && (
              <button
                onClick={() => setShowEndModal(true)}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md text-sm"
              >
                Encerrar
              </button>
            )}
          </div>

          {/* Participants */}
          <div>
            <p className="text-sm text-gray-400 mb-2">
              Participantes ({activeSession.participants.filter(p => !p.left_at).length})
            </p>
            <div className="space-y-1">
              {activeSession.participants
                .filter(p => !p.left_at)
                .map(p => (
                  <div key={p.id} className="flex items-center justify-between bg-gray-700 rounded px-3 py-2">
                    <span className="text-white">{p.character_name}</span>
                    <span className="text-sm text-gray-400">{p.username}</span>
                    {(isStoryteller || myParticipant?.id === p.id) && (
                      <button
                        onClick={() => handleLeave(p.character_id)}
                        className="text-red-400 hover:text-red-300 text-sm"
                      >
                        Sair
                      </button>
                    )}
                  </div>
                ))}
            </div>
          </div>

          {/* Join if not participant */}
          {!myParticipant && userCharacters.length > 0 && (
            <div className="flex gap-2">
              <select
                value={selectedCharacter}
                onChange={(e) => setSelectedCharacter(e.target.value)}
                className="flex-1 px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white"
              >
                <option value="">Escolher personagem...</option>
                {userCharacters.map(c => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
              <button
                onClick={handleJoin}
                disabled={!selectedCharacter || isLoading}
                className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md disabled:opacity-50"
              >
                Entrar
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-4">
          <p className="text-gray-400 mb-4">Nenhuma sessao ativa</p>
          {isStoryteller && (
            <button
              onClick={() => setShowStartModal(true)}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md"
            >
              Iniciar Sessao
            </button>
          )}
        </div>
      )}

      {/* Start Session Modal */}
      {showStartModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-white mb-4">Iniciar Nova Sessao</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-1">Nome (opcional)</label>
                <input
                  type="text"
                  value={sessionName}
                  onChange={(e) => setSessionName(e.target.value)}
                  placeholder="Sessao 1"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Notas (opcional)</label>
                <textarea
                  value={sessionNotes}
                  onChange={(e) => setSessionNotes(e.target.value)}
                  placeholder="Anotacoes da sessao..."
                  rows={3}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white"
                />
              </div>
              <div className="flex gap-2 justify-end">
                <button
                  onClick={() => setShowStartModal(false)}
                  className="px-4 py-2 bg-gray-600 hover:bg-gray-500 text-white rounded-md"
                >
                  Cancelar
                </button>
                <button
                  onClick={handleStartSession}
                  disabled={isLoading}
                  className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md disabled:opacity-50"
                >
                  {isLoading ? 'Iniciando...' : 'Iniciar'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* End Session Modal */}
      <EndSessionModal
        isOpen={showEndModal}
        onClose={() => setShowEndModal(false)}
        onConfirm={handleEndSession}
        sessionId={activeSession?.id || ''}
        characters={chronicleCharacters.filter(c =>
          activeSession?.participants.some(p => p.character_id === c.id && !p.left_at)
        )}
        isLoading={isLoading}
      />
    </div>
  )
}
