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
    source_book: str = "Livro Basico"


class Discipline(BaseModel):
    name: DisciplineType
    description: str
    resonance: str
    characteristics: str
    powers: List[DisciplinePower]


# === ANIMALISMO ===
ANIMALISM = Discipline(
    name=DisciplineType.ANIMALISM,
    description="Animalismo traz o vampiro mais perto de sua natureza predatoria. Permite comunicacao e controle sobre animais, assim como influencia sobre a Besta interior.",
    resonance="Sangue animal, especialmente predadores; humanos extremamente passivos ou ferozes",
    characteristics="Olhos podem brilhar como os de um animal; animais reagem fortemente a presenca do vampiro",
    powers=[
        DisciplinePower(
            name="Vinculo com Famulus",
            level=1,
            cost="1 Rouse Check",
            description="O vampiro cria um laco permanente com um animal, tornando-o seu servo leal.",
            system="Gaste uma cena alimentando o animal com seu sangue por 3 noites consecutivas. O animal se torna um Famulus: obedece comandos mentais, o vampiro sente suas emocoes e localizacao aproximada. Limite de 1 Famulus por ponto de Animalismo.",
            duration="Permanente"
        ),
        DisciplinePower(
            name="Sentir a Besta",
            level=1,
            cost="Gratis",
            dice_pool="Determinacao + Animalismo",
            vs_pool="Autocontrole + Labia",
            description="O vampiro pode detectar a Besta em outros, sentindo vampiros, lobisomens e criaturas em frenesi.",
            system="Teste contestado. Sucesso revela: se o alvo e sobrenatural, seu nivel aproximado de Fome/Furia, se esta em frenesi ou prestes a entrar.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Sussurros Selvagens",
            level=2,
            cost="Gratis / 1 Rouse Check",
            dice_pool="Manipulacao + Animalismo",
            description="O vampiro pode se comunicar com animais e dar comandos simples.",
            system="Comunicacao basica e gratuita. Comandos complexos ou contra a natureza do animal exigem Rouse Check e teste.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Suculencia Animal",
            level=3,
            cost="Gratis",
            description="O vampiro extrai mais sustento de sangue animal.",
            system="Ao se alimentar de animais, reduza Fome em 2 ao inves de 1 (mas ainda nao pode reduzir abaixo de 1 com sangue animal).",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Acalmar a Besta",
            level=3,
            cost="1 Rouse Check",
            dice_pool="Carisma + Animalismo",
            vs_pool="Vigor + Determinacao",
            description="Acalma a Besta em outro vampiro, encerrando frenesi, ou aterroriza um mortal ate a submissao.",
            system="Contra vampiro em frenesi: sucesso encerra o frenesi imediatamente. O alvo fica letargico por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Subsumir o Espirito",
            level=4,
            cost="1 Rouse Check",
            dice_pool="Manipulacao + Animalismo",
            description="O vampiro projeta sua consciencia para dentro de um animal, controlando seu corpo.",
            system="O corpo do vampiro fica em torpor enquanto controla o animal. Pode usar Auspicios e Animalismo atraves do animal.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Dominio Animal",
            level=5,
            cost="2 Rouse Checks",
            dice_pool="Carisma + Animalismo",
            description="O vampiro comanda todos os animais de um tipo especifico em uma grande area.",
            system="Todos os animais do tipo escolhido em um raio de varios quarteiroes atendem ao chamado.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Extrair a Besta",
            level=5,
            cost="1 Rouse Check",
            dice_pool="Raciocinio + Animalismo",
            vs_pool="Autocontrole + Determinacao",
            description="O vampiro transfere sua Besta para outro, fazendo-o entrar em frenesi enquanto o usuario fica calmo.",
            system="Se bem-sucedido, o vampiro fica imune a frenesi enquanto a Besta esta fora. O alvo entra em frenesi imediato.",
            duration="Ate a Besta retornar"
        ),
    ]
)

