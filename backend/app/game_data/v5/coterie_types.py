from typing import List, Optional
from pydantic import BaseModel


class CoterieType(BaseModel):
    name: str
    description: str
    chasse_pool: str
    typical_members: str
    advantages: List[str]
    flaws: List[str]
    shared_backgrounds: List[str]
    source_book: str


COTERIE_TYPES_V5: dict[str, CoterieType] = {
    "blood_cult": CoterieType(
        name="Blood Cult",
        description="O coterie é adorado como deuses por mortais em um culto organizado. Os membros são as divindades, profetas ou santos deste culto.",
        chasse_pool="Manipulation + Performance",
        typical_members="Ministry, Ventrue, Malkavian",
        advantages=[
            "Herd compartilhado (membros do culto)",
            "Domain em templo/local de culto",
            "Mortais fanaticamente leais"
        ],
        flaws=[
            "Atenção da polícia e mídia",
            "Risco de quebra de Máscara",
            "Conflitos religiosos"
        ],
        shared_backgrounds=["Herd", "Domain", "Retainers", "Haven"],
        source_book="core"
    ),

    "cerberus": CoterieType(
        name="Cerberus",
        description="Guardiões de um local importante - Elysium, haven de Elder, território estratégico. São os cães de guarda da Camarilla.",
        chasse_pool="Strength + Athletics",
        typical_members="Gangrel, Brujah, Nosferatu",
        advantages=[
            "Domain garantido no local protegido",
            "Status com quem vocês protegem",
            "Acesso a informações sensíveis"
        ],
        flaws=[
            "Responsabilidade constante",
            "Alvos de ataques",
            "Pouca liberdade de movimento"
        ],
        shared_backgrounds=["Domain", "Status", "Haven"],
        source_book="core"
    ),

    "champions": CoterieType(
        name="Champions",
        description="Defensores de uma causa ou facção. Podem ser revolucionários Anarquistas, tradicionalistas Camarilla, ou qualquer grupo ideológico.",
        chasse_pool="Charisma + Leadership",
        typical_members="Brujah, Ventrue, Toreador",
        advantages=[
            "Status na facção escolhida",
            "Aliados ideológicos",
            "Reconhecimento por suas ações"
        ],
        flaws=[
            "Inimigos da facção oposta",
            "Esperado que lutem por sua causa",
            "Rigidez ideológica"
        ],
        shared_backgrounds=["Status", "Allies", "Contacts"],
        source_book="core"
    ),

    "commando": CoterieType(
        name="Commando",
        description="Força de ataque. Resolvem problemas com violência cirúrgica. Podem ser assassinos, caçadores de Kindred, ou soldados.",
        chasse_pool="Dexterity + Stealth",
        typical_members="Banu Haqim, Gangrel, Brujah",
        advantages=[
            "Treinamento de combate conjunto",
            "Equipamento compartilhado",
            "Reputação temida"
        ],
        flaws=[
            "Esperado resolver tudo com força",
            "Alvos de retaliação",
            "Dificuldade diplomática"
        ],
        shared_backgrounds=["Retainers", "Resources", "Haven"],
        source_book="core"
    ),

    "day_watch": CoterieType(
        name="Day Watch",
        description="Especialistas em operações diurnas através de servos e carniçais. Olhos e mãos do coterie enquanto dormem.",
        chasse_pool="Intelligence + Awareness",
        typical_members="Tremere, Malkavian, Ventrue",
        advantages=[
            "Retainers competentes",
            "Operações 24 horas",
            "Informação diurna"
        ],
        flaws=[
            "Dependência de mortais",
            "Risco de traição",
            "Custos de manutenção"
        ],
        shared_backgrounds=["Retainers", "Allies", "Resources"],
        source_book="core"
    ),

    "fang_gang": CoterieType(
        name="Fang Gang",
        description="Gangue vampírica que controla território como criminosos mortais. Tráfico, extorsão, violência de rua.",
        chasse_pool="Strength + Intimidation",
        typical_members="Brujah, Gangrel, Nosferatu",
        advantages=[
            "Domain em território de gangue",
            "Resources de atividades criminais",
            "Herd entre a população local"
        ],
        flaws=[
            "Conflitos com outras gangues",
            "Atenção policial",
            "Violência constante"
        ],
        shared_backgrounds=["Domain", "Resources", "Herd", "Contacts"],
        source_book="core"
    ),

    "hunting_party": CoterieType(
        name="Hunting Party",
        description="Caçadores sociais que fazem da alimentação um evento. Frequentam os mesmos locais, compartilham presas, caçam juntos.",
        chasse_pool="Manipulation + Persuasion",
        typical_members="Toreador, Ventrue, Ministry",
        advantages=[
            "Herd compartilhado",
            "Locais de caça estabelecidos",
            "Segurança na caçada"
        ],
        flaws=[
            "Dependência mútua para alimentação",
            "Competição por presas de qualidade",
            "Padrões previsíveis"
        ],
        shared_backgrounds=["Herd", "Domain", "Haven"],
        source_book="core"
    ),

    "marechal": CoterieType(
        name="Marechal",
        description="Executores da lei Kindred. Caçam violadores da Máscara, investigam crimes vampíricos, aplicam a Tradição.",
        chasse_pool="Wits + Investigation",
        typical_members="Nosferatu, Banu Haqim, Ventrue",
        advantages=[
            "Status como autoridade",
            "Acesso a informações de crimes",
            "Proteção legal Kindred"
        ],
        flaws=[
            "Dever antes de tudo",
            "Conflitos de interesse",
            "Pressão de Elders"
        ],
        shared_backgrounds=["Status", "Contacts", "Influence"],
        source_book="core"
    ),

    "nomads": CoterieType(
        name="Nomads",
        description="Viajantes sem lar fixo. Movem-se de cidade em cidade, nunca ficando tempo suficiente para criar raízes.",
        chasse_pool="Wits + Survival",
        typical_members="Gangrel, Ravnos, Ministry",
        advantages=[
            "Contatos em múltiplas cidades",
            "Difíceis de rastrear",
            "Conhecimento diversificado"
        ],
        flaws=[
            "Sem Domain permanente",
            "Sem Status local",
            "Sempre estrangeiros"
        ],
        shared_backgrounds=["Contacts", "Allies", "Resources"],
        source_book="core"
    ),

    "plumaires": CoterieType(
        name="Plumaires",
        description="Artistas e patronos da arte Kindred. Salões, galerias, performances - a beleza é seu domínio.",
        chasse_pool="Charisma + Performance",
        typical_members="Toreador, Malkavian, Ventrue",
        advantages=[
            "Fame entre mortais e Kindred",
            "Haven em local artístico",
            "Acesso à elite cultural"
        ],
        flaws=[
            "Rivalidades artísticas",
            "Escrutínio público",
            "Expectativas de patronagem"
        ],
        shared_backgrounds=["Fame", "Haven", "Resources", "Status"],
        source_book="core"
    ),

    "questari": CoterieType(
        name="Questari",
        description="Buscadores de conhecimento oculto. Arqueólogos do sobrenatural, investigadores de mistérios vampíricos.",
        chasse_pool="Intelligence + Occult",
        typical_members="Tremere, Malkavian, Hecata",
        advantages=[
            "Conhecimento oculto",
            "Acesso a bibliotecas e relíquias",
            "Reputação acadêmica"
        ],
        flaws=[
            "Obsessão com mistérios",
            "Inimigos sobrenaturais",
            "Perigos da busca"
        ],
        shared_backgrounds=["Resources", "Contacts", "Haven"],
        source_book="core"
    ),

    "regency": CoterieType(
        name="Regency",
        description="Governantes de um território específico. Seja um bairro, instituição, ou comunidade - vocês mandam.",
        chasse_pool="Composure + Politics",
        typical_members="Ventrue, Lasombra, Toreador",
        advantages=[
            "Domain extenso",
            "Influência sobre mortais",
            "Status como governantes"
        ],
        flaws=[
            "Responsabilidade pelo território",
            "Ameaças constantes",
            "Política Kindred intensa"
        ],
        shared_backgrounds=["Domain", "Influence", "Status", "Herd"],
        source_book="core"
    ),

    "sbirri": CoterieType(
        name="Sbirri",
        description="Servos de um Elder ou Primogen. Fazem o trabalho sujo, protegem interesses, executam ordens.",
        chasse_pool="Manipulation + Subterfuge",
        typical_members="Qualquer clã",
        advantages=[
            "Proteção do patrono",
            "Resources fornecidos",
            "Acesso a poder"
        ],
        flaws=[
            "Lealdade absoluta exigida",
            "Trabalho sujo constante",
            "Inimigos do patrono são seus"
        ],
        shared_backgrounds=["Mawla", "Resources", "Status"],
        source_book="core"
    ),

    "vehme": CoterieType(
        name="Vehme",
        description="Sociedade secreta dentro da sociedade. Conspiradores com agenda oculta, trabalhando nas sombras.",
        chasse_pool="Wits + Stealth",
        typical_members="Nosferatu, Lasombra, Malkavian",
        advantages=[
            "Segredos valiosos",
            "Rede de informantes",
            "Agenda oculta protegida"
        ],
        flaws=[
            "Paranoia constante",
            "Segredos perigosos",
            "Traição sempre possível"
        ],
        shared_backgrounds=["Contacts", "Haven", "Mask"],
        source_book="core"
    ),

    "watchmen": CoterieType(
        name="Watchmen",
        description="Vigilantes noturnos. Protegem os mortais - de outros Kindred, de si mesmos, de ameaças sobrenaturais.",
        chasse_pool="Resolve + Awareness",
        typical_members="Brujah, Gangrel, Salubri",
        advantages=[
            "Herd entre protegidos",
            "Domain em área de proteção",
            "Humanidade mais fácil de manter"
        ],
        flaws=[
            "Conflito com outros Kindred",
            "Responsabilidade pelos mortais",
            "Podem ser vistos como fracos"
        ],
        shared_backgrounds=["Domain", "Herd", "Haven"],
        source_book="core"
    ),
}


