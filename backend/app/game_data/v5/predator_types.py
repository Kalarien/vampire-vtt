from typing import List, Optional
from pydantic import BaseModel


class PredatorType(BaseModel):
    name: str
    description: str
    hunting_pool: str
    specialty_options: List[str]
    discipline_options: List[str]
    advantages: str
    disadvantages: str
    source_book: str


PREDATOR_TYPES_V5: dict[str, PredatorType] = {
    "alleycat": PredatorType(
        name="Gato de Rua",
        description="Você caça usando violência, emboscando vítimas em becos escuros e locais isolados. É rápido, brutal e eficiente.",
        hunting_pool="Strength + Brawl",
        specialty_options=["Intimidation (Stickups)", "Brawl (Grappling)"],
        discipline_options=["Celerity", "Potence"],
        advantages="Ganhe 3 pontos em Contacts (criminal) OU um Retainer (3) de gangue",
        disadvantages="Humanity -1 (começa com 6)",
        source_book="core"
    ),
    "bagger": PredatorType(
        name="Ensacador",
        description="Você evita caçar ativamente, obtendo sangue de bolsas hospitalares, bancos de sangue ou mercado negro.",
        hunting_pool="Intelligence + Streetwise",
        specialty_options=["Larceny (Lock-picking)", "Streetwise (Black Market)"],
        discipline_options=["Blood Sorcery", "Obfuscate"],
        advantages="Iron Gullet (Merit 3) gratuito; comece com 2 de Fome extra (sangue é velho)",
        disadvantages="Enemy (1): alguém de quem você roubou sangue",
        source_book="core"
    ),
    "blood_leech": PredatorType(
        name="Sanguessuga",
        description="Você se alimenta de outros vampiros - o maior tabu da sociedade Kindred. Seja por necessidade ou prazer.",
        hunting_pool="Wits + Stealth (para encontrar) ou combate (para tomar)",
        specialty_options=["Brawl (Kindred)", "Stealth (Against Kindred)"],
        discipline_options=["Celerity", "Protean"],
        advantages="Ganhe 1 ponto extra de Celerity ou Protean",
        disadvantages="Dark Secret (Diablerist ou Blood Leech, 2 pontos); Shunned (2)",
        source_book="core"
    ),
    "cleaver": PredatorType(
        name="Acougueiro",
        description="Você mantém vínculos mortais, alimentando-se de família, amigos ou colegas de trabalho. Perigoso para a Máscara.",
        hunting_pool="Manipulation + Subterfuge",
        specialty_options=["Persuasion (Gaslighting)", "Subterfuge (Cover-ups)"],
        discipline_options=["Animalism", "Dominate"],
        advantages="Herd (1) representando família/amigos",
        disadvantages="Dark Secret (1): Violação da Máscara esperando acontecer",
        source_book="core"
    ),
    "consensualist": PredatorType(
        name="Consensualista",
        description="Você só se alimenta de vítimas que consentem, seja através de fetiches, subculturas ou explicação da verdade.",
        hunting_pool="Manipulation + Persuasion",
        specialty_options=["Medicine (Phlebotomy)", "Persuasion (Victims)"],
        discipline_options=["Auspex", "Fortitude"],
        advantages="Humanity +1 (começa com 8)",
        disadvantages="Feeding Restriction (3): apenas vítimas voluntárias",
        source_book="core"
    ),
    "farmer": PredatorType(
        name="Fazendeiro",
        description="Você se alimenta apenas de animais, rejeitando a predação de humanos por escolha moral ou necessidade.",
        hunting_pool="Composure + Animal Ken",
        specialty_options=["Animal Ken (Specific Animal)", "Survival (Hunting)"],
        discipline_options=["Animalism", "Protean"],
        advantages="Humanity +1 (começa com 8)",
        disadvantages="Feeding Restriction (2): apenas animais; +1 Fome mínima por noite",
        source_book="core"
    ),
    "osiris": PredatorType(
        name="Osiris",
        description="Você é uma celebridade, influencer ou líder de culto. Seus seguidores oferecem sangue voluntariamente.",
        hunting_pool="Manipulation + Fame/Cult",
        specialty_options=["Occult (Specific Tradition)", "Performance (Specific Medium)"],
        discipline_options=["Blood Sorcery", "Presence"],
        advantages="Fame (1) e Herd (1): culto ou fandom",
        disadvantages="3 pontos em Enemies refletindo escrutínio público ou rivais",
        source_book="core"
    ),
    "sandman": PredatorType(
        name="Sonifero",
        description="Você invade lares à noite, alimentando-se de vítimas adormecidas que nunca sabem que foram predadas.",
        hunting_pool="Dexterity + Stealth",
        specialty_options=["Medicine (Anesthetics)", "Stealth (Break-in)"],
        discipline_options=["Auspex", "Obfuscate"],
        advantages="Resources (1) de pequenos furtos",
        disadvantages="Feeding Restriction (1): vítimas devem estar dormindo",
        source_book="core"
    ),
    "scene_queen": PredatorType(
        name="Rainha da Cena",
        description="Você domina uma cena social - clubes, bares, festas - e se alimenta dos frequentadores.",
        hunting_pool="Manipulation + Persuasion",
        specialty_options=["Etiquette (Specific Scene)", "Leadership (Scene)"],
        discipline_options=["Dominate", "Presence"],
        advantages="Fame (1), Contact (1), e um rival Disliked (1)",
        disadvantages="Influence Flaw (1): a cena espera favores",
        source_book="core"
    ),
    "siren": PredatorType(
        name="Sereia",
        description="Você seduz suas vítimas, alimentando-se durante o sexo ou intimidade. Clássico e eficaz.",
        hunting_pool="Charisma + Subterfuge",
        specialty_options=["Persuasion (Seduction)", "Subterfuge (Seduction)"],
        discipline_options=["Fortitude", "Presence"],
        advantages="Looks (2) - Beautiful",
        disadvantages="Enemy (1): amante rejeitado",
        source_book="core"
    ),

    # === CAMARILLA BOOK ===
    "extortionist": PredatorType(
        name="Extorsionario",
        description="Você força vítimas a alimentá-lo através de chantagem, coerção ou ameaças. Poder sobre sangue.",
        hunting_pool="Manipulation + Intimidation",
        specialty_options=["Intimidation (Extortion)", "Streetwise (Rumors)"],
        discipline_options=["Dominate", "Potence"],
        advantages="Resources (1) e Contact (1): vítima de chantagem",
        disadvantages="Enemy (2): vítima passada buscando vingança",
        source_book="camarilla"
    ),
    "graverobber": PredatorType(
        name="Ladrão de Tumulos",
        description="Você se alimenta dos recém-mortos ou moribundos - hospitais, necrotérios, cenas de acidentes.",
        hunting_pool="Resolve + Medicine",
        specialty_options=["Occult (Ghosts)", "Medicine (Cadavers)"],
        discipline_options=["Fortitude", "Oblivion"],
        advantages="Iron Gullet (Merit 3), Feeding Restriction (1): apenas mortos/moribundos",
        disadvantages="Obvious Predator (2) ou Stigma: outros vampiros acham repugnante",
        source_book="camarilla"
    ),

    # === ANARCH BOOK ===
    "roadside_killer": PredatorType(
        name="Assassino de Estrada",
        description="Você caça nas estradas, atacando viajantes solitários, caroneiros ou motoristas em paradas.",
        hunting_pool="Dexterity + Drive",
        specialty_options=["Survival (Highways)", "Drive (Pursuit)"],
        discipline_options=["Fortitude", "Protean"],
        advantages="Resources (1) dos pertences das vítimas",
        disadvantages="Obvious Predator (2): não consegue esconder sua natureza violenta",
        source_book="anarch"
    ),
}


def get_predator_type(predator_id: str) -> Optional[PredatorType]:
    """Get predator type by ID"""
    return PREDATOR_TYPES_V5.get(predator_id.lower().replace(" ", "_"))


def get_predator_types_by_source(source: str) -> dict[str, PredatorType]:
    """Get all predator types from a specific source book"""
    return {k: v for k, v in PREDATOR_TYPES_V5.items() if v.source_book == source}