# === AUSPICIOS ===
AUSPEX = Discipline(
    name=DisciplineType.AUSPEX,
    description="Auspicios aguca os sentidos do vampiro alem dos limites mortais, permitindo percepcao sobrenatural, leitura de auras e ate telepatia.",
    resonance="Artistas, visionarios, investigadores, usuarios de drogas psicodelicas",
    characteristics="Olhar penetrante, dificuldade em ignorar detalhes, hipersensibilidade",
    powers=[
        DisciplinePower(
            name="Sentidos Aguados",
            level=1,
            cost="Gratis",
            description="Todos os sentidos do vampiro se tornam sobrenaturalmente agucados.",
            system="Adicione Auspicios a testes de percepcao. Pode ver no escuro, ouvir frequencias inaudiveis, etc. Vulneravel a sobrecarga sensorial.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Sentir o Oculto",
            level=1,
            cost="Gratis",
            dice_pool="Raciocinio + Auspicios",
            description="O vampiro pode sentir presencas sobrenaturais ocultas.",
            system="Detecta vampiros usando Ofuscacao, fantasmas, magia ativa, e outras presencas sobrenaturais.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Premonicao",
            level=2,
            cost="Gratis / 1 Rouse Check",
            dice_pool="Determinacao + Auspicios",
            description="O vampiro recebe vislumbres do futuro ou insights sobre situacoes.",
            system="Pode receber avisos de perigo iminente (gratis) ou buscar ativamente visoes (Rouse Check).",
            duration="Instantaneo"
        ),
        DisciplinePower(
            name="Ler a Alma",
            level=3,
            cost="1 Rouse Check",
            dice_pool="Inteligencia + Auspicios",
            vs_pool="Autocontrole + Labia",
            description="O vampiro pode ver a aura de um alvo, revelando seu estado emocional e natureza.",
            system="Revela: estado emocional, se e sobrenatural, Ressonancia do sangue, se esta sob Dominacao/Presenca, diablerie.",
            duration="Concentracao"
        ),
        DisciplinePower(
            name="Compartilhar Sentidos",
            level=3,
            cost="1 Rouse Check",
            dice_pool="Determinacao + Auspicios",
            description="O vampiro pode usar os sentidos de outro ser com quem tenha conexao.",
            system="Pode ver atraves dos olhos de alguem com quem tenha Laco de Sangue, Famulus, ou que tenha provado seu sangue.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Toque do Espirito",
            level=4,
            cost="1 Rouse Check",
            dice_pool="Inteligencia + Auspicios",
            description="O vampiro pode ler a historia psiquica de um objeto ao toca-lo.",
            system="Revela visoes do passado do objeto, especialmente eventos emocionalmente intensos.",
            duration="Instantaneo"
        ),
        DisciplinePower(
            name="Clarividencia",
            level=5,
            cost="1 Rouse Check",
            dice_pool="Inteligencia + Auspicios",
            description="O vampiro pode projetar seus sentidos para um local distante.",
            system="Pode perceber um local conhecido a distancia. Quanto mais familiar, mais facil.",
            duration="Concentracao"
        ),
        DisciplinePower(
            name="Telepatia",
            level=5,
            cost="1 Rouse Check",
            dice_pool="Determinacao + Auspicios",
            vs_pool="Raciocinio + Labia",
            description="O vampiro pode ler pensamentos e se comunicar mentalmente.",
            system="Pode ler pensamentos superficiais ou enviar mensagens mentais. Pensamentos profundos requerem contestacao.",
            duration="Concentracao"
        ),
    ]
)

# === RAPIDEZ ===
CELERITY = Discipline(
    name=DisciplineType.CELERITY,
    description="Rapidez concede velocidade e reflexos sobre-humanos, permitindo ao vampiro agir mais rapido que qualquer mortal.",
    resonance="Atletas, pessoas em perigo fugindo, usuarios de estimulantes",
    characteristics="Movimentos fluidos, reflexos instantaneos, impaciencia",
    powers=[
        DisciplinePower(
            name="Graca Felina",
            level=1,
            cost="Gratis",
            description="O vampiro se move com graca sobrenatural.",
            system="Automaticamente bem-sucedido em testes de equilibrio. Pode cair de qualquer altura sem dano.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Reflexos Rapidos",
            level=1,
            cost="Gratis",
            description="O vampiro reage antes que outros possam agir.",
            system="Adicione Rapidez a iniciativa. Pode usar uma acao de Defesa adicional por turno.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Ligeireza",
            level=2,
            cost="1 Rouse Check",
            description="O vampiro pode se mover em velocidade incrivel.",
            system="Adicione Rapidez a testes de Destreza nao-combate. Velocidade de movimento dobrada.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Piscar",
            level=3,
            cost="1 Rouse Check",
            description="O vampiro pode atravessar curtas distancias instantaneamente.",
            system="Mova-se ate 50 metros instantaneamente. Nao pode atacar no mesmo turno.",
            duration="Instantaneo"
        ),
        DisciplinePower(
            name="Travessia",
            level=3,
            cost="1 Rouse Check",
            description="O vampiro pode correr sobre superficies verticais ou liquidas.",
            system="Pode correr em paredes, tetos ou sobre agua enquanto mantiver velocidade.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Gole de Elegancia",
            level=4,
            cost="1 Rouse Check",
            description="O vampiro pode conceder Rapidez a outro atraves de seu sangue.",
            system="Alvo que beber seu sangue ganha 2 pontos de Rapidez por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Mira Infalivel",
            level=4,
            cost="1 Rouse Check",
            description="O vampiro pode mirar com precisao perfeita.",
            system="Proximo ataque a distancia ignora cobertura e adiciona Rapidez ao dano.",
            duration="Um ataque"
        ),
        DisciplinePower(
            name="Golpe Relampago",
            level=5,
            cost="1 Rouse Check",
            description="O vampiro pode fazer multiplos ataques em um unico turno.",
            system="Faca um ataque adicional por turno, ou divida sua pool para atacar multiplos alvos.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Fracao de Segundo",
            level=5,
            cost="1 Rouse Check",
            description="O vampiro pode agir em um instante congelado no tempo.",
            system="Ganhe uma acao adicional completa antes de qualquer um poder reagir.",
            duration="Um turno"
        ),
    ]
)

