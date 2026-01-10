import { useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import Layout from '@/components/layout/Layout'
import LandingPage from '@/pages/LandingPage'
import { LoginPage } from '@/pages/LoginPage'
import { ResetPasswordPage } from '@/pages/ResetPasswordPage'
import DashboardPage from '@/pages/DashboardPage'
import ChroniclesPage from '@/pages/ChroniclesPage'
import ChroniclePage from '@/pages/ChroniclePage'
import CharactersPage from '@/pages/CharactersPage'
import CharacterSheetPage from '@/pages/CharacterSheetPage'
import DiceRollerPage from '@/pages/DiceRollerPage'
import AuthCallback from '@/pages/AuthCallback'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading, checkAuth } = useAuthStore()

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-midnight-950 flex items-center justify-center">
        <div className="text-blood-500 font-gothic text-2xl animate-pulse">
          Carregando...
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/" replace />
  }

  return <>{children}</>
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/reset-password" element={<ResetPasswordPage />} />
      <Route path="/auth/callback" element={<AuthCallback />} />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Layout>
              <DashboardPage />
            </Layout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/chronicles"
        element={
          <ProtectedRoute>
            <Layout>
              <ChroniclesPage />
            </Layout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/chronicles/:id"
        element={
          <ProtectedRoute>
            <Layout>
              <ChroniclePage />
            </Layout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/characters"
        element={
          <ProtectedRoute>
            <Layout>
              <CharactersPage />
            </Layout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/characters/:id"
        element={
          <ProtectedRoute>
            <Layout>
              <CharacterSheetPage />
            </Layout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/dice"
        element={
          <ProtectedRoute>
            <Layout>
              <DiceRollerPage />
            </Layout>
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}

export default App
