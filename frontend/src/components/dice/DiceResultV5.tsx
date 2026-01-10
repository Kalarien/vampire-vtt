import { useState } from 'react'
import { cn, formatTime } from '@/lib/utils'
import { Skull, Sparkles, AlertTriangle, RefreshCw, Zap } from 'lucide-react'

interface DiceResultV5Props {
  result: {
    id: string
    timestamp: Date
    description?: string
    pool?: number
    hunger?: number
    difficulty?: number
    regularDice?: number[]
    hungerDice?: number[]
    successes?: number
    isSuccess?: boolean
    isCritical?: boolean
    isMessyCritical?: boolean
    isBestialFailure?: boolean
    willpowerRerolled?: boolean
    rerolledIndices?: number[]
  }
  onWillpowerReroll?: (resultId: string, diceIndices: number[]) => void
  canUseWillpower?: boolean
}

export default function DiceResultV5({
  result,
  onWillpowerReroll,
  canUseWillpower = true
}: DiceResultV5Props) {
  const {
    id,
    timestamp,
    description,
    pool,
    hunger,
    difficulty,
    regularDice = [],
    hungerDice = [],
    successes = 0,
    isSuccess,
    isCritical,
    isMessyCritical,
    isBestialFailure,
    willpowerRerolled = false,
    rerolledIndices = [],
  } = result

  const [selectedDice, setSelectedDice] = useState<number[]>([])
  const [isSelectingForReroll, setIsSelectingForReroll] = useState(false)

  const getResultType = () => {
    if (isBestialFailure) return 'bestial'
    if (isMessyCritical) return 'messy'
    if (isCritical) return 'critical'
    if (isSuccess) return 'success'
    return 'failure'
  }

  const resultType = getResultType()

  const resultStyles = {
    bestial: 'border-blood-600 bg-blood-900/30',
    messy: 'border-yellow-600 bg-yellow-900/20',
    critical: 'border-green-600 bg-green-900/20',
    success: 'border-green-700/50 bg-midnight-800',
    failure: 'border-midnight-600 bg-midnight-800',
  }

  const resultLabels = {
    bestial: { text: 'Falha Bestial', icon: Skull, color: 'text-blood-400' },
    messy: { text: 'Critico Sujo', icon: AlertTriangle, color: 'text-yellow-400' },
    critical: { text: 'Critico!', icon: Sparkles, color: 'text-green-400' },
    success: { text: 'Sucesso', icon: null, color: 'text-green-400' },
    failure: { text: 'Falha', icon: null, color: 'text-midnight-400' },
  }

  const ResultIcon = resultLabels[resultType].icon

  const toggleDiceSelection = (index: number) => {
    if (!isSelectingForReroll) return

    setSelectedDice(prev => {
      if (prev.includes(index)) {
        return prev.filter(i => i !== index)
      }
      if (prev.length >= 3) {
        // Max 3 dice
        return prev
      }
      return [...prev, index]
    })
  }

  const handleStartReroll = () => {
    setIsSelectingForReroll(true)
    setSelectedDice([])
  }

  const handleCancelReroll = () => {
    setIsSelectingForReroll(false)
    setSelectedDice([])
  }

  const handleConfirmReroll = () => {
    if (selectedDice.length > 0 && onWillpowerReroll) {
      onWillpowerReroll(id, selectedDice)
      setIsSelectingForReroll(false)
      setSelectedDice([])
    }
  }

  const canReroll = !willpowerRerolled && canUseWillpower && onWillpowerReroll && regularDice.length > 0

  return (
    <div className={cn('rounded-lg border p-4', resultStyles[resultType])}>
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="flex items-center gap-2">
            {ResultIcon && <ResultIcon className={cn('w-5 h-5', resultLabels[resultType].color)} />}
            <span className={cn('font-gothic text-lg', resultLabels[resultType].color)}>
              {resultLabels[resultType].text}
            </span>
            {willpowerRerolled && (
              <span className="px-2 py-0.5 bg-purple-900/50 text-purple-300 text-xs rounded flex items-center gap-1">
                <Zap className="w-3 h-3" />
                Reroll usado
              </span>
            )}
          </div>
          {description && (
            <p className="text-bone-400 text-sm mt-1">{description}</p>
          )}
        </div>
        <span className="text-midnight-500 text-xs">
          {formatTime(timestamp)}
        </span>
      </div>

      {/* Selection Instructions */}
      {isSelectingForReroll && (
        <div className="mb-3 p-2 bg-purple-900/30 border border-purple-700 rounded text-sm text-purple-200">
          <p className="flex items-center gap-2">
            <Zap className="w-4 h-4" />
            Selecione ate 3 dados normais para re-rolar (custa 1 Forca de Vontade)
          </p>
          <p className="text-xs text-purple-400 mt-1">
            Selecionados: {selectedDice.length}/3 - Clique nos dados normais para selecionar
          </p>
        </div>
      )}

      {/* Dice Display */}
      <div className="flex flex-wrap gap-2 mb-3">
        {/* Regular Dice */}
        {regularDice.map((die, index) => {
          const isSelected = selectedDice.includes(index)
          const wasRerolled = rerolledIndices.includes(index)

          return (
            <div
              key={`regular-${index}`}
              onClick={() => toggleDiceSelection(index)}
              className={cn(
                'die die-normal relative',
                die >= 6 && 'die-success',
                die === 10 && 'die-critical',
                isSelectingForReroll && 'cursor-pointer hover:ring-2 hover:ring-purple-500',
                isSelected && 'ring-2 ring-purple-500 bg-purple-900/50',
                wasRerolled && 'ring-2 ring-purple-400'
              )}
            >
              {die}
              {wasRerolled && (
                <RefreshCw className="absolute -top-1 -right-1 w-3 h-3 text-purple-400" />
              )}
            </div>
          )
        })}

        {/* Divider if both types exist */}
        {regularDice.length > 0 && hungerDice.length > 0 && (
          <div className="w-px h-8 bg-midnight-600 mx-1" />
        )}

        {/* Hunger Dice - cannot be rerolled */}
        {hungerDice.map((die, index) => (
          <div
            key={`hunger-${index}`}
            className={cn(
              'die die-hunger',
              die >= 6 && 'die-success',
              die === 10 && 'die-critical',
              die === 1 && 'die-bestial',
              isSelectingForReroll && 'opacity-50 cursor-not-allowed'
            )}
            title={isSelectingForReroll ? 'Dados de Fome nao podem ser re-rolados' : undefined}
          >
            {die}
          </div>
        ))}
      </div>

      {/* Stats */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4 text-sm text-midnight-400">
          <span>Pool: {pool}</span>
          <span>Fome: {hunger}</span>
          <span>Dificuldade: {difficulty}</span>
          <span className={cn(
            'font-gothic',
            isSuccess ? 'text-green-400' : 'text-blood-400'
          )}>
            {successes} sucessos
          </span>
        </div>

        {/* Willpower Reroll Controls */}
        {canReroll && !isSelectingForReroll && (
          <button
            onClick={handleStartReroll}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-purple-800/50 hover:bg-purple-700/50 text-purple-200 text-sm rounded transition-colors"
            title="Gastar 1 Forca de Vontade para re-rolar ate 3 dados"
          >
            <Zap className="w-4 h-4" />
            Willpower Reroll
          </button>
        )}

        {isSelectingForReroll && (
          <div className="flex items-center gap-2">
            <button
              onClick={handleCancelReroll}
              className="px-3 py-1.5 bg-midnight-700 hover:bg-midnight-600 text-midnight-300 text-sm rounded transition-colors"
            >
              Cancelar
            </button>
            <button
              onClick={handleConfirmReroll}
              disabled={selectedDice.length === 0}
              className={cn(
                'flex items-center gap-1.5 px-3 py-1.5 text-sm rounded transition-colors',
                selectedDice.length > 0
                  ? 'bg-purple-700 hover:bg-purple-600 text-white'
                  : 'bg-midnight-700 text-midnight-500 cursor-not-allowed'
              )}
            >
              <RefreshCw className="w-4 h-4" />
              Re-rolar ({selectedDice.length})
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