# === DOMINACAO ===
DOMINATE = Discipline(
    name=DisciplineType.DOMINATE,
    description="Dominacao permite ao vampiro controlar mentes, implantar comandos e apagar memorias atraves do contato visual.",
    resonance="Pessoas em posicao de autoridade, manipuladores, controladores",
    characteristics="Olhar intenso e penetrante, dificuldade em aceitar ordens de outros",
    powers=[
        DisciplinePower(
            name="Nublar Memoria",
            level=1,
            cost="Gratis",
            dice_pool="Carisma + Dominacao",
            vs_pool="Raciocinio + Determinacao",
            description="O vampiro pode fazer o alvo esquecer os ultimos minutos.",
            system="Apaga memorias dos ultimos minutos. Alvo nao se lembra do encontro com o vampiro.",
            duration="Permanente"
        ),
        DisciplinePower(
            name="Compelir",
            level=1,
            cost="Gratis",
            dice_pool="Carisma + Dominacao",
            vs_pool="Inteligencia + Determinacao",
            description="O vampiro da um comando simples de uma palavra que deve ser obedecido.",
            system="Comando de uma palavra ('Fuja', 'Pare', 'Durma') que o alvo obedece imediatamente.",
            duration="Um turno"
        ),
        DisciplinePower(
            name="Mesmerizar",
            level=2,
            cost="1 Rouse Check",
            dice_pool="Manipulacao + Dominacao",
            vs_pool="Inteligencia + Determinacao",
            description="O vampiro pode implantar comandos mais complexos na mente do alvo.",
            system="Implante um comando que sera executado imediatamente ou quando um gatilho for ativado.",
            duration="Ate ser cumprido ou uma noite"
        ),
        DisciplinePower(
            name="Dementacao",
            level=2,
            cost="1 Rouse Check",
            dice_pool="Manipulacao + Dominacao",
            vs_pool="Autocontrole + Inteligencia",
            amalgam="Ofuscacao 2",
            description="O vampiro pode causar disturbios mentais temporarios.",
            system="Cause medo, paranoia, alucinacoes ou outros efeitos mentais no alvo.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="A Mente Esquecida",
            level=3,
            cost="1 Rouse Check",
            dice_pool="Manipulacao + Dominacao",
            vs_pool="Inteligencia + Determinacao",
            description="O vampiro pode reescrever memorias do alvo.",
            system="Apague, altere ou crie memorias falsas no alvo. Memorias complexas levam mais tempo.",
            duration="Permanente"
        ),
        DisciplinePower(
            name="Diretiva Submersa",
            level=3,
            cost="Gratis",
            description="Comandos podem ser implantados para execucao futura.",
            system="Comandos de Mesmerizar podem ser enterrados profundamente, ativando por gatilho especifico.",
            duration="Ate ser ativado"
        ),
        DisciplinePower(
            name="Racionalizar",
            level=4,
            cost="Gratis",
            description="O alvo acredita que acoes ordenadas foram sua propria ideia.",
            system="O alvo nao percebe que foi controlado e racionaliza suas acoes.",
            duration="Permanente"
        ),
        DisciplinePower(
            name="Manipulacao em Massa",
            level=5,
            cost="1 Rouse Check",
            dice_pool="Manipulacao + Dominacao",
            description="O vampiro pode afetar multiplos alvos simultaneamente.",
            system="Use qualquer poder de Dominacao em multiplos alvos que possam ver seus olhos.",
            duration="Variavel"
        ),
        DisciplinePower(
            name="Decreto Terminal",
            level=5,
            cost="2 Rouse Checks",
            dice_pool="Carisma + Dominacao",
            vs_pool="Determinacao + Inteligencia",
            description="O vampiro pode ordenar que o alvo morra.",
            system="O alvo mortal morre de parada cardiaca. Vampiros entram em torpor.",
            duration="Permanente"
        ),
    ]
)

