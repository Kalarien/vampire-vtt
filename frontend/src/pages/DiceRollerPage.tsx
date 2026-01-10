import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { useDiceStore } from '@/stores/diceStore'
import { diceApi } from '@/lib/api'
import { Dice6, RefreshCw, Trash2 } from 'lucide-react'
import { cn, generateId } from '@/lib/utils'
import DiceResultV5 from '@/components/dice/DiceResultV5'
import DiceResultV20 from '@/components/dice/DiceResultV20'

export default function DiceRollerPage() {
  const {
    version,
    pool,
    hunger,
    difficulty,
    dicePool,
    targetNumber,
    specialty,
    results,
    isRolling,
    setVersion,
    setPool,
    setHunger,
    setDifficulty,
    setDicePool,
    setTargetNumber,
    setSpecialty,
    addResult,
    willpowerReroll,
    clearResults,
    setIsRolling,
  } = useDiceStore()

  const [description, setDescription] = useState('')

  const rollV5Mutation = useMutation({
    mutationFn: diceApi.rollV5,
    onMutate: () => setIsRolling(true),
    onSuccess: (response) => {
      const data = response.data
      addResult({
        id: generateId(),
        version: 'v5',
        timestamp: new Date(),
        description: description || undefined,
        pool: data.pool,
        hunger: data.hunger,
        difficulty: data.difficulty,
        regularDice: data.regular_dice,
        hungerDice: data.hunger_dice,
        successes: data.successes,
        isSuccess: data.is_success,
        isCritical: data.is_critical,
        isMessyCritical: data.is_messy_critical,
        isBestialFailure: data.is_bestial_failure,
      })
      setDescription('')
    },
    onSettled: () => setIsRolling(false),
  })

  const rollV20Mutation = useMutation({
    mutationFn: diceApi.rollV20,
    onMutate: () => setIsRolling(true),
    onSuccess: (response) => {
      const data = response.data
      addResult({
        id: generateId(),
        version: 'v20',
        timestamp: new Date(),
        description: description || undefined,
        dicePool: data.pool,
        targetNumber: data.difficulty,
        dice: data.dice,
        successes: data.successes,
        isSuccess: data.is_success,
        isBotch: data.is_botch,
        specialty: data.specialty,
      })
      setDescription('')
    },
    onSettled: () => setIsRolling(false),
  })

  const handleRoll = () => {
    if (version === 'v5') {
      rollV5Mutation.mutate({
        pool,
        hunger,
        difficulty,
        description: description || undefined,
      })
    } else {
      rollV20Mutation.mutate({
        pool: dicePool,
        difficulty: targetNumber,
        specialty,
        description: description || undefined,
      })
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="font-gothic text-3xl text-bone-100">Rolador de Dados</h1>
        <p className="text-midnight-400 mt-1">
          Role dados para V5 ou V20 com todas as regras especiais.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Dice Controls */}
        <div className="lg:col-span-1 space-y-6">
          {/* Version Toggle */}
          <div className="card-gothic p-4">
            <div className="flex rounded-lg bg-midnight-800 p-1">
              <button
                onClick={() => setVersion('v5')}
                className={cn(
                  'flex-1 py-2 px-4 rounded-md font-gothic text-sm transition-colors',
                  version === 'v5'
                    ? 'bg-blood-700 text-bone-100'
                    : 'text-midnight-400 hover:text-bone-100'
                )}
              >
                V5
              </button>
              <button
                onClick={() => setVersion('v20')}
                className={cn(
                  'flex-1 py-2 px-4 rounded-md font-gothic text-sm transition-colors',
                  version === 'v20'
                    ? 'bg-blood-700 text-bone-100'
                    : 'text-midnight-400 hover:text-bone-100'
                )}
              >
                V20
              </button>
            </div>
          </div>

          {/* Dice Configuration */}
          <div className="card-gothic p-6 space-y-4">
            <h3 className="font-gothic text-lg text-bone-100">
              Configuracao
            </h3>

            {version === 'v5' ? (
              <>
                {/* V5 Controls */}
                <div>
                  <label className="block text-bone-300 text-sm mb-2">
                    Pool de Dados: {pool}
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="20"
                    value={pool}
                    onChange={(e) => setPool(parseInt(e.target.value))}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-bone-300 text-sm mb-2">
                    Fome: {hunger}
                  </label>
                  <div className="flex gap-2">
                    {[0, 1, 2, 3, 4, 5].map((h) => (
                      <button
                        key={h}
                        onClick={() => setHunger(h)}
                        className={cn(
                          'hunger-pip',
                          h <= hunger ? 'hunger-pip-full' : 'hunger-pip-empty'
                        )}
                      />
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-bone-300 text-sm mb-2">
                    Dificuldade: {difficulty}
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={difficulty}
                    onChange={(e) => setDifficulty(parseInt(e.target.value))}
                    className="w-full"
                  />
                </div>
              </>
            ) : (
              <>
                {/* V20 Controls */}
                <div>
                  <label className="block text-bone-300 text-sm mb-2">
                    Pool de Dados: {dicePool}
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="20"
                    value={dicePool}
                    onChange={(e) => setDicePool(parseInt(e.target.value))}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-bone-300 text-sm mb-2">
                    Dificuldade: {targetNumber}
                  </label>
                  <input
                    type="range"
                    min="2"
                    max="10"
                    value={targetNumber}
                    onChange={(e) => setTargetNumber(parseInt(e.target.value))}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="flex items-center gap-2 text-bone-300 text-sm cursor-pointer">
                    <input
                      type="checkbox"
                      checked={specialty}
                      onChange={(e) => setSpecialty(e.target.checked)}
                      className="w-4 h-4 rounded border-midnight-600 bg-midnight-800 text-blood-600 focus:ring-blood-600"
                    />
                    Especialidade (reroll 10s)
                  </label>
                </div>
              </>
            )}

            {/* Description */}
            <div>
              <label className="block text-bone-300 text-sm mb-2">
                Descricao (opcional)
              </label>
              <input
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="input-gothic w-full"
                placeholder="Ex: Intimidation + Strength"
              />
            </div>

            {/* Roll Button */}
            <button
              onClick={handleRoll}
              disabled={isRolling}
              className="btn-blood w-full flex items-center justify-center gap-2 py-3"
            >
              {isRolling ? (
                <RefreshCw className="w-5 h-5 animate-spin" />
              ) : (
                <Dice6 className="w-5 h-5" />
              )}
              {isRolling ? 'Rolando...' : 'Rolar Dados'}
            </button>
          </div>

          {/* Quick Reference */}
          <div className="card-gothic p-4">
            <h4 className="font-gothic text-sm text-bone-300 mb-2">
              Referencia Rapida
            </h4>
            {version === 'v5' ? (
              <ul className="text-midnight-400 text-xs space-y-1">
                <li>• 6+ = Sucesso</li>
                <li>• 10 = Sucesso Critico (2 sucessos com par)</li>
                <li>• 1 em Hunger Dice = Possivel Falha Bestial</li>
                <li>• 10 em Hunger Dice = Possivel Critico Sujo</li>
              </ul>
            ) : (
              <ul className="text-midnight-400 text-xs space-y-1">
                <li>• Dificuldade+ = Sucesso</li>
                <li>• 10 = Sucesso (reroll com especialidade)</li>
                <li>• 1 = Remove um sucesso</li>
                <li>• Botch = Falha critica (1s sem sucessos)</li>
              </ul>
            )}
          </div>
        </div>

        {/* Results */}
        <div className="lg:col-span-2">
          <div className="card-gothic p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-gothic text-lg text-bone-100">
                Resultados
              </h3>
              {results.length > 0 && (
                <button
                  onClick={clearResults}
                  className="text-midnight-400 hover:text-bone-100 transition-colors flex items-center gap-1 text-sm"
                >
                  <Trash2 className="w-4 h-4" />
                  Limpar
                </button>
              )}
            </div>

            {results.length > 0 ? (
              <div className="space-y-4 max-h-[600px] overflow-y-auto scrollbar-gothic">
                {results.map((result) =>
                  result.version === 'v5' ? (
                    <DiceResultV5
                      key={result.id}
                      result={result}
                      onWillpowerReroll={willpowerReroll}
                    />
                  ) : (
                    <DiceResultV20 key={result.id} result={result} />
                  )
                )}
              </div>
            ) : (
              <div className="text-center py-12">
                <Dice6 className="w-16 h-16 text-midnight-600 mx-auto mb-4" />
                <p className="text-midnight-400">
                  Nenhuma rolagem ainda. Configure e role os dados!
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
