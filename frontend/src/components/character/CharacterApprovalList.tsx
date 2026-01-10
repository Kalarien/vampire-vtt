import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { charactersApi, chroniclesApi } from '../../lib/api'
import { Check, X, Eye, UserCheck, UserX, Clock } from 'lucide-react'

interface PendingCharacter {
  id: string
  name: string
  clan: string
  concept: string
  game_version: string
  owner_name: string
  owner_id: string
  approval_status: string
  pending_sheet: any
  storyteller_notes: string
  sheet: any
}

interface CharacterApprovalListProps {
  chronicleId: string
  isStoryteller: boolean
  onApprovalChange?: () => void
}

export function CharacterApprovalList({
  chronicleId,
  isStoryteller,
  onApprovalChange
}: CharacterApprovalListProps) {
  const queryClient = useQueryClient()
  const [processingId, setProcessingId] = useState<string | null>(null)
  const [showRejectModal, setShowRejectModal] = useState<string | null>(null)
  const [rejectMessage, setRejectMessage] = useState('')
  const [viewingSheet, setViewingSheet] = useState<PendingCharacter | null>(null)
  const [error, setError] = useState('')

  // Fetch pending characters
  const { data: pendingCharacters = [], isLoading: loadingPending, refetch: refetchPending } = useQuery({
    queryKey: ['characters', 'pending', chronicleId],
    queryFn: async () => {
      const response = await charactersApi.listPendingApprovals(chronicleId)
      return response.data
    },
    enabled: isStoryteller,
  })

  // Fetch all chronicle characters from chronicle data
  const { data: chronicle } = useQuery({
    queryKey: ['chronicle', chronicleId],
    queryFn: async () => {
      const response = await chroniclesApi.get(chronicleId)
      return response.data
    },
  })

  const allCharacters = chronicle?.characters || []

  const handleApprove = async (characterId: string) => {
    setProcessingId(characterId)
    try {
      await charactersApi.approve(characterId)
      refetchPending()
      queryClient.invalidateQueries({ queryKey: ['chronicle', chronicleId] })
      onApprovalChange?.()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao aprovar')
    } finally {
      setProcessingId(null)
    }
  }

  const handleReject = async (characterId: string) => {
    setProcessingId(characterId)
    try {
      await charactersApi.reject(characterId, rejectMessage || undefined)
      setShowRejectModal(null)
      setRejectMessage('')
      refetchPending()
      queryClient.invalidateQueries({ queryKey: ['chronicle', chronicleId] })
      onApprovalChange?.()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao rejeitar')
    } finally {
      setProcessingId(null)
    }
  }

  const handleRemove = async (characterId: string) => {
    if (!confirm('Tem certeza que deseja remover este personagem da cronica?')) return
    setProcessingId(characterId)
    try {
      await charactersApi.unassignFromChronicle(characterId)
      queryClient.invalidateQueries({ queryKey: ['chronicle', chronicleId] })
      onApprovalChange?.()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao remover')
    } finally {
      setProcessingId(null)
    }
  }

  if (!isStoryteller) return null

  const approvedCharacters = allCharacters.filter((c: any) => c.approval_status === 'approved')
  const rejectedCharacters = allCharacters.filter((c: any) => c.approval_status === 'rejected')

  return (
    <div className="space-y-6">
      {/* Pending Approvals Section */}
      <div className="bg-midnight-800/50 rounded-lg p-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-bone-100 flex items-center gap-2">
            <Clock className="w-5 h-5 text-yellow-500" />
            Aguardando Aprovacao
          </h3>
          <span className="px-2 py-1 bg-yellow-600/30 text-yellow-400 text-sm rounded">
            {pendingCharacters.length} pendente{pendingCharacters.length !== 1 ? 's' : ''}
          </span>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-900/50 border border-red-700 rounded text-red-200 text-sm">
            {error}
            <button onClick={() => setError('')} className="ml-2 text-red-400 hover:text-white">&times;</button>
          </div>
        )}

        {loadingPending ? (
          <p className="text-midnight-400 text-center py-4">Carregando...</p>
        ) : pendingCharacters.length === 0 ? (
          <p className="text-midnight-400 text-center py-4">Nenhum personagem aguardando aprovacao</p>
        ) : (
          <div className="space-y-3">
            {pendingCharacters.map((char: PendingCharacter) => (
              <div key={char.id} className="bg-midnight-700/50 rounded-lg p-4 border border-yellow-800/30">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-bone-100">{char.name}</span>
                      <span className="px-2 py-0.5 bg-yellow-600/30 text-yellow-300 rounded-full text-xs">
                        {char.pending_sheet ? 'Mudancas' : 'Novo'}
                      </span>
                    </div>
                    <p className="text-sm text-midnight-400">
                      {char.clan || 'Sem cla'} - {char.game_version.toUpperCase()}
                    </p>
                    <p className="text-xs text-midnight-500">Jogador: {char.owner_name}</p>
                  </div>
                </div>

                {char.concept && (
                  <p className="mt-2 text-sm text-bone-400">
                    <span className="text-midnight-500">Conceito:</span> {char.concept}
                  </p>
                )}

                {char.storyteller_notes && (
                  <div className="mt-2 p-2 bg-midnight-600/50 rounded text-sm">
                    <p className="text-midnight-400">Notas:</p>
                    <p className="text-bone-300">{char.storyteller_notes}</p>
                  </div>
                )}

                <div className="mt-4 flex gap-2 justify-end">
                  <button
                    onClick={() => setViewingSheet(char)}
                    className="px-3 py-1.5 bg-midnight-600 hover:bg-midnight-500 text-bone-200 rounded-md text-sm flex items-center gap-1"
                  >
                    <Eye className="w-4 h-4" />
                    Ver Ficha
                  </button>
                  <button
                    onClick={() => setShowRejectModal(char.id)}
                    disabled={processingId === char.id}
                    className="px-3 py-1.5 bg-red-700 hover:bg-red-600 text-white rounded-md text-sm flex items-center gap-1 disabled:opacity-50"
                  >
                    <X className="w-4 h-4" />
                    Rejeitar
                  </button>
                  <button
                    onClick={() => handleApprove(char.id)}
                    disabled={processingId === char.id}
                    className="px-3 py-1.5 bg-green-700 hover:bg-green-600 text-white rounded-md text-sm flex items-center gap-1 disabled:opacity-50"
                  >
                    <Check className="w-4 h-4" />
                    {processingId === char.id ? 'Aprovando...' : 'Aprovar'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Approved Characters Section */}
      <div className="bg-midnight-800/50 rounded-lg p-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-bone-100 flex items-center gap-2">
            <UserCheck className="w-5 h-5 text-green-500" />
            Personagens Aprovados
          </h3>
          <span className="px-2 py-1 bg-green-600/30 text-green-400 text-sm rounded">
            {approvedCharacters.length}
          </span>
        </div>

        {approvedCharacters.length === 0 ? (
          <p className="text-midnight-400 text-center py-4">Nenhum personagem aprovado ainda</p>
        ) : (
          <div className="space-y-2">
            {approvedCharacters.map((char: any) => (
              <div key={char.id} className="flex items-center justify-between bg-midnight-700/50 rounded-lg p-3 group">
                <Link to={`/characters/${char.id}`} className="flex items-center gap-3 flex-1">
                  <div className="w-10 h-10 bg-green-700/30 rounded-full flex items-center justify-center">
                    <span className="text-green-400">{char.name[0]}</span>
                  </div>
                  <div>
                    <p className="text-bone-100 font-medium">{char.name}</p>
                    <p className="text-midnight-400 text-sm">
                      {char.clan || 'Sem cla'} - {char.owner_name}
                    </p>
                  </div>
                </Link>
                <button
                  onClick={() => handleRemove(char.id)}
                  disabled={processingId === char.id}
                  className="p-2 text-midnight-400 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
                  title="Remover da cronica"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Rejected Characters Section */}
      {rejectedCharacters.length > 0 && (
        <div className="bg-midnight-800/50 rounded-lg p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-bone-100 flex items-center gap-2">
              <UserX className="w-5 h-5 text-red-500" />
              Personagens Rejeitados
            </h3>
            <span className="px-2 py-1 bg-red-600/30 text-red-400 text-sm rounded">
              {rejectedCharacters.length}
            </span>
          </div>

          <div className="space-y-2">
            {rejectedCharacters.map((char: any) => (
              <div key={char.id} className="flex items-center justify-between bg-midnight-700/50 rounded-lg p-3 group">
                <div className="flex items-center gap-3 flex-1">
                  <div className="w-10 h-10 bg-red-700/30 rounded-full flex items-center justify-center">
                    <span className="text-red-400">{char.name[0]}</span>
                  </div>
                  <div>
                    <p className="text-bone-100 font-medium">{char.name}</p>
                    <p className="text-midnight-400 text-sm">
                      {char.clan || 'Sem cla'} - {char.owner_name}
                    </p>
                    {char.storyteller_notes && (
                      <p className="text-red-400 text-xs mt-1">Motivo: {char.storyteller_notes}</p>
                    )}
                  </div>
                </div>
                <button
                  onClick={() => handleRemove(char.id)}
                  disabled={processingId === char.id}
                  className="p-2 text-midnight-400 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
                  title="Remover da cronica"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Reject Modal */}
      {showRejectModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-midnight-900 rounded-lg p-6 w-full max-w-md border border-midnight-700">
            <h3 className="text-lg font-semibold text-bone-100 mb-4">Rejeitar Personagem</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-bone-400 mb-1">Motivo (opcional)</label>
                <textarea
                  value={rejectMessage}
                  onChange={(e) => setRejectMessage(e.target.value)}
                  placeholder="Explique o que precisa ser ajustado..."
                  rows={3}
                  className="w-full px-3 py-2 bg-midnight-800 border border-midnight-600 rounded-md text-bone-100 placeholder-midnight-500"
                />
              </div>
              <div className="flex gap-2 justify-end">
                <button
                  onClick={() => {
                    setShowRejectModal(null)
                    setRejectMessage('')
                  }}
                  className="px-4 py-2 bg-midnight-700 hover:bg-midnight-600 text-bone-200 rounded-md"
                >
                  Cancelar
                </button>
                <button
                  onClick={() => handleReject(showRejectModal)}
                  disabled={processingId === showRejectModal}
                  className="px-4 py-2 bg-red-700 hover:bg-red-600 text-white rounded-md disabled:opacity-50"
                >
                  {processingId === showRejectModal ? 'Rejeitando...' : 'Confirmar'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* View Sheet Modal */}
      {viewingSheet && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-midnight-900 rounded-lg p-6 w-full max-w-2xl max-h-[80vh] overflow-y-auto border border-midnight-700">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-bone-100">
                Ficha: {viewingSheet.name}
              </h3>
              <button
                onClick={() => setViewingSheet(null)}
                className="text-midnight-400 hover:text-bone-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {viewingSheet.pending_sheet && (
              <div className="mb-4 p-3 bg-yellow-900/30 border border-yellow-700 rounded">
                <p className="text-yellow-200 text-sm font-medium">Mudancas Propostas:</p>
                <pre className="mt-2 text-xs text-bone-300 overflow-x-auto">
                  {JSON.stringify(viewingSheet.pending_sheet, null, 2)}
                </pre>
              </div>
            )}

            <div className="p-3 bg-midnight-800 rounded">
              <p className="text-midnight-400 text-sm font-medium mb-2">Ficha Atual:</p>
              <pre className="text-xs text-bone-300 overflow-x-auto">
                {JSON.stringify(viewingSheet.sheet, null, 2)}
              </pre>
            </div>

            <div className="mt-4 flex gap-2 justify-end">
              <button
                onClick={() => setViewingSheet(null)}
                className="px-4 py-2 bg-midnight-700 hover:bg-midnight-600 text-bone-200 rounded-md"
              >
                Fechar
              </button>
              <Link
                to={`/characters/${viewingSheet.id}`}
                className="px-4 py-2 bg-blood-700 hover:bg-blood-600 text-white rounded-md"
              >
                Abrir Ficha Completa
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