# === FORTITUDE ===
FORTITUDE = Discipline(
    name=DisciplineType.FORTITUDE,
    description="Fortitude concede resistencia sobrenatural contra dano fisico e mental.",
    resonance="Sobreviventes, pessoas que passaram por trauma, trabalhadores bracais",
    characteristics="Aparencia inabalavel, indiferenca a dor, compostura sob pressao",
    powers=[
        DisciplinePower(
            name="Resiliencia",
            level=1,
            cost="Gratis",
            description="O vampiro pode ignorar fontes menores de dano.",
            system="Adicione Fortitude a saude Superficial. Converta dano Superficial de fontes frias em nada.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Mente Inabalavel",
            level=1,
            cost="Gratis",
            description="O vampiro resiste a manipulacao mental e emocional.",
            system="Adicione Fortitude a testes de resistencia contra Dominacao, Presenca e efeitos mentais.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Dureza",
            level=2,
            cost="1 Rouse Check",
            description="O vampiro pode converter dano Agravado em Superficial.",
            system="Uma vez por cena, converta niveis de dano Agravado igual a Fortitude em Superficial.",
            duration="Instantaneo"
        ),
        DisciplinePower(
            name="Bestas Resistentes",
            level=2,
            cost="1 Rouse Check",
            description="O vampiro pode conceder resistencia a animais e carnicais.",
            system="Famulus ou carnicais ganham Fortitude/2 (arredondado para cima) a resistencia.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Desafiar a Perdicao",
            level=3,
            cost="1 Rouse Check",
            description="O vampiro pode resistir a fraquezas tradicionais.",
            system="Reduza dano de fogo e luz solar em Fortitude por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Fortalecer a Fachada Interior",
            level=3,
            cost="Gratis",
            description="O vampiro pode resistir a Auspicios e leitura de aura.",
            system="Contestacoes contra Auspicios usam Fortitude + Autocontrole.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Gole de Resistencia",
            level=4,
            cost="1 Rouse Check",
            description="O vampiro pode conceder Fortitude atraves de seu sangue.",
            system="Quem beber seu sangue ganha 2 pontos de Fortitude por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Carne de Marmore",
            level=5,
            cost="2 Rouse Checks",
            description="A pele do vampiro se torna dura como pedra.",
            system="Reduza todo dano recebido pela metade. Imune a estacas.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Poder da Dor",
            level=5,
            cost="Gratis",
            description="O vampiro se torna mais poderoso quando ferido.",
            system="Adicione niveis de dano sofrido como bonus a ataques e resistencia.",
            duration="Enquanto ferido"
        ),
    ]
)

