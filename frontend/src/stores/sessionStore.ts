import { create } from 'zustand'
import { sessionsApi } from '../lib/api'

interface Participant {
  id: string
  character_id: string
  character_name: string
  user_id: string
  username: string
  joined_at: string
  left_at?: string
  xp_received: number
}

interface GameSession {
  id: string
  chronicle_id: string
  name: string
  number: number
  notes?: string
  started_at: string
  ended_at?: string
  is_active: boolean
  active_scene_id?: string
  xp_awarded: number
  started_by_id: string
  started_by_name: string
  participants: Participant[]
}

interface SessionState {
  activeSession: GameSession | null
  sessions: GameSession[]
  isLoading: boolean
  error: string | null

  fetchActiveSession: (chronicleId: string) => Promise<void>
  fetchSessions: (chronicleId: string) => Promise<void>
  startSession: (chronicleId: string, name?: string, notes?: string) => Promise<void>
  endSession: (sessionId: string, xpAmount: number, description: string, notes?: string) => Promise<void>
  joinSession: (sessionId: string, characterId: string) => Promise<void>
  leaveSession: (sessionId: string, characterId: string) => Promise<void>
  setActiveScene: (sessionId: string, sceneId: string) => Promise<void>
  clearError: () => void
}

export const useSessionStore = create<SessionState>((set, get) => ({
  activeSession: null,
  sessions: [],
  isLoading: false,
  error: null,

  fetchActiveSession: async (chronicleId: string) => {
    set({ isLoading: true, error: null })
    try {
      const response = await sessionsApi.getActive(chronicleId)
      set({ activeSession: response.data, isLoading: false })
    } catch (error: any) {
      set({ activeSession: null, isLoading: false })
    }
  },

  fetchSessions: async (chronicleId: string) => {
    set({ isLoading: true, error: null })
    try {
      const response = await sessionsApi.list(chronicleId)
      set({ sessions: response.data, isLoading: false })
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Erro ao carregar sessoes', isLoading: false })
    }
  },

  startSession: async (chronicleId: string, name?: string, notes?: string) => {
    set({ isLoading: true, error: null })
    try {
      await sessionsApi.start(chronicleId, { name, notes })
      // Refetch active session
      await get().fetchActiveSession(chronicleId)
      set({ isLoading: false })
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Erro ao iniciar sessao', isLoading: false })
      throw error
    }
  },

  endSession: async (sessionId: string, xpAmount: number, description: string, notes?: string) => {
    set({ isLoading: true, error: null })
    try {
      await sessionsApi.end(sessionId, {
        xp_amount: xpAmount,
        xp_description: description,
        notes
      })
      set({ activeSession: null, isLoading: false })
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Erro ao encerrar sessao', isLoading: false })
      throw error
    }
  },

  joinSession: async (sessionId: string, characterId: string) => {
    set({ isLoading: true, error: null })
    try {
      await sessionsApi.join(sessionId, characterId)
      // Refetch to get updated participants
      const response = await sessionsApi.get(sessionId)
      set({ activeSession: response.data, isLoading: false })
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Erro ao entrar na sessao', isLoading: false })
      throw error
    }
  },

  leaveSession: async (sessionId: string, characterId: string) => {
    set({ isLoading: true, error: null })
    try {
      await sessionsApi.leave(sessionId, characterId)
      const response = await sessionsApi.get(sessionId)
      set({ activeSession: response.data, isLoading: false })
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Erro ao sair da sessao', isLoading: false })
      throw error
    }
  },

  setActiveScene: async (sessionId: string, sceneId: string) => {
    try {
      await sessionsApi.setScene(sessionId, sceneId)
      set((state) => ({
        activeSession: state.activeSession
          ? { ...state.activeSession, active_scene_id: sceneId }
          : null
      }))
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Erro ao definir cena' })
    }
  },

  clearError: () => set({ error: null }),
}))
