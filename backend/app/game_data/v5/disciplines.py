from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class DisciplineType(str, Enum):
    ANIMALISM = "Animalismo"
    AUSPEX = "Auspicios"
    BLOOD_SORCERY = "Feiticaria de Sangue"
    CELERITY = "Rapidez"
    DOMINATE = "Dominacao"
    FORTITUDE = "Fortitude"
    OBFUSCATE = "Ofuscacao"
    OBLIVION = "Oblivio"
    POTENCE = "Potencia"
    PRESENCE = "Presenca"
    PROTEAN = "Metamorfose"
    THIN_BLOOD_ALCHEMY = "Alquimia de Sangue Fraco"


class DisciplinePower(BaseModel):
    name: str
    level: int
    amalgam: Optional[str] = None
    prerequisite: Optional[str] = None
    cost: str
    dice_pool: Optional[str] = None
    vs_pool: Optional[str] = None
    description: str
    system: str
    duration: str
    source_book: str = "core"


class Discipline(BaseModel):
    name: DisciplineType
    description: str
    resonance: str
    characteristics: str
    powers: List[DisciplinePower]


# === ANIMALISM ===
ANIMALISM = Discipline(
    name=DisciplineType.ANIMALISM,
    description="A Disciplina Animalism traz o vampiro mais perto de sua natureza predatória. Permite comunicação e controle sobre animais, assim como influência sobre a Besta interior.",
    resonance="Sangue animal, especialmente predadores; humanos que são extremamente passivos ou ferozes",
    characteristics="Olhos podem brilhar como os de um animal; animais reagem fortemente à presença do vampiro",
    powers=[
        DisciplinePower(
            name="Bond Famulus",
            level=1,
            cost="One Rouse Check",
            description="O vampiro cria um laço permanente com um animal, tornando-o seu servo leal.",
            system="Gaste uma cena alimentando o animal com seu sangue por 3 noites consecutivas. O animal se torna um Famulus: obedece comandos mentais, o vampiro sente suas emoções e localização aproximada. Limite de 1 Famulus por ponto de Animalism.",
            duration="Permanente até quebrado"
        ),
        DisciplinePower(
            name="Sense the Beast",
            level=1,
            cost="Free",
            dice_pool="Resolve + Animalism",
            vs_pool="Composure + Subterfuge",
            description="O vampiro pode detectar a Besta em outros, sentindo vampiros, lobisomens e criaturas em frenesi.",
            system="Teste contestado. Sucesso revela: se o alvo é sobrenatural, seu nível aproximado de Fome/Fúria, se está em frenesi ou prestes a entrar.",
            duration="Passivo ou uma cena quando focado"
        ),
        DisciplinePower(
            name="Feral Whispers",
            level=2,
            cost="Free / One Rouse Check",
            dice_pool="Manipulation + Animalism",
            description="O vampiro pode se comunicar com animais e dar comandos simples.",
            system="Comunicação básica é gratuita. Comandos complexos ou que vão contra a natureza do animal exigem Rouse Check e teste.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Animal Succulence",
            level=3,
            cost="Free",
            description="O vampiro extrai mais sustento de sangue animal.",
            system="Ao se alimentar de animais, reduza Fome em 2 ao invés de 1 (mas ainda não pode reduzir abaixo de 1 com sangue animal).",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Quell the Beast",
            level=3,
            cost="One Rouse Check",
            dice_pool="Charisma + Animalism",
            vs_pool="Stamina + Resolve",
            description="Acalma a Besta em outro vampiro, encerrando frenesi, ou aterroriza um mortal até a submissão.",
            system="Contra vampiro em frenesi: sucesso encerra o frenesi imediatamente. O alvo fica letárgico por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Subsume the Spirit",
            level=4,
            cost="One Rouse Check",
            dice_pool="Manipulation + Animalism",
            description="O vampiro projeta sua consciência para dentro de um animal, controlando seu corpo.",
            system="O corpo do vampiro fica em torpor enquanto controla o animal. Pode usar Auspex e Animalism através do animal.",
            duration="Uma cena ou até encerrado"
        ),
        DisciplinePower(
            name="Animal Dominion",
            level=5,
            cost="Two Rouse Checks",
            dice_pool="Charisma + Animalism",
            description="O vampiro comanda todos os animais de um tipo específico em uma grande área.",
            system="Todos os animais do tipo escolhido em um raio de vários quarteirões atendem ao chamado.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Drawing Out the Beast",
            level=5,
            cost="One Rouse Check",
            dice_pool="Wits + Animalism",
            vs_pool="Composure + Resolve",
            description="O vampiro transfere sua Besta para outro, fazendo-o entrar em frenesi enquanto o usuário fica calmo.",
            system="Se bem-sucedido, o vampiro fica imune a frenesi enquanto a Besta está fora. O alvo entra em frenesi imediato.",
            duration="Até a Besta retornar"
        ),
    ]
)

