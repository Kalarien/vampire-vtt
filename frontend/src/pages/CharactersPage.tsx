import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { charactersApi, gameDataApi } from '@/lib/api'
import { Plus, Users, Trash2, X, Edit } from 'lucide-react'

interface Character {
  id: string
  name: string
  game_version: string
  chronicle_id?: string
  clan?: string
  concept?: string
  generation?: number
  sheet?: {
    clan?: string
    generation?: number
    sire?: string
    concept?: string
  }
}

export default function CharactersPage() {
  const queryClient = useQueryClient()
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [newCharacter, setNewCharacter] = useState({
    name: '',
    game_version: 'v5',
    clan: '',
  })

  const { data: characters, isLoading } = useQuery({
    queryKey: ['characters'],
    queryFn: async () => {
      const response = await charactersApi.list()
      return response.data as Character[]
    },
  })

  const { data: clansV5 } = useQuery({
    queryKey: ['clans-v5'],
    queryFn: async () => {
      const response = await gameDataApi.getClansV5()
      return response.data
    },
  })

  const { data: clansV20 } = useQuery({
    queryKey: ['clans-v20'],
    queryFn: async () => {
      const response = await gameDataApi.getClansV20()
      return response.data
    },
  })

  const createMutation = useMutation({
    mutationFn: (data: { name: string; game_version: string; clan?: string }) =>
      charactersApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['characters'] })
      setShowCreateModal(false)
      setNewCharacter({ name: '', game_version: 'v5', clan: '' })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: charactersApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['characters'] })
    },
  })

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault()
    createMutation.mutate({
      name: newCharacter.name,
      game_version: newCharacter.game_version,
      clan: newCharacter.clan || undefined,
    })
  }

  const currentClans = newCharacter.game_version === 'v5' ? clansV5 : clansV20

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
          <h1 className="font-gothic text-3xl text-bone-100">Personagens</h1>
          <p className="text-midnight-400 mt-1">
            Gerencie suas fichas de personagem.
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="btn-blood flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Novo Personagem
        </button>
      </div>

      {/* Characters Grid */}
      {characters && characters.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {characters.map((character) => (
            <div
              key={character.id}
              className="card-gothic p-6 hover:border-blood-700 transition-colors group"
            >
              <div className="flex items-start gap-4 mb-4">
                <div className="w-14 h-14 bg-blood-700/30 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="font-gothic text-blood-400 text-2xl">
                    {character.name[0]}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <Link to={`/characters/${character.id}`}>
                    <h3 className="font-gothic text-xl text-bone-100 group-hover:text-blood-400 transition-colors truncate">
                      {character.name}
                    </h3>
                  </Link>
                  <p className="text-midnight-400 text-sm">
                    {character.clan || character.sheet?.clan || 'Sem cla'}
                  </p>
                  <span className="text-xs px-2 py-0.5 bg-midnight-700 rounded text-bone-400 inline-block mt-1">
                    {character.game_version.toUpperCase()}
                  </span>
                </div>
              </div>

              {character.sheet?.concept && (
                <p className="text-bone-400 text-sm mb-4 line-clamp-2">
                  {character.sheet.concept}
                </p>
              )}

              <div className="flex items-center gap-2">
                <Link
                  to={`/characters/${character.id}`}
                  className="btn-midnight flex-1 text-center text-sm py-2 flex items-center justify-center gap-2"
                >
                  <Edit className="w-4 h-4" />
                  Editar Ficha
                </Link>
                <button
                  onClick={() => deleteMutation.mutate(character.id)}
                  className="p-2 text-midnight-400 hover:text-blood-500 transition-colors"
                  title="Excluir"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card-gothic p-12 text-center">
          <Users className="w-16 h-16 text-midnight-600 mx-auto mb-4" />
          <h3 className="font-gothic text-xl text-bone-100 mb-2">
            Nenhum personagem encontrado
          </h3>
          <p className="text-midnight-400 mb-6">
            Crie seu primeiro personagem para comecar.
          </p>
          <button
            onClick={() => setShowCreateModal(true)}
            className="btn-blood inline-flex items-center gap-2"
          >
            <Plus className="w-5 h-5" />
            Criar Personagem
          </button>
        </div>
      )}

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="card-gothic p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-6">
              <h2 className="font-gothic text-xl text-bone-100">
                Novo Personagem
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
                  Nome do Personagem
                </label>
                <input
                  type="text"
                  value={newCharacter.name}
                  onChange={(e) =>
                    setNewCharacter({ ...newCharacter, name: e.target.value })
                  }
                  className="input-gothic w-full"
                  placeholder="Ex: Marcus de Ravnos"
                  required
                />
              </div>

              <div>
                <label className="block text-bone-300 text-sm mb-2">
                  Versao do Jogo
                </label>
                <select
                  value={newCharacter.game_version}
                  onChange={(e) =>
                    setNewCharacter({
                      ...newCharacter,
                      game_version: e.target.value,
                      clan: '', // Reset clan when changing version
                    })
                  }
                  className="input-gothic w-full"
                >
                  <option value="v5">V5 - 5a Edicao</option>
                  <option value="v20">V20 - 20o Aniversario</option>
                </select>
              </div>

              <div>
                <label className="block text-bone-300 text-sm mb-2">
                  Cla
                </label>
                <select
                  value={newCharacter.clan}
                  onChange={(e) =>
                    setNewCharacter({ ...newCharacter, clan: e.target.value })
                  }
                  className="input-gothic w-full"
                >
                  <option value="">Selecione um cla...</option>
                  {currentClans &&
                    Object.entries(currentClans).map(([key, clan]: [string, any]) => (
                      <option key={key} value={clan.name}>
                        {clan.name}
                      </option>
                    ))}
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
                  {createMutation.isPending ? 'Criando...' : 'Criar Personagem'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
