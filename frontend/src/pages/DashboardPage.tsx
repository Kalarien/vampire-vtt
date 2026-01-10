import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { useAuthStore } from '@/stores/authStore'
import { chroniclesApi, charactersApi } from '@/lib/api'
import { BookOpen, Users, Dice6, Plus } from 'lucide-react'

export default function DashboardPage() {
  const { user } = useAuthStore()

  const { data: chronicles } = useQuery({
    queryKey: ['chronicles'],
    queryFn: async () => {
      const response = await chroniclesApi.list()
      return response.data
    },
  })

  const { data: characters } = useQuery({
    queryKey: ['characters'],
    queryFn: async () => {
      const response = await charactersApi.list()
      return response.data
    },
  })

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div className="card-blood p-8">
        <h1 className="font-gothic text-3xl text-bone-100 mb-2">
          Bem-vindo, {user?.username}
        </h1>
        <p className="text-bone-400">
          A Noite Pertence aos Imortais. O que deseja fazer esta noite?
        </p>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link
          to="/chronicles"
          className="card-gothic p-6 hover:border-blood-700 transition-colors group"
        >
          <div className="flex items-center gap-4 mb-4">
            <div className="w-12 h-12 bg-blood-700/20 rounded-lg flex items-center justify-center group-hover:bg-blood-700/40 transition-colors">
              <BookOpen className="w-6 h-6 text-blood-500" />
            </div>
            <div>
              <h3 className="font-gothic text-bone-100 text-lg">Cronicas</h3>
              <p className="text-midnight-400 text-sm">
                {chronicles?.length || 0} cronicas
              </p>
            </div>
          </div>
          <p className="text-bone-400 text-sm">
            Crie ou participe de cronicas com outros jogadores.
          </p>
        </Link>

        <Link
          to="/characters"
          className="card-gothic p-6 hover:border-blood-700 transition-colors group"
        >
          <div className="flex items-center gap-4 mb-4">
            <div className="w-12 h-12 bg-blood-700/20 rounded-lg flex items-center justify-center group-hover:bg-blood-700/40 transition-colors">
              <Users className="w-6 h-6 text-blood-500" />
            </div>
            <div>
              <h3 className="font-gothic text-bone-100 text-lg">Personagens</h3>
              <p className="text-midnight-400 text-sm">
                {characters?.length || 0} personagens
              </p>
            </div>
          </div>
          <p className="text-bone-400 text-sm">
            Gerencie suas fichas de personagem V5 e V20.
          </p>
        </Link>

        <Link
          to="/dice"
          className="card-gothic p-6 hover:border-blood-700 transition-colors group"
        >
          <div className="flex items-center gap-4 mb-4">
            <div className="w-12 h-12 bg-blood-700/20 rounded-lg flex items-center justify-center group-hover:bg-blood-700/40 transition-colors">
              <Dice6 className="w-6 h-6 text-blood-500" />
            </div>
            <div>
              <h3 className="font-gothic text-bone-100 text-lg">Dados</h3>
              <p className="text-midnight-400 text-sm">Rolador de dados</p>
            </div>
          </div>
          <p className="text-bone-400 text-sm">
            Role dados V5 com Hunger ou V20 com Botch.
          </p>
        </Link>
      </div>

      {/* Recent Chronicles */}
      <div className="card-gothic p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="font-gothic text-xl text-bone-100">
            Cronicas Recentes
          </h2>
          <Link
            to="/chronicles"
            className="text-blood-500 hover:text-blood-400 text-sm font-gothic"
          >
            Ver todas
          </Link>
        </div>

        {chronicles && chronicles.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {chronicles.slice(0, 4).map((chronicle: any) => (
              <Link
                key={chronicle.id}
                to={`/chronicles/${chronicle.id}`}
                className="bg-midnight-800/50 rounded-lg p-4 hover:bg-midnight-800 transition-colors"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-gothic text-bone-100">
                    {chronicle.name}
                  </h3>
                  <span className="text-xs px-2 py-1 bg-midnight-700 rounded text-bone-400">
                    {chronicle.game_version.toUpperCase()}
                  </span>
                </div>
                <p className="text-midnight-400 text-sm line-clamp-2">
                  {chronicle.description || 'Sem descricao'}
                </p>
              </Link>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-midnight-400 mb-4">
              Voce ainda nao participa de nenhuma cronica.
            </p>
            <Link to="/chronicles" className="btn-blood inline-flex items-center gap-2">
              <Plus className="w-5 h-5" />
              Criar Cronica
            </Link>
          </div>
        )}
      </div>

      {/* Recent Characters */}
      <div className="card-gothic p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="font-gothic text-xl text-bone-100">
            Seus Personagens
          </h2>
          <Link
            to="/characters"
            className="text-blood-500 hover:text-blood-400 text-sm font-gothic"
          >
            Ver todos
          </Link>
        </div>

        {characters && characters.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {characters.slice(0, 6).map((character: any) => (
              <Link
                key={character.id}
                to={`/characters/${character.id}`}
                className="bg-midnight-800/50 rounded-lg p-4 hover:bg-midnight-800 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-blood-700/30 rounded-full flex items-center justify-center">
                    <span className="font-gothic text-blood-400">
                      {character.name[0]}
                    </span>
                  </div>
                  <div>
                    <h3 className="font-gothic text-bone-100">
                      {character.name}
                    </h3>
                    <p className="text-midnight-400 text-xs">
                      {character.sheet?.clan || 'Sem cla'} - {character.game_version.toUpperCase()}
                    </p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-midnight-400 mb-4">
              Voce ainda nao criou nenhum personagem.
            </p>
            <Link to="/characters" className="btn-blood inline-flex items-center gap-2">
              <Plus className="w-5 h-5" />
              Criar Personagem
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}