# === AUSPEX ===
AUSPEX = Discipline(
    name=DisciplineType.AUSPEX,
    description="Auspex aguça os sentidos do vampiro além dos limites mortais, permitindo percepção sobrenatural, leitura de auras e até telepatia.",
    resonance="Artistas, visionários, investigadores, usuários de drogas psicodélicas",
    characteristics="Olhar penetrante, dificuldade em ignorar detalhes, hipersensibilidade",
    powers=[
        DisciplinePower(
            name="Heightened Senses",
            level=1,
            cost="Free",
            description="Todos os sentidos do vampiro se tornam sobrenaturalmente aguçados.",
            system="Adicione Auspex a testes de percepção. Pode ver no escuro, ouvir frequências inaudíveis, etc. Vulnerável a sobrecarga sensorial.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Sense the Unseen",
            level=1,
            cost="Free",
            dice_pool="Wits + Auspex",
            description="O vampiro pode sentir presenças sobrenaturais ocultas.",
            system="Detecta vampiros usando Obfuscate, fantasmas, magia ativa, e outras presenças sobrenaturais.",
            duration="Passivo ou focado por uma cena"
        ),
        DisciplinePower(
            name="Premonition",
            level=2,
            cost="Free / One Rouse Check",
            dice_pool="Resolve + Auspex",
            description="O vampiro recebe vislumbres do futuro ou insights sobre situações.",
            system="Pode receber avisos de perigo iminente (grátis) ou buscar ativamente visões (Rouse Check).",
            duration="Instantâneo"
        ),
        DisciplinePower(
            name="Scry the Soul",
            level=3,
            cost="One Rouse Check",
            dice_pool="Intelligence + Auspex",
            vs_pool="Composure + Subterfuge",
            description="O vampiro pode ver a aura de um alvo, revelando seu estado emocional e natureza.",
            system="Revela: estado emocional, se é sobrenatural, Ressonância do sangue, se está sob Dominate/Presence, diablerie.",
            duration="Concentração"
        ),
        DisciplinePower(
            name="Share the Senses",
            level=3,
            cost="One Rouse Check",
            dice_pool="Resolve + Auspex",
            description="O vampiro pode usar os sentidos de outro ser com quem tenha conexão.",
            system="Pode ver através dos olhos de alguém com quem tenha Laço de Sangue, Famulus, ou que tenha provado seu sangue.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Spirit's Touch",
            level=4,
            cost="One Rouse Check",
            dice_pool="Intelligence + Auspex",
            description="O vampiro pode ler a história psíquica de um objeto ao tocá-lo.",
            system="Revela visões do passado do objeto, especialmente eventos emocionalmente intensos.",
            duration="Instantâneo"
        ),
        DisciplinePower(
            name="Clairvoyance",
            level=5,
            cost="One Rouse Check",
            dice_pool="Intelligence + Auspex",
            description="O vampiro pode projetar seus sentidos para um local distante.",
            system="Pode perceber um local conhecido à distância. Quanto mais familiar, mais fácil.",
            duration="Concentração"
        ),
        DisciplinePower(
            name="Telepathy",
            level=5,
            cost="One Rouse Check",
            dice_pool="Resolve + Auspex",
            vs_pool="Wits + Subterfuge",
            description="O vampiro pode ler pensamentos e se comunicar mentalmente.",
            system="Pode ler pensamentos superficiais ou enviar mensagens mentais. Pensamentos profundos requerem contestação.",
            duration="Concentração"
        ),
    ]
)

