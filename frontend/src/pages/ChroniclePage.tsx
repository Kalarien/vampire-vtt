import { useState, useEffect, useRef } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { chroniclesApi, scenesApi, charactersApi } from '@/lib/api'
import { useAuthStore } from '@/stores/authStore'
import {
  Users, Calendar, BookOpen, Plus, MapPin, Play, Pause,
  Copy, RefreshCw, Check, X, Edit3, Trash2, UserPlus,
  MessageSquare, Swords, Award
} from 'lucide-react'
import { formatDate, cn } from '@/lib/utils'
import { SessionControls } from '@/components/session/SessionControls'
import { SessionHistory } from '@/components/session/SessionHistory'
import { ChatPanel } from '@/components/chat/ChatPanel'
import { InitiativeTracker } from '@/components/initiative/InitiativeTracker'
import { XPRequestList } from '@/components/xp/XPRequestList'
import { CharacterApprovalList } from '@/components/character/CharacterApprovalList'

export default function ChroniclePage() {
  const { id } = useParams<{ id: string }>()
  const { user, token } = useAuthStore()
  const queryClient = useQueryClient()

  const [showCreateScene, setShowCreateScene] = useState(false)
  const [showEditChronicle, setShowEditChronicle] = useState(false)
  const [showAssignCharacter, setShowAssignCharacter] = useState(false)
  const [showConfirmAssign, setShowConfirmAssign] = useState(false)
  const [selectedCharacterToAssign, setSelectedCharacterToAssign] = useState<any>(null)
  const [copiedInvite, setCopiedInvite] = useState(false)
  const [newScene, setNewScene] = useState({ name: '', description: '', location: '' })
  const [editData, setEditData] = useState({ name: '', description: '' })
  const [activeTab, setActiveTab] = useState<'scenes' | 'chat' | 'combat' | 'sessions' | 'xp' | 'characters'>('scenes')
  const [websocket, setWebsocket] = useState<WebSocket | null>(null)
  const wsRef = useRef<WebSocket | null>(null)

  // WebSocket connection
  useEffect(() => {
    if (!id || !user || !token) return

    const wsUrl = `ws://localhost:8001/ws/chronicle/${id}?token=${token}`
    const ws = new WebSocket(wsUrl)

    ws.onopen = () => {
      console.log('WebSocket connected')
      setWebsocket(ws)
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected')
      setWebsocket(null)
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    wsRef.current = ws

    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close()
      }
    }
  }, [id, user, token])

  const { data: chronicle, isLoading } = useQuery({
    queryKey: ['chronicle', id],
    queryFn: async () => {
      const response = await chroniclesApi.get(id!)
      return response.data
    },
    enabled: !!id,
  })

  const { data: scenes } = useQuery({
    queryKey: ['scenes', id],
    queryFn: async () => {
      const response = await scenesApi.list(id!)
      return response.data
    },
    enabled: !!id,
  })

  // Get user's characters that are not in any chronicle
  const { data: availableCharacters } = useQuery({
    queryKey: ['characters', 'available'],
    queryFn: async () => {
      const response = await charactersApi.list()
      return (response.data as any[]).filter((c: any) => !c.chronicle_id)
    },
  })

  // Mutations
  const createSceneMutation = useMutation({
    mutationFn: (data: { name: string; description?: string; location?: string }) =>
      scenesApi.create(id!, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scenes', id] })
      setShowCreateScene(false)
      setNewScene({ name: '', description: '', location: '' })
    },
  })

  const toggleSceneMutation = useMutation({
    mutationFn: (scene: any) =>
      scenesApi.update(id!, scene.id, { is_active: !scene.is_active }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scenes', id] })
    },
  })

  const deleteSceneMutation = useMutation({
    mutationFn: (sceneId: string) => scenesApi.delete(id!, sceneId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scenes', id] })
    },
  })

  const updateChronicleMutation = useMutation({
    mutationFn: (data: { name?: string; description?: string }) =>
      chroniclesApi.update(id!, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chronicle', id] })
      setShowEditChronicle(false)
    },
  })

  const regenerateInviteMutation = useMutation({
    mutationFn: () => chroniclesApi.regenerateInvite(id!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chronicle', id] })
    },
  })

  const assignCharacterMutation = useMutation({
    mutationFn: (characterId: string) => charactersApi.assignToChronicle(characterId, id!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chronicle', id] })
      queryClient.invalidateQueries({ queryKey: ['characters'] })
      queryClient.invalidateQueries({ queryKey: ['characters', 'available'] })
      setShowAssignCharacter(false)
      setShowConfirmAssign(false)
      setSelectedCharacterToAssign(null)
    },
    onError: (error: any) => {
      console.error('Erro ao adicionar personagem:', error)
      alert(error.response?.data?.detail || 'Erro ao adicionar personagem')
    },
  })

  const unassignCharacterMutation = useMutation({
    mutationFn: (characterId: string) => charactersApi.unassignFromChronicle(characterId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chronicle', id] })
      queryClient.invalidateQueries({ queryKey: ['characters'] })
    },
  })

  const copyInviteCode = () => {
    if (chronicle?.invite_code) {
      navigator.clipboard.writeText(chronicle.invite_code)
      setCopiedInvite(true)
      setTimeout(() => setCopiedInvite(false), 2000)
    }
  }

  const openEditModal = () => {
    setEditData({ name: chronicle?.name || '', description: chronicle?.description || '' })
    setShowEditChronicle(true)
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

  if (!chronicle) {
    return (
      <div className="card-gothic p-12 text-center">
        <h2 className="font-gothic text-2xl text-bone-100 mb-4">
          Cronica nao encontrada
        </h2>
        <Link to="/chronicles" className="btn-blood">
          Voltar para Cronicas
        </Link>
      </div>
    )
  }

  const isStoryteller = chronicle.storyteller_id === user?.id

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card-blood p-8">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="font-gothic text-3xl text-bone-100">
                {chronicle.name}
              </h1>
              <span className="text-xs px-2 py-1 bg-midnight-700 rounded text-bone-400">
                {chronicle.game_version.toUpperCase()}
              </span>
            </div>
            <p className="text-bone-400 max-w-2xl">
              {chronicle.description || 'Sem descricao'}
            </p>
          </div>
          <div className="flex items-center gap-2">
            {isStoryteller && (
              <button
                onClick={openEditModal}
                className="p-2 text-midnight-400 hover:text-bone-100 transition-colors"
                title="Editar cronica"
              >
                <Edit3 className="w-5 h-5" />
              </button>
            )}
            <span className="text-xs px-3 py-1 bg-blood-700/30 rounded text-blood-400 font-gothic">
              {isStoryteller ? 'Narrador' : 'Jogador'}
            </span>
          </div>
        </div>

        <div className="flex items-center justify-between mt-6">
          <div className="flex items-center gap-6 text-midnight-400 text-sm">
            <span className="flex items-center gap-2">
              <Users className="w-4 h-4" />
              {chronicle.members?.length || 1} membros
            </span>
            <span className="flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              Criada em {formatDate(chronicle.created_at)}
            </span>
          </div>

          {/* Invite Code */}
          {isStoryteller && chronicle.invite_code && (
            <div className="flex items-center gap-2">
              <span className="text-midnight-400 text-sm">Convite:</span>
              <code className="px-3 py-1 bg-midnight-800 rounded text-bone-300 font-mono text-sm">
                {chronicle.invite_code}
              </code>
              <button
                onClick={copyInviteCode}
                className="p-1.5 text-midnight-400 hover:text-bone-100 transition-colors"
                title="Copiar codigo"
              >
                {copiedInvite ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
              </button>
              <button
                onClick={() => regenerateInviteMutation.mutate()}
                className="p-1.5 text-midnight-400 hover:text-bone-100 transition-colors"
                title="Gerar novo codigo"
                disabled={regenerateInviteMutation.isPending}
              >
                <RefreshCw className={cn("w-4 h-4", regenerateInviteMutation.isPending && "animate-spin")} />
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-midnight-700 pb-2">
        <button
          onClick={() => setActiveTab('scenes')}
          className={cn(
            "px-4 py-2 rounded-t-lg flex items-center gap-2 transition-colors",
            activeTab === 'scenes'
              ? "bg-midnight-800 text-bone-100"
              : "text-midnight-400 hover:text-bone-300"
          )}
        >
          <BookOpen className="w-4 h-4" />
          Cenas
        </button>
        <button
          onClick={() => setActiveTab('chat')}
          className={cn(
            "px-4 py-2 rounded-t-lg flex items-center gap-2 transition-colors",
            activeTab === 'chat'
              ? "bg-midnight-800 text-bone-100"
              : "text-midnight-400 hover:text-bone-300"
          )}
        >
          <MessageSquare className="w-4 h-4" />
          Chat
        </button>
        <button
          onClick={() => setActiveTab('combat')}
          className={cn(
            "px-4 py-2 rounded-t-lg flex items-center gap-2 transition-colors",
            activeTab === 'combat'
              ? "bg-midnight-800 text-bone-100"
              : "text-midnight-400 hover:text-bone-300"
          )}
        >
          <Swords className="w-4 h-4" />
          Combate
        </button>
        <button
          onClick={() => setActiveTab('sessions')}
          className={cn(
            "px-4 py-2 rounded-t-lg flex items-center gap-2 transition-colors",
            activeTab === 'sessions'
              ? "bg-midnight-800 text-bone-100"
              : "text-midnight-400 hover:text-bone-300"
          )}
        >
          <Calendar className="w-4 h-4" />
          Sessoes
        </button>
        {isStoryteller && (
          <button
            onClick={() => setActiveTab('xp')}
            className={cn(
              "px-4 py-2 rounded-t-lg flex items-center gap-2 transition-colors",
              activeTab === 'xp'
                ? "bg-midnight-800 text-bone-100"
                : "text-midnight-400 hover:text-bone-300"
            )}
          >
            <Award className="w-4 h-4" />
            XP Pendentes
          </button>
        )}
        <button
          onClick={() => setActiveTab('characters')}
          className={cn(
            "px-4 py-2 rounded-t-lg flex items-center gap-2 transition-colors",
            activeTab === 'characters'
              ? "bg-midnight-800 text-bone-100"
              : "text-midnight-400 hover:text-bone-300"
          )}
        >
          <Users className="w-4 h-4" />
          Personagens
        </button>
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content Area */}
        <div className="lg:col-span-2 space-y-6">
          {/* Session Controls - Always visible for storyteller */}
          {isStoryteller && (
            <SessionControls
              chronicleId={id!}
              isStoryteller={isStoryteller}
              userCharacters={chronicle.characters?.map((c: any) => ({ id: c.id, name: c.name })) || []}
              chronicleCharacters={chronicle.characters?.map((c: any) => ({
                id: c.id,
                name: c.name,
                clan: c.clan,
                owner_name: c.owner_name
              })) || []}
            />
          )}

          {/* Scenes Tab */}
          {activeTab === 'scenes' && (
          <div className="card-gothic p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="font-gothic text-xl text-bone-100">Cenas</h2>
              {isStoryteller && (
                <button
                  onClick={() => setShowCreateScene(true)}
                  className="btn-blood text-sm flex items-center gap-2"
                >
                  <Plus className="w-4 h-4" />
                  Nova Cena
                </button>
              )}
            </div>

            {scenes && scenes.length > 0 ? (
              <div className="space-y-4">
                {scenes.map((scene: any) => (
                  <div
                    key={scene.id}
                    className={cn(
                      "rounded-lg p-4 transition-colors",
                      scene.is_active
                        ? "bg-green-900/20 border border-green-800/30"
                        : "bg-midnight-800/50 hover:bg-midnight-800"
                    )}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <h3 className="font-gothic text-bone-100">
                            {scene.name}
                          </h3>
                          {scene.is_active && (
                            <span className="flex items-center gap-1 text-xs px-2 py-0.5 bg-green-900/30 text-green-400 rounded">
                              <Play className="w-3 h-3" />
                              Ativa
                            </span>
                          )}
                        </div>
                        {scene.location && (
                          <p className="text-midnight-400 text-sm flex items-center gap-1">
                            <MapPin className="w-3 h-3" />
                            {scene.location}
                          </p>
                        )}
                        <p className="text-bone-400 text-sm mt-2">
                          {scene.description || 'Sem descricao'}
                        </p>
                      </div>
                      {isStoryteller && (
                        <div className="flex items-center gap-1">
                          <button
                            onClick={() => toggleSceneMutation.mutate(scene)}
                            className={cn(
                              "p-2 rounded transition-colors",
                              scene.is_active
                                ? "text-green-400 hover:bg-green-900/30"
                                : "text-midnight-400 hover:bg-midnight-700"
                            )}
                            title={scene.is_active ? "Pausar cena" : "Ativar cena"}
                          >
                            {scene.is_active ? (
                              <Pause className="w-4 h-4" />
                            ) : (
                              <Play className="w-4 h-4" />
                            )}
                          </button>
                          <button
                            onClick={() => deleteSceneMutation.mutate(scene.id)}
                            className="p-2 text-midnight-400 hover:text-blood-500 rounded hover:bg-midnight-700 transition-colors"
                            title="Excluir cena"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <BookOpen className="w-12 h-12 text-midnight-600 mx-auto mb-4" />
                <p className="text-midnight-400">
                  Nenhuma cena criada ainda.
                </p>
                {isStoryteller && (
                  <button
                    onClick={() => setShowCreateScene(true)}
                    className="btn-blood text-sm mt-4 inline-flex items-center gap-2"
                  >
                    <Plus className="w-4 h-4" />
                    Criar Primeira Cena
                  </button>
                )}
              </div>
            )}
          </div>
          )}

          {/* Chat Tab */}
          {activeTab === 'chat' && (
            <div className="h-[600px]">
              <ChatPanel
                chronicleId={id!}
                userId={user?.id || ''}
                username={user?.username || ''}
                characterId={chronicle.characters?.find((c: any) => c.owner_id === user?.id)?.id}
                characterName={chronicle.characters?.find((c: any) => c.owner_id === user?.id)?.name}
                websocket={websocket}
              />
            </div>
          )}

          {/* Combat Tab */}
          {activeTab === 'combat' && (
            <InitiativeTracker
              sessionId={id!}
              isStoryteller={isStoryteller}
              chronicleCharacters={chronicle.characters?.map((c: any) => ({ id: c.id, name: c.name })) || []}
            />
          )}

          {/* Sessions Tab */}
          {activeTab === 'sessions' && (
            <div className="card-gothic p-6">
              <SessionHistory chronicleId={id!} />
            </div>
          )}

          {/* XP Requests Tab (Storyteller only) */}
          {activeTab === 'xp' && isStoryteller && (
            <XPRequestList
              chronicleId={id!}
              isStoryteller={isStoryteller}
            />
          )}

          {/* Characters Tab - Different views for storyteller and player */}
          {activeTab === 'characters' && (
            <div className="card-gothic p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="font-gothic text-xl text-bone-100">
                  {isStoryteller ? 'Gerenciar Personagens' : 'Personagens da Cronica'}
                </h2>
                {!isStoryteller && (
                  <button
                    onClick={() => setShowAssignCharacter(true)}
                    className="btn-blood text-sm flex items-center gap-2"
                  >
                    <Plus className="w-4 h-4" />
                    Adicionar Meu Personagem
                  </button>
                )}
              </div>

              {/* Storyteller view - Show approval list */}
              {isStoryteller && (
                <CharacterApprovalList
                  chronicleId={id!}
                  isStoryteller={isStoryteller}
                  onApprovalChange={() => {
                    queryClient.invalidateQueries({ queryKey: ['chronicle', id] })
                  }}
                />
              )}

              {/* Player view - Show approved characters and my pending ones */}
              {!isStoryteller && (
                <div className="space-y-4">
                  {/* My characters in this chronicle */}
                  {chronicle.characters?.filter((c: any) => c.owner_id === user?.id).length > 0 && (
                    <div className="mb-6">
                      <h3 className="text-sm text-gray-400 mb-3">Meus Personagens</h3>
                      <div className="space-y-2">
                        {chronicle.characters
                          ?.filter((c: any) => c.owner_id === user?.id)
                          .map((char: any) => (
                            <div
                              key={char.id}
                              className="flex items-center justify-between bg-midnight-800/50 rounded-lg p-3"
                            >
                              <Link to={`/characters/${char.id}`} className="flex items-center gap-3">
                                <div className="w-10 h-10 bg-blood-700/30 rounded-full flex items-center justify-center">
                                  <span className="text-blood-400">{char.name[0]}</span>
                                </div>
                                <div>
                                  <p className="text-bone-100 font-medium">{char.name}</p>
                                  <p className="text-midnight-400 text-sm">{char.clan || 'Sem cla'}</p>
                                </div>
                              </Link>
                              <div className="flex items-center gap-2">
                                {char.approval_status === 'pending' && (
                                  <span className="px-2 py-1 bg-yellow-600/30 text-yellow-400 text-xs rounded">
                                    Aguardando Aprovacao
                                  </span>
                                )}
                                {char.approval_status === 'approved' && (
                                  <span className="px-2 py-1 bg-green-600/30 text-green-400 text-xs rounded">
                                    Aprovado
                                  </span>
                                )}
                                {char.approval_status === 'rejected' && (
                                  <span className="px-2 py-1 bg-red-600/30 text-red-400 text-xs rounded" title={char.storyteller_notes}>
                                    Rejeitado
                                  </span>
                                )}
                              </div>
                            </div>
                          ))}
                      </div>
                    </div>
                  )}

                  {/* Other approved characters */}
                  <div>
                    <h3 className="text-sm text-gray-400 mb-3">Outros Personagens Aprovados</h3>
                    {chronicle.characters?.filter((c: any) => c.owner_id !== user?.id && c.approval_status === 'approved').length > 0 ? (
                      <div className="space-y-2">
                        {chronicle.characters
                          ?.filter((c: any) => c.owner_id !== user?.id && c.approval_status === 'approved')
                          .map((char: any) => (
                            <div
                              key={char.id}
                              className="flex items-center gap-3 bg-midnight-800/50 rounded-lg p-3"
                            >
                              <div className="w-10 h-10 bg-blood-700/30 rounded-full flex items-center justify-center">
                                <span className="text-blood-400">{char.name[0]}</span>
                              </div>
                              <div>
                                <p className="text-bone-100 font-medium">{char.name}</p>
                                <p className="text-midnight-400 text-sm">
                                  {char.clan || 'Sem cla'} - {char.owner_name}
                                </p>
                              </div>
                            </div>
                          ))}
                      </div>
                    ) : (
                      <p className="text-midnight-400 text-center py-4">
                        Nenhum outro personagem aprovado ainda.
                      </p>
                    )}
                  </div>

                  {/* No characters at all */}
                  {!chronicle.characters?.some((c: any) => c.owner_id === user?.id) && (
                    <div className="text-center py-8 border-t border-midnight-700 mt-6">
                      <p className="text-midnight-400 mb-4">
                        Voce ainda nao adicionou nenhum personagem a esta cronica.
                      </p>
                      <button
                        onClick={() => setShowAssignCharacter(true)}
                        className="btn-blood inline-flex items-center gap-2"
                      >
                        <Plus className="w-4 h-4" />
                        Adicionar Personagem
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Members */}
          <div className="card-gothic p-6">
            <h2 className="font-gothic text-xl text-bone-100 mb-4">Membros</h2>
            <div className="space-y-3">
              {chronicle.members?.map((member: any) => (
                <div
                  key={member.user_id}
                  className="flex items-center gap-3 p-2 rounded hover:bg-midnight-800/50"
                >
                  <div className="w-8 h-8 bg-blood-700/30 rounded-full flex items-center justify-center">
                    <span className="text-blood-400 text-sm">
                      {member.username?.[0] || '?'}
                    </span>
                  </div>
                  <div className="flex-1">
                    <p className="text-bone-100 text-sm">
                      {member.username || 'Usuario'}
                    </p>
                    <p className="text-midnight-400 text-xs">
                      {member.role === 'storyteller' ? 'Narrador' : 'Jogador'}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Characters in Chronicle */}
          <div className="card-gothic p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-gothic text-xl text-bone-100">
                Personagens
              </h2>
              <button
                onClick={() => setShowAssignCharacter(true)}
                className="p-1.5 text-midnight-400 hover:text-bone-100 transition-colors"
                title="Adicionar personagem"
              >
                <UserPlus className="w-4 h-4" />
              </button>
            </div>
            {chronicle.characters?.length > 0 ? (
              <div className="space-y-3">
                {chronicle.characters.map((char: any) => {
                  const canViewSheet = char.owner_id === user?.id || isStoryteller

                  const CharContent = (
                    <>
                      <div className="w-8 h-8 bg-blood-700/30 rounded-full flex items-center justify-center">
                        <span className="text-blood-400 text-sm">
                          {char.name[0]}
                        </span>
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <p className="text-bone-100 text-sm">{char.name}</p>
                          {char.owner_id === user?.id && (
                            <span className="px-1.5 py-0.5 bg-blood-600/30 text-blood-400 text-xs rounded">
                              Meu
                            </span>
                          )}
                          {char.approval_status === 'pending' && (
                            <span className="px-1.5 py-0.5 bg-yellow-600/30 text-yellow-400 text-xs rounded">
                              Pendente
                            </span>
                          )}
                          {char.approval_status === 'rejected' && (
                            <span className="px-1.5 py-0.5 bg-red-600/30 text-red-400 text-xs rounded">
                              Rejeitado
                            </span>
                          )}
                        </div>
                        <p className="text-midnight-400 text-xs">
                          {char.clan || char.sheet?.clan || 'Sem cla'}
                        </p>
                      </div>
                    </>
                  )

                  return (
                    <div
                      key={char.id}
                      className="flex items-center gap-3 p-2 rounded hover:bg-midnight-800/50 group"
                    >
                      {canViewSheet ? (
                        <Link
                          to={`/characters/${char.id}`}
                          className="flex items-center gap-3 flex-1 cursor-pointer"
                        >
                          {CharContent}
                        </Link>
                      ) : (
                        <div className="flex items-center gap-3 flex-1">
                          {CharContent}
                        </div>
                      )}
                      {isStoryteller && (
                        <button
                          onClick={() => unassignCharacterMutation.mutate(char.id)}
                          className="p-1.5 text-midnight-400 hover:text-blood-500 opacity-0 group-hover:opacity-100 transition-opacity"
                          title="Remover da cronica"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  )
                })}
              </div>
            ) : (
              <div className="text-center py-4">
                <p className="text-midnight-400 text-sm">
                  Nenhum personagem na cronica.
                </p>
                <button
                  onClick={() => setShowAssignCharacter(true)}
                  className="btn-midnight text-xs mt-3 inline-flex items-center gap-1"
                >
                  <UserPlus className="w-3 h-3" />
                  Adicionar
                </button>
              </div>
            )}
          </div>

          {/* Quick Actions */}
          <div className="card-gothic p-6">
            <h2 className="font-gothic text-xl text-bone-100 mb-4">Acoes</h2>
            <div className="space-y-2">
              <Link
                to="/dice"
                className="btn-midnight w-full justify-center text-sm"
              >
                Rolar Dados
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Create Scene Modal */}
      {showCreateScene && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="card-gothic p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-6">
              <h2 className="font-gothic text-xl text-bone-100">Nova Cena</h2>
              <button
                onClick={() => setShowCreateScene(false)}
                className="text-midnight-400 hover:text-bone-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault()
                createSceneMutation.mutate(newScene)
              }}
              className="space-y-4"
            >
              <div>
                <label className="block text-bone-300 text-sm mb-2">
                  Nome da Cena
                </label>
                <input
                  type="text"
                  value={newScene.name}
                  onChange={(e) => setNewScene({ ...newScene, name: e.target.value })}
                  className="input-gothic w-full"
                  placeholder="Ex: O Elysium"
                  required
                />
              </div>

              <div>
                <label className="block text-bone-300 text-sm mb-2">
                  Localizacao
                </label>
                <input
                  type="text"
                  value={newScene.location}
                  onChange={(e) => setNewScene({ ...newScene, location: e.target.value })}
                  className="input-gothic w-full"
                  placeholder="Ex: Centro da cidade"
                />
              </div>

              <div>
                <label className="block text-bone-300 text-sm mb-2">
                  Descricao
                </label>
                <textarea
                  value={newScene.description}
                  onChange={(e) => setNewScene({ ...newScene, description: e.target.value })}
                  className="input-gothic w-full h-24 resize-none"
                  placeholder="Descreva a cena..."
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowCreateScene(false)}
                  className="btn-midnight flex-1"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="btn-blood flex-1"
                  disabled={createSceneMutation.isPending}
                >
                  {createSceneMutation.isPending ? 'Criando...' : 'Criar Cena'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Chronicle Modal */}
      {showEditChronicle && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="card-gothic p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-6">
              <h2 className="font-gothic text-xl text-bone-100">Editar Cronica</h2>
              <button
                onClick={() => setShowEditChronicle(false)}
                className="text-midnight-400 hover:text-bone-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault()
                updateChronicleMutation.mutate(editData)
              }}
              className="space-y-4"
            >
              <div>
                <label className="block text-bone-300 text-sm mb-2">
                  Nome da Cronica
                </label>
                <input
                  type="text"
                  value={editData.name}
                  onChange={(e) => setEditData({ ...editData, name: e.target.value })}
                  className="input-gothic w-full"
                  required
                />
              </div>

              <div>
                <label className="block text-bone-300 text-sm mb-2">
                  Descricao
                </label>
                <textarea
                  value={editData.description}
                  onChange={(e) => setEditData({ ...editData, description: e.target.value })}
                  className="input-gothic w-full h-24 resize-none"
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowEditChronicle(false)}
                  className="btn-midnight flex-1"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="btn-blood flex-1"
                  disabled={updateChronicleMutation.isPending}
                >
                  {updateChronicleMutation.isPending ? 'Salvando...' : 'Salvar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Assign Character Modal - Step 1: Select character */}
      {showAssignCharacter && !showConfirmAssign && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="card-gothic p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-6">
              <h2 className="font-gothic text-xl text-bone-100">Escolher Personagem</h2>
              <button
                onClick={() => setShowAssignCharacter(false)}
                className="text-midnight-400 hover:text-bone-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-bone-400 text-sm mb-4">
              Selecione o personagem que deseja adicionar a esta cronica.
              O Narrador precisara aprovar antes de poder jogar.
            </p>

            {availableCharacters && availableCharacters.length > 0 ? (
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {availableCharacters
                  .filter((c: any) => c.game_version === chronicle.game_version)
                  .map((char: any) => (
                    <button
                      key={char.id}
                      onClick={() => {
                        setSelectedCharacterToAssign(char)
                        setShowConfirmAssign(true)
                      }}
                      className="w-full flex items-center gap-3 p-3 rounded hover:bg-midnight-800 transition-colors text-left border border-midnight-700 hover:border-blood-700"
                    >
                      <div className="w-10 h-10 bg-blood-700/30 rounded-full flex items-center justify-center">
                        <span className="text-blood-400">{char.name[0]}</span>
                      </div>
                      <div className="flex-1">
                        <p className="text-bone-100">{char.name}</p>
                        <p className="text-midnight-400 text-sm">
                          {char.clan || 'Sem cla'} - {char.game_version.toUpperCase()}
                        </p>
                      </div>
                      <span className="text-blood-400">→</span>
                    </button>
                  ))}
                {availableCharacters.filter((c: any) => c.game_version === chronicle.game_version).length === 0 && (
                  <p className="text-midnight-400 text-center py-4">
                    Nenhum personagem {chronicle.game_version.toUpperCase()} disponivel.
                    <br />
                    <Link to="/characters" className="text-blood-400 hover:underline">
                      Criar um personagem
                    </Link>
                  </p>
                )}
              </div>
            ) : (
              <div className="text-center py-6">
                <p className="text-midnight-400 mb-4">
                  Voce nao tem nenhum personagem disponivel.
                </p>
                <Link to="/characters" className="btn-blood inline-flex items-center gap-2">
                  <Plus className="w-4 h-4" />
                  Criar Personagem
                </Link>
              </div>
            )}

            <div className="flex gap-3 pt-4 mt-4 border-t border-midnight-700">
              <button
                onClick={() => setShowAssignCharacter(false)}
                className="btn-midnight flex-1"
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Assign Character Modal - Step 2: Confirmation */}
      {showConfirmAssign && selectedCharacterToAssign && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="card-gothic p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-6">
              <h2 className="font-gothic text-xl text-bone-100">Confirmar Submissao</h2>
              <button
                onClick={() => {
                  setShowConfirmAssign(false)
                  setSelectedCharacterToAssign(null)
                }}
                className="text-midnight-400 hover:text-bone-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="bg-midnight-800/50 rounded-lg p-4 mb-6">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 bg-blood-700/30 rounded-full flex items-center justify-center">
                  <span className="text-blood-400 text-xl">{selectedCharacterToAssign.name[0]}</span>
                </div>
                <div>
                  <p className="text-bone-100 text-lg font-gothic">{selectedCharacterToAssign.name}</p>
                  <p className="text-midnight-400">
                    {selectedCharacterToAssign.clan || 'Sem cla'} - {selectedCharacterToAssign.game_version.toUpperCase()}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-yellow-900/20 border border-yellow-800/30 rounded-lg p-4 mb-6">
              <p className="text-yellow-200 text-sm">
                <strong>Atencao:</strong> Ao submeter este personagem, ele ficara aguardando a aprovacao do Narrador.
                Voce so podera usa-lo nas sessoes apos a aprovacao.
              </p>
            </div>

            <p className="text-bone-400 text-center mb-6">
              Deseja submeter <strong className="text-bone-100">{selectedCharacterToAssign.name}</strong> para a cronica <strong className="text-bone-100">{chronicle.name}</strong>?
            </p>

            <div className="flex gap-3">
              <button
                onClick={() => {
                  setShowConfirmAssign(false)
                  setSelectedCharacterToAssign(null)
                }}
                className="btn-midnight flex-1"
              >
                Voltar
              </button>
              <button
                onClick={() => assignCharacterMutation.mutate(selectedCharacterToAssign.id)}
                disabled={assignCharacterMutation.isPending}
                className="btn-blood flex-1"
              >
                {assignCharacterMutation.isPending ? 'Enviando...' : 'Submeter Personagem'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
