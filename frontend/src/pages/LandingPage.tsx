import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'

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

          {/* Login Button */}
          <div className="flex justify-center">
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
              Entrar
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