# === OFUSCACAO ===
OBFUSCATE = Discipline(
    name=DisciplineType.OBFUSCATE,
    description="Ofuscacao permite ao vampiro desaparecer, alterar sua aparencia e apagar sua presenca das mentes ao redor.",
    resonance="Pessoas ignoradas pela sociedade, introvertidos, espioes",
    characteristics="Facilmente esquecido, presenca indistinta, habilidade de passar despercebido",
    powers=[
        DisciplinePower(
            name="Manto de Sombras",
            level=1,
            cost="Gratis",
            description="O vampiro pode desaparecer enquanto estiver imovel em sombras.",
            system="Torna-se invisivel se imovel e em area escura. Movimento quebra o efeito.",
            duration="Enquanto imovel"
        ),
        DisciplinePower(
            name="Silencio da Morte",
            level=1,
            cost="Gratis",
            description="O vampiro pode silenciar completamente seus sons.",
            system="Nao produz som algum. Pode silenciar objetos que carrega.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Passagem Invisivel",
            level=2,
            cost="1 Rouse Check",
            description="O vampiro pode se mover enquanto permanece invisivel.",
            system="Invisivel mesmo em movimento. Acoes violentas ou chamar atencao quebram o efeito.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Fantasma na Maquina",
            level=3,
            cost="Gratis",
            description="O vampiro tambem desaparece de gravacoes eletronicas.",
            system="Nao aparece em cameras, gravadores ou outros dispositivos eletronicos.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Mascara de Mil Faces",
            level=3,
            cost="1 Rouse Check",
            description="O vampiro pode alterar sua aparencia para parecer qualquer pessoa.",
            system="Mude aparencia, voz e maneirismos. Pode imitar pessoas especificas com teste.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Ocultar",
            level=4,
            cost="1 Rouse Check",
            description="O vampiro pode esconder objetos e ate outras pessoas.",
            system="Oculte objetos do tamanho de um carro ou ate 2 pessoas alem de si mesmo.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Desaparecer",
            level=4,
            cost="1 Rouse Check",
            description="O vampiro pode desaparecer instantaneamente mesmo sendo observado.",
            system="Desapareca instantaneamente, mesmo se todos estiverem olhando diretamente.",
            duration="Instantaneo"
        ),
        DisciplinePower(
            name="Encobrir o Grupo",
            level=5,
            cost="1 Rouse Check",
            description="O vampiro pode ocultar um grupo inteiro.",
            system="Aplique Passagem Invisivel a um grupo de ate 5 pessoas + voce.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Disfarce do Impostor",
            level=5,
            cost="1 Rouse Check",
            dice_pool="Manipulacao + Ofuscacao",
            description="O vampiro pode alterar a aparencia de outros.",
            system="Aplique Mascara de Mil Faces a outra pessoa.",
            duration="Uma cena"
        ),
    ]
)

# === POTENCIA ===
POTENCE = Discipline(
    name=DisciplineType.POTENCE,
    description="Potencia concede forca fisica sobre-humana, permitindo feitos impossiveis de forca bruta.",
    resonance="Atletas de forca, trabalhadores bracais, pessoas furiosas",
    characteristics="Presenca fisica intimidadora, forca desproporcional ao tamanho",
    powers=[
        DisciplinePower(
            name="Corpo Letal",
            level=1,
            cost="Gratis",
            description="O vampiro pode causar dano Agravado com maos nuas.",
            system="Ataques desarmados causam dano Agravado contra mortais.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Salto Elevado",
            level=1,
            cost="Gratis",
            description="O vampiro pode saltar distancias incriveis.",
            system="Salte verticalmente 3 metros por ponto de Potencia, ou o dobro horizontalmente.",
            duration="Instantaneo"
        ),
        DisciplinePower(
            name="Proeza",
            level=2,
            cost="1 Rouse Check",
            description="O vampiro adiciona forca sobrenatural a acoes fisicas.",
            system="Adicione Potencia a todos os testes de Forca e dano corpo a corpo por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Alimentacao Brutal",
            level=3,
            cost="Gratis",
            description="O vampiro causa dano terrivel ao se alimentar.",
            system="Ao se alimentar, causa 2 niveis adicionais de dano Agravado a vitima.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Centelha de Raiva",
            level=3,
            cost="1 Rouse Check",
            dice_pool="Manipulacao + Potencia",
            vs_pool="Autocontrole + Inteligencia",
            description="O vampiro pode provocar furia violenta em outros.",
            system="O alvo entra em furia violenta, atacando o provocador mais proximo.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Gole de Poder",
            level=4,
            cost="1 Rouse Check",
            description="O vampiro pode conceder forca atraves de seu sangue.",
            system="Quem beber seu sangue ganha 2 pontos de Potencia por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Abalo Sismico",
            level=5,
            cost="2 Rouse Checks",
            dice_pool="Forca + Potencia",
            description="O vampiro pode criar um tremor de terra devastador.",
            system="Golpeie o chao para derrubar todos em um raio de 10 metros e causar dano estrutural.",
            duration="Instantaneo"
        ),
        DisciplinePower(
            name="Punho de Caim",
            level=5,
            cost="1 Rouse Check",
            description="O vampiro pode causar dano Agravado a outros vampiros.",
            system="Ataques desarmados causam dano Agravado contra vampiros.",
            duration="Uma cena"
        ),
    ]
)

