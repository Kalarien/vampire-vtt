import { Link, useLocation } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import {
  Home,
  BookOpen,
  Users,
  Dice6,
  LogOut,
  Menu,
  X,
} from 'lucide-react'
import { useState } from 'react'
import { cn } from '@/lib/utils'

interface LayoutProps {
  children: React.ReactNode
}

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: Home },
  { path: '/chronicles', label: 'Crônicas', icon: BookOpen },
  { path: '/characters', label: 'Personagens', icon: Users },
  { path: '/dice', label: 'Dados', icon: Dice6 },
]

export default function Layout({ children }: LayoutProps) {
  const { user, logout } = useAuthStore()
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <div className="min-h-screen bg-midnight-950">
      {/* Header */}
      <header className="bg-midnight-900/95 border-b border-midnight-700 sticky top-0 z-50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/dashboard" className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blood-700 rounded-lg flex items-center justify-center">
                <span className="font-gothic text-bone-100 text-xl">V</span>
              </div>
              <span className="font-gothic text-bone-100 text-xl hidden sm:block">
                Vampire VTT
              </span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-1">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname.startsWith(item.path)
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={cn(
                      'flex items-center gap-2 px-4 py-2 rounded-lg transition-colors',
                      isActive
                        ? 'bg-blood-700/30 text-blood-400'
                        : 'text-bone-300 hover:bg-midnight-800 hover:text-bone-100'
                    )}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-gothic">{item.label}</span>
                  </Link>
                )
              })}
            </nav>

            {/* User Menu */}
            <div className="flex items-center gap-4">
              <div className="hidden sm:flex items-center gap-2">
                {user?.avatar && (
                  <img
                    src={`https://cdn.discordapp.com/avatars/${user.discord_id}/${user.avatar}.png`}
                    alt={user.username}
                    className="w-8 h-8 rounded-full"
                  />
                )}
                <span className="text-bone-300 text-sm">{user?.username}</span>
              </div>
              <button
                onClick={logout}
                className="p-2 text-bone-400 hover:text-blood-400 transition-colors"
                title="Sair"
              >
                <LogOut className="w-5 h-5" />
              </button>

              {/* Mobile menu button */}
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="md:hidden p-2 text-bone-300 hover:text-bone-100"
              >
                {mobileMenuOpen ? (
                  <X className="w-6 h-6" />
                ) : (
                  <Menu className="w-6 h-6" />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-midnight-700 bg-midnight-900">
            <nav className="px-4 py-2 space-y-1">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname.startsWith(item.path)
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setMobileMenuOpen(false)}
                    className={cn(
                      'flex items-center gap-3 px-4 py-3 rounded-lg transition-colors',
                      isActive
                        ? 'bg-blood-700/30 text-blood-400'
                        : 'text-bone-300 hover:bg-midnight-800'
                    )}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-gothic">{item.label}</span>
                  </Link>
                )
              })}
            </nav>
          </div>
        )}
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-midnight-900/50 border-t border-midnight-800 py-6 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-midnight-500 text-sm">
            Vampire VTT - Virtual Tabletop for Vampire: The Masquerade
          </p>
        </div>
      </footer>
    </div>
  )
}
