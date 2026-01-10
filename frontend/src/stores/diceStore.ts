import { create } from 'zustand'

export type GameVersion = 'v5' | 'v20'

interface DiceResult {
  id: string
  version: GameVersion
  timestamp: Date
  characterName?: string
  description?: string
  // V5 specific
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
  // V20 specific
  dicePool?: number  // Pool for V20
  dice?: number[]
  targetNumber?: number
  specialty?: boolean
  isBotch?: boolean
}

interface DiceState {
  version: GameVersion
  results: DiceResult[]
  isRolling: boolean
  // V5 state
  pool: number
  hunger: number
  difficulty: number
  // V20 state
  dicePool: number
  targetNumber: number
  specialty: boolean
  // Actions
  setVersion: (version: GameVersion) => void
  setPool: (pool: number) => void
  setHunger: (hunger: number) => void
  setDifficulty: (difficulty: number) => void
  setDicePool: (pool: number) => void
  setTargetNumber: (target: number) => void
  setSpecialty: (specialty: boolean) => void
  addResult: (result: DiceResult) => void
  updateResult: (id: string, updates: Partial<DiceResult>) => void
  willpowerReroll: (resultId: string, diceIndices: number[]) => void
  clearResults: () => void
  setIsRolling: (rolling: boolean) => void
}

export const useDiceStore = create<DiceState>((set) => ({
  version: 'v5',
  results: [],
  isRolling: false,
  // V5 defaults
  pool: 5,
  hunger: 1,
  difficulty: 1,
  // V20 defaults
  dicePool: 5,
  targetNumber: 6,
  specialty: false,

  setVersion: (version) => set({ version }),
  setPool: (pool) => set({ pool: Math.max(0, Math.min(30, pool)) }),
  setHunger: (hunger) => set({ hunger: Math.max(0, Math.min(5, hunger)) }),
  setDifficulty: (difficulty) => set({ difficulty: Math.max(1, Math.min(10, difficulty)) }),
  setDicePool: (dicePool) => set({ dicePool: Math.max(1, Math.min(30, dicePool)) }),
  setTargetNumber: (targetNumber) => set({ targetNumber: Math.max(2, Math.min(10, targetNumber)) }),
  setSpecialty: (specialty) => set({ specialty }),
  addResult: (result) =>
    set((state) => ({
      results: [result, ...state.results].slice(0, 50), // Keep last 50 rolls
    })),
  updateResult: (id, updates) =>
    set((state) => ({
      results: state.results.map((r) =>
        r.id === id ? { ...r, ...updates } : r
      ),
    })),
  willpowerReroll: (resultId, diceIndices) =>
    set((state) => {
      const result = state.results.find((r) => r.id === resultId)
      if (!result || result.willpowerRerolled || result.version !== 'v5') {
        return state
      }

      // Reroll the selected regular dice
      const newRegularDice = [...(result.regularDice || [])]
      diceIndices.forEach((index) => {
        if (index < newRegularDice.length) {
          newRegularDice[index] = Math.floor(Math.random() * 10) + 1
        }
      })

      // Recalculate successes and special results
      const hungerDice = result.hungerDice || []
      const difficulty = result.difficulty || 1

      // Count successes (6+ = 1 success)
      let successes = 0
      let regularCrits = 0
      let hungerCrits = 0
      let hungerOnes = 0

      newRegularDice.forEach((die) => {
        if (die >= 6) successes++
        if (die === 10) regularCrits++
      })

      hungerDice.forEach((die) => {
        if (die >= 6) successes++
        if (die === 10) hungerCrits++
        if (die === 1) hungerOnes++
      })

      // Calculate criticals (pairs of 10s = 2 extra successes each pair)
      const totalCrits = regularCrits + hungerCrits
      const critPairs = Math.floor(totalCrits / 2)
      successes += critPairs * 2

      // Determine result type
      const isSuccess = successes >= difficulty
      const isCritical = critPairs > 0 && isSuccess
      const isMessyCritical = isCritical && hungerCrits > 0
      const isBestialFailure = !isSuccess && hungerOnes > 0

      return {
        results: state.results.map((r) =>
          r.id === resultId
            ? {
                ...r,
                regularDice: newRegularDice,
                successes,
                isSuccess,
                isCritical,
                isMessyCritical,
                isBestialFailure,
                willpowerRerolled: true,
                rerolledIndices: diceIndices,
              }
            : r
        ),
      }
    }),
  clearResults: () => set({ results: [] }),
  setIsRolling: (isRolling) => set({ isRolling }),
}))
