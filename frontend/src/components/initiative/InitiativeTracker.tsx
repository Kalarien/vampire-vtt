import { useState, useEffect } from 'react'
import { initiativeApi } from '../../lib/api'

interface InitiativeEntry {
  id: string
  order_id: string
  character_id?: string
  character_name: string
  initiative_value: number
  initiative_modifier: number
  is_npc: boolean
  has_acted: boolean
  is_delayed: boolean
}

interface InitiativeOrder {
  id: string
  session_id: string
  name: string
  is_active: boolean
  current_round: number
  current_turn_index: number
  entries: InitiativeEntry[]
}

interface InitiativeTrackerProps {
  sessionId: string
  isStoryteller: boolean
  chronicleCharacters?: Array<{ id: string; name: string }>
}

export function InitiativeTracker({
  sessionId,
  isStoryteller,
  chronicleCharacters = []
}: InitiativeTrackerProps) {
  const [order, setOrder] = useState<InitiativeOrder | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [showAddModal, setShowAddModal] = useState(false)
  const [newEntry, setNewEntry] = useState({
    character_id: '',
    character_name: '',
    initiative_modifier: 0,
    is_npc: false
  })

  const loadInitiative = async () => {
    try {
      const response = await initiativeApi.getCurrent(sessionId)
      setOrder(response.data)
    } catch (err) {
      setOrder(null)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadInitiative()
  }, [sessionId])

  const handleStartCombat = async () => {
    setIsLoading(true)
    try {
      await initiativeApi.start(sessionId, 'Combate')
      loadInitiative()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao iniciar combate')
    } finally {
      setIsLoading(false)
    }
  }

  const handleEndCombat = async () => {
    if (!order) return
    try {
      await initiativeApi.end(order.id)
      setOrder(null)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao encerrar combate')
    }
  }

  const handleRollAll = async () => {
    if (!order) return
    try {
      const response = await initiativeApi.roll(order.id)
      setOrder(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao rolar iniciativa')
    }
  }

  const handleNextTurn = async () => {
    if (!order) return
    try {
      const response = await initiativeApi.next(order.id)
      setOrder(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao avancar turno')
    }
  }

  const handleAddEntry = async () => {
    if (!order || !newEntry.character_name) return
    try {
      const response = await initiativeApi.add(order.id, {
        character_id: newEntry.character_id || undefined,
        character_name: newEntry.character_name,
        initiative_modifier: newEntry.initiative_modifier,
        is_npc: newEntry.is_npc
      })
      setOrder(response.data)
      setShowAddModal(false)
      setNewEntry({ character_id: '', character_name: '', initiative_modifier: 0, is_npc: false })
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao adicionar')
    }
  }

  const handleRemoveEntry = async (entryId: string) => {
    if (!order) return
    try {
      const response = await initiativeApi.remove(order.id, entryId)
      setOrder(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao remover')
    }
  }

  const sortedEntries = order?.entries
    ? [...order.entries].sort((a, b) => b.initiative_value - a.initiative_value)
    : []

  if (isLoading) {
    return (
      <div className="bg-gray-800 rounded-lg p-4">
        <p className="text-gray-400 text-center">Carregando...</p>
      </div>
    )
  }

  if (!order) {
    return (
      <div className="bg-gray-800 rounded-lg p-4">
        <h3 className="text-lg font-semibold text-white mb-4">Iniciativa</h3>
        <p className="text-gray-400 text-center mb-4">Nenhum combate ativo</p>
        {isStoryteller && (
          <button
            onClick={handleStartCombat}
            className="w-full px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md"
          >
            Iniciar Combate
          </button>
        )}
      </div>
    )
  }

  return (
    <div className="bg-gray-800 rounded-lg p-4">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-white">Iniciativa</h3>
          <p className="text-sm text-gray-400">Rodada {order.current_round}</p>
        </div>
        {isStoryteller && (
          <div className="flex gap-2">
            <button
              onClick={handleRollAll}
              className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm"
            >
              Rolar Todos
            </button>
            <button
              onClick={handleEndCombat}
              className="px-3 py-1 bg-gray-600 hover:bg-gray-500 text-white rounded text-sm"
            >
              Encerrar
            </button>
          </div>
        )}
      </div>

      {error && (
        <div className="mb-4 p-2 bg-red-900/50 border border-red-700 rounded text-red-200 text-sm">
          {error}
        </div>
      )}

      <div className="space-y-2 mb-4">
        {sortedEntries.map((entry, index) => (
          <div
            key={entry.id}
            className={`flex items-center justify-between p-3 rounded-lg ${
              index === order.current_turn_index
                ? 'bg-red-900/50 border border-red-600'
                : entry.has_acted
                ? 'bg-gray-700/50'
                : 'bg-gray-700'
            }`}
          >
            <div className="flex items-center gap-3">
              <span className="text-2xl font-bold text-white w-8 text-center">
                {entry.initiative_value}
              </span>
              <div>
                <p className={`font-medium ${entry.has_acted ? 'text-gray-400' : 'text-white'}`}>
                  {entry.character_name}
                  {entry.is_npc && <span className="ml-2 text-xs text-yellow-400">[NPC]</span>}
                </p>
                {entry.is_delayed && (
                  <span className="text-xs text-orange-400">Atrasado</span>
                )}
              </div>
            </div>
            {isStoryteller && (
              <button
                onClick={() => handleRemoveEntry(entry.id)}
                className="text-red-400 hover:text-red-300"
              >
                &times;
              </button>
            )}
          </div>
        ))}
      </div>

      {isStoryteller && (
        <div className="flex gap-2">
          <button
            onClick={() => setShowAddModal(true)}
            className="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-md"
          >
            + Adicionar
          </button>
          <button
            onClick={handleNextTurn}
            className="flex-1 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md"
          >
            Proximo Turno
          </button>
        </div>
      )}

      {/* Add Entry Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-white mb-4">Adicionar a Iniciativa</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-1">Personagem</label>
                <select
                  value={newEntry.character_id}
                  onChange={(e) => {
                    const char = chronicleCharacters.find(c => c.id === e.target.value)
                    setNewEntry({
                      ...newEntry,
                      character_id: e.target.value,
                      character_name: char?.name || ''
                    })
                  }}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white"
                >
                  <option value="">-- NPC ou custom --</option>
                  {chronicleCharacters.map(c => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
              </div>

              {!newEntry.character_id && (
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Nome</label>
                  <input
                    type="text"
                    value={newEntry.character_name}
                    onChange={(e) => setNewEntry({ ...newEntry, character_name: e.target.value })}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white"
                    placeholder="Nome do NPC ou personagem"
                  />
                </div>
              )}

              <div>
                <label className="block text-sm text-gray-400 mb-1">Modificador de Iniciativa</label>
                <input
                  type="number"
                  value={newEntry.initiative_modifier}
                  onChange={(e) => setNewEntry({ ...newEntry, initiative_modifier: parseInt(e.target.value) || 0 })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white"
                />
              </div>

              <label className="flex items-center gap-2 text-white">
                <input
                  type="checkbox"
                  checked={newEntry.is_npc}
                  onChange={(e) => setNewEntry({ ...newEntry, is_npc: e.target.checked })}
                  className="w-4 h-4"
                />
                <span>E um NPC</span>
              </label>

              <div className="flex gap-2 justify-end">
                <button
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 bg-gray-600 hover:bg-gray-500 text-white rounded-md"
                >
                  Cancelar
                </button>
                <button
                  onClick={handleAddEntry}
                  disabled={!newEntry.character_name && !newEntry.character_id}
                  className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md disabled:opacity-50"
                >
                  Adicionar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