# === CELERITY ===
CELERITY = Discipline(
    name=DisciplineType.CELERITY,
    description="Celerity concede velocidade e reflexos sobre-humanos, permitindo ao vampiro agir mais rápido que qualquer mortal.",
    resonance="Atletas, pessoas em perigo fugindo, usuários de estimulantes",
    characteristics="Movimentos fluidos, reflexos instantâneos, impaciência",
    powers=[
        DisciplinePower(
            name="Cat's Grace",
            level=1,
            cost="Free",
            description="O vampiro se move com graça sobrenatural.",
            system="Automaticamente bem-sucedido em testes de equilíbrio. Pode cair de qualquer altura sem dano.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Rapid Reflexes",
            level=1,
            cost="Free",
            description="O vampiro reage antes que outros possam agir.",
            system="Adicione Celerity à iniciativa. Pode usar uma ação de Defesa adicional por turno.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Fleetness",
            level=2,
            cost="One Rouse Check",
            description="O vampiro pode se mover em velocidade incrível.",
            system="Adicione Celerity a testes de Destreza não-combate. Velocidade de movimento dobrada.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Blink",
            level=3,
            cost="One Rouse Check",
            description="O vampiro pode atravessar curtas distâncias instantaneamente.",
            system="Mova-se até 50 metros instantaneamente. Não pode atacar no mesmo turno.",
            duration="Instantâneo"
        ),
        DisciplinePower(
            name="Traversal",
            level=3,
            cost="One Rouse Check",
            description="O vampiro pode correr sobre superfícies verticais ou líquidas.",
            system="Pode correr em paredes, tetos ou sobre água enquanto mantiver velocidade.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Draught of Elegance",
            level=4,
            cost="One Rouse Check",
            description="O vampiro pode conceder Celerity a outro através de seu sangue.",
            system="Alvo que beber seu sangue ganha 2 pontos de Celerity por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Unerring Aim",
            level=4,
            cost="One Rouse Check",
            description="O vampiro pode mirar com precisão perfeita.",
            system="Próximo ataque à distância ignora cobertura e adiciona Celerity ao dano.",
            duration="Um ataque"
        ),
        DisciplinePower(
            name="Lightning Strike",
            level=5,
            cost="One Rouse Check",
            description="O vampiro pode fazer múltiplos ataques em um único turno.",
            system="Faça um ataque adicional por turno, ou divida sua pool para atacar múltiplos alvos.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Split Second",
            level=5,
            cost="One Rouse Check",
            description="O vampiro pode agir em um instante congelado no tempo.",
            system="Ganhe uma ação adicional completa antes de qualquer um poder reagir.",
            duration="Um turno"
        ),
    ]
)

# === DOMINATE ===
DOMINATE = Discipline(
    name=DisciplineType.DOMINATE,
    description="Dominate permite ao vampiro controlar mentes, implantar comandos e apagar memórias através do contato visual.",
    resonance="Pessoas em posição de autoridade, manipuladores, controladores",
    characteristics="Olhar intenso e penetrante, dificuldade em aceitar ordens de outros",
    powers=[
        DisciplinePower(
            name="Cloud Memory",
            level=1,
            cost="Free",
            dice_pool="Charisma + Dominate",
            vs_pool="Wits + Resolve",
            description="O vampiro pode fazer o alvo esquecer os últimos minutos.",
            system="Apaga memórias dos últimos minutos. Alvo não se lembra do encontro com o vampiro.",
            duration="Permanente"
        ),
        DisciplinePower(
            name="Compel",
            level=1,
            cost="Free",
            dice_pool="Charisma + Dominate",
            vs_pool="Intelligence + Resolve",
            description="O vampiro dá um comando simples de uma palavra que deve ser obedecido.",
            system="Comando de uma palavra ('Fuja', 'Pare', 'Durma') que o alvo obedece imediatamente.",
            duration="Um turno"
        ),
        DisciplinePower(
            name="Mesmerize",
            level=2,
            cost="One Rouse Check",
            dice_pool="Manipulation + Dominate",
            vs_pool="Intelligence + Resolve",
            description="O vampiro pode implantar comandos mais complexos na mente do alvo.",
            system="Implante um comando que será executado imediatamente ou quando um gatilho for ativado.",
            duration="Até ser cumprido ou uma noite"
        ),
        DisciplinePower(
            name="Dementation",
            level=2,
            cost="One Rouse Check",
            dice_pool="Manipulation + Dominate",
            vs_pool="Composure + Intelligence",
            amalgam="Obfuscate 2",
            description="O vampiro pode causar distúrbios mentais temporários.",
            system="Cause medo, paranoia, alucinações ou outros efeitos mentais no alvo.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="The Forgetful Mind",
            level=3,
            cost="One Rouse Check",
            dice_pool="Manipulation + Dominate",
            vs_pool="Intelligence + Resolve",
            description="O vampiro pode reescrever memórias do alvo.",
            system="Apague, altere ou crie memórias falsas no alvo. Memórias complexas levam mais tempo.",
            duration="Permanente"
        ),
        DisciplinePower(
            name="Submerged Directive",
            level=3,
            cost="Free",
            description="Comandos podem ser implantados para execução futura.",
            system="Comandos de Mesmerize podem ser enterrados profundamente, ativando por gatilho específico.",
            duration="Até ser ativado"
        ),
        DisciplinePower(
            name="Rationalize",
            level=4,
            cost="Free",
            description="O alvo acredita que ações ordenadas foram sua própria ideia.",
            system="O alvo não percebe que foi controlado e racionaliza suas ações.",
            duration="Permanente"
        ),
        DisciplinePower(
            name="Mass Manipulation",
            level=5,
            cost="One Rouse Check",
            dice_pool="Manipulation + Dominate",
            description="O vampiro pode afetar múltiplos alvos simultaneamente.",
            system="Use qualquer poder de Dominate em múltiplos alvos que possam ver seus olhos.",
            duration="Varia"
        ),
        DisciplinePower(
            name="Terminal Decree",
            level=5,
            cost="Two Rouse Checks",
            dice_pool="Charisma + Dominate",
            vs_pool="Resolve + Intelligence",
            description="O vampiro pode ordenar que o alvo morra.",
            system="O alvo mortal morre de parada cardíaca. Vampiros entram em torpor.",
            duration="Permanente"
        ),
    ]
)

