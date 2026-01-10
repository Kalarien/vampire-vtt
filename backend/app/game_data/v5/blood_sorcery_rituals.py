from typing import List, Optional
from pydantic import BaseModel


class Ritual(BaseModel):
    name: str
    level: int
    ingredients: List[str]
    process: str
    system: str
    duration: str
    description: str
    source_book: str = "core"


BLOOD_SORCERY_RITUALS_V5: dict[str, Ritual] = {
    # === LEVEL 1 ===
    "blood_walk": Ritual(
        name="Blood Walk",
        level=1,
        ingredients=["Sangue do alvo (1 ponto)", "Vela negra", "Pires de prata"],
        process="Queime o sangue na chama da vela enquanto medita por 10 minutos.",
        system="Intelligence + Blood Sorcery, dificuldade 2. Sucesso revela: sire do alvo, geração aproximada, potência de sangue, se cometeu diablerie.",
        duration="Instantâneo (informação permanente)",
        description="Analisa o sangue de um Kindred, revelando sua linhagem e segredos de vitae."
    ),

    "clinging_of_the_insect": Ritual(
        name="Clinging of the Insect",
        level=1,
        ingredients=["Aranha viva", "Próprio sangue (1 Rouse Check)"],
        process="Esmague a aranha na palma da mão enquanto canta o encantamento.",
        system="O vampiro pode andar em paredes e tetos por uma cena.",
        duration="Uma cena",
        description="Permite escalar superfícies verticais e andar de cabeça para baixo."
    ),

    "craft_bloodstone": Ritual(
        name="Craft Bloodstone",
        level=1,
        ingredients=["Pedra pequena", "Próprio sangue (1 Rouse Check)", "Hora de meditação"],
        process="Infunda a pedra com seu sangue durante meditação ritual.",
        system="A pedra armazena um ponto de vitae. Pode ser consumido depois quebrando a pedra.",
        duration="Até ser usada",
        description="Cria uma pedra que armazena sangue para emergências."
    ),

    "wake_with_evenings_freshness": Ritual(
        name="Wake With Evening's Freshness",
        level=1,
        ingredients=["Giz ritual", "Próprio sangue"],
        process="Desenhe símbolos ao redor do local de descanso antes de dormir.",
        system="O vampiro acorda instantaneamente ao pôr do sol, sem penalidades diurnas por uma cena.",
        duration="Um dia",
        description="Permite acordar completamente alerta ao anoitecer."
    ),

    "illuminate_trail_of_prey": Ritual(
        name="Illuminate the Trail of Prey",
        level=1,
        ingredients=["Gota de sangue do alvo", "Lanterna"],
        process="Deixe o sangue cair na chama da lanterna.",
        system="Pegadas do alvo brilham visivelmente por uma noite.",
        duration="Uma noite",
        description="Rastreia um alvo por suas pegadas luminosas.",
        source_book="camarilla"
    ),

    # === LEVEL 2 ===
    "communicate_with_sire": Ritual(
        name="Communicate with Kindred Sire",
        level=2,
        ingredients=["Item do sire ou sangue", "Círculo de sal", "Velas vermelhas"],
        process="Medite no círculo por 30 minutos focando em seu sire.",
        system="Intelligence + Blood Sorcery, dificuldade 3. Sucesso permite comunicação telepática por uma cena.",
        duration="Uma cena",
        description="Estabelece comunicação mental com seu sire, independente da distância."
    ),

    "eyes_of_babel": Ritual(
        name="Eyes of Babel",
        level=2,
        ingredients=["Tinta feita com próprio sangue", "Pergaminho"],
        process="Escreva o idioma desejado no pergaminho com a tinta de sangue.",
        system="O vampiro pode ler qualquer idioma escrito por uma noite.",
        duration="Uma noite",
        description="Permite ler qualquer idioma escrito."
    ),

    "ward_against_ghouls": Ritual(
        name="Ward Against Ghouls",
        level=2,
        ingredients=["Giz misturado com sangue", "Superfície para desenhar"],
        process="Desenhe o glifo ward em uma superfície (porta, janela, objeto).",
        system="Carniçais que tocam o ward sofrem 2 níveis de dano Agravado e são repelidos.",
        duration="Permanente até quebrado",
        description="Cria uma proteção que impede carniçais de passar."
    ),

    "binding_mark": Ritual(
        name="The Binding Mark",
        level=2,
        ingredients=["Tinta misturada com sangue", "Agulha de tatuagem"],
        process="Tatue o glifo na pele do alvo.",
        system="O ritualizador sempre sabe a direção e distância aproximada do alvo marcado.",
        duration="Permanente",
        description="Marca um alvo para rastreamento perpétuo.",
        source_book="camarilla"
    ),

    # === LEVEL 3 ===
    "dagons_call": Ritual(
        name="Dagon's Call",
        level=3,
        ingredients=["Sangue do alvo (pelo menos um gole)", "Bacia de água salgada"],
        process="Deixe o sangue cair na água enquanto canta. Concentre-se no alvo.",
        system="Intelligence + Blood Sorcery vs Stamina + Resolve. Sucesso faz o alvo sufocar, perdendo 1 Health por sucesso.",
        duration="Concentração (máximo uma cena)",
        description="Enche os pulmões do alvo com sangue, causando afogamento."
    ),

    "deflection_of_wooden_doom": Ritual(
        name="Deflection of Wooden Doom",
        level=3,
        ingredients=["Lasca de madeira", "Próprio sangue"],
        process="Engula a lasca de madeira embebida em seu sangue.",
        system="A primeira estaca que o atingiria durante a noite é automaticamente desviada.",
        duration="Uma noite ou até ativado",
        description="Proteção contra estacas - desvia o primeiro ataque."
    ),

    "essence_of_air": Ritual(
        name="Essence of Air",
        level=3,
        ingredients=["Pena de coruja", "Próprio sangue", "Vento"],
        process="Queime a pena ao vento enquanto canta.",
        system="O vampiro pode se tornar gasoso por uma cena, como o poder Protean 'Mist Form'.",
        duration="Uma cena",
        description="Transforma o corpo em névoa."
    ),

    "ward_against_kindred": Ritual(
        name="Ward Against Kindred",
        level=3,
        ingredients=["Cinzas de vampiro destruído", "Próprio sangue"],
        process="Misture as cinzas com sangue e desenhe o glifo.",
        system="Vampiros que tocam sofrem 3 Agravado e são repelidos. Não afeta o criador.",
        duration="Permanente até quebrado",
        description="Cria proteção que impede outros vampiros de passar."
    ),

    "truth_of_blood": Ritual(
        name="Truth of Blood",
        level=3,
        ingredients=["Sangue do alvo", "Cálice de prata", "Incenso"],
        process="Beba o sangue do cálice enquanto faz perguntas.",
        system="Detecta mentiras do alvo cujo sangue foi bebido por uma cena.",
        duration="Uma cena",
        description="Detector de mentiras através do sangue.",
        source_book="camarilla"
    ),

    # === LEVEL 4 ===
    "defense_of_sacred_haven": Ritual(
        name="Defense of the Sacred Haven",
        level=4,
        ingredients=["Próprio sangue (3 Rouse Checks)", "Giz ritual", "8 horas de trabalho"],
        process="Desenhe glifos complexos em todas as entradas e paredes do haven.",
        system="Durante o dia, o haven é impossível de entrar. Mesmo se destruído fisicamente, o interior permanece protegido.",
        duration="Permanente (requer manutenção mensal)",
        description="Torna um haven completamente seguro durante o dia."
    ),

    "eyes_of_the_nighthawk": Ritual(
        name="Eyes of the Nighthawk",
        level=4,
        ingredients=["Olho de falcão", "Próprio sangue", "Tigela de cobre"],
        process="Coloque o olho na tigela de cobre cheia de seu sangue. Medite.",
        system="Pode ver através dos olhos de qualquer pássaro em um raio de vários quilômetros.",
        duration="Uma noite",
        description="Veja através dos olhos de pássaros na área."
    ),

    "incorporeal_passage": Ritual(
        name="Incorporeal Passage",
        level=4,
        ingredients=["Espelho", "Próprio sangue"],
        process="Cubra o espelho com seu sangue e caminhe através dele.",
        system="Pode caminhar através de objetos sólidos por uma cena. Não pode parar dentro de objetos.",
        duration="Uma cena",
        description="Permite atravessar paredes e objetos sólidos."
    ),

    "shaft_of_belated_dissolution": Ritual(
        name="Shaft of Belated Dissolution",
        level=4,
        ingredients=["Estaca de carvalho", "Próprio sangue", "Noite de lua nova"],
        process="Enterre a estaca em seu sangue durante uma lua nova, cantando por toda a noite.",
        system="Se usada para estacar um vampiro, a estaca se dissolve uma hora depois, liberando a vítima.",
        duration="Permanente (até uso)",
        description="Cria uma estaca que se dissolve após estacar alguém."
    ),

    # === LEVEL 5 ===
    "blood_contract": Ritual(
        name="Blood Contract",
        level=5,
        ingredients=["Pergaminho virgem", "Sangue de todos os signatários", "Cera de vela negra"],
        process="Escreva o contrato com sangue, sele com cera. Todos signam com sangue.",
        system="Qualquer um que quebrar o contrato sofre efeito definido na criação (até Morte Final). Detectar automaticamente se o contrato foi quebrado.",
        duration="Até cumprido ou quebrado",
        description="Cria um contrato magicamente vinculante impossível de quebrar sem consequências."
    ),

    "escape_to_true_sanctuary": Ritual(
        name="Escape to True Sanctuary",
        level=5,
        ingredients=["Círculo preparado no haven destino", "Próprio sangue"],
        process="Ao completar o ritual em perigo, é instantaneamente transportado ao círculo preparado.",
        system="Teletransporta instantaneamente para haven preparado, não importa a distância. Só funciona uma vez por círculo.",
        duration="Instantâneo",
        description="Fuga de emergência para um haven seguro."
    ),

    "heart_of_stone": Ritual(
        name="Heart of Stone",
        level=5,
        ingredients=["Coração de pedra esculpido", "Próprio sangue (5 Rouse Checks)"],
        process="Substitua metaforicamente seu coração pelo de pedra durante um ritual de 8 horas.",
        system="Imune a estacas e diablerie por uma semana. Também: -2 em todas pools Sociais, não pode gastar Willpower em emoções.",
        duration="Uma semana",
        description="Torna o coração imune a estacas, mas remove emoções."
    ),

    "shaft_of_belated_quiescence": Ritual(
        name="Shaft of Belated Quiescence",
        level=5,
        ingredients=["Estaca de madeira de árvore atingida por raio", "Sangue de 3 vampiros diferentes"],
        process="Banha a estaca nos três sangues durante três noites de lua cheia.",
        system="Quando usada, a vítima não entra em torpor imediatamente, mas exatamente 24 horas depois.",
        duration="Permanente (até uso)",
        description="Cria uma estaca com efeito retardado."
    ),
}


def get_ritual(ritual_id: str) -> Optional[Ritual]:
    """Get ritual by ID"""
    return BLOOD_SORCERY_RITUALS_V5.get(ritual_id.lower().replace(" ", "_").replace("'", ""))


def get_rituals_by_level(level: int) -> dict[str, Ritual]:
    """Get all rituals of a specific level"""
    return {k: v for k, v in BLOOD_SORCERY_RITUALS_V5.items() if v.level == level}


def get_rituals_by_source(source: str) -> dict[str, Ritual]:
    """Get all rituals from a specific source book"""
    return {k: v for k, v in BLOOD_SORCERY_RITUALS_V5.items() if v.source_book == source}
