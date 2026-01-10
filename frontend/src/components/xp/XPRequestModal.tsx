import { useState } from 'react'
import { xpApi } from '../../lib/api'

interface XPRequestModalProps {
  characterId: string
  characterName: string
  traitType: string
  traitName: string
  traitCategory?: string
  currentValue: number
  gameVersion: 'v5' | 'v20'
  onClose: () => void
  onSuccess?: () => void
}

const XP_COSTS: Record<string, Record<string, (current: number, target: number) => number>> = {
  v5: {
    attribute: (current: number, target: number) => (target - current) * 5,
    skill: (current: number, target: number) => (target - current) * 3,
    discipline: (current: number, target: number) => (target - current) * 5,
    blood_potency: (current: number, target: number) => (target - current) * 10,
    humanity: (current: number, target: number) => (target - current) * 2,
  },
  v20: {
    attribute: (_current: number, target: number) => target * 4,
    skill: (_current: number, target: number) => target * 2,
    discipline: (_current: number, target: number) => target * 7,
    ability: (_current: number, target: number) => target * 2,
  }
}

export function XPRequestModal({
  characterId,
  characterName,
  traitType,
  traitName,
  traitCategory,
  currentValue,
  gameVersion,
  onClose,
  onSuccess
}: XPRequestModalProps) {
  const [targetValue, setTargetValue] = useState(currentValue + 1)
  const [justification, setJustification] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const calculateCost = () => {
    const costFn = XP_COSTS[gameVersion]?.[traitType as keyof typeof XP_COSTS.v5]
    if (costFn) {
      return costFn(currentValue, targetValue)
    }
    // Default cost
    return (targetValue - currentValue) * 5
  }

  const xpCost = calculateCost()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (targetValue <= currentValue) {
      setError('O valor alvo deve ser maior que o atual')
      return
    }

    setIsLoading(true)
    setError('')

    try {
      await xpApi.createRequest({
        character_id: characterId,
        trait_type: traitType,
        trait_name: traitName,
        trait_category: traitCategory,
        current_value: currentValue,
        requested_value: targetValue,
        xp_cost: xpCost,
        justification: justification || undefined
      })
      onSuccess?.()
      onClose()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao criar solicitacao')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md">
        <h3 className="text-lg font-semibold text-white mb-4">Solicitar XP</h3>

        {error && (
          <div className="mb-4 p-3 bg-red-900/50 border border-red-700 rounded text-red-200 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Personagem</label>
            <p className="text-white">{characterName}</p>
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1">Trait</label>
            <p className="text-white">
              {traitName}
              {traitCategory && <span className="text-gray-400 text-sm ml-2">({traitCategory})</span>}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Valor Atual</label>
              <p className="text-2xl font-bold text-white">{currentValue}</p>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Valor Desejado</label>
              <input
                type="number"
                min={currentValue + 1}
                max={5}
                value={targetValue}
                onChange={(e) => setTargetValue(parseInt(e.target.value) || currentValue + 1)}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white text-lg"
              />
            </div>
          </div>

          <div className="bg-gray-700 rounded-lg p-4 text-center">
            <p className="text-sm text-gray-400">Custo de XP</p>
            <p className="text-3xl font-bold text-red-500">{xpCost}</p>
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1">Justificativa (opcional)</label>
            <textarea
              value={justification}
              onChange={(e) => setJustification(e.target.value)}
              placeholder="Explique por que deseja esse aumento..."
              rows={3}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white"
            />
          </div>

          <div className="flex gap-2 justify-end">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-gray-600 hover:bg-gray-500 text-white rounded-md"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isLoading || targetValue <= currentValue}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md disabled:opacity-50"
            >
              {isLoading ? 'Enviando...' : 'Solicitar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
