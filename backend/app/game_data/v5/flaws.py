from typing import Optional
from pydantic import BaseModel


class Flaw(BaseModel):
    name: str
    dots: int
    variable_cost: bool
    description: str
    mechanical_effect: str
    source_book: str


FLAWS_V5: dict[str, Flaw] = {
    # === PHYSICAL ===
    "ugly": Flaw(
        name="Ugly",
        dots=1,
        variable_cost=False,
        description="Você é notavelmente feio.",
        mechanical_effect="-1 dado em pools Sociais quando aparência importa (não Intimidation).",
        source_book="core"
    ),
    "repulsive": Flaw(
        name="Repulsive",
        dots=2,
        variable_cost=False,
        description="Grotescamente feio.",
        mechanical_effect="-2 dados em pools Sociais baseados em aparência.",
        source_book="core"
    ),
    "obvious_predator": Flaw(
        name="Obvious Predator",
        dots=2,
        variable_cost=False,
        description="Mortais instintivamente sentem perigo em você.",
        mechanical_effect="Animais fogem, mortais ficam desconfortáveis. -2 em pools Sociais com mortais desconhecidos.",
        source_book="core"
    ),

    # === FEEDING ===
    "feeding_restriction": Flaw(
        name="Feeding Restriction",
        dots=1,
        variable_cost=True,
        description="Só pode se alimentar sob certas condições.",
        mechanical_effect="1: Condição comum (dormindo, sedutor). 2: Condição incomum (apenas um gênero, apenas criminosos). 3: Condição rara (apenas voluntários, apenas inocentes).",
        source_book="core"
    ),
    "prey_exclusion": Flaw(
        name="Prey Exclusion",
        dots=1,
        variable_cost=False,
        description="Não pode se alimentar de certo tipo de mortal.",
        mechanical_effect="Se alimentar do tipo proibido causa Stains e náusea. Deve cuspir o sangue.",
        source_book="core"
    ),
    "organovore": Flaw(
        name="Organovore",
        dots=2,
        variable_cost=False,
        description="Deve consumir carne humana além de sangue.",
        mechanical_effect="Uma vez por semana deve consumir órgãos humanos ou ganhar Hunger adicional.",
        source_book="core"
    ),
    "farmer_flaw": Flaw(
        name="Farmer (Flaw)",
        dots=2,
        variable_cost=False,
        description="Só consegue se alimentar de animais.",
        mechanical_effect="Sangue humano causa vômito. Nunca pode reduzir Hunger abaixo de 1.",
        source_book="core"
    ),

    # === MENTAL ===
    "addiction": Flaw(
        name="Addiction",
        dots=1,
        variable_cost=True,
        description="Viciado em substância específica através do sangue.",
        mechanical_effect="1: Substância comum. 2: Substância ilegal. 3: Substância rara ou perigosa. Deve se alimentar de usuários ou sofrer penalidades.",
        source_book="core"
    ),
    "nightmare": Flaw(
        name="Nightmare",
        dots=1,
        variable_cost=False,
        description="Pesadelos horríveis durante o sono diurno.",
        mechanical_effect="Ao acordar, teste Willpower dif 3 ou comece com 1 Willpower Superficial damage.",
        source_book="core"
    ),
    "paranoia": Flaw(
        name="Paranoia",
        dots=2,
        variable_cost=False,
        description="Desconfia de todos obsessivamente.",
        mechanical_effect="-2 dados em pools Sociais envolvendo confiança. ST pode pedir testes para acreditar em aliados.",
        source_book="core"
    ),

    # === SOCIAL ===
    "dark_secret": Flaw(
        name="Dark Secret",
        dots=1,
        variable_cost=True,
        description="Você esconde algo que destruiria sua reputação.",
        mechanical_effect="1: Vergonhoso. 2: Grave (ex: diablerie passada). 3: Potencialmente fatal (traição à seita).",
        source_book="core"
    ),
    "enemy": Flaw(
        name="Enemy",
        dots=1,
        variable_cost=True,
        description="Alguém quer você destruído.",
        mechanical_effect="1: Neonate. 2: Ancilla. 3: Elder. 4: Facção. 5: Seita ou poder maior.",
        source_book="core"
    ),
    "shunned": Flaw(
        name="Shunned",
        dots=2,
        variable_cost=False,
        description="A sociedade Kindred local te evita.",
        mechanical_effect="Não recebe ajuda de outros Kindred. -2 em Status. Excluído de Elysium.",
        source_book="core"
    ),

    # === SUPERNATURAL ===
    "folkloric_bane": Flaw(
        name="Folkloric Bane",
        dots=1,
        variable_cost=True,
        description="Afetado por um bane folclórico tradicional.",
        mechanical_effect="1: Inconveniência (contar grãos de arroz). 2: Limitante (não pode entrar sem convite). 3: Perigoso (alho causa dano).",
        source_book="core"
    ),
    "stake_bait": Flaw(
        name="Stake Bait",
        dots=2,
        variable_cost=False,
        description="Coração anormalmente acessível.",
        mechanical_effect="Estacas precisam de apenas 3 sucessos ao invés de 5.",
        source_book="core"
    ),

    # === CLAN-SPECIFIC ===
    "known_blankbody": Flaw(
        name="Known Blankbody",
        dots=2,
        variable_cost=False,
        description="Segunda Inquisição tem seus dados.",
        mechanical_effect="Risco constante de caçadores. Não pode usar tecnologia sem precauções.",
        source_book="camarilla"
    ),
}


def get_flaw(flaw_id: str) -> Optional[Flaw]:
    """Get flaw by ID"""
    return FLAWS_V5.get(flaw_id.lower().replace(" ", "_").replace("-", "_"))


def get_flaws_by_source(source: str) -> dict[str, Flaw]:
    """Get all flaws from a specific source book"""
    return {k: v for k, v in FLAWS_V5.items() if v.source_book == source}
