import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { authApi } from '@/lib/api'

export default function LandingPage() {
  const navigate = useNavigate()
  const { isAuthenticated, checkAuth } = useAuthStore()

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard')
    }
  }, [isAuthenticated, navigate])

  const handleDiscordLogin = async () => {
    try {
      const response = await authApi.getDiscordUrl()
      window.location.href = response.data.url
    } catch (error) {
      console.error('Failed to get Discord URL:', error)
    }
  }

  return (
    <div className="min-h-screen bg-midnight-950 flex flex-col">
      {/* Hero Section */}
      <div className="flex-1 flex flex-col items-center justify-center px-4 relative overflow-hidden">
        {/* Background Effect */}
        <div className="absolute inset-0 bg-gradient-radial from-blood-900/20 via-transparent to-transparent" />

        {/* Content */}
        <div className="relative z-10 text-center max-w-3xl">
          {/* Logo */}
          <div className="mb-8 flex justify-center">
            <div className="w-24 h-24 bg-blood-700 rounded-2xl flex items-center justify-center shadow-blood-lg animate-pulse-blood">
              <span className="font-gothic text-bone-100 text-5xl">V</span>
            </div>
          </div>

          {/* Title */}
          <h1 className="font-gothic text-5xl md:text-7xl text-bone-100 mb-4 text-shadow-blood">
            Vampire VTT
          </h1>

          <p className="text-bone-300 text-xl md:text-2xl mb-2 font-gothic">
            Virtual Tabletop
          </p>

          <p className="text-midnight-400 text-lg mb-12 max-w-xl mx-auto">
            A Noite Pertence aos Imortais. Crie crônicas, gerencie personagens e role dados
            em tempo real com seu coterie.
          </p>

          {/* Login Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center flex-wrap">
            {/* Discord Login Button */}
            <button
              onClick={handleDiscordLogin}
              className="group relative inline-flex items-center gap-3 bg-[#5865F2] hover:bg-[#4752C4]
                         text-white font-gothic text-lg px-8 py-4 rounded-lg
                         transition-all duration-300 shadow-lg hover:shadow-xl
                         hover:scale-105"
            >
              <svg
                className="w-6 h-6"
                fill="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z" />
              </svg>
              Entrar com Discord
            </button>

            {/* Email Login Button */}
            <button
              onClick={() => navigate('/login')}
              className="group relative inline-flex items-center gap-3 bg-blood-700 hover:bg-blood-600
                         text-bone-100 font-gothic text-lg px-8 py-4 rounded-lg
                         transition-all duration-300 shadow-lg hover:shadow-xl
                         hover:scale-105"
            >
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Entrar com Email
            </button>
          </div>

          {/* Features */}
          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="card-gothic p-6">
              <div className="text-blood-500 mb-4">
                <svg className="w-10 h-10 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <h3 className="font-gothic text-bone-100 text-lg mb-2">V5 & V20</h3>
              <p className="text-midnight-400 text-sm">
                Suporte completo para ambas as edições do jogo.
              </p>
            </div>

            <div className="card-gothic p-6">
              <div className="text-blood-500 mb-4">
                <svg className="w-10 h-10 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="font-gothic text-bone-100 text-lg mb-2">Real-Time</h3>
              <p className="text-midnight-400 text-sm">
                Jogue em tempo real com seu coterie via WebSocket.
              </p>
            </div>

            <div className="card-gothic p-6">
              <div className="text-blood-500 mb-4">
                <svg className="w-10 h-10 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
              </div>
              <h3 className="font-gothic text-bone-100 text-lg mb-2">Dados Especiais</h3>
              <p className="text-midnight-400 text-sm">
                Hunger Dice, Messy Criticals e Bestial Failures automáticos.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="py-6 text-center text-midnight-600 text-sm">
        Vampire: The Masquerade is a trademark of Paradox Interactive AB.
      </footer>
    </div>
  )
}