# === PRESENCA ===
PRESENCE = Discipline(
    name=DisciplineType.PRESENCE,
    description="Presenca permite ao vampiro afetar emocoes, inspirar devocao ou causar terror atraves de sua presenca sobrenatural.",
    resonance="Celebridades, lideres carismaticos, pessoas emocionalmente intensas",
    characteristics="Magnetismo natural, presenca cativante, intensidade emocional",
    powers=[
        DisciplinePower(
            name="Fascinio",
            level=1,
            cost="Gratis",
            dice_pool="Manipulacao + Presenca",
            description="O vampiro se torna o centro das atencoes, fascinando todos ao redor.",
            system="Todos na area prestam atencao no vampiro. +2 dados em testes Sociais.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Intimidar",
            level=1,
            cost="Gratis",
            dice_pool="Carisma + Presenca",
            description="O vampiro projeta uma aura intimidadora.",
            system="Alvos sentem medo e hesitam em confrontar o vampiro. -2 dados contra o vampiro.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Beijo Persistente",
            level=2,
            cost="Gratis",
            description="A mordida do vampiro causa prazer e vicio intensos.",
            system="Vitimas da mordida ficam viciadas no prazer. -1 dado para resistir novas mordidas.",
            duration="Passivo"
        ),
        DisciplinePower(
            name="Olhar Aterrorizante",
            level=3,
            cost="1 Rouse Check",
            dice_pool="Carisma + Presenca",
            vs_pool="Autocontrole + Determinacao",
            description="O vampiro causa terror paralisante em um alvo.",
            system="Alvo foge em panico ou fica paralisado de medo.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Encantamento",
            level=3,
            cost="1 Rouse Check",
            dice_pool="Carisma + Presenca",
            vs_pool="Autocontrole + Inteligencia",
            description="O vampiro faz um alvo se tornar devotado a ele.",
            system="Alvo faz quase qualquer coisa para agradar o vampiro, exceto se machucar.",
            duration="Uma hora por sucesso"
        ),
        DisciplinePower(
            name="Voz Irresistivel",
            level=4,
            cost="1 Rouse Check",
            description="Presenca funciona atraves de meios de comunicacao.",
            system="Use Presenca atraves de telefone, radio, video ou outras midias.",
            duration="Variavel"
        ),
        DisciplinePower(
            name="Convocar",
            level=4,
            cost="1 Rouse Check",
            dice_pool="Manipulacao + Presenca",
            vs_pool="Autocontrole + Inteligencia",
            description="O vampiro pode convocar alguem que tenha encontrado antes.",
            system="Alvo sente compulsao irresistivel de ir ate o vampiro.",
            duration="Ate chegar ou uma noite"
        ),
        DisciplinePower(
            name="Majestade",
            level=5,
            cost="2 Rouse Checks",
            dice_pool="Carisma + Presenca",
            vs_pool="Autocontrole + Determinacao",
            description="O vampiro se torna impossivel de atacar ou contradizer.",
            system="Ninguem pode atacar, contrariar ou mesmo ser rude com o vampiro.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Magnetismo Estelar",
            level=5,
            cost="1 Rouse Check",
            dice_pool="Manipulacao + Presenca",
            description="O vampiro pode afetar multidoes inteiras.",
            system="Aplique Fascinio ou Olhar Aterrorizante a todos em uma area grande.",
            duration="Uma cena"
        ),
    ]
)

# === METAMORFOSE ===
PROTEAN = Discipline(
    name=DisciplineType.PROTEAN,
    description="Metamorfose permite ao vampiro transformar seu corpo, desde garras mortais ate formas animais completas.",
    resonance="Pessoas em transicao, sobrevivencialistas, aqueles conectados a natureza",
    characteristics="Adaptabilidade fisica, conexao animal, fluidez de forma",
    powers=[
        DisciplinePower(
            name="Olhos da Besta",
            level=1,
            cost="Gratis",
            description="Os olhos do vampiro brilham vermelho e podem ver no escuro total.",
            system="Visao perfeita no escuro. Olhos brilham visivelmente.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Peso da Pluma",
            level=1,
            cost="Gratis",
            description="O vampiro pode reduzir seu peso para quase nada.",
            system="Caia de qualquer altura sem dano. Caminhe sobre superficies frageis.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Armas Selvagens",
            level=2,
            cost="1 Rouse Check",
            description="O vampiro pode fazer crescer garras e presas mortais.",
            system="Garras causam dano Agravado +2. Podem ser usadas para escalar.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Fusao com a Terra",
            level=3,
            cost="1 Rouse Check",
            description="O vampiro pode se fundir com a terra para descansar.",
            system="Afunde na terra para dormir protegido. Desperta ao anoitecer ou se perturbado.",
            duration="Ate despertar"
        ),
        DisciplinePower(
            name="Mudanca de Forma",
            level=3,
            cost="1 Rouse Check",
            description="O vampiro pode se transformar em um animal.",
            system="Transforme-se em lobo ou morcego (escolha na criacao). Mantenha mente vampirica.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Metamorfose Avancada",
            level=4,
            cost="2 Rouse Checks",
            description="O vampiro pode se transformar em animais adicionais.",
            system="Ganhe uma forma animal adicional (cobra, corvo, etc.).",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Forma de Nevoa",
            level=5,
            cost="1 Rouse Check",
            description="O vampiro pode se transformar em nevoa intangivel.",
            system="Torne-se nevoa imune a dano fisico. Pode passar por frestas. Vento forte dispersa.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="O Coracao Livre",
            level=5,
            cost="Gratis",
            description="O vampiro pode mover seus orgaos vitais.",
            system="Mova o coracao para outro local. Imune a estacas convencionais.",
            duration="Uma cena"
        ),
    ]
)

