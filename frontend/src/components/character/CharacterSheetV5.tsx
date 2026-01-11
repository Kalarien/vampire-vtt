import { cn } from '@/lib/utils'
import { useQuery } from '@tanstack/react-query'
import { gameDataApi } from '@/lib/api'
import { useState, useEffect } from 'react'
import { Info, ChevronDown, ChevronUp, BookOpen } from 'lucide-react'

interface CharacterSheetV5Props {
  sheet: any
  onChange: (sheet: any) => void
  characterClan?: string
  isOwner?: boolean
}

const ATRIBUTOS = {
  fisicos: [
    { key: 'forca', label: 'Forca' },
    { key: 'destreza', label: 'Destreza' },
    { key: 'vigor', label: 'Vigor' },
  ],
  sociais: [
    { key: 'carisma', label: 'Carisma' },
    { key: 'manipulacao', label: 'Manipulacao' },
    { key: 'autocontrole', label: 'Autocontrole' },
  ],
  mentais: [
    { key: 'inteligencia', label: 'Inteligencia' },
    { key: 'raciocinio', label: 'Raciocinio' },
    { key: 'determinacao', label: 'Determinacao' },
  ],
}

const HABILIDADES = {
  fisicas: [
    { key: 'armasBrancas', label: 'Armas Brancas' },
    { key: 'armasDeFogo', label: 'Armas de Fogo' },
    { key: 'atletismo', label: 'Atletismo' },
    { key: 'briga', label: 'Briga' },
    { key: 'conducao', label: 'Conducao' },
    { key: 'furtividade', label: 'Furtividade' },
    { key: 'ladroagem', label: 'Ladroagem' },
    { key: 'oficios', label: 'Oficios' },
    { key: 'sobrevivencia', label: 'Sobrevivencia' },
  ],
  sociais: [
    { key: 'empatiaComAnimais', label: 'Empatia c/ Animais' },
    { key: 'etiqueta', label: 'Etiqueta' },
    { key: 'intimidacao', label: 'Intimidacao' },
    { key: 'lideranca', label: 'Lideranca' },
    { key: 'manha', label: 'Manha' },
    { key: 'performance', label: 'Performance' },
    { key: 'persuasao', label: 'Persuasao' },
    { key: 'sagacidade', label: 'Sagacidade' },
    { key: 'labia', label: 'Labia' },
  ],
  mentais: [
    { key: 'ciencia', label: 'Ciencia' },
    { key: 'erudicao', label: 'Erudicao' },
    { key: 'financas', label: 'Financas' },
    { key: 'investigacao', label: 'Investigacao' },
    { key: 'medicina', label: 'Medicina' },
    { key: 'ocultismo', label: 'Ocultismo' },
    { key: 'percepcao', label: 'Percepcao' },
    { key: 'politica', label: 'Politica' },
    { key: 'tecnologia', label: 'Tecnologia' },
  ],
}

// Custos de XP V5
const XP_COSTS = {
  atributo: (nivel: number) => nivel * 5,
  habilidade: (nivel: number) => nivel === 0 ? 3 : nivel * 3,
  disciplinaClã: (nivel: number) => nivel * 5,
  disciplinaFora: (nivel: number) => nivel * 7,
  potenciaDeSangue: (nivel: number) => nivel * 10,
}

