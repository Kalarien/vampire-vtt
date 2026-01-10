from typing import List, Optional
from pydantic import BaseModel


class HumanityLevel(BaseModel):
    level: int
    description: str
    effects: List[str]


HUMANITY_TABLE: dict[int, HumanityLevel] = {
    10: HumanityLevel(
        level=10,
        description="Santos e pacifistas absolutos. Extremamente raro entre vampiros.",
        effects=[
            "Pode ficar acordado durante o dia sem penalidade",
            "Pode comer comida normalmente",
            "Morte de qualquer ser vivo causa teste de degeneração"
        ]
    ),
    9: HumanityLevel(
        level=9,
        description="Quase humano. A maioria dos mortais éticos opera aqui.",
        effects=[
            "Morte causa Stains",
            "Violência séria causa Stains",
            "Penalidade diurna: -1 dado"
        ]
    ),
    8: HumanityLevel(
        level=8,
        description="Ética elevada. Comum entre Consensualists e Farmers.",
        effects=[
            "Matar causa Stains",
            "Permitir morte que poderia prevenir causa Stains",
            "Penalidade diurna: -1 dado"
        ]
    ),
    7: HumanityLevel(
        level=7,
        description="Humanidade padrão para neonatos. Moral normal.",
        effects=[
            "Assassinato intencional causa Stains",
            "Crueldade desnecessária causa Stains",
            "Penalidade diurna: -2 dados"
        ]
    ),
    6: HumanityLevel(
        level=6,
        description="Caçadores violentos. A Besta está mais presente.",
        effects=[
            "Assassinato a sangue frio causa Stains",
            "Tortura causa Stains",
            "Penalidade diurna: -2 dados"
        ]
    ),
    5: HumanityLevel(
        level=5,
        description="Distante da humanidade. Criminosos violentos.",
        effects=[
            "Apenas atos verdadeiramente monstruosos causam Stains",
            "Dificuldade em se conectar com mortais",
            "Penalidade diurna: -3 dados"
        ]
    ),
    4: HumanityLevel(
        level=4,
        description="Predador desumano. Poucos vestígios de consciência.",
        effects=[
            "Apenas genocídio ou tortura extrema causa Stains",
            "Mortais sentem algo errado",
            "Penalidade diurna: -3 dados"
        ]
    ),
    3: HumanityLevel(
        level=3,
        description="Monstro. Comportamento totalmente alienígena.",
        effects=[
            "Quase nada causa Stains",
            "Aparência começando a parecer monstruosa",
            "Penalidade diurna: -4 dados"
        ]
    ),
    2: HumanityLevel(
        level=2,
        description="À beira do colapso total. A Besta domina.",
        effects=[
            "Nenhuma ação causa Stains",
            "Dificuldade em simular comportamento humano",
            "Penalidade diurna: -4 dados"
        ]
    ),
    1: HumanityLevel(
        level=1,
        description="Praticamente Wassail. Um fio de consciência permanece.",
        effects=[
            "Próximo Stain = Wassail",
            "Aparência claramente monstruosa",
            "Penalidade diurna: -5 dados"
        ]
    ),
    0: HumanityLevel(
        level=0,
        description="Wassail. A Besta assumiu completamente.",
        effects=[
            "Personagem se torna NPC",
            "Atacará qualquer um, amigo ou inimigo",
            "Sem controle - apenas instinto"
        ]
    ),
}


class StainAction(BaseModel):
    action: str
    stains: int
    humanity_threshold: int  # Só causa Stains se Humanity >= este valor


STAINS_ACTIONS: List[StainAction] = [
    # Humanity 10
    StainAction(action="Matar qualquer ser vivo (incluindo animais)", stains=1, humanity_threshold=10),

    # Humanity 9
    StainAction(action="Morte de mortal (mesmo indireta)", stains=1, humanity_threshold=9),
    StainAction(action="Violência séria contra mortal", stains=1, humanity_threshold=9),

    # Humanity 8
    StainAction(action="Matar mortal (não em autodefesa)", stains=2, humanity_threshold=8),
    StainAction(action="Permitir morte que poderia prevenir", stains=1, humanity_threshold=8),

    # Humanity 7
    StainAction(action="Assassinato intencional", stains=2, humanity_threshold=7),
    StainAction(action="Crueldade desnecessária", stains=1, humanity_threshold=7),
    StainAction(action="Violar uma Convicção", stains=1, humanity_threshold=7),

    # Humanity 6
    StainAction(action="Assassinato a sangue frio", stains=2, humanity_threshold=6),
    StainAction(action="Tortura", stains=2, humanity_threshold=6),

    # Humanity 5
    StainAction(action="Atos monstruosos (massacre, tortura prolongada)", stains=2, humanity_threshold=5),

    # Humanity 4
    StainAction(action="Genocídio ou horror equivalente", stains=1, humanity_threshold=4),

    # Humanity 3+
    StainAction(action="Atos impensáveis", stains=1, humanity_threshold=3),
]


def get_humanity_info(level: int) -> Optional[HumanityLevel]:
    """Get humanity level info"""
    return HUMANITY_TABLE.get(level)


def get_daytime_penalty(humanity: int) -> int:
    """Get dice penalty for daytime activities"""
    if humanity >= 9:
        return -1
    elif humanity >= 7:
        return -2
    elif humanity >= 5:
        return -3
    elif humanity >= 3:
        return -4
    else:
        return -5


def calculate_stains(action: str, humanity: int) -> int:
    """Calculate stains for an action at a given humanity level"""
    for stain_action in STAINS_ACTIONS:
        if stain_action.action.lower() in action.lower() and humanity >= stain_action.humanity_threshold:
            return stain_action.stains
    return 0