# === FEITICARIA DE SANGUE ===
BLOOD_SORCERY = Discipline(
    name=DisciplineType.BLOOD_SORCERY,
    description="Feiticaria de Sangue permite manipular sangue de formas sobrenaturais, desde maldicoes ate rituais elaborados.",
    resonance="Ocultistas, pessoas supersticiosas, aqueles com conexao a magia",
    characteristics="Fascinacao com sangue e rituais, conhecimento oculto",
    powers=[
        DisciplinePower(
            name="Vitae Corrosivo",
            level=1,
            cost="1 Rouse Check",
            description="O vampiro pode tornar seu sangue corrosivo.",
            system="Sangue causa 2 niveis de dano Agravado por turno ao contato.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Gosto de Sangue",
            level=1,
            cost="Gratis",
            dice_pool="Determinacao + Feiticaria de Sangue",
            description="O vampiro pode analisar sangue ao prova-lo.",
            system="Prove sangue para determinar: Ressonancia, se e vampiro, aproximacao de Potencia de Sangue.",
            duration="Instantaneo"
        ),
        DisciplinePower(
            name="Extinguir Vitae",
            level=2,
            cost="1 Rouse Check",
            dice_pool="Inteligencia + Feiticaria de Sangue",
            vs_pool="Vigor + Autocontrole",
            description="O vampiro pode destruir vitae no corpo de outro vampiro.",
            system="Aumente a Fome do alvo em 1 por sucesso.",
            duration="Instantaneo"
        ),
        DisciplinePower(
            name="Sangue de Potencia",
            level=3,
            cost="1 Rouse Check",
            description="O vampiro pode temporariamente aumentar sua Potencia de Sangue.",
            system="Aumente Potencia de Sangue em 1-2 por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Toque do Escorpiao",
            level=3,
            cost="1 Rouse Check",
            description="O vampiro pode transformar seu sangue em veneno paralisante.",
            system="Transforme sangue em veneno. Mortais ficam paralisados. Vampiros sofrem penalidades.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Roubo de Vitae",
            level=4,
            cost="1 Rouse Check",
            dice_pool="Raciocinio + Feiticaria de Sangue",
            description="O vampiro pode extrair sangue a distancia.",
            system="Arranque sangue de um alvo visivel ate 10 metros de distancia.",
            duration="Instantaneo"
        ),
        DisciplinePower(
            name="Caricia de Baal",
            level=4,
            cost="1 Rouse Check",
            description="O vampiro pode transformar seu sangue em veneno letal.",
            system="Cubra uma arma com sangue venenoso. Dano da arma se torna Agravado.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Caldeirao de Sangue",
            level=5,
            cost="2 Rouse Checks",
            dice_pool="Determinacao + Feiticaria de Sangue",
            vs_pool="Autocontrole + Fortitude",
            description="O vampiro pode ferver o sangue dentro de um alvo.",
            system="Ferva o sangue do alvo, causando dano Agravado massivo.",
            duration="Concentracao"
        ),
    ]
)

