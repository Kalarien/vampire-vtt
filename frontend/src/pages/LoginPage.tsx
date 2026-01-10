import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Eye, EyeOff } from 'lucide-react'
import { authApi } from '../lib/api'
import { useAuthStore } from '../stores/authStore'

export function LoginPage() {
  const navigate = useNavigate()
  const login = useAuthStore((state) => state.login)
  const [isLogin, setIsLogin] = useState(true)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [showForgotPassword, setShowForgotPassword] = useState(false)
  const [forgotEmail, setForgotEmail] = useState('')
  const [forgotMessage, setForgotMessage] = useState('')

  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      if (isLogin) {
        const response = await authApi.login({
          email: formData.email,
          password: formData.password,
        })
        const { access_token, user } = response.data
        // zustand persist handles localStorage automatically
        login(access_token, user)
        navigate('/dashboard')
      } else {
        const response = await authApi.register({
          username: formData.username,
          email: formData.email,
          password: formData.password,
        })
        const { access_token, user } = response.data
        // zustand persist handles localStorage automatically
        login(access_token, user)
        navigate('/dashboard')
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao autenticar')
    } finally {
      setIsLoading(false)
    }
  }

  const handleForgotPassword = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setForgotMessage('')

    try {
      await authApi.forgotPassword(forgotEmail)
      setForgotMessage('Se o email existir, enviaremos um link para redefinir sua senha.')
    } catch (err: any) {
      // Don't reveal if email exists or not for security
      setForgotMessage('Se o email existir, enviaremos um link para redefinir sua senha.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center px-4">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-red-600">Vampire VTT</h1>
          <p className="mt-2 text-gray-400">
            {isLogin ? 'Entre na sua conta' : 'Crie sua conta'}
          </p>
        </div>

        <div className="bg-gray-800 rounded-lg shadow-xl p-8">
          {error && (
            <div className="mb-4 p-3 bg-red-900/50 border border-red-700 rounded text-red-200 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {!isLogin && (
              <div>
                <label htmlFor="username" className="block text-sm font-medium text-gray-300">
                  Nome de Usuario
                </label>
                <input
                  id="username"
                  type="text"
                  required={!isLogin}
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  className="mt-1 block w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  placeholder="Seu nome"
                />
              </div>
            )}

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-300">
                Email
              </label>
              <input
                id="email"
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="mt-1 block w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
                placeholder="seu@email.com"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300">
                Senha
              </label>
              <div className="relative mt-1">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="block w-full px-3 py-2 pr-10 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  placeholder="********"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-white"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {isLogin && (
              <div className="text-right">
                <button
                  type="button"
                  onClick={() => setShowForgotPassword(true)}
                  className="text-sm text-red-400 hover:text-red-300"
                >
                  Esqueceu a senha?
                </button>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Carregando...' : isLogin ? 'Entrar' : 'Criar Conta'}
            </button>
          </form>

          <div className="mt-4">
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="w-full text-center text-sm text-gray-400 hover:text-white"
            >
              {isLogin ? 'Nao tem conta? Criar uma' : 'Ja tem conta? Entrar'}
            </button>
          </div>

        </div>
      </div>

      {/* Forgot Password Modal */}
      {showForgotPassword && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold text-white mb-4">Recuperar Senha</h2>

            {forgotMessage ? (
              <div className="space-y-4">
                <p className="text-green-400 text-sm">{forgotMessage}</p>
                <p className="text-gray-400 text-xs">
                  Em desenvolvimento, verifique o console do servidor para ver o link de recuperacao.
                </p>
                <button
                  onClick={() => {
                    setShowForgotPassword(false)
                    setForgotEmail('')
                    setForgotMessage('')
                  }}
                  className="w-full py-2 px-4 bg-gray-600 hover:bg-gray-500 text-white rounded-md"
                >
                  Fechar
                </button>
              </div>
            ) : (
              <form onSubmit={handleForgotPassword} className="space-y-4">
                <p className="text-gray-400 text-sm">
                  Digite seu email e enviaremos um link para redefinir sua senha.
                </p>
                <div>
                  <label htmlFor="forgot-email" className="block text-sm font-medium text-gray-300">
                    Email
                  </label>
                  <input
                    id="forgot-email"
                    type="email"
                    required
                    value={forgotEmail}
                    onChange={(e) => setForgotEmail(e.target.value)}
                    className="mt-1 block w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
                    placeholder="seu@email.com"
                  />
                </div>
                <div className="flex gap-3">
                  <button
                    type="button"
                    onClick={() => {
                      setShowForgotPassword(false)
                      setForgotEmail('')
                    }}
                    className="flex-1 py-2 px-4 bg-gray-600 hover:bg-gray-500 text-white rounded-md"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="flex-1 py-2 px-4 bg-red-600 hover:bg-red-700 text-white rounded-md disabled:opacity-50"
                  >
                    {isLoading ? 'Enviando...' : 'Enviar'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
