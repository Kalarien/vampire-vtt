from typing import Optional
from pydantic import BaseModel


class Merit(BaseModel):
    name: str
    dots: int
    variable_cost: bool
    description: str
    mechanical_effect: str
    prerequisites: Optional[str] = None
    source_book: str


MERITS_V5: dict[str, Merit] = {
    # === PHYSICAL ===
    "beautiful": Merit(
        name="Beautiful",
        dots=2,
        variable_cost=False,
        description="Você é excepcionalmente atraente.",
        mechanical_effect="+1 dado em pools Sociais quando aparência importa. Não funciona para Nosferatu.",
        source_book="core"
    ),
    "stunning": Merit(
        name="Stunning",
        dots=4,
        variable_cost=False,
        description="Você é deslumbrantemente belo.",
        mechanical_effect="+2 dados em pools Sociais quando aparência importa. Não funciona para Nosferatu.",
        prerequisites="Beautiful",
        source_book="core"
    ),
    "cat_like_balance": Merit(
        name="Cat-Like Balance",
        dots=1,
        variable_cost=False,
        description="Equilíbrio excepcional.",
        mechanical_effect="+2 dados para manter equilíbrio ou evitar quedas.",
        source_book="core"
    ),
    "iron_gullet": Merit(
        name="Iron Gullet",
        dots=3,
        variable_cost=False,
        description="Pode consumir sangue velho, contaminado ou animal sem problemas.",
        mechanical_effect="Não sofre penalidades por sangue de qualidade inferior. Sangue animal reduz Hunger normalmente até 1.",
        source_book="core"
    ),

    # === SOCIAL ===
    "linguistics": Merit(
        name="Linguistics",
        dots=1,
        variable_cost=True,
        description="Idiomas adicionais além do nativo.",
        mechanical_effect="Cada ponto dá fluência em um idioma adicional.",
        source_book="core"
    ),
    "etiquette_merit": Merit(
        name="Etiquette",
        dots=1,
        variable_cost=False,
        description="Conhece os protocolos Elysium e corte Kindred.",
        mechanical_effect="+1 dado em situações de etiqueta Kindred formal.",
        source_book="core"
    ),
    "high_society": Merit(
        name="High Society",
        dots=3,
        variable_cost=False,
        description="Acesso aos círculos da elite mortal.",
        mechanical_effect="Pode participar de eventos de alta sociedade sem chamar atenção.",
        source_book="core"
    ),
    "cobbler": Merit(
        name="Cobbler",
        dots=1,
        variable_cost=False,
        description="Habilidade de criar identidades falsas.",
        mechanical_effect="Pode criar Masks para si ou outros. Tempo e recursos necessários.",
        source_book="core"
    ),

    # === MENTAL ===
    "acute_senses": Merit(
        name="Acute Senses",
        dots=1,
        variable_cost=False,
        description="Um sentido particularmente aguçado.",
        mechanical_effect="+1 dado em testes de Percepção usando aquele sentido.",
        source_book="core"
    ),
    "eidetic_memory": Merit(
        name="Eidetic Memory",
        dots=3,
        variable_cost=False,
        description="Memória fotográfica perfeita.",
        mechanical_effect="Pode recordar qualquer coisa já vista/ouvida com clareza perfeita.",
        source_book="core"
    ),
    "light_sleeper": Merit(
        name="Light Sleeper",
        dots=1,
        variable_cost=False,
        description="Acorda facilmente durante o dia.",
        mechanical_effect="Acorda instantaneamente se perturbado. -2 na penalidade diurna.",
        source_book="core"
    ),

    # === FEEDING ===
    "bloodhound": Merit(
        name="Bloodhound",
        dots=1,
        variable_cost=False,
        description="Olfato aguçado para sangue.",
        mechanical_effect="Pode farejar sangue e determinar Ressonância pelo cheiro.",
        source_book="core"
    ),

    # === SUPERNATURAL ===
    "unbondable": Merit(
        name="Unbondable",
        dots=5,
        variable_cost=False,
        description="Imune a Blood Bonds.",
        mechanical_effect="Não pode formar Blood Bonds com outros vampiros. Extremamente raro.",
        source_book="core"
    ),

    # === THIN-BLOOD SPECIFIC ===
    "lifelike": Merit(
        name="Lifelike",
        dots=1,
        variable_cost=False,
        description="Aparência muito humana.",
        mechanical_effect="Pode passar por humano mesmo sob inspeção. Blush of Life gratuito.",
        prerequisites="Thin-Blood only",
        source_book="core"
    ),
    "thin_blood_daywalker": Merit(
        name="Thin-Blood: Day Drinker",
        dots=1,
        variable_cost=False,
        description="Resistência moderada à luz solar.",
        mechanical_effect="Sofre dano Superficial (não Agravado) do sol por algumas horas.",
        prerequisites="Thin-Blood only",
        source_book="core"
    ),

    # === CAMARILLA BOOK ===
    "domain_security": Merit(
        name="Domain Security",
        dots=1,
        variable_cost=True,
        description="Segurança adicional no seu Domain.",
        mechanical_effect="Cada ponto adiciona +1 dado para detectar intrusos no Domain.",
        prerequisites="Domain 1+",
        source_book="camarilla"
    ),
    "legacy": Merit(
        name="Legacy",
        dots=2,
        variable_cost=False,
        description="Descendente de linha vampírica notável.",
        mechanical_effect="+1 dado em Social com vampiros que valorizam linhagem.",
        source_book="camarilla"
    ),
}


def get_merit(merit_id: str) -> Optional[Merit]:
    """Get merit by ID"""
    return MERITS_V5.get(merit_id.lower().replace(" ", "_").replace("-", "_"))


def get_merits_by_source(source: str) -> dict[str, Merit]:
    """Get all merits from a specific source book"""
    return {k: v for k, v in MERITS_V5.items() if v.source_book == source}