# === OBLIVIO ===
OBLIVION = Discipline(
    name=DisciplineType.OBLIVION,
    description="Oblivio conecta o vampiro as sombras e ao submundo, permitindo manipular escuridao e interagir com os mortos.",
    resonance="Moribundos, pessoas enlutadas, necrofilos, depressivos profundos",
    characteristics="Aura de morte, frieza, conexao com sombras",
    powers=[
        DisciplinePower(
            name="Manto de Sombra",
            level=1,
            cost="Gratis",
            description="O vampiro pode se envolver em sombras protetoras.",
            system="+2 dados em Furtividade em areas escuras. Sombras se movem anormalmente.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Visao do Oblivio",
            level=1,
            cost="Gratis",
            description="O vampiro pode ver fantasmas e marcas de morte.",
            system="Veja fantasmas, espiritos e perceba se alguem morreu recentemente.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Bracos de Ahriman",
            level=2,
            cost="1 Rouse Check",
            dice_pool="Raciocinio + Oblivio",
            description="O vampiro pode criar tentaculos de sombra.",
            system="Crie tentaculos de sombra para agarrar, atacar ou manipular objetos.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Projecao de Sombras",
            level=2,
            cost="1 Rouse Check",
            description="O vampiro pode manipular e animar sombras ao redor.",
            system="Controle sombras para criar efeitos visuais, distracoes ou escuridao.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Toque do Oblivio",
            level=3,
            cost="1 Rouse Check",
            dice_pool="Forca + Oblivio",
            description="O vampiro pode causar dano com o frio do abismo.",
            system="Toque causa dano Agravado e sensacao de frio mortal.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Mortalha Estigia",
            level=3,
            cost="1 Rouse Check",
            description="O vampiro pode criar uma area de escuridao total.",
            system="Crie area de 5 metros de escuridao impenetravel, mesmo para Auspicios.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Percepcao de Skuld",
            level=4,
            cost="1 Rouse Check",
            dice_pool="Determinacao + Oblivio",
            description="O vampiro pode ver o destino de morte de alguem.",
            system="Veja como e quando alguem vai morrer (se nada mudar).",
            duration="Instantaneo"
        ),
        DisciplinePower(
            name="Passo nas Sombras",
            level=4,
            cost="1 Rouse Check",
            description="O vampiro pode viajar atraves das sombras.",
            system="Entre em uma sombra e saia de outra em ate 50 metros.",
            duration="Instantaneo"
        ),
        DisciplinePower(
            name="Avatar Tenebroso",
            level=5,
            cost="2 Rouse Checks",
            description="O vampiro se torna uma criatura de sombra viva.",
            system="Transforme-se em sombra. Imune a dano fisico. Pode atravessar frestas.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Maldicao de Lasombra",
            level=5,
            cost="1 Rouse Check",
            dice_pool="Manipulacao + Oblivio",
            vs_pool="Vigor + Fortitude",
            description="O vampiro pode afundar um alvo nas sombras.",
            system="Afunde alvo nas sombras. Enquanto preso, nao pode agir e sofre dano.",
            duration="Concentracao"
        ),
    ]
)

# === ALQUIMIA DE SANGUE FRACO ===
THIN_BLOOD_ALCHEMY = Discipline(
    name=DisciplineType.THIN_BLOOD_ALCHEMY,
    description="Alquimia exclusiva dos Sangue Fraco, permitindo criar formulas que imitam Disciplinas.",
    resonance="Varia conforme a formula",
    characteristics="Conhecimento alquimico, experimentacao, criatividade",
    powers=[
        DisciplinePower(
            name="Alcance Distante",
            level=1,
            cost="1 Rouse Check",
            description="Cria telecinese temporaria.",
            system="Mova objetos a distancia como se tivesse Potencia 1.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Nevoa",
            level=1,
            cost="1 Rouse Check",
            description="Cria um efeito de Ofuscacao limitado.",
            system="Funciona como Manto de Sombras por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Envolver",
            level=2,
            cost="1 Rouse Check",
            description="Cria um escudo protetor.",
            system="Funciona como Resiliencia + Dureza por uma cena.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Hieros Gamos Profano",
            level=3,
            cost="2 Rouse Checks",
            description="Permite ato sexual que resulta em gravidez.",
            system="Sangue Fraco pode conceber/engravidar. Filho e Dhampir.",
            duration="Permanente se bem-sucedido"
        ),
        DisciplinePower(
            name="Disciplina Falsificada",
            level=4,
            cost="2 Rouse Checks",
            description="Imita temporariamente uma Disciplina.",
            system="Ganhe acesso a um poder de nivel 1-3 de qualquer Disciplina.",
            duration="Uma cena"
        ),
        DisciplinePower(
            name="Despertar o Adormecido",
            level=5,
            cost="Especial",
            description="Pode despertar um vampiro em torpor ou se tornar vampiro completo.",
            system="Ritual complexo que pode despertar ancioes ou transformar o alquimista.",
            duration="Permanente"
        ),
    ]
)

# Dicionario com todas as disciplinas
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