# === FORTITUDE ===
FORTITUDE = Discipline(
    name=DisciplineType.FORTITUDE,
    description="Fortitude concede resistência sobrenatural contra dano físico e mental.",
    resonance="Sobreviventes, pessoas que passaram por trauma, trabalhadores braçais",
    characteristics="Aparência inabalável, indiferença à dor, compostura sob pressão",
    powers=[
        DisciplinePower(
            name="Resilience",
            level=1,
            cost="Free",
            description="O vampiro pode ignorar fontes menores de dano.",
            system="Adicione Fortitude à saúde Superficial. Converta dano Superficial de fontes frias em nada.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Unswayed Mind",
            level=1,
            cost="Free",
            description="O vampiro resiste a manipulação mental e emocional.",
            system="Adicione Fortitude a testes de resistência contra Dominate, Presence e efeitos mentais.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Toughness",
            level=2,
            cost="One Rouse Check",
            description="O vampiro pode converter dano Agravado em Superficial.",
            system="Uma vez por cena, converta níveis de dano Agravado igual a Fortitude em Superficial.",
            duration="Instantâneo"
        ),
        DisciplinePower(
            name="Enduring Beasts",
            level=2,
            cost="One Rouse Check",
            description="O vampiro pode conceder resistência a animais e carniçais.",
            system="Famulus ou carniçais ganham Fortitude/2 (arredondado para cima) à resistência.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Defy Bane",
            level=3,
            cost="One Rouse Check",
            description="O vampiro pode resistir a fraquezas tradicionais.",
            system="Reduza dano de fogo e luz solar em Fortitude por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Fortify the Inner Facade",
            level=3,
            cost="Free",
            description="O vampiro pode resistir a Auspex e leitura de aura.",
            system="Contestações contra Auspex usam Fortitude + Composure.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Draught of Endurance",
            level=4,
            cost="One Rouse Check",
            description="O vampiro pode conceder Fortitude através de seu sangue.",
            system="Quem beber seu sangue ganha 2 pontos de Fortitude por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Flesh of Marble",
            level=5,
            cost="Two Rouse Checks",
            description="A pele do vampiro se torna dura como pedra.",
            system="Reduza todo dano recebido pela metade. Imune a estacas.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Prowess from Pain",
            level=5,
            cost="Free",
            description="O vampiro se torna mais poderoso quando ferido.",
            system="Adicione níveis de dano sofrido como bônus a ataques e resistência.",
            duration="Enquanto ferido"
        ),
    ]
)

