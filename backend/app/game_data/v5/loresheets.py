from typing import List, Optional
from pydantic import BaseModel


class LoresheetLevel(BaseModel):
    level: int
    name: str
    description: str
    mechanical_effect: str


class Loresheet(BaseModel):
    name: str
    description: str
    source_book: str
    clan_restriction: Optional[List[str]] = None
    sect_restriction: Optional[List[str]] = None
    levels: List[LoresheetLevel]


LORESHEETS_V5: dict[str, Loresheet] = {
    # === CORE ===
    "descendant_of_helena": Loresheet(
        name="Descendant of Helena",
        description="Você descende de Helena, uma das Toreador mais antigas e belas. Sua linhagem traz tanto admiração quanto inveja.",
        source_book="core",
        clan_restriction=["toreador"],
        levels=[
            LoresheetLevel(
                level=1,
                name="Legacy of Beauty",
                description="Sua beleza é lendária, mesmo entre Toreador.",
                mechanical_effect="+1 dado em pools Sociais quando aparência importa."
            ),
            LoresheetLevel(
                level=2,
                name="Devotees",
                description="Mortais e neonatos são atraídos por você.",
                mechanical_effect="Ganhe Herd (1) e Status (Toreador, 1)."
            ),
            LoresheetLevel(
                level=3,
                name="Helen's Army",
                description="Outros descendentes de Helena vêm em seu auxílio.",
                mechanical_effect="Uma vez por história, convoque ajuda de descendentes de Helena."
            ),
            LoresheetLevel(
                level=4,
                name="Star-Crossed",
                description="Romances trágicos cercam você.",
                mechanical_effect="+2 dados em Presence; -2 para resistir manipulação emocional."
            ),
            LoresheetLevel(
                level=5,
                name="Helena's Grace",
                description="A própria Helena sabe de sua existência.",
                mechanical_effect="Linha direta com Helena. Uma vez por crônica, peça um favor maior."
            ),
        ]
    ),

    "high_clan": Loresheet(
        name="High Clan",
        description="Você pertence a uma linhagem reconhecida como 'High Clan' - superiores na hierarquia Kindred.",
        source_book="core",
        clan_restriction=["lasombra", "toreador", "tremere", "ventrue"],
        levels=[
            LoresheetLevel(
                level=1,
                name="Prestigious Lineage",
                description="Sua linhagem é respeitada.",
                mechanical_effect="+1 dado em Social com Kindred que valorizam linhagem."
            ),
            LoresheetLevel(
                level=2,
                name="Advantageous Connections",
                description="Você tem contatos em alta sociedade.",
                mechanical_effect="Ganhe Contacts (1) em círculos de elite."
            ),
            LoresheetLevel(
                level=3,
                name="Clan Support",
                description="Seu clã o apoia ativamente.",
                mechanical_effect="Uma vez por história, solicite recursos do clã."
            ),
            LoresheetLevel(
                level=4,
                name="Keeper of Secrets",
                description="Você conhece segredos de seu clã.",
                mechanical_effect="Ganhe acesso a conhecimento oculto do clã."
            ),
            LoresheetLevel(
                level=5,
                name="Elder Recognition",
                description="Anciões reconhecem seu potencial.",
                mechanical_effect="Ganhe Mawla (2): um ancião de seu clã."
            ),
        ]
    ),

    # === CAMARILLA ===
    "the_founders": Loresheet(
        name="The Founders",
        description="Você tem conexão com os fundadores da Camarilla original em 1493.",
        source_book="camarilla",
        sect_restriction=["camarilla"],
        levels=[
            LoresheetLevel(
                level=1,
                name="Convention of Thorns",
                description="Você conhece os detalhes da fundação da Camarilla.",
                mechanical_effect="Ganhe Lore (Camarilla) especializada. +1 dado em política Kindred."
            ),
            LoresheetLevel(
                level=2,
                name="Founder's Boon",
                description="Um ancião lhe deve um favor por serviços ancestrais.",
                mechanical_effect="Comece com uma Boon menor de um ancião de sua cidade."
            ),
            LoresheetLevel(
                level=3,
                name="Traditional Accounting",
                description="Você é reconhecido como tradicionalista respeitável.",
                mechanical_effect="Ganhe Status (Camarilla, 1). Anciões confiam mais em você."
            ),
            LoresheetLevel(
                level=4,
                name="Inner Circle Knowledge",
                description="Você sabe coisas sobre o Círculo Interno.",
                mechanical_effect="Uma vez por história, obtenha informação secreta sobre política Kindred global."
            ),
            LoresheetLevel(
                level=5,
                name="Founder's Blood",
                description="Você descende diretamente de um dos fundadores.",
                mechanical_effect="Ganhe Mawla (4): Justicar ou Arconte sênior como mentor/aliado."
            ),
        ]
    ),

    "second_inquisition_survivor": Loresheet(
        name="Second Inquisition Survivor",
        description="Você sobreviveu a um ataque da Segunda Inquisição - a caçada humana moderna contra vampiros.",
        source_book="camarilla",
        levels=[
            LoresheetLevel(
                level=1,
                name="Sole Survivor",
                description="Você escapou quando outros morreram.",
                mechanical_effect="Trauma específico da SI; +2 para resistir medo de mortais."
            ),
            LoresheetLevel(
                level=2,
                name="Known Face",
                description="A SI tem seu rosto em arquivo.",
                mechanical_effect="Known Blankbody (2) - risco; Streetwise (SI) specialty."
            ),
            LoresheetLevel(
                level=3,
                name="Stolen Intelligence",
                description="Você pegou informações antes de fugir.",
                mechanical_effect="Uma vez por história, saiba sobre operações SI na sua cidade."
            ),
            LoresheetLevel(
                level=4,
                name="Inside Man",
                description="Você tem um contato dentro da SI.",
                mechanical_effect="Contact (2): operativo SI que vaza informações."
            ),
            LoresheetLevel(
                level=5,
                name="Slayer of Inquisitors",
                description="Você destruiu uma célula inteira da SI.",
                mechanical_effect="Ganhe Status (2) entre Anarquistas ou Camarilla por seu feito."
            ),
        ]
    ),

    # === ANARCH ===
    "anarch_revolt": Loresheet(
        name="The Anarch Revolt",
        description="Sua linhagem participou da Revolta Anarquista original contra os anciões.",
        source_book="anarch",
        sect_restriction=["anarch"],
        levels=[
            LoresheetLevel(
                level=1,
                name="Child of the Revolt",
                description="Você foi abraçado na tradição revolucionária.",
                mechanical_effect="Ganhe Haven (1) em território Anarquista seguro."
            ),
            LoresheetLevel(
                level=2,
                name="Firebrand",
                description="Sua paixão revolucionária inspira outros.",
                mechanical_effect="+2 dados em Leadership ao motivar Anarquistas."
            ),
            LoresheetLevel(
                level=3,
                name="Diablerist's Legacy",
                description="Seu sire ou grandsire cometeu diablerie durante a Revolta.",
                mechanical_effect="Conhecimento de técnicas de diablerie; Dark Secret (1)."
            ),
            LoresheetLevel(
                level=4,
                name="Tyler's Get",
                description="Você descende de Tyler, líder lendário da Revolta.",
                mechanical_effect="Status (Anarch, 2). Anarquistas velhos respeitam sua linhagem."
            ),
            LoresheetLevel(
                level=5,
                name="Voice of Revolution",
                description="Você é considerado um herdeiro espiritual dos fundadores Anarquistas.",
                mechanical_effect="Ganhe Mawla (3): Barão ou líder Anarquista influente."
            ),
        ]
    ),

    "week_of_nightmares": Loresheet(
        name="Week of Nightmares",
        description="Você tem conexão com os eventos catastróficos da Semana dos Pesadelos, quando Ravnos foi destruído.",
        source_book="anarch",
        clan_restriction=["ravnos"],
        levels=[
            LoresheetLevel(
                level=1,
                name="Survivor's Guilt",
                description="Você sobreviveu quando seu clã quase foi extinto.",
                mechanical_effect="Trauma relacionado ao evento; -1 Humanity, +1 dado contra frenesi."
            ),
            LoresheetLevel(
                level=2,
                name="Nightmare Visions",
                description="Você tem visões do que aconteceu.",
                mechanical_effect="Premonições ocasionais sobre perigo. ST determina quando ocorrem."
            ),
            LoresheetLevel(
                level=3,
                name="Hidden Survivor",
                description="Outros Ravnos sobreviventes sabem de você.",
                mechanical_effect="Contato com rede secreta de Ravnos sobreviventes."
            ),
            LoresheetLevel(
                level=4,
                name="Touched by Antediluvian",
                description="Você sentiu a morte do Antediluviano.",
                mechanical_effect="+1 Blood Potency temporário em situações de perigo extremo."
            ),
            LoresheetLevel(
                level=5,
                name="Last of the Line",
                description="Você pode ser o último Ravnos verdadeiro.",
                mechanical_effect="Poder ou conhecimento único relacionado à queda de seu Antediluviano."
            ),
        ]
    ),

    # === CHICAGO BY NIGHT ===
    "descendant_of_lasombra": Loresheet(
        name="Descendant of Gratiano",
        description="Você descende de Gratiano, o Lasombra que alegadamente matou seu próprio Antediluviano.",
        source_book="chicago_by_night",
        clan_restriction=["lasombra"],
        levels=[
            LoresheetLevel(
                level=1,
                name="Whispers of Shadow",
                description="As sombras falam com você.",
                mechanical_effect="+1 dado em Oblivion. Sombras se movem estranhamente perto de você."
            ),
            LoresheetLevel(
                level=2,
                name="Sabbat Connections",
                description="Você ainda tem contatos no Sabbat.",
                mechanical_effect="Contacts (1) no Sabbat. Perigoso de usar."
            ),
            LoresheetLevel(
                level=3,
                name="Legacy of Diablerism",
                description="Sua linhagem é manchada por diablerie.",
                mechanical_effect="Conhecimento de diablerie; Dark Secret se descoberto."
            ),
            LoresheetLevel(
                level=4,
                name="Amici Noctis",
                description="Você é reconhecido pela facção política Lasombra.",
                mechanical_effect="Status (Lasombra, 2). Influência dentro do clã."
            ),
            LoresheetLevel(
                level=5,
                name="Eyes of the Abyss",
                description="Você tem visões do Abismo.",
                mechanical_effect="Poder especial relacionado ao Abismo e ao destino Lasombra."
            ),
        ]
    ),
}


def get_loresheet(loresheet_id: str) -> Optional[Loresheet]:
    """Get loresheet by ID"""
    return LORESHEETS_V5.get(loresheet_id.lower().replace(" ", "_"))


def get_loresheets_by_clan(clan: str) -> dict[str, Loresheet]:
    """Get all loresheets available for a specific clan"""
    return {
        k: v for k, v in LORESHEETS_V5.items()
        if v.clan_restriction is None or clan.lower() in [c.lower() for c in v.clan_restriction]
    }


def get_loresheets_by_sect(sect: str) -> dict[str, Loresheet]:
    """Get all loresheets available for a specific sect"""
    return {
        k: v for k, v in LORESHEETS_V5.items()
        if v.sect_restriction is None or sect.lower() in [s.lower() for s in v.sect_restriction]
    }