# Coterie Flaws
COTERIE_FLAWS: dict[str, dict] = {
    "compromised": {
        "name": "Compromised",
        "dots": 2,
        "description": "Alguém tem informação comprometedora sobre o coterie.",
        "effect": "Uma vez por história, o ST pode usar esse segredo contra o grupo."
    },
    "indebted": {
        "name": "Indebted",
        "dots": 1,
        "description": "O coterie deve uma Boon coletiva.",
        "effect": "Deve ser paga ou gera complicações. 1 = menor, 2 = moderada, 3 = maior."
    },
    "territorial_weakness": {
        "name": "Territorial Weakness",
        "dots": 1,
        "description": "Domain do coterie tem problema sério.",
        "effect": "Pode ser: perigoso (gangues), pobre (poucos mortais), vigiado (SI), ou exposto."
    },
    "obvious": {
        "name": "Obvious",
        "dots": 1,
        "description": "O coterie é conhecido demais.",
        "effect": "Inimigos sabem onde encontrá-los. -1 em pools para agir secretamente."
    },
}


def get_coterie_type(coterie_id: str) -> Optional[CoterieType]:
    """Get coterie type by ID"""
    return COTERIE_TYPES_V5.get(coterie_id.lower().replace(" ", "_"))


def get_coterie_flaw(flaw_id: str) -> Optional[dict]:
    """Get coterie flaw by ID"""
    return COTERIE_FLAWS.get(flaw_id.lower().replace(" ", "_"))
