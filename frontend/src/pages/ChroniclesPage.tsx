import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { chroniclesApi } from '@/lib/api'
import { useAuthStore } from '@/stores/authStore'
import { Plus, BookOpen, Users, Calendar, Trash2, X, LogIn } from 'lucide-react'
import { formatDate } from '@/lib/utils'

interface Chronicle {
  id: string
  name: string
  description?: string
  game_version: string
  storyteller_id: string
  created_at: string
  members_count?: number
}

export default function ChroniclesPage() {
  const { user } = useAuthStore()
  const queryClient = useQueryClient()
  const navigate = useNavigate()
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showJoinModal, setShowJoinModal] = useState(false)
  const [inviteCode, setInviteCode] = useState('')
  const [joinError, setJoinError] = useState('')
  const [newChronicle, setNewChronicle] = useState({
    name: '',
    description: '',
    game_version: 'v5',
  })

  const { data: chronicles, isLoading } = useQuery({
    queryKey: ['chronicles'],
    queryFn: async () => {
      const response = await chroniclesApi.list()
      return response.data as Chronicle[]
    },
  })

  const createMutation = useMutation({
    mutationFn: chroniclesApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chronicles'] })
      setShowCreateModal(false)
      setNewChronicle({ name: '', description: '', game_version: 'v5' })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: chroniclesApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chronicles'] })
    },
  })

  const joinMutation = useMutation({
    mutationFn: chroniclesApi.join,
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['chronicles'] })
      setShowJoinModal(false)
      setInviteCode('')
      setJoinError('')
      // Navigate to the joined chronicle
      if (response.data?.chronicle_id) {
        navigate(`/chronicles/${response.data.chronicle_id}`)
      }
    },
    onError: (error: any) => {
      setJoinError(error.response?.data?.detail || 'Codigo de convite invalido')
    },
  })

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault()
    createMutation.mutate(newChronicle)
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-blood-500 font-gothic text-xl animate-pulse">
          Carregando...
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-gothic text-3xl text-bone-100">Cronicas</h1>
          <p className="text-midnight-400 mt-1">
            Gerencie suas cronicas e participe de jogos.
          </p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setShowJoinModal(true)}
            className="btn-midnight flex items-center gap-2"
          >
            <LogIn className="w-5 h-5" />
            Entrar
          </button>
          <button
            onClick={() => setShowCreateModal(true)}
            className="btn-blood flex items-center gap-2"
          >
            <Plus className="w-5 h-5" />
            Nova Cronica
          </button>
        </div>
      </div>

      {/* Chronicles Grid */}
      {chronicles && chronicles.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {chronicles.map((chronicle) => (
            <div
              key={chronicle.id}
              className="card-gothic p-6 hover:border-blood-700 transition-colors group"
            >
              <div className="flex items-start justify-between mb-4">
                <Link to={`/chronicles/${chronicle.id}`} className="flex-1">
                  <h3 className="font-gothic text-xl text-bone-100 group-hover:text-blood-400 transition-colors">
                    {chronicle.name}
                  </h3>
                </Link>
                <div className="flex items-center gap-2">
                  {chronicle.storyteller_id === user?.id && (
                    <span className="text-xs px-2 py-1 bg-blood-700/30 rounded text-blood-400">
                      Narrador
                    </span>
                  )}
                  <span className="text-xs px-2 py-1 bg-midnight-700 rounded text-bone-400">
                    {chronicle.game_version.toUpperCase()}
                  </span>
                </div>
              </div>

              <p className="text-bone-400 text-sm mb-4 line-clamp-2">
                {chronicle.description || 'Sem descricao'}
              </p>

              <div className="flex items-center gap-4 text-midnight-400 text-sm mb-4">
                <span className="flex items-center gap-1">
                  <Users className="w-4 h-4" />
                  {chronicle.members_count || 1} membros
                </span>
                <span className="flex items-center gap-1">
                  <Calendar className="w-4 h-4" />
                  {formatDate(chronicle.created_at)}
                </span>
              </div>

              <div className="flex items-center gap-2">
                <Link
                  to={`/chronicles/${chronicle.id}`}
                  className="btn-midnight flex-1 text-center text-sm py-2"
                >
                  <BookOpen className="w-4 h-4 inline mr-2" />
                  Abrir
                </Link>
                {chronicle.storyteller_id === user?.id ? (
                  <button
                    onClick={() => deleteMutation.mutate(chronicle.id)}
                    className="p-2 text-midnight-400 hover:text-blood-500 transition-colors"
                    title="Excluir"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                ) : (
                  <span className="text-xs px-2 py-1 bg-midnight-700/50 rounded text-midnight-400">
                    Jogador
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card-gothic p-12 text-center">
          <BookOpen className="w-16 h-16 text-midnight-600 mx-auto mb-4" />
          <h3 className="font-gothic text-xl text-bone-100 mb-2">
            Nenhuma cronica encontrada
          </h3>
          <p className="text-midnight-400 mb-6">
            Crie sua primeira cronica para comecar a jogar.
          </p>
          <button
            onClick={() => setShowCreateModal(true)}
            className="btn-blood inline-flex items-center gap-2"
          >
            <Plus className="w-5 h-5" />
            Criar Cronica
          </button>
        </div>
      )}

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="card-gothic p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-6">
              <h2 className="font-gothic text-xl text-bone-100">
                Nova Cronica
              </h2>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-midnight-400 hover:text-bone-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-bone-300 text-sm mb-2">
                  Nome da Cronica
                </label>
                <input
                  type="text"
                  value={newChronicle.name}
                  onChange={(e) =>
                    setNewChronicle({ ...newChronicle, name: e.target.value })
                  }
                  className="input-gothic w-full"
                  placeholder="Ex: Noites de Sangue"
                  required
                />
              </div>

              <div>
                <label className="block text-bone-300 text-sm mb-2">
                  Descricao
                </label>
                <textarea
                  value={newChronicle.description}
                  onChange={(e) =>
                    setNewChronicle({
                      ...newChronicle,
                      description: e.target.value,
                    })
                  }
                  className="input-gothic w-full h-24 resize-none"
                  placeholder="Uma breve descricao da cronica..."
                />
              </div>

              <div>
                <label className="block text-bone-300 text-sm mb-2">
                  Versao do Jogo
                </label>
                <select
                  value={newChronicle.game_version}
                  onChange={(e) =>
                    setNewChronicle({
                      ...newChronicle,
                      game_version: e.target.value,
                    })
                  }
                  className="input-gothic w-full"
                >
                  <option value="v5">Vampiro: A Mascara - 5a Edicao</option>
                  <option value="v20">Vampiro: A Mascara - 20o Aniversario</option>
                </select>
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="btn-midnight flex-1"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="btn-blood flex-1"
                  disabled={createMutation.isPending}
                >
                  {createMutation.isPending ? 'Criando...' : 'Criar Cronica'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Join Modal */}
      {showJoinModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="card-gothic p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-6">
              <h2 className="font-gothic text-xl text-bone-100">
                Entrar em uma Cronica
              </h2>
              <button
                onClick={() => {
                  setShowJoinModal(false)
                  setInviteCode('')
                  setJoinError('')
                }}
                className="text-midnight-400 hover:text-bone-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault()
                setJoinError('')
                joinMutation.mutate(inviteCode)
              }}
              className="space-y-4"
            >
              <div>
                <label className="block text-bone-300 text-sm mb-2">
                  Codigo de Convite
                </label>
                <input
                  type="text"
                  value={inviteCode}
                  onChange={(e) => {
                    setInviteCode(e.target.value.trim())
                    setJoinError('')
                  }}
                  className="input-gothic w-full font-mono text-center text-lg"
                  placeholder="Cole o codigo aqui"
                  required
                />
                <p className="text-midnight-400 text-xs mt-2">
                  Peca o codigo de convite ao narrador da cronica.
                </p>
              </div>

              {joinError && (
                <p className="text-blood-500 text-sm">{joinError}</p>
              )}

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowJoinModal(false)
                    setInviteCode('')
                    setJoinError('')
                  }}
                  className="btn-midnight flex-1"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="btn-blood flex-1"
                  disabled={joinMutation.isPending || inviteCode.length < 1}
                >
                  {joinMutation.isPending ? 'Entrando...' : 'Entrar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
