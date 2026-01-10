import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { queryClient } from '../lib/queryClient'

interface User {
  id: string
  discord_id?: string
  username: string
  avatar?: string
  email?: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (token: string, user?: User) => void
  logout: () => void
  checkAuth: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: true,

      login: (token: string, user?: User) => {
        set({
          token,
          user: user || null,
          isAuthenticated: true,
          isLoading: false,
        })
      },

      logout: () => {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        queryClient.clear() // Clear all cached queries
        set({ user: null, token: null, isAuthenticated: false })
      },

      checkAuth: () => {
        // First check the persisted zustand state (from vampire-vtt-auth)
        const { token, user } = get()

        // Also check legacy localStorage (for backwards compatibility)
        const legacyToken = localStorage.getItem('token')
        const legacyUser = localStorage.getItem('user')

        // Prefer zustand persisted state, fallback to legacy
        const activeToken = token || legacyToken
        let activeUser = user

        // If we don't have a user in zustand but have one in legacy storage
        if (!activeUser && legacyUser) {
          try {
            activeUser = JSON.parse(legacyUser)
            // Migrate to zustand persist
            if (activeToken && activeUser) {
              set({
                token: activeToken,
                user: activeUser,
                isAuthenticated: true,
                isLoading: false,
              })
              // Clean up legacy storage
              localStorage.removeItem('token')
              localStorage.removeItem('user')
              return
            }
          } catch (e) {
            // Invalid stored user, ignore
          }
        }

        if (!activeToken) {
          set({ isLoading: false, isAuthenticated: false })
          return
        }

        // We have a token and possibly a user
        set({
          token: activeToken,
          user: activeUser,
          isAuthenticated: true,
          isLoading: false,
        })
      },
    }),
    {
      name: 'vampire-vtt-auth',
      partialize: (state) => ({ token: state.token, user: state.user }),
    }
  )
)