export default function CharacterSheetV5({ sheet, onChange, characterClan, isOwner = true }: CharacterSheetV5Props) {
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    info: true,
    atributos: true,
    habilidades: true,
    disciplinas: true,
    lore: false,
  })
  const [showClanInfo, setShowClanInfo] = useState(false)
  const [showPredatorInfo, setShowPredatorInfo] = useState(false)

  // Fetch game data
  const { data: clans } = useQuery({
    queryKey: ['clans-v5'],
    queryFn: async () => (await gameDataApi.getClansV5()).data,
  })

  const { data: predatorTypes } = useQuery({
    queryKey: ['predator-types-v5'],
    queryFn: async () => (await gameDataApi.getPredatorTypesV5()).data,
  })

  const { data: disciplines } = useQuery({
    queryKey: ['disciplines-v5'],
    queryFn: async () => (await gameDataApi.getDisciplinesV5()).data,
  })

  // Calculos automaticos
  useEffect(() => {
    const vigor = getField('atributos.fisicos.vigor', 1)
    const autocontrole = getField('atributos.sociais.autocontrole', 1)
    const determinacao = getField('atributos.mentais.determinacao', 1)

    const novaVitalidade = vigor + 3
    const novaFdV = autocontrole + determinacao

    if (getField('vitalidade.max', 0) !== novaVitalidade) {
      updateField('vitalidade.max', novaVitalidade)
    }
    if (getField('forcaDeVontade.max', 0) !== novaFdV) {
      updateField('forcaDeVontade.max', novaFdV)
    }
  }, [
    sheet?.atributos?.fisicos?.vigor,
    sheet?.atributos?.sociais?.autocontrole,
    sheet?.atributos?.mentais?.determinacao,
  ])

  const updateField = (path: string, value: any) => {
    const keys = path.split('.')
    const newSheet = JSON.parse(JSON.stringify(sheet))
    let current: any = newSheet

    for (let i = 0; i < keys.length - 1; i++) {
      if (!current[keys[i]]) current[keys[i]] = {}
      current = current[keys[i]]
    }

    current[keys[keys.length - 1]] = value
    onChange(newSheet)
  }

  const getField = (path: string, defaultValue: any = '') => {
    const keys = path.split('.')
    let current = sheet

    for (const key of keys) {
      if (current === undefined || current === null) return defaultValue
      current = current[key]
    }

    return current ?? defaultValue
  }

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }))
  }

  const selectedClan = (clans && characterClan
    ? Object.values(clans).find((c: any) => c.name === characterClan)
    : null) as { name: string; description: string; disciplines: string[]; bane: string; compulsion: string } | null

  const selectedPredator = (predatorTypes && getField('tipoDePredador')
    ? Object.values(predatorTypes).find((p: any) => p.name === getField('tipoDePredador'))
    : null) as { name: string; description: string; discipline_options: string[]; specialty: string } | null

  const DotRating = ({
    value,
    max = 5,
    onChange: onDotChange,
    showXP = false,
    xpCost = 0,
  }: {
    value: number
    max?: number
    onChange: (v: number) => void
    showXP?: boolean
    xpCost?: number
  }) => (
    <div className="flex items-center gap-2">
      <div className="flex gap-1">
        {Array.from({ length: max }, (_, i) => (
          <button
            key={i}
            type="button"
            onClick={() => onDotChange(i + 1 === value ? i : i + 1)}
            className={cn(
              'w-4 h-4 rounded-full border-2 transition-colors',
              i < value
                ? 'bg-blood-600 border-blood-500'
                : 'bg-midnight-800 border-midnight-600 hover:border-midnight-500'
            )}
          />
        ))}
      </div>
      {showXP && xpCost > 0 && (
        <span className="text-xs text-midnight-500">({xpCost} XP)</span>
      )}
    </div>
  )

  // Componente especial para disciplinas com tooltip de poderes
  const [hoveredPower, setHoveredPower] = useState<{ level: number; powers: any[]; position: { x: number; y: number } } | null>(null)

  const DisciplineDotRating = ({
    value,
    max = 5,
    onChange: onDotChange,
    showXP = false,
    xpCost = 0,
    disciplinePowers = [],
  }: {
    value: number
    max?: number
    onChange: (v: number) => void
    showXP?: boolean
    xpCost?: number
    disciplinePowers?: any[]
  }) => {
    const getPowersForLevel = (level: number) => {
      return disciplinePowers.filter((p: any) => p.level === level)
    }

    return (
      <div className="flex items-center gap-2">
        <div className="flex gap-1">
          {Array.from({ length: max }, (_, i) => {
            const level = i + 1
            const powersAtLevel = getPowersForLevel(level)

            return (
              <button
                key={i}
                type="button"
                onMouseDown={(e) => {
                  e.preventDefault()
                  onDotChange(level === value ? i : level)
                }}
                onMouseEnter={(e) => {
                  if (powersAtLevel.length > 0) {
                    const rect = e.currentTarget.getBoundingClientRect()
                    setHoveredPower({
                      level,
                      powers: powersAtLevel,
                      position: { x: rect.left, y: rect.bottom + 5 }
                    })
                  }
                }}
                onMouseLeave={() => setHoveredPower(null)}
                className={cn(
                  'w-6 h-6 rounded-full border-2 transition-colors cursor-pointer select-none',
                  i < value
                    ? 'bg-blood-600 border-blood-500'
                    : 'bg-midnight-800 border-midnight-600 hover:border-blood-400'
                )}
                title={powersAtLevel.length > 0 ? `Nivel ${level}: ${powersAtLevel.map((p: any) => p.name).join(', ')}` : `Nivel ${level}`}
              />
            )
          })}
        </div>
        {showXP && xpCost > 0 && (
          <span className="text-xs text-midnight-500">({xpCost} XP)</span>
        )}
      </div>
    )
  }

  const TrackerBox = ({ value, onChange: onBoxChange }: { value: number; onChange: (v: number) => void }) => (
    <button
      type="button"
      onClick={() => onBoxChange((value + 1) % 3)}
      className={cn(
        'w-6 h-6 border-2 transition-colors',
        value === 0 && 'bg-midnight-800 border-midnight-600',
        value === 1 && 'bg-midnight-600 border-bone-400',
        value === 2 && 'bg-blood-700 border-blood-500'
      )}
    />
  )

  const SectionHeader = ({ title, section }: { title: string; section: string }) => (
    <button
      type="button"
      onClick={() => toggleSection(section)}
      className="w-full flex items-center justify-between font-gothic text-lg text-bone-100 mb-4 hover:text-blood-400 transition-colors"
    >
      <span>{title}</span>
      {expandedSections[section] ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
    </button>
  )

  // Calcula pontos gastos em atributos
  const calcPontosAtributos = (categoria: string) => {
    const attrs = ATRIBUTOS[categoria as keyof typeof ATRIBUTOS]
    return attrs.reduce((sum, attr) => sum + (getField(`atributos.${categoria}.${attr.key}`, 1) - 1), 0)
  }

  // Calcula pontos gastos em habilidades
  const calcPontosHabilidades = (categoria: string) => {
    const habs = HABILIDADES[categoria as keyof typeof HABILIDADES]
    return habs.reduce((sum, hab) => sum + getField(`habilidades.${hab.key}`, 0), 0)
  }

  return (
    <div className="space-y-6">
      {/* Tooltip flutuante para poderes de disciplina */}
      {hoveredPower && (
        <div
          className="fixed z-50 bg-midnight-900 border border-blood-700 rounded-lg shadow-xl p-4 max-w-sm"
          style={{
            left: Math.min(hoveredPower.position.x, window.innerWidth - 350),
            top: hoveredPower.position.y,
          }}
        >
          <h4 className="text-blood-400 font-gothic text-sm mb-2">
            Nivel {hoveredPower.level}
          </h4>
          {hoveredPower.powers.map((power: any, idx: number) => (
            <div key={idx} className={idx > 0 ? 'mt-3 pt-3 border-t border-midnight-700' : ''}>
              <p className="text-bone-100 font-semibold text-sm">{power.name}</p>
              {power.amalgam && (
                <p className="text-purple-400 text-xs">Amalgama: {power.amalgam}</p>
              )}
              <p className="text-midnight-300 text-xs mt-1">{power.description}</p>
              <div className="flex gap-3 mt-2 text-xs">
                <span className="text-blood-400">Custo: {power.cost}</span>
                {power.dice_pool && <span className="text-bone-400">Parada: {power.dice_pool}</span>}
              </div>
              {power.duration && (
                <p className="text-midnight-400 text-xs mt-1">Duracao: {power.duration}</p>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Informacoes Basicas */}
      <div className="card-gothic p-6">
        <SectionHeader title="Informacoes Basicas" section="info" />
        {expandedSections.info && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-bone-400 text-sm mb-1">Conceito</label>
              <input
                type="text"
                value={getField('conceito', '')}
                onChange={(e) => updateField('conceito', e.target.value)}
                className="input-gothic w-full"
                placeholder="Ex: Detetive Cansado"
              />
            </div>

            <div>
              <label className="block text-bone-400 text-sm mb-1 flex items-center gap-1">
                Cla
                {selectedClan && (
                  <button
                    type="button"
                    onClick={() => setShowClanInfo(!showClanInfo)}
                    className="text-blood-400 hover:text-blood-300"
                  >
                    <Info className="w-4 h-4" />
                  </button>
                )}
              </label>
              <select
                value={characterClan || ''}
                disabled
                className="input-gothic w-full opacity-70"
              >
                <option value="">{characterClan || 'Definido na criacao'}</option>
              </select>
              {showClanInfo && selectedClan && (
                <div className="mt-2 p-3 bg-midnight-800 rounded border border-midnight-600 text-sm">
                  <p className="text-bone-300 mb-2">{selectedClan.description}</p>
                  <p className="text-blood-400"><strong>Disciplinas:</strong> {selectedClan.disciplines?.join(', ')}</p>
                  <p className="text-bone-400 mt-1"><strong>Bane:</strong> {selectedClan.bane}</p>
                  <p className="text-midnight-300 mt-1"><strong>Compulsao:</strong> {selectedClan.compulsion}</p>
                </div>
              )}
            </div>

            <div>
              <label className="block text-bone-400 text-sm mb-1">Sire</label>
              <input
                type="text"
                value={getField('sire', '')}
                onChange={(e) => updateField('sire', e.target.value)}
                className="input-gothic w-full"
                placeholder="Nome do Sire"
              />
            </div>

            <div>
              <label className="block text-bone-400 text-sm mb-1">Geracao</label>
              <select
                value={getField('geracao', 13)}
                onChange={(e) => updateField('geracao', parseInt(e.target.value))}
                className="input-gothic w-full"
              >
                {[16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4].map(g => (
                  <option key={g} value={g}>{g}a Geracao</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-bone-400 text-sm mb-1 flex items-center gap-1">
                Tipo de Predador
                {selectedPredator && (
                  <button
                    type="button"
                    onClick={() => setShowPredatorInfo(!showPredatorInfo)}
                    className="text-blood-400 hover:text-blood-300"
                  >
                    <Info className="w-4 h-4" />
                  </button>
                )}
              </label>
              <select
                value={getField('tipoDePredador', '')}
                onChange={(e) => updateField('tipoDePredador', e.target.value)}
                className="input-gothic w-full"
              >
                <option value="">Selecione...</option>
                {predatorTypes && Object.values(predatorTypes).map((pt: any) => (
                  <option key={pt.name} value={pt.name}>{pt.name}</option>
                ))}
              </select>
              {showPredatorInfo && selectedPredator && (
                <div className="mt-2 p-3 bg-midnight-800 rounded border border-midnight-600 text-sm">
                  <p className="text-bone-300 mb-2">{selectedPredator.description}</p>
                  <p className="text-blood-400"><strong>Disciplina:</strong> {selectedPredator.discipline_options?.join(' ou ')}</p>
                  <p className="text-bone-400 mt-1"><strong>Especialidade:</strong> {selectedPredator.specialty}</p>
                </div>
              )}
            </div>

            <div>
              <label className="block text-bone-400 text-sm mb-1">Ambicao</label>
              <input
                type="text"
                value={getField('ambicao', '')}
                onChange={(e) => updateField('ambicao', e.target.value)}
                className="input-gothic w-full"
                placeholder="Sua ambicao de longo prazo"
              />
            </div>

            <div>
              <label className="block text-bone-400 text-sm mb-1">Desejo</label>
              <input
                type="text"
                value={getField('desejo', '')}
                onChange={(e) => updateField('desejo', e.target.value)}
                className="input-gothic w-full"
                placeholder="Seu desejo imediato"
              />
            </div>

            <div>
              <label className="block text-bone-400 text-sm mb-1">Ressonancia</label>
              <select
                value={getField('ressonancia', '')}
                onChange={(e) => updateField('ressonancia', e.target.value)}
                className="input-gothic w-full"
              >
                <option value="">Selecione...</option>
                <option value="Colerico">Colerico (Raiva)</option>
                <option value="Melancolico">Melancolico (Tristeza)</option>
                <option value="Fleumatico">Fleumatico (Calma)</option>
                <option value="Sanguineo">Sanguineo (Alegria)</option>
                <option value="Animal">Animal</option>
                <option value="Vazia">Vazia</option>
              </select>
            </div>
          </div>
        )}
      </div>

      {/* Atributos */}
      <div className="card-gothic p-6">
        <SectionHeader title="Atributos" section="atributos" />
        {expandedSections.atributos && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {Object.entries(ATRIBUTOS).map(([categoria, attrs]) => (
                <div key={categoria}>
                  <h4 className="text-blood-400 text-sm uppercase font-gothic mb-3 flex items-center justify-between">
                    <span>{categoria === 'fisicos' ? 'Fisicos' : categoria === 'sociais' ? 'Sociais' : 'Mentais'}</span>
                    <span className="text-midnight-400 text-xs normal-case">
                      ({calcPontosAtributos(categoria)} pts)
                    </span>
                  </h4>
                  <div className="space-y-2">
                    {attrs.map((attr) => {
                      const valor = getField(`atributos.${categoria}.${attr.key}`, 1)
                      return (
                        <div key={attr.key} className="flex items-center justify-between">
                          <span className="text-bone-300 text-sm">{attr.label}</span>
                          <DotRating
                            value={valor}
                            onChange={(v) => updateField(`atributos.${categoria}.${attr.key}`, v)}
                            showXP
                            xpCost={XP_COSTS.atributo(valor + 1)}
                          />
                        </div>
                      )
                    })}
                  </div>
                </div>
              ))}
            </div>
            <p className="text-midnight-500 text-xs mt-4">
              Criacao: Distribua 7/5/3 pontos (alem do 1 gratis em cada). XP para subir: Novo Nivel x 5
            </p>
          </>
        )}
      </div>

      {/* Habilidades */}
      <div className="card-gothic p-6">
        <SectionHeader title="Habilidades" section="habilidades" />
        {expandedSections.habilidades && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {Object.entries(HABILIDADES).map(([categoria, habs]) => (
                <div key={categoria}>
                  <h4 className="text-blood-400 text-sm uppercase font-gothic mb-3 flex items-center justify-between">
                    <span>{categoria === 'fisicas' ? 'Fisicas' : categoria === 'sociais' ? 'Sociais' : 'Mentais'}</span>
                    <span className="text-midnight-400 text-xs normal-case">
                      ({calcPontosHabilidades(categoria)} pts)
                    </span>
                  </h4>
                  <div className="space-y-2">
                    {habs.map((hab) => {
                      const valor = getField(`habilidades.${hab.key}`, 0)
                      const especializacao = getField(`especializacoes.${hab.key}`, '')
                      return (
                        <div key={hab.key} className="flex items-center gap-2">
                          <span className="text-bone-300 text-sm min-w-[100px]">{hab.label}</span>
                          <input
                            type="text"
                            value={especializacao}
                            onChange={(e) => updateField(`especializacoes.${hab.key}`, e.target.value)}
                            placeholder="Espec."
                            className="input-gothic text-xs px-1 py-0.5 w-20 flex-shrink-0"
                            title="Especializacao (ex: Contra Membros)"
                          />
                          <div className="flex-1" />
                          <DotRating
                            value={valor}
                            onChange={(v) => updateField(`habilidades.${hab.key}`, v)}
                            showXP
                            xpCost={XP_COSTS.habilidade(valor + 1)}
                          />
                        </div>
                      )
                    })}
                  </div>
                </div>
              ))}
            </div>
            <p className="text-midnight-500 text-xs mt-4">
              Criacao: Distribua 11/7/4 pontos. XP: Nova habilidade = 3, subir = Novo Nivel x 3.
              Especializacoes dao +1 dado em situacoes especificas.
            </p>
          </>
        )}
      </div>

      {/* Vitalidade & Forca de Vontade */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card-gothic p-6">
          <h3 className="font-gothic text-lg text-bone-100 mb-2">Vitalidade</h3>
          <p className="text-midnight-400 text-xs mb-3">
            Vigor ({getField('atributos.fisicos.vigor', 1)}) + 3 = {getField('vitalidade.max', 3)}
          </p>
          <div className="flex gap-1 flex-wrap">
            {Array.from({ length: getField('vitalidade.max', 3) }, (_, i) => (
              <TrackerBox
                key={i}
                value={getField(`vitalidade.dano.${i}`, 0)}
                onChange={(v) => updateField(`vitalidade.dano.${i}`, v)}
              />
            ))}
          </div>
          <p className="text-midnight-400 text-xs mt-2">
            Vazio → Superficial → Agravado
          </p>
        </div>

        <div className="card-gothic p-6">
          <h3 className="font-gothic text-lg text-bone-100 mb-2">Forca de Vontade</h3>
          <p className="text-midnight-400 text-xs mb-3">
            Autocontrole ({getField('atributos.sociais.autocontrole', 1)}) + Determinacao ({getField('atributos.mentais.determinacao', 1)}) = {getField('forcaDeVontade.max', 3)}
          </p>
          <div className="flex gap-1 flex-wrap">
            {Array.from({ length: getField('forcaDeVontade.max', 3) }, (_, i) => (
              <TrackerBox
                key={i}
                value={getField(`forcaDeVontade.dano.${i}`, 0)}
                onChange={(v) => updateField(`forcaDeVontade.dano.${i}`, v)}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Fome & Humanidade */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card-gothic p-6">
          <h3 className="font-gothic text-lg text-bone-100 mb-4">Fome</h3>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map((h) => (
              <button
                key={h}
                type="button"
                onClick={() => updateField('fome', h === getField('fome', 1) ? 0 : h)}
                className={cn(
                  'w-10 h-10 rounded-full border-2 transition-colors font-bold',
                  h <= getField('fome', 1)
                    ? 'bg-blood-600 border-blood-500 text-bone-100'
                    : 'bg-midnight-800 border-midnight-600 hover:border-blood-700 text-midnight-400'
                )}
              >
                {h}
              </button>
            ))}
          </div>
          <p className="text-midnight-400 text-xs mt-2">
            Fome 5 = Frenesi iminente
          </p>
        </div>

        <div className="card-gothic p-6">
          <h3 className="font-gothic text-lg text-bone-100 mb-4">Humanidade</h3>
          <div className="flex gap-1 flex-wrap">
            {[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0].map((h) => (
              <button
                key={h}
                type="button"
                onClick={() => updateField('humanidade', h)}
                className={cn(
                  'w-7 h-7 rounded border-2 text-xs transition-colors font-bold',
                  h <= getField('humanidade', 7)
                    ? 'bg-bone-300 border-bone-200 text-midnight-900'
                    : 'bg-midnight-800 border-midnight-600 text-midnight-400 hover:border-midnight-500'
                )}
              >
                {h}
              </button>
            ))}
          </div>
          <p className="text-midnight-400 text-xs mt-2">
            Humanidade {getField('humanidade', 7)} - {getField('humanidade', 7) >= 8 ? 'Quase humano' : getField('humanidade', 7) >= 6 ? 'Equilibrado' : getField('humanidade', 7) >= 4 ? 'Distante' : 'Monstruoso'}
          </p>
        </div>
      </div>

      {/* Potencia de Sangue */}
      <div className="card-gothic p-6">
        <h3 className="font-gothic text-lg text-bone-100 mb-4">Potencia de Sangue</h3>
        <DotRating
          value={getField('potenciaDeSangue', 1)}
          max={10}
          onChange={(v) => updateField('potenciaDeSangue', v)}
          showXP
          xpCost={XP_COSTS.potenciaDeSangue(getField('potenciaDeSangue', 1) + 1)}
        />
        <p className="text-midnight-500 text-xs mt-2">
          XP para subir: Novo Nivel x 10
        </p>
      </div>

      {/* Disciplinas */}
      <div className="card-gothic p-6">
        <SectionHeader title="Disciplinas" section="disciplinas" />
        {expandedSections.disciplinas && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[1, 2, 3, 4].map((index) => {
                const key = `disciplina${index}`
                const nome = getField(`disciplinas.${key}.nome`, '')
                const nivel = getField(`disciplinas.${key}.nivel`, 0)
                const poderes = getField(`disciplinas.${key}.poderes`, '')
                const isClã = selectedClan && selectedClan.disciplines?.includes(nome)
                const disciplinaData = disciplines && nome
                  ? Object.values(disciplines).find((d: any) => d.name === nome) as { name: string; description?: string; powers?: any[] } | undefined
                  : null

                return (
                  <div key={key} className="p-4 bg-midnight-800/50 rounded border border-midnight-700">
                    <div className="flex gap-2 mb-2">
                      <select
                        value={nome}
                        onChange={(e) => updateField(`disciplinas.${key}.nome`, e.target.value)}
                        className="input-gothic flex-1"
                      >
                        <option value="">Selecione disciplina...</option>
                        {disciplines && Object.values(disciplines).map((d: any) => (
                          <option key={d.name} value={d.name}>
                            {d.name} {selectedClan && selectedClan.disciplines?.includes(d.name) ? '(Cla)' : ''}
                          </option>
                        ))}
                      </select>
                      {disciplinaData && (
                        <button
                          type="button"
                          onClick={() => setExpandedSections(prev => ({
                            ...prev,
                            [`disciplinaInfo_${key}`]: !prev[`disciplinaInfo_${key}`]
                          }))}
                          className="text-blood-400 hover:text-blood-300 p-1"
                          title="Ver descricao da disciplina"
                        >
                          <Info className="w-5 h-5" />
                        </button>
                      )}
                    </div>

                    {/* Descricao da disciplina (tooltip expandido) */}
                    {expandedSections[`disciplinaInfo_${key}`] && disciplinaData && (
                      <div className="mb-3 p-3 bg-midnight-900 rounded border border-midnight-600 text-sm">
                        <p className="text-bone-300">{disciplinaData.description || 'Sem descricao disponivel.'}</p>
                        {disciplinaData.powers && disciplinaData.powers.length > 0 && (
                          <div className="mt-2 pt-2 border-t border-midnight-700">
                            <p className="text-blood-400 text-xs font-gothic mb-1">Poderes disponiveis:</p>
                            <ul className="text-midnight-300 text-xs space-y-0.5">
                              {disciplinaData.powers.slice(0, nivel || 5).map((p: any, i: number) => (
                                <li key={i}>• Nivel {p.level || i + 1}: {p.name}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    )}

                    <div className="flex items-center justify-between mb-2">
                      <span className="text-bone-400 text-sm">
                        Nivel {nivel}
                        {nome && (
                          <span className={cn('ml-2 text-xs', isClã ? 'text-blood-400' : 'text-midnight-400')}>
                            ({isClã ? 'Do Cla' : 'Fora do Cla'})
                          </span>
                        )}
                      </span>
                      <DisciplineDotRating
                        value={nivel}
                        onChange={(v) => updateField(`disciplinas.${key}.nivel`, v)}
                        showXP
                        xpCost={isClã ? XP_COSTS.disciplinaClã(nivel + 1) : XP_COSTS.disciplinaFora(nivel + 1)}
                        disciplinePowers={disciplinaData?.powers || []}
                      />
                    </div>

                    {/* Campo para poderes escolhidos */}
                    {nome && (
                      <textarea
                        value={poderes}
                        onChange={(e) => updateField(`disciplinas.${key}.poderes`, e.target.value)}
                        placeholder="Poderes escolhidos (um por linha)..."
                        className="input-gothic w-full h-16 text-xs resize-none mt-2"
                      />
                    )}
                  </div>
                )
              })}
            </div>
            <p className="text-midnight-500 text-xs mt-4">
              XP: Cla = Nivel x 5, Fora = Nivel x 7. Criacao: 2 pontos em disciplinas do cla.
              Passe o mouse sobre as bolinhas para ver os poderes de cada nivel.
            </p>
          </>
        )}
      </div>

      {/* Vantagens e Defeitos */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card-gothic p-6">
          <h3 className="font-gothic text-lg text-bone-100 mb-4">Vantagens</h3>
          <textarea
            value={Array.isArray(getField('vantagens', [])) ? getField('vantagens', []).join('\n') : getField('vantagens', '')}
            onChange={(e) => updateField('vantagens', e.target.value.split('\n').filter((v: string) => v.trim()))}
            className="input-gothic w-full h-24 resize-none"
            placeholder="Uma vantagem por linha (ex: Recursos 3)"
          />
        </div>
        <div className="card-gothic p-6">
          <h3 className="font-gothic text-lg text-bone-100 mb-4">Defeitos</h3>
          <textarea
            value={Array.isArray(getField('defeitos', [])) ? getField('defeitos', []).join('\n') : getField('defeitos', '')}
            onChange={(e) => updateField('defeitos', e.target.value.split('\n').filter((v: string) => v.trim()))}
            className="input-gothic w-full h-24 resize-none"
            placeholder="Um defeito por linha (ex: Inimigo 2)"
          />
        </div>
      </div>

      {/* Conviccoes e Toques */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card-gothic p-6">
          <h3 className="font-gothic text-lg text-bone-100 mb-4">Conviccoes</h3>
          <textarea
            value={Array.isArray(getField('convicoes', [])) ? getField('convicoes', []).join('\n') : getField('convicoes', '')}
            onChange={(e) => updateField('convicoes', e.target.value.split('\n').filter((v: string) => v.trim()))}
            className="input-gothic w-full h-24 resize-none"
            placeholder="Uma conviccao por linha"
          />
          <p className="text-midnight-500 text-xs mt-2">Ancoram sua Humanidade</p>
        </div>
        <div className="card-gothic p-6">
          <h3 className="font-gothic text-lg text-bone-100 mb-4">Toques (Touchstones)</h3>
          <textarea
            value={Array.isArray(getField('toques', [])) ? getField('toques', []).join('\n') : getField('toques', '')}
            onChange={(e) => updateField('toques', e.target.value.split('\n').filter((v: string) => v.trim()))}
            className="input-gothic w-full h-24 resize-none"
            placeholder="Pessoas que representam suas conviccoes"
          />
        </div>
      </div>

      {/* Experiencia */}
      <div className="card-gothic p-6">
        <h3 className="font-gothic text-lg text-bone-100 mb-4">Experiencia</h3>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-bone-400 text-sm mb-1">Total</label>
            <input
              type="number"
              value={getField('experiencia.total', 0)}
              onChange={(e) => updateField('experiencia.total', parseInt(e.target.value) || 0)}
              className="input-gothic w-full"
              min={0}
            />
          </div>
          <div>
            <label className="block text-bone-400 text-sm mb-1">Gasta</label>
            <input
              type="number"
              value={getField('experiencia.gasta', 0)}
              onChange={(e) => updateField('experiencia.gasta', parseInt(e.target.value) || 0)}
              className="input-gothic w-full"
              min={0}
            />
          </div>
          <div>
            <label className="block text-bone-400 text-sm mb-1">Disponivel</label>
            <div className="input-gothic w-full bg-midnight-700 flex items-center justify-center font-bold text-blood-400">
              {getField('experiencia.total', 0) - getField('experiencia.gasta', 0)} XP
            </div>
          </div>
        </div>
      </div>

      {/* Notas */}
      <div className="card-gothic p-6">
        <h3 className="font-gothic text-lg text-bone-100 mb-4">Notas</h3>
        <textarea
          value={getField('notas', '')}
          onChange={(e) => updateField('notas', e.target.value)}
          className="input-gothic w-full h-32 resize-none"
          placeholder="Anotacoes, historia do personagem, etc..."
        />
      </div>

      {/* Lore - Historia do Personagem */}
      <div className="card-gothic p-6">
        <button
          type="button"
          onClick={() => toggleSection('lore')}
          className="w-full flex items-center justify-between font-gothic text-lg text-bone-100 hover:text-blood-400 transition-colors"
        >
          <span className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-blood-400" />
            Lore - Historia do Personagem
          </span>
          {expandedSections.lore ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>

        {expandedSections.lore && (
          <div className="mt-4">
            {isOwner ? (
              <>
                <textarea
                  value={getField('lore', '')}
                  onChange={(e) => updateField('lore', e.target.value)}
                  className="input-gothic w-full min-h-[500px] resize-y"
                  placeholder="Escreva aqui a historia completa do seu personagem...

Origem, vida antes do Abraco, como foi Abracado, seus primeiros anos como vampiro, eventos marcantes, relacoes importantes, segredos, objetivos...

Sinta-se livre para escrever o quanto quiser. Esta secao e apenas sua."
                />
                <p className="text-midnight-500 text-xs mt-2">
                  Apenas voce (dono da ficha) pode editar esta secao.
                </p>
              </>
            ) : (
              <div className="bg-midnight-800/50 rounded border border-midnight-700 p-4 min-h-[200px]">
                {getField('lore', '') ? (
                  <div className="text-bone-300 whitespace-pre-wrap">
                    {getField('lore', '')}
                  </div>
                ) : (
                  <p className="text-midnight-500 italic">
                    O jogador ainda nao escreveu a lore deste personagem.
                  </p>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
