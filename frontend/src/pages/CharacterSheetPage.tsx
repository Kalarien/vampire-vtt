import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { charactersApi } from '@/lib/api'
import { ArrowLeft, Save } from 'lucide-react'
import { useState, useEffect } from 'react'
import CharacterSheetV5 from '@/components/character/CharacterSheetV5'
import CharacterSheetV20 from '@/components/character/CharacterSheetV20'
import { SheetChangeNotification } from '@/components/character/SheetChangeNotification'
import { useAuthStore } from '@/stores/authStore'

export default function CharacterSheetPage() {
  const { id } = useParams<{ id: string }>()
  const queryClient = useQueryClient()
  const { user } = useAuthStore()
  const [sheet, setSheet] = useState<any>(null)
  const [hasChanges, setHasChanges] = useState(false)

  const { data: character, isLoading } = useQuery({
    queryKey: ['character', id],
    queryFn: async () => {
      const response = await charactersApi.get(id!)
      return response.data
    },
    enabled: !!id,
  })

  useEffect(() => {
    if (character?.sheet) {
      setSheet(character.sheet)
    }
  }, [character])

  const [pendingMessage, setPendingMessage] = useState<string | null>(null)

  const updateMutation = useMutation({
    mutationFn: (newSheet: object) => charactersApi.updateSheet(id!, newSheet),
    onSuccess: (response) => {
      queryClient.invalidateQueries({ queryKey: ['character', id] })
      setHasChanges(false)
      // Verificar se foi enviado para aprovacao
      if (response.data.pending_approval) {
        setPendingMessage(response.data.message || 'Alteracoes enviadas para aprovacao do Narrador')
        setTimeout(() => setPendingMessage(null), 5000)
      }
    },
    onError: (error: any) => {
      const message = error.response?.data?.detail || 'Erro ao salvar'
      setPendingMessage(message)
      setTimeout(() => setPendingMessage(null), 5000)
    }
  })

  const handleSheetChange = (newSheet: any) => {
    setSheet(newSheet)
    setHasChanges(true)
  }

  const handleSave = () => {
    if (sheet) {
      updateMutation.mutate(sheet)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-blood-500 font-gothic text-xl animate-pulse">
          Carregando...
        </div>
      </div>
    )
  }

  if (!character) {
    return (
      <div className="card-gothic p-12 text-center">
        <h2 className="font-gothic text-2xl text-bone-100 mb-4">
          Personagem nao encontrado
        </h2>
        <Link to="/characters" className="btn-blood">
          Voltar para Personagens
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link
            to="/characters"
            className="p-2 text-midnight-400 hover:text-bone-100 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="font-gothic text-3xl text-bone-100">
              {character.name}
            </h1>
            <p className="text-midnight-400">
              {character.clan || 'Sem cla'} -{' '}
              {character.game_version.toUpperCase()}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          {/* Show notifications only for character owner */}
          {user?.id === character.owner_id && id && (
            <SheetChangeNotification characterId={id} />
          )}
          <button
            onClick={handleSave}
            disabled={!hasChanges || updateMutation.isPending}
            className={`btn-blood flex items-center gap-2 ${
              !hasChanges ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            <Save className="w-5 h-5" />
            {updateMutation.isPending ? 'Salvando...' : 'Salvar'}
          </button>
        </div>
      </div>

      {/* Status Messages */}
      {pendingMessage && (
        <div className="bg-blood-700/20 border border-blood-700 text-bone-100 px-4 py-3 rounded-lg">
          {pendingMessage}
        </div>
      )}

      {/* Pending Approval Warning */}
      {character.approval_status === 'pending' && character.pending_sheet && (
        <div className="bg-amber-900/20 border border-amber-600 text-amber-200 px-4 py-3 rounded-lg flex items-center gap-2">
          <span className="text-amber-500">⏳</span>
          <span>Voce tem alteracoes aguardando aprovacao do Narrador</span>
        </div>
      )}

      {/* In Chronicle Notice */}
      {character.chronicle_id && user?.id === character.owner_id && (
        <div className="bg-midnight-800/50 border border-midnight-600 text-midnight-300 px-4 py-3 rounded-lg text-sm">
          Este personagem esta em uma cronica. Alteracoes precisam de aprovacao do Narrador.
        </div>
      )}

      {/* Character Sheet */}
      {sheet && (
        character.game_version === 'v5' ? (
          <CharacterSheetV5
            sheet={sheet}
            onChange={handleSheetChange}
            characterClan={character.clan}
            isOwner={user?.id === character.owner_id}
          />
        ) : (
          <CharacterSheetV20 sheet={sheet} onChange={handleSheetChange} />
        )
      )}
    </div>
  )
}
