import { cn, formatTime } from '@/lib/utils'
import { Skull, Sparkles } from 'lucide-react'

interface DiceResultV20Props {
  result: {
    id: string
    timestamp: Date
    description?: string
    dicePool?: number
    targetNumber?: number
    dice?: number[]
    successes?: number
    isSuccess?: boolean
    isBotch?: boolean
    specialty?: boolean
  }
}

export default function DiceResultV20({ result }: DiceResultV20Props) {
  const {
    timestamp,
    description,
    dicePool,
    targetNumber = 6,
    dice = [],
    successes = 0,
    isSuccess,
    isBotch,
    specialty,
  } = result

  const getResultType = () => {
    if (isBotch) return 'botch'
    if (isSuccess && successes >= 5) return 'exceptional'
    if (isSuccess) return 'success'
    return 'failure'
  }

  const resultType = getResultType()

  const resultStyles = {
    botch: 'border-blood-600 bg-blood-900/30',
    exceptional: 'border-yellow-600 bg-yellow-900/20',
    success: 'border-green-700/50 bg-midnight-800',
    failure: 'border-midnight-600 bg-midnight-800',
  }

  const resultLabels = {
    botch: { text: 'Botch!', icon: Skull, color: 'text-blood-400' },
    exceptional: { text: 'Sucesso Excepcional!', icon: Sparkles, color: 'text-yellow-400' },
    success: { text: 'Sucesso', icon: null, color: 'text-green-400' },
    failure: { text: 'Falha', icon: null, color: 'text-midnight-400' },
  }

  const ResultIcon = resultLabels[resultType].icon

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
          </div>
          {description && (
            <p className="text-bone-400 text-sm mt-1">{description}</p>
          )}
        </div>
        <span className="text-midnight-500 text-xs">
          {formatTime(timestamp)}
        </span>
      </div>

      {/* Dice Display */}
      <div className="flex flex-wrap gap-2 mb-3">
        {dice.map((die, index) => (
          <div
            key={index}
            className={cn(
              'die die-normal',
              die >= targetNumber && 'die-success',
              die === 10 && specialty && 'die-critical',
              die === 1 && 'opacity-50'
            )}
          >
            {die}
          </div>
        ))}
      </div>

      {/* Stats */}
      <div className="flex items-center gap-4 text-sm text-midnight-400">
        <span>Pool: {dicePool}</span>
        <span>Dificuldade: {targetNumber}</span>
        {specialty && <span className="text-yellow-500">Especialidade</span>}
        <span className={cn(
          'font-gothic',
          isSuccess ? 'text-green-400' : isBotch ? 'text-blood-400' : 'text-midnight-400'
        )}>
          {successes} sucessos
        </span>
      </div>
    </div>
  )
}
