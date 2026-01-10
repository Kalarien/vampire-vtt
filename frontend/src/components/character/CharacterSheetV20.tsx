import { cn } from '@/lib/utils'

interface CharacterSheetV20Props {
  sheet: any
  onChange: (sheet: any) => void
}

const ATTRIBUTES = {
  physical: [
    { key: 'strength', label: 'Forca' },
    { key: 'dexterity', label: 'Destreza' },
    { key: 'stamina', label: 'Vigor' },
  ],
  social: [
    { key: 'charisma', label: 'Carisma' },
    { key: 'manipulation', label: 'Manipulacao' },
    { key: 'appearance', label: 'Aparencia' },
  ],
  mental: [
    { key: 'perception', label: 'Percepcao' },
    { key: 'intelligence', label: 'Inteligencia' },
    { key: 'wits', label: 'Raciocinio' },
  ],
}

const ABILITIES = {
  talents: [
    { key: 'alertness', label: 'Prontidao' },
    { key: 'athletics', label: 'Atletismo' },
    { key: 'awareness', label: 'Consciencia' },
    { key: 'brawl', label: 'Briga' },
    { key: 'empathy', label: 'Empatia' },
    { key: 'expression', label: 'Expressao' },
    { key: 'intimidation', label: 'Intimidacao' },
    { key: 'leadership', label: 'Lideranca' },
    { key: 'streetwise', label: 'Manha' },
    { key: 'subterfuge', label: 'Labia' },
  ],
  skills: [
    { key: 'animal_ken', label: 'Empatia c/ Animais' },
    { key: 'crafts', label: 'Oficios' },
    { key: 'drive', label: 'Conducao' },
    { key: 'etiquette', label: 'Etiqueta' },
    { key: 'firearms', label: 'Armas de Fogo' },
    { key: 'larceny', label: 'Furto' },
    { key: 'melee', label: 'Armas Brancas' },
    { key: 'performance', label: 'Performance' },
    { key: 'stealth', label: 'Furtividade' },
    { key: 'survival', label: 'Sobrevivencia' },
  ],
  knowledges: [
    { key: 'academics', label: 'Academicos' },
    { key: 'computer', label: 'Computador' },
    { key: 'finance', label: 'Financas' },
    { key: 'investigation', label: 'Investigacao' },
    { key: 'law', label: 'Direito' },
    { key: 'medicine', label: 'Medicina' },
    { key: 'occult', label: 'Ocultismo' },
    { key: 'politics', label: 'Politica' },
    { key: 'science', label: 'Ciencia' },
    { key: 'technology', label: 'Tecnologia' },
  ],
}

const VIRTUES = [
  { key: 'conscience', label: 'Consciencia' },
  { key: 'self_control', label: 'Autocontrole' },
  { key: 'courage', label: 'Coragem' },
]

const HEALTH_LEVELS = [
  { key: 'bruised', label: 'Escoriado', penalty: 0 },
  { key: 'hurt', label: 'Machucado', penalty: -1 },
  { key: 'injured', label: 'Ferido', penalty: -1 },
  { key: 'wounded', label: 'Ferido Gravemente', penalty: -2 },
  { key: 'mauled', label: 'Espancado', penalty: -2 },
  { key: 'crippled', label: 'Aleijado', penalty: -5 },
  { key: 'incapacitated', label: 'Incapacitado', penalty: 0 },
]

