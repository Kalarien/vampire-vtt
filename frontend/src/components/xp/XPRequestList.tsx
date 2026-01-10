import { useState, useEffect } from 'react'
import { xpApi } from '../../lib/api'

interface XPRequest {
  id: string
  character_id: string
  character_name: string
  requester_id: string
  requester_name: string
  trait_type: string
  trait_name: string
  trait_category?: string
  current_value: number
  requested_value: number
  xp_cost: number
  justification?: string
  status: string
  storyteller_message?: string
  created_at: string
}

interface XPRequestListProps {
  chronicleId: string
  isStoryteller: boolean
}

export function XPRequestList({ chronicleId, isStoryteller }: XPRequestListProps) {
  const [requests, setRequests] = useState<XPRequest[]>([])
  const [statusFilter, setStatusFilter] = useState('pending')
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [processingId, setProcessingId] = useState<string | null>(null)
  const [rejectMessage, setRejectMessage] = useState('')
  const [showRejectModal, setShowRejectModal] = useState<string | null>(null)

  const loadRequests = async () => {
    setIsLoading(true)
    try {
      const response = await xpApi.listChronicleRequests(chronicleId, statusFilter)
      setRequests(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao carregar solicitacoes')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadRequests()
  }, [chronicleId, statusFilter])

  const handleApprove = async (requestId: string) => {
    setProcessingId(requestId)
    try {
      await xpApi.approve(requestId)
      loadRequests()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao aprovar')
    } finally {
      setProcessingId(null)
    }
  }

  const handleReject = async (requestId: string) => {
    setProcessingId(requestId)
    try {
      await xpApi.reject(requestId, rejectMessage || undefined)
      setShowRejectModal(null)
      setRejectMessage('')
      loadRequests()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao rejeitar')
    } finally {
      setProcessingId(null)
    }
  }

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'pending':
        return <span className="px-2 py-0.5 bg-yellow-600 text-yellow-100 rounded-full text-xs">Pendente</span>
      case 'approved':
        return <span className="px-2 py-0.5 bg-green-600 text-green-100 rounded-full text-xs">Aprovado</span>
      case 'rejected':
        return <span className="px-2 py-0.5 bg-red-600 text-red-100 rounded-full text-xs">Rejeitado</span>
      default:
        return null
    }
  }

  return (
    <div className="bg-gray-800 rounded-lg p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white">Solicitacoes de XP</h3>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="px-3 py-1 bg-gray-700 border border-gray-600 rounded-md text-white text-sm"
        >
          <option value="pending">Pendentes</option>
          <option value="approved">Aprovadas</option>
          <option value="rejected">Rejeitadas</option>
          <option value="all">Todas</option>
        </select>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-900/50 border border-red-700 rounded text-red-200 text-sm">
          {error}
        </div>
      )}

      {isLoading ? (
        <p className="text-gray-400 text-center py-4">Carregando...</p>
      ) : requests.length === 0 ? (
        <p className="text-gray-400 text-center py-4">Nenhuma solicitacao encontrada</p>
      ) : (
        <div className="space-y-3">
          {requests.map((req) => (
            <div key={req.id} className="bg-gray-700 rounded-lg p-4">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-white">{req.character_name}</span>
                    {getStatusBadge(req.status)}
                  </div>
                  <p className="text-sm text-gray-400">{req.requester_name}</p>
                </div>
                <span className="text-xs text-gray-500">{formatDate(req.created_at)}</span>
              </div>

              <div className="mt-3 grid grid-cols-3 gap-4 text-center">
                <div>
                  <p className="text-xs text-gray-400">Trait</p>
                  <p className="text-white font-medium">{req.trait_name}</p>
                  {req.trait_category && (
                    <p className="text-xs text-gray-500">{req.trait_category}</p>
                  )}
                </div>
                <div>
                  <p className="text-xs text-gray-400">Valor</p>
                  <p className="text-white">
                    {req.current_value} <span className="text-gray-400">→</span> {req.requested_value}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-400">Custo XP</p>
                  <p className="text-red-400 font-bold">{req.xp_cost}</p>
                </div>
              </div>

              {req.justification && (
                <div className="mt-3 p-2 bg-gray-600 rounded">
                  <p className="text-xs text-gray-400">Justificativa:</p>
                  <p className="text-sm text-gray-200">{req.justification}</p>
                </div>
              )}

              {req.storyteller_message && (
                <div className="mt-3 p-2 bg-gray-600 rounded">
                  <p className="text-xs text-gray-400">Mensagem do Narrador:</p>
                  <p className="text-sm text-gray-200">{req.storyteller_message}</p>
                </div>
              )}

              {isStoryteller && req.status === 'pending' && (
                <div className="mt-4 flex gap-2 justify-end">
                  <button
                    onClick={() => setShowRejectModal(req.id)}
                    disabled={processingId === req.id}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md text-sm disabled:opacity-50"
                  >
                    Rejeitar
                  </button>
                  <button
                    onClick={() => handleApprove(req.id)}
                    disabled={processingId === req.id}
                    className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md text-sm disabled:opacity-50"
                  >
                    {processingId === req.id ? 'Processando...' : 'Aprovar'}
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Reject Modal */}
      {showRejectModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-white mb-4">Rejeitar Solicitacao</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-1">Motivo (opcional)</label>
                <textarea
                  value={rejectMessage}
                  onChange={(e) => setRejectMessage(e.target.value)}
                  placeholder="Explique o motivo da rejeicao..."
                  rows={3}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white"
                />
              </div>
              <div className="flex gap-2 justify-end">
                <button
                  onClick={() => {
                    setShowRejectModal(null)
                    setRejectMessage('')
                  }}
                  className="px-4 py-2 bg-gray-600 hover:bg-gray-500 text-white rounded-md"
                >
                  Cancelar
                </button>
                <button
                  onClick={() => handleReject(showRejectModal)}
                  disabled={processingId === showRejectModal}
                  className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md disabled:opacity-50"
                >
                  {processingId === showRejectModal ? 'Rejeitando...' : 'Confirmar Rejeicao'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
