import { cn } from '@/lib/utils'
import { useQuery } from '@tanstack/react-query'
import { gameDataApi } from '@/lib/api'
import { useState, useEffect } from 'react'
import { Info, ChevronDown, ChevronUp } from 'lucide-react'

interface CharacterSheetV5Props {
  sheet: any
  onChange: (sheet: any) => void
  characterClan?: string
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
    { key: 'compostura', label: 'Compostura' },
  ],
  mentais: [
    { key: 'inteligencia', label: 'Inteligencia' },
    { key: 'raciocinio', label: 'Raciocinio' },
    { key: 'determinacao', label: 'Determinacao' },
  ],
}

const HABILIDADES = {
  fisicas: [
    { key: 'atletismo', label: 'Atletismo' },
    { key: 'briga', label: 'Briga' },
    { key: 'conducao', label: 'Conducao' },
    { key: 'armasDeFogo', label: 'Armas de Fogo' },
    { key: 'armasBrancas', label: 'Armas Brancas' },
    { key: 'furtividade', label: 'Furtividade' },
    { key: 'furto', label: 'Furto' },
    { key: 'oficio', label: 'Oficio' },
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
    { key: 'perspicacia', label: 'Perspicacia' },
    { key: 'labia', label: 'Labia' },
  ],
  mentais: [
    { key: 'academicos', label: 'Academicos' },
    { key: 'ciencia', label: 'Ciencia' },
    { key: 'consciencia', label: 'Consciencia' },
    { key: 'financas', label: 'Financas' },
    { key: 'investigacao', label: 'Investigacao' },
    { key: 'medicina', label: 'Medicina' },
    { key: 'ocultismo', label: 'Ocultismo' },
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

export default function CharacterSheetV5({ sheet, onChange, characterClan }: CharacterSheetV5Props) {
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    info: true,
    atributos: true,
    habilidades: true,
    disciplinas: true,
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
    const compostura = getField('atributos.sociais.compostura', 1)
    const determinacao = getField('atributos.mentais.determinacao', 1)

    const novaVitalidade = vigor + 3
    const novaFdV = compostura + determinacao

    if (getField('vitalidade.max', 0) !== novaVitalidade) {
      updateField('vitalidade.max', novaVitalidade)
    }
    if (getField('forcaDeVontade.max', 0) !== novaFdV) {
      updateField('forcaDeVontade.max', novaFdV)
    }
  }, [
    sheet?.atributos?.fisicos?.vigor,
    sheet?.atributos?.sociais?.compostura,
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
                      return (
                        <div key={hab.key} className="flex items-center justify-between">
                          <span className="text-bone-300 text-sm">{hab.label}</span>
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
              Criacao: Distribua 11/7/4 pontos. XP: Nova habilidade = 3, subir = Novo Nivel x 3
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
            Compostura ({getField('atributos.sociais.compostura', 1)}) + Determinacao ({getField('atributos.mentais.determinacao', 1)}) = {getField('forcaDeVontade.max', 3)}
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
                const isClã = selectedClan && selectedClan.disciplines?.includes(nome)

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
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-bone-400 text-sm">
                        Nivel {nivel}
                        {nome && (
                          <span className={cn('ml-2 text-xs', isClã ? 'text-blood-400' : 'text-midnight-400')}>
                            ({isClã ? 'Do Cla' : 'Fora do Cla'})
                          </span>
                        )}
                      </span>
                      <DotRating
                        value={nivel}
                        onChange={(v) => updateField(`disciplinas.${key}.nivel`, v)}
                        showXP
                        xpCost={isClã ? XP_COSTS.disciplinaClã(nivel + 1) : XP_COSTS.disciplinaFora(nivel + 1)}
                      />
                    </div>
                  </div>
                )
              })}
            </div>
            <p className="text-midnight-500 text-xs mt-4">
              XP: Cla = Nivel x 5, Fora = Nivel x 7. Criacao: 2 pontos em disciplinas do cla.
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
    </div>
  )
}