export default function CharacterSheetV20({ sheet, onChange }: CharacterSheetV20Props) {
  const updateField = (path: string, value: any) => {
    const keys = path.split('.')
    const newSheet = { ...sheet }
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

  const DotRating = ({ value, max = 5, onChange: onDotChange }: { value: number; max?: number; onChange: (v: number) => void }) => (
    <div className="flex gap-1">
      {Array.from({ length: max }, (_, i) => (
        <button
          key={i}
          type="button"
          onClick={() => onDotChange(i + 1 === value ? 0 : i + 1)}
          className={cn(
            'w-4 h-4 rounded-full border-2 transition-colors',
            i < value
              ? 'bg-blood-600 border-blood-500'
              : 'bg-midnight-800 border-midnight-600 hover:border-midnight-500'
          )}
        />
      ))}
    </div>
  )

  const HealthBox = ({ value, onChange: onBoxChange }: { value: string; onChange: (v: string) => void }) => {
    const states = ['', '/', 'X']
    const currentIndex = states.indexOf(value) >= 0 ? states.indexOf(value) : 0
    return (
      <button
        type="button"
        onClick={() => onBoxChange(states[(currentIndex + 1) % states.length])}
        className={cn(
          'w-6 h-6 border-2 rounded flex items-center justify-center text-xs font-bold transition-colors',
          value === '' && 'bg-midnight-800 border-midnight-600',
          value === '/' && 'bg-midnight-600 border-midnight-500 text-bone-300',
          value === 'X' && 'bg-blood-700 border-blood-600 text-bone-100'
        )}
      >
        {value}
      </button>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header Info */}
      <div className="card-gothic p-6">
        <h3 className="font-gothic text-lg text-bone-100 mb-4">Informacoes Basicas</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-bone-400 text-sm mb-1">Conceito</label>
            <input
              type="text"
              value={getField('concept')}
              onChange={(e) => updateField('concept', e.target.value)}
              className="input-gothic w-full"
              placeholder="Ex: Antiquario Paranoico"
            />
          </div>
          <div>
            <label className="block text-bone-400 text-sm mb-1">Cla</label>
            <input
              type="text"
              value={getField('clan')}
              onChange={(e) => updateField('clan', e.target.value)}
              className="input-gothic w-full"
              placeholder="Ex: Tremere"
            />
          </div>
          <div>
            <label className="block text-bone-400 text-sm mb-1">Sire</label>
            <input
              type="text"
              value={getField('sire')}
              onChange={(e) => updateField('sire', e.target.value)}
              className="input-gothic w-full"
              placeholder="Nome do Sire"
            />
          </div>
          <div>
            <label className="block text-bone-400 text-sm mb-1">Natureza</label>
            <input
              type="text"
              value={getField('nature')}
              onChange={(e) => updateField('nature', e.target.value)}
              className="input-gothic w-full"
              placeholder="Arquetipo"
            />
          </div>
          <div>
            <label className="block text-bone-400 text-sm mb-1">Comportamento</label>
            <input
              type="text"
              value={getField('demeanor')}
              onChange={(e) => updateField('demeanor', e.target.value)}
              className="input-gothic w-full"
              placeholder="Arquetipo"
            />
          </div>
          <div>
            <label className="block text-bone-400 text-sm mb-1">Geracao</label>
            <input
              type="number"
              value={getField('generation', 13)}
              onChange={(e) => updateField('generation', parseInt(e.target.value))}
              className="input-gothic w-full"
              min={4}
              max={15}
            />
          </div>
        </div>
      </div>

      {/* Attributes */}
      <div className="card-gothic p-6">
        <h3 className="font-gothic text-lg text-bone-100 mb-4">Atributos</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {Object.entries(ATTRIBUTES).map(([category, attrs]) => (
            <div key={category}>
              <h4 className="text-blood-400 text-sm uppercase font-gothic mb-3">
                {category === 'physical' ? 'Fisicos' : category === 'social' ? 'Sociais' : 'Mentais'}
              </h4>
              <div className="space-y-2">
                {attrs.map((attr) => (
                  <div key={attr.key} className="flex items-center justify-between">
                    <span className="text-bone-300 text-sm">
                      {attr.label}
                    </span>
                    <DotRating
                      value={getField(`attributes.${attr.key}`, 1)}
                      onChange={(v) => updateField(`attributes.${attr.key}`, v)}
                    />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Abilities */}
      <div className="card-gothic p-6">
        <h3 className="font-gothic text-lg text-bone-100 mb-4">Habilidades</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {Object.entries(ABILITIES).map(([category, abilities]) => (
            <div key={category}>
              <h4 className="text-blood-400 text-sm uppercase font-gothic mb-3">
                {category === 'talents' ? 'Talentos' : category === 'skills' ? 'Pericias' : 'Conhecimentos'}
              </h4>
              <div className="space-y-2">
                {abilities.map((ability) => (
                  <div key={ability.key} className="flex items-center justify-between">
                    <span className="text-bone-300 text-sm">
                      {ability.label}
                    </span>
                    <DotRating
                      value={getField(`abilities.${ability.key}`, 0)}
                      onChange={(v) => updateField(`abilities.${ability.key}`, v)}
                    />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Disciplines */}
      <div className="card-gothic p-6">
        <h3 className="font-gothic text-lg text-bone-100 mb-4">Disciplinas</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {['discipline1', 'discipline2', 'discipline3'].map((key, index) => (
            <div key={key}>
              <input
                type="text"
                value={getField(`disciplines.${key}.name`, '')}
                onChange={(e) => updateField(`disciplines.${key}.name`, e.target.value)}
                className="input-gothic w-full mb-2"
                placeholder={`Disciplina ${index + 1}`}
              />
              <DotRating
                value={getField(`disciplines.${key}.level`, 0)}
                onChange={(v) => updateField(`disciplines.${key}.level`, v)}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Backgrounds */}
      <div className="card-gothic p-6">
        <h3 className="font-gothic text-lg text-bone-100 mb-4">Antecedentes</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {['background1', 'background2', 'background3'].map((key, index) => (
            <div key={key}>
              <input
                type="text"
                value={getField(`backgrounds.${key}.name`, '')}
                onChange={(e) => updateField(`backgrounds.${key}.name`, e.target.value)}
                className="input-gothic w-full mb-2"
                placeholder={`Antecedente ${index + 1}`}
              />
              <DotRating
                value={getField(`backgrounds.${key}.level`, 0)}
                onChange={(v) => updateField(`backgrounds.${key}.level`, v)}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Virtues */}
      <div className="card-gothic p-6">
        <h3 className="font-gothic text-lg text-bone-100 mb-4">Virtudes</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {VIRTUES.map((virtue) => (
            <div key={virtue.key}>
              <label className="block text-bone-300 text-sm mb-2">
                {virtue.label}
              </label>
              <DotRating
                value={getField(`virtues.${virtue.key}`, 1)}
                onChange={(v) => updateField(`virtues.${virtue.key}`, v)}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Health & Willpower */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card-gothic p-6">
          <h3 className="font-gothic text-lg text-bone-100 mb-4">Vitalidade</h3>
          <div className="space-y-2">
            {HEALTH_LEVELS.map((level) => (
              <div key={level.key} className="flex items-center gap-3">
                <span className="text-bone-400 text-sm w-32">{level.label}</span>
                <HealthBox
                  value={getField(`health.${level.key}`, '')}
                  onChange={(v) => updateField(`health.${level.key}`, v)}
                />
                {level.penalty !== 0 && (
                  <span className="text-midnight-500 text-xs">
                    {level.penalty} dados
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="card-gothic p-6">
          <h3 className="font-gothic text-lg text-bone-100 mb-4">Forca de Vontade</h3>
          <div className="mb-4">
            <label className="block text-bone-400 text-sm mb-2">Permanente</label>
            <DotRating
              value={getField('willpower.permanent', 3)}
              max={10}
              onChange={(v) => updateField('willpower.permanent', v)}
            />
          </div>
          <div>
            <label className="block text-bone-400 text-sm mb-2">Temporaria</label>
            <div className="flex gap-1 flex-wrap">
              {Array.from({ length: 10 }, (_, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => updateField('willpower.temporary', i + 1 === getField('willpower.temporary', 3) ? 0 : i + 1)}
                  className={cn(
                    'w-5 h-5 rounded border transition-colors',
                    i < getField('willpower.temporary', 3)
                      ? 'bg-midnight-500 border-midnight-400'
                      : 'bg-midnight-800 border-midnight-600'
                  )}
                />
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Blood Pool */}
      <div className="card-gothic p-6">
        <h3 className="font-gothic text-lg text-bone-100 mb-4">Pontos de Sangue</h3>
        <div className="flex gap-1 flex-wrap">
          {Array.from({ length: getField('blood_pool.max', 10) }, (_, i) => (
            <button
              key={i}
              type="button"
              onClick={() => updateField('blood_pool.current', i + 1 === getField('blood_pool.current', 10) ? 0 : i + 1)}
              className={cn(
                'blood-drop',
                i < getField('blood_pool.current', 10)
                  ? 'blood-drop-full'
                  : 'blood-drop-empty'
              )}
            />
          ))}
        </div>
        <p className="text-midnight-400 text-sm mt-2">
          {getField('blood_pool.current', 10)} / {getField('blood_pool.max', 10)} pontos de sangue
        </p>
      </div>

      {/* Humanity / Path */}
      <div className="card-gothic p-6">
        <h3 className="font-gothic text-lg text-bone-100 mb-4">Humanidade / Trilha</h3>
        <div className="flex gap-1">
          {Array.from({ length: 10 }, (_, i) => (
            <button
              key={i}
              type="button"
              onClick={() => updateField('humanity', i + 1)}
              className={cn(
                'w-6 h-6 rounded-full border-2 text-xs transition-colors',
                i < getField('humanity', 7)
                  ? 'bg-bone-300 border-bone-200 text-midnight-900'
                  : 'bg-midnight-800 border-midnight-600 text-midnight-400 hover:border-midnight-500'
              )}
            >
              {i + 1}
            </button>
          ))}
        </div>
        <p className="text-midnight-400 text-sm mt-2">
          Humanidade: {getField('humanity', 7)}
        </p>
      </div>

      {/* Experience */}
      <div className="card-gothic p-6">
        <h3 className="font-gothic text-lg text-bone-100 mb-4">Experiencia</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-bone-400 text-sm mb-1">Total</label>
            <input
              type="number"
              value={getField('experience.total', 0)}
              onChange={(e) => updateField('experience.total', parseInt(e.target.value))}
              className="input-gothic w-full"
              min={0}
            />
          </div>
          <div>
            <label className="block text-bone-400 text-sm mb-1">Disponivel</label>
            <input
              type="number"
              value={getField('experience.current', 0)}
              onChange={(e) => updateField('experience.current', parseInt(e.target.value))}
              className="input-gothic w-full"
              min={0}
            />
          </div>
        </div>
      </div>

      {/* Notes */}
      <div className="card-gothic p-6">
        <h3 className="font-gothic text-lg text-bone-100 mb-4">Notas</h3>
        <textarea
          value={getField('notes', '')}
          onChange={(e) => updateField('notes', e.target.value)}
          className="input-gothic w-full h-32 resize-none"
          placeholder="Anotacoes sobre o personagem..."
        />
      </div>
    </div>
  )
}