# === OBFUSCATE ===
OBFUSCATE = Discipline(
    name=DisciplineType.OBFUSCATE,
    description="Obfuscate permite ao vampiro desaparecer, alterar sua aparência e apagar sua presença das mentes ao redor.",
    resonance="Pessoas ignoradas pela sociedade, introvertidos, espiões",
    characteristics="Facilmente esquecido, presença indistinta, habilidade de passar despercebido",
    powers=[
        DisciplinePower(
            name="Cloak of Shadows",
            level=1,
            cost="Free",
            description="O vampiro pode desaparecer enquanto estiver imóvel em sombras.",
            system="Torna-se invisível se imóvel e em área escura. Movimento quebra o efeito.",
            duration="Enquanto imóvel"
        ),
        DisciplinePower(
            name="Silence of Death",
            level=1,
            cost="Free",
            description="O vampiro pode silenciar completamente seus sons.",
            system="Não produz som algum. Pode silenciar objetos que carrega.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Unseen Passage",
            level=2,
            cost="One Rouse Check",
            description="O vampiro pode se mover enquanto permanece invisível.",
            system="Invisível mesmo em movimento. Ações violentas ou chamar atenção quebram o efeito.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Ghost in the Machine",
            level=3,
            cost="Free",
            description="O vampiro também desaparece de gravações eletrônicas.",
            system="Não aparece em câmeras, gravadores ou outros dispositivos eletrônicos.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Mask of a Thousand Faces",
            level=3,
            cost="One Rouse Check",
            description="O vampiro pode alterar sua aparência para parecer qualquer pessoa.",
            system="Mude aparência, voz e maneirismos. Pode imitar pessoas específicas com teste.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Conceal",
            level=4,
            cost="One Rouse Check",
            description="O vampiro pode esconder objetos e até outras pessoas.",
            system="Oculte objetos do tamanho de um carro ou até 2 pessoas além de si mesmo.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Vanish",
            level=4,
            cost="One Rouse Check",
            description="O vampiro pode desaparecer instantaneamente mesmo sendo observado.",
            system="Desapareça instantaneamente, mesmo se todos estiverem olhando diretamente.",
            duration="Instantâneo (depois segue regras normais)"
        ),
        DisciplinePower(
            name="Cloak the Gathering",
            level=5,
            cost="One Rouse Check",
            description="O vampiro pode ocultar um grupo inteiro.",
            system="Aplique Unseen Passage a um grupo de até 5 pessoas + você.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Impostor's Guise",
            level=5,
            cost="One Rouse Check",
            dice_pool="Manipulation + Obfuscate",
            description="O vampiro pode alterar a aparência de outros.",
            system="Aplique Mask of a Thousand Faces a outra pessoa.",
            duration="Uma cena"
        ),
    ]
)

# === POTENCE ===
POTENCE = Discipline(
    name=DisciplineType.POTENCE,
    description="Potence concede força física sobre-humana, permitindo feitos impossíveis de força bruta.",
    resonance="Atletas de força, trabalhadores braçais, pessoas furiosas",
    characteristics="Presença física intimidadora, força desproporcional ao tamanho",
    powers=[
        DisciplinePower(
            name="Lethal Body",
            level=1,
            cost="Free",
            description="O vampiro pode causar dano Agravado com mãos nuas.",
            system="Ataques desarmados causam dano Agravado contra mortais.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Soaring Leap",
            level=1,
            cost="Free",
            description="O vampiro pode saltar distâncias incríveis.",
            system="Salte verticalmente 3 metros por ponto de Potence, ou o dobro horizontalmente.",
            duration="Instantâneo"
        ),
        DisciplinePower(
            name="Prowess",
            level=2,
            cost="One Rouse Check",
            description="O vampiro adiciona força sobrenatural a ações físicas.",
            system="Adicione Potence a todos os testes de Força e dano corpo a corpo por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Brutal Feed",
            level=3,
            cost="Free",
            description="O vampiro causa dano terrível ao se alimentar.",
            system="Ao se alimentar, causa 2 níveis adicionais de dano Agravado à vítima.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Spark of Rage",
            level=3,
            cost="One Rouse Check",
            dice_pool="Manipulation + Potence",
            vs_pool="Composure + Intelligence",
            description="O vampiro pode provocar fúria violenta em outros.",
            system="O alvo entra em fúria violenta, atacando o provocador mais próximo.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Draught of Might",
            level=4,
            cost="One Rouse Check",
            description="O vampiro pode conceder força através de seu sangue.",
            system="Quem beber seu sangue ganha 2 pontos de Potence por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Earthshock",
            level=5,
            cost="Two Rouse Checks",
            dice_pool="Strength + Potence",
            description="O vampiro pode criar um tremor de terra devastador.",
            system="Golpeie o chão para derrubar todos em um raio de 10 metros e causar dano estrutural.",
            duration="Instantâneo"
        ),
        DisciplinePower(
            name="Fist of Caine",
            level=5,
            cost="One Rouse Check",
            description="O vampiro pode causar dano Agravado a outros vampiros.",
            system="Ataques desarmados causam dano Agravado contra vampiros.",
            duration="Uma cena"
        ),
    ]
)

