import { useState, useEffect } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { X, Award, Users } from 'lucide-react'
import { xpApi } from '../../lib/api'

interface Character {
  id: string
  name: string
  clan?: string
  owner_name?: string
}

interface EndSessionModalProps {
  isOpen: boolean
  onClose: () => void
  onConfirm: (xpData: { character_id: string; amount: number }[], notes: string) => void
  sessionId: string
  characters: Character[]
  isLoading?: boolean
}

export function EndSessionModal({
  isOpen,
  onClose,
  onConfirm,
  sessionId,
  characters,
  isLoading
}: EndSessionModalProps) {
  const queryClient = useQueryClient()
  const [xpAmounts, setXpAmounts] = useState<Record<string, number>>({})
  const [notes, setNotes] = useState('')
  const [baseXP, setBaseXP] = useState(3)
  const [isAwarding, setIsAwarding] = useState(false)

  useEffect(() => {
    if (isOpen) {
      // Reset XP amounts when modal opens
      const initial: Record<string, number> = {}
      characters.forEach(c => {
        initial[c.id] = baseXP
      })
      setXpAmounts(initial)
    }
  }, [isOpen, characters])

  const handleBaseXPChange = (value: number) => {
    setBaseXP(value)
    // Apply base XP to all characters
    const updated: Record<string, number> = {}
    characters.forEach(c => {
      updated[c.id] = value
    })
    setXpAmounts(updated)
  }

  const handleIndividualXPChange = (characterId: string, value: number) => {
    setXpAmounts(prev => ({
      ...prev,
      [characterId]: Math.max(0, value)
    }))
  }

  const handleConfirm = async () => {
    setIsAwarding(true)
    try {
      // Award XP to each character
      const xpData = characters
        .filter(c => xpAmounts[c.id] > 0)
        .map(c => ({
          character_id: c.id,
          amount: xpAmounts[c.id]
        }))

      // Award XP individually
      for (const data of xpData) {
        await xpApi.award({
          character_id: data.character_id,
          amount: data.amount,
          description: `XP da sessao`,
          session_id: sessionId
        })
      }

      // Invalidate character queries to refresh XP in character sheets
      queryClient.invalidateQueries({ queryKey: ['characters'] })
      for (const data of xpData) {
        queryClient.invalidateQueries({ queryKey: ['character', data.character_id] })
      }

      onConfirm(xpData, notes)
    } catch (error) {
      console.error('Erro ao conceder XP:', error)
    } finally {
      setIsAwarding(false)
    }
  }

  if (!isOpen) return null

  const totalXP = Object.values(xpAmounts).reduce((sum, val) => sum + val, 0)

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 rounded-lg w-full max-w-lg max-h-[80vh] overflow-hidden flex flex-col">
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <h2 className="text-xl font-semibold text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-yellow-500" />
            Encerrar Sessao e Conceder XP
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-4 overflow-y-auto flex-1">
          {/* Base XP selector */}
          <div className="mb-6">
            <label className="block text-sm text-gray-400 mb-2">
              XP Base para Todos
            </label>
            <div className="flex items-center gap-2">
              {[1, 2, 3, 4, 5].map(val => (
                <button
                  key={val}
                  onClick={() => handleBaseXPChange(val)}
                  className={`w-10 h-10 rounded-lg font-bold transition-colors ${
                    baseXP === val
                      ? 'bg-yellow-600 text-white'
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  {val}
                </button>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Clique para aplicar a todos, ou ajuste individualmente abaixo
            </p>
          </div>

          {/* Characters list */}
          <div className="mb-4">
            <h3 className="text-sm text-gray-400 mb-2 flex items-center gap-2">
              <Users className="w-4 h-4" />
              Personagens ({characters.length})
            </h3>

            {characters.length === 0 ? (
              <p className="text-gray-500 text-center py-4">
                Nenhum personagem na sessao
              </p>
            ) : (
              <div className="space-y-2">
                {characters.map(char => (
                  <div
                    key={char.id}
                    className="flex items-center justify-between bg-gray-700 rounded-lg p-3"
                  >
                    <div>
                      <p className="text-white font-medium">{char.name}</p>
                      <p className="text-xs text-gray-400">
                        {char.clan || 'Sem cla'}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleIndividualXPChange(char.id, (xpAmounts[char.id] || 0) - 1)}
                        className="w-8 h-8 bg-gray-600 hover:bg-gray-500 rounded text-white"
                      >
                        -
                      </button>
                      <span className="w-8 text-center text-yellow-400 font-bold">
                        {xpAmounts[char.id] || 0}
                      </span>
                      <button
                        onClick={() => handleIndividualXPChange(char.id, (xpAmounts[char.id] || 0) + 1)}
                        className="w-8 h-8 bg-gray-600 hover:bg-gray-500 rounded text-white"
                      >
                        +
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Session notes */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">
              Notas da Sessao (opcional)
            </label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Resumo do que aconteceu na sessao..."
              rows={3}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-500"
            />
          </div>
        </div>

        <div className="p-4 border-t border-gray-700 bg-gray-800">
          <div className="flex items-center justify-between mb-4">
            <span className="text-gray-400">Total de XP a conceder:</span>
            <span className="text-2xl font-bold text-yellow-400">{totalXP}</span>
          </div>

          <div className="flex gap-3">
            <button
              onClick={onClose}
              disabled={isLoading || isAwarding}
              className="flex-1 px-4 py-2 bg-gray-600 hover:bg-gray-500 text-white rounded-md disabled:opacity-50"
            >
              Cancelar
            </button>
            <button
              onClick={handleConfirm}
              disabled={isLoading || isAwarding}
              className="flex-1 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md disabled:opacity-50"
            >
              {isAwarding ? 'Concedendo XP...' : 'Encerrar e Conceder XP'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
