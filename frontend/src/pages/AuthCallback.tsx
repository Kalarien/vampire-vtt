import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { authApi } from '@/lib/api'

export default function AuthCallback() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { login } = useAuthStore()
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const code = searchParams.get('code')
    if (!code) {
      setError('Codigo de autorizacao nao recebido')
      return
    }

    const handleCallback = async () => {
      try {
        const response = await authApi.callback(code)
        await login(response.data.access_token)
        navigate('/dashboard')
      } catch (err) {
        console.error('Auth callback error:', err)
        setError('Falha na autenticacao. Por favor, tente novamente.')
      }
    }

    handleCallback()
  }, [searchParams, login, navigate])

  if (error) {
    return (
      <div className="min-h-screen bg-midnight-950 flex items-center justify-center">
        <div className="card-gothic p-8 text-center max-w-md">
          <h1 className="font-gothic text-2xl text-blood-500 mb-4">
            Erro de Autenticacao
          </h1>
          <p className="text-bone-300 mb-6">{error}</p>
          <button
            onClick={() => navigate('/')}
            className="btn-blood"
          >
            Voltar ao Inicio
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-midnight-950 flex items-center justify-center">
      <div className="text-center">
        <div className="w-16 h-16 bg-blood-700 rounded-2xl flex items-center justify-center mx-auto mb-6 animate-pulse-blood">
          <span className="font-gothic text-bone-100 text-3xl">V</span>
        </div>
        <p className="text-bone-300 font-gothic text-xl">Autenticando...</p>
      </div>
    </div>
  )
}