# === PRESENCE ===
PRESENCE = Discipline(
    name=DisciplineType.PRESENCE,
    description="Presence permite ao vampiro afetar emoções, inspirar devoção ou causar terror através de sua presença sobrenatural.",
    resonance="Celebridades, líderes carismáticos, pessoas emocionalmente intensas",
    characteristics="Magnetismo natural, presença cativante, intensidade emocional",
    powers=[
        DisciplinePower(
            name="Awe",
            level=1,
            cost="Free",
            dice_pool="Manipulation + Presence",
            description="O vampiro se torna o centro das atenções, fascinando todos ao redor.",
            system="Todos na área prestam atenção no vampiro. +2 dados em testes Sociais.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Daunt",
            level=1,
            cost="Free",
            dice_pool="Charisma + Presence",
            description="O vampiro projeta uma aura intimidadora.",
            system="Alvos sentem medo e hesitam em confrontar o vampiro. -2 dados contra o vampiro.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Lingering Kiss",
            level=2,
            cost="Free",
            description="A mordida do vampiro causa prazer e vício intensos.",
            system="Vítimas da mordida ficam viciadas no prazer. -1 dado para resistir novas mordidas.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Dread Gaze",
            level=3,
            cost="One Rouse Check",
            dice_pool="Charisma + Presence",
            vs_pool="Composure + Resolve",
            description="O vampiro causa terror paralisante em um alvo.",
            system="Alvo foge em pânico ou fica paralisado de medo.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Entrancement",
            level=3,
            cost="One Rouse Check",
            dice_pool="Charisma + Presence",
            vs_pool="Composure + Intelligence",
            description="O vampiro faz um alvo se tornar devotado a ele.",
            system="Alvo faz quase qualquer coisa para agradar o vampiro, exceto se machucar.",
            duration="Uma hora por sucesso"
        ),
        DisciplinePower(
            name="Irresistible Voice",
            level=4,
            cost="One Rouse Check",
            description="Presence funciona através de meios de comunicação.",
            system="Use Presence através de telefone, rádio, vídeo ou outras mídias.",
            duration="Varia"
        ),
        DisciplinePower(
            name="Summon",
            level=4,
            cost="One Rouse Check",
            dice_pool="Manipulation + Presence",
            vs_pool="Composure + Intelligence",
            description="O vampiro pode convocar alguém que tenha encontrado antes.",
            system="Alvo sente compulsão irresistível de ir até o vampiro.",
            duration="Até chegar ou uma noite"
        ),
        DisciplinePower(
            name="Majesty",
            level=5,
            cost="Two Rouse Checks",
            dice_pool="Charisma + Presence",
            vs_pool="Composure + Resolve",
            description="O vampiro se torna impossível de atacar ou contradizer.",
            system="Ninguém pode atacar, contrariar ou mesmo ser rude com o vampiro.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Star Magnetism",
            level=5,
            cost="One Rouse Check",
            dice_pool="Manipulation + Presence",
            description="O vampiro pode afetar multidões inteiras.",
            system="Aplique Awe ou Dread Gaze a todos em uma área grande.",
            duration="Uma cena"
        ),
    ]
)

# === PROTEAN ===
PROTEAN = Discipline(
    name=DisciplineType.PROTEAN,
    description="Protean permite ao vampiro transformar seu corpo, desde garras mortais até formas animais completas.",
    resonance="Pessoas em transição, sobrevivencialistas, aqueles conectados à natureza",
    characteristics="Adaptabilidade física, conexão animal, fluidez de forma",
    powers=[
        DisciplinePower(
            name="Eyes of the Beast",
            level=1,
            cost="Free",
            description="Os olhos do vampiro brilham vermelho e podem ver no escuro total.",
            system="Visão perfeita no escuro. Olhos brilham visivelmente.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Weight of the Feather",
            level=1,
            cost="Free",
            description="O vampiro pode reduzir seu peso para quase nada.",
            system="Caia de qualquer altura sem dano. Caminhe sobre superfícies frágeis.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Feral Weapons",
            level=2,
            cost="One Rouse Check",
            description="O vampiro pode fazer crescer garras e presas mortais.",
            system="Garras causam dano Agravado +2. Podem ser usadas para escalar.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Earth Meld",
            level=3,
            cost="One Rouse Check",
            description="O vampiro pode se fundir com a terra para descansar.",
            system="Afunde na terra para dormir protegido. Desperta ao anoitecer ou se perturbado.",
            duration="Até despertar"
        ),
        DisciplinePower(
            name="Shapechange",
            level=3,
            cost="One Rouse Check",
            description="O vampiro pode se transformar em um animal.",
            system="Transforme-se em lobo ou morcego (escolha na criação). Mantenha mente vampírica.",
            duration="Uma cena ou até mudar de volta"
        ),
        DisciplinePower(
            name="Metamorphosis",
            level=4,
            cost="Two Rouse Checks",
            description="O vampiro pode se transformar em animais adicionais.",
            system="Ganhe uma forma animal adicional (cobra, corvo, etc.).",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Mist Form",
            level=5,
            cost="One Rouse Check",
            description="O vampiro pode se transformar em névoa intangível.",
            system="Torne-se névoa imune a dano físico. Pode passar por frestas. Vento forte dispersa.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="The Unfettered Heart",
            level=5,
            cost="Free",
            description="O vampiro pode mover seus órgãos vitais.",
            system="Mova o coração para outro local. Imune a estacas convencionais.",
            duration="Uma cena"
        ),
    ]
)

# === BLOOD SORCERY ===
BLOOD_SORCERY = Discipline(
    name=DisciplineType.BLOOD_SORCERY,
    description="Blood Sorcery permite manipular sangue de formas sobrenaturais, desde maldições até rituais elaborados.",
    resonance="Ocultistas, pessoas supersticiosas, aqueles com conexão a magia",
    characteristics="Fascinação com sangue e rituais, conhecimento oculto",
    powers=[
        DisciplinePower(
            name="Corrosive Vitae",
            level=1,
            cost="One Rouse Check",
            description="O vampiro pode tornar seu sangue corrosivo.",
            system="Sangue causa 2 níveis de dano Agravado por turno ao contato.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="A Taste for Blood",
            level=1,
            cost="Free",
            dice_pool="Resolve + Blood Sorcery",
            description="O vampiro pode analisar sangue ao prová-lo.",
            system="Prove sangue para determinar: Ressonância, se é vampiro, aproximação de Blood Potency.",
            duration="Instantâneo"
        ),
        DisciplinePower(
            name="Extinguish Vitae",
            level=2,
            cost="One Rouse Check",
            dice_pool="Intelligence + Blood Sorcery",
            vs_pool="Stamina + Composure",
            description="O vampiro pode destruir vitae no corpo de outro vampiro.",
            system="Aumente a Fome do alvo em 1 por sucesso.",
            duration="Instantâneo"
        ),
        DisciplinePower(
            name="Blood of Potency",
            level=3,
            cost="One Rouse Check",
            description="O vampiro pode temporariamente aumentar sua Blood Potency.",
            system="Aumente Blood Potency em 1-2 por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Scorpion's Touch",
            level=3,
            cost="One Rouse Check",
            description="O vampiro pode transformar seu sangue em veneno paralisante.",
            system="Transforme sangue em veneno. Mortais ficam paralisados. Vampiros sofrem penalidades.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Theft of Vitae",
            level=4,
            cost="One Rouse Check",
            dice_pool="Wits + Blood Sorcery",
            description="O vampiro pode extrair sangue à distância.",
            system="Arranque sangue de um alvo visível até 10 metros de distância.",
            duration="Instantâneo"
        ),
        DisciplinePower(
            name="Baal's Caress",
            level=4,
            cost="One Rouse Check",
            description="O vampiro pode transformar seu sangue em veneno letal.",
            system="Cubra uma arma com sangue venenoso. Dano da arma se torna Agravado.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Cauldron of Blood",
            level=5,
            cost="Two Rouse Checks",
            dice_pool="Resolve + Blood Sorcery",
            vs_pool="Composure + Fortitude",
            description="O vampiro pode ferver o sangue dentro de um alvo.",
            system="Ferva o sangue do alvo, causando dano Agravado massivo.",
            duration="Concentração"
        ),
    ]
)

# === OBLIVION ===
OBLIVION = Discipline(
    name=DisciplineType.OBLIVION,
    description="Oblivion conecta o vampiro às sombras e ao submundo, permitindo manipular escuridão e interagir com os mortos.",
    resonance="Moribundos, pessoas enlutadas, necrófilos, depressivos profundos",
    characteristics="Aura de morte, frieza, conexão com sombras",
    powers=[
        DisciplinePower(
            name="Shadow Cloak",
            level=1,
            cost="Free",
            description="O vampiro pode se envolver em sombras protetoras.",
            system="+2 dados em Furtividade em áreas escuras. Sombras se movem anormalmente.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Oblivion's Sight",
            level=1,
            cost="Free",
            description="O vampiro pode ver fantasmas e marcas de morte.",
            system="Veja fantasmas, espíritos e perceba se alguém morreu recentemente.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Arms of Ahriman",
            level=2,
            cost="One Rouse Check",
            dice_pool="Wits + Oblivion",
            description="O vampiro pode criar tentáculos de sombra.",
            system="Crie tentáculos de sombra para agarrar, atacar ou manipular objetos.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Shadow Cast",
            level=2,
            cost="One Rouse Check",
            description="O vampiro pode manipular e animar sombras ao redor.",
            system="Controle sombras para criar efeitos visuais, distrações ou escuridão.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Touch of Oblivion",
            level=3,
            cost="One Rouse Check",
            dice_pool="Strength + Oblivion",
            description="O vampiro pode causar dano com o frio do abismo.",
            system="Toque causa dano Agravado e sensação de frio mortal.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Stygian Shroud",
            level=3,
            cost="One Rouse Check",
            description="O vampiro pode criar uma área de escuridão total.",
            system="Crie área de 5 metros de escuridão impenetrável, mesmo para Auspex.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Skuld's Perception",
            level=4,
            cost="One Rouse Check",
            dice_pool="Resolve + Oblivion",
            description="O vampiro pode ver o destino de morte de alguém.",
            system="Veja como e quando alguém vai morrer (se nada mudar).",
            duration="Instantâneo"
        ),
        DisciplinePower(
            name="Shadow Step",
            level=4,
            cost="One Rouse Check",
            description="O vampiro pode viajar através das sombras.",
            system="Entre em uma sombra e saia de outra em até 50 metros.",
            duration="Instantâneo"
        ),
        DisciplinePower(
            name="Tenebrous Avatar",
            level=5,
            cost="Two Rouse Checks",
            description="O vampiro se torna uma criatura de sombra viva.",
            system="Transforme-se em sombra. Imune a dano físico. Pode atravessar frestas.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Lasombra's Curse",
            level=5,
            cost="One Rouse Check",
            dice_pool="Manipulation + Oblivion",
            vs_pool="Stamina + Fortitude",
            description="O vampiro pode afundar um alvo nas sombras.",
            system="Afunde alvo nas sombras. Enquanto preso, não pode agir e sofre dano.",
            duration="Concentração"
        ),
    ]
)

# === THIN-BLOOD ALCHEMY ===
THIN_BLOOD_ALCHEMY = Discipline(
    name=DisciplineType.THIN_BLOOD_ALCHEMY,
    description="Alquimia exclusiva dos Thin-Bloods, permitindo criar fórmulas que imitam Disciplinas.",
    resonance="Varia conforme a fórmula",
    characteristics="Conhecimento alquímico, experimentação, criatividade",
    powers=[
        DisciplinePower(
            name="Far Reach",
            level=1,
            cost="One Rouse Check",
            description="Cria telecinese temporária.",
            system="Mova objetos à distância como se tivesse Potence 1.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Haze",
            level=1,
            cost="One Rouse Check",
            description="Cria um efeito de Obfuscate limitado.",
            system="Funciona como Cloak of Shadows por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Envelop",
            level=2,
            cost="One Rouse Check",
            description="Cria um escudo protetor.",
            system="Funciona como Resilience + Toughness por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Profane Hieros Gamos",
            level=3,
            cost="Two Rouse Checks",
            description="Permite ato sexual que resulta em gravidez.",
            system="Thin-Blood pode conceber/engravidar. Filho é Dhampir.",
            duration="Permanente se bem-sucedido"
        ),
        DisciplinePower(
            name="Counterfeit Discipline",
            level=4,
            cost="Two Rouse Checks",
            description="Imita temporariamente uma Disciplina.",
            system="Ganhe acesso a um poder de nível 1-3 de qualquer Disciplina.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Awaken the Sleeper",
            level=5,
            cost="Special",
            description="Pode despertar um vampiro em torpor ou se tornar vampiro completo.",
            system="Ritual complexo que pode despertar anciões ou transformar o alquimista.",
            duration="Permanente"
        ),
    ]
)

# Dicionário com todas as disciplinas
DISCIPLINES_V5: dict[str, Discipline] = {
    "animalism": ANIMALISM,
    "auspex": AUSPEX,
    "blood_sorcery": BLOOD_SORCERY,
    "celerity": CELERITY,
    "dominate": DOMINATE,
    "fortitude": FORTITUDE,
    "obfuscate": OBFUSCATE,
    "oblivion": OBLIVION,
    "potence": POTENCE,
    "presence": PRESENCE,
    "protean": PROTEAN,
    "thin_blood_alchemy": THIN_BLOOD_ALCHEMY,
}


def get_discipline(discipline_id: str) -> Optional[Discipline]:
    """Get discipline by ID"""
    return DISCIPLINES_V5.get(discipline_id.lower().replace(" ", "_").replace("-", "_"))


def get_powers_by_level(discipline_id: str, level: int) -> List[DisciplinePower]:
    """Get all powers of a specific level from a discipline"""
    discipline = get_discipline(discipline_id)
    if not discipline:
        return []
    return [p for p in discipline.powers if p.level == level]
