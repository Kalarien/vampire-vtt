from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class AdvantageType(str, Enum):
    BACKGROUND = "background"
    MERIT = "merit"


class Advantage(BaseModel):
    name: str
    type: AdvantageType
    max_dots: int
    description: str
    levels: dict[int, str]
    source_book: str


BACKGROUNDS_V5: dict[str, Advantage] = {
    "allies": Advantage(
        name="Allies",
        type=AdvantageType.BACKGROUND,
        max_dots=5,
        description="Mortais que ajudam você voluntariamente. Diferentes de Retainers, Allies têm suas próprias vidas e agendas.",
        levels={
            1: "Um aliado de influência ou habilidade menor (vizinho prestativo, policial de patrulha)",
            2: "Um aliado competente ou dois menores (detetive, pequeno empresário)",
            3: "Um aliado influente ou grupo pequeno (vereador, gangue pequena)",
            4: "Um aliado poderoso ou grupo competente (chefe de polícia, firma de advocacia)",
            5: "Um aliado extremamente poderoso ou organização (juiz federal, sindicato)"
        },
        source_book="core"
    ),

    "contacts": Advantage(
        name="Contacts",
        type=AdvantageType.BACKGROUND,
        max_dots=5,
        description="Pessoas que fornecem informações. Não são leais, mas úteis para coleta de inteligência.",
        levels={
            1: "Um informante em uma área (bartender, recepcionista)",
            2: "Informantes em algumas áreas ou um bem conectado",
            3: "Rede de informantes em várias áreas",
            4: "Informantes em muitas áreas, alguns em posições sensíveis",
            5: "Rede extensa, informantes em quase qualquer área"
        },
        source_book="core"
    ),

    "domain": Advantage(
        name="Domain",
        type=AdvantageType.BACKGROUND,
        max_dots=5,
        description="Território reconhecido como seu pela sociedade Kindred local. Inclui direitos de caça.",
        levels={
            1: "Quarteirão ou edifício pequeno",
            2: "Alguns quarteirões ou edifício grande",
            3: "Bairro pequeno ou complexo",
            4: "Bairro inteiro ou campus",
            5: "Múltiplos bairros ou distrito"
        },
        source_book="core"
    ),

    "fame": Advantage(
        name="Fame",
        type=AdvantageType.BACKGROUND,
        max_dots=5,
        description="Reconhecimento público entre mortais. Pode ajudar socialmente mas também atrai atenção.",
        levels={
            1: "Conhecido localmente (DJ local, blogueiro)",
            2: "Figura menor da cena (músico indie, influencer regional)",
            3: "Celebridade local (âncora de TV local, político municipal)",
            4: "Celebridade nacional (ator de TV, músico famoso)",
            5: "Estrela internacional (ator de Hollywood, rockstar)"
        },
        source_book="core"
    ),

    "haven": Advantage(
        name="Haven",
        type=AdvantageType.BACKGROUND,
        max_dots=5,
        description="Seu refúgio durante o dia. Segurança, conforto e localização.",
        levels={
            1: "Esconderijo precário (porão abandonado, cripta)",
            2: "Refúgio básico (apartamento simples, depósito)",
            3: "Refúgio confortável (apartamento bom, casa)",
            4: "Refúgio seguro e luxuoso (cobertura, mansão)",
            5: "Fortaleza (bunker, propriedade fortificada)"
        },
        source_book="core"
    ),

    "herd": Advantage(
        name="Herd",
        type=AdvantageType.BACKGROUND,
        max_dots=5,
        description="Grupo de mortais dos quais você se alimenta regularmente. Facilita a caça.",
        levels={
            1: "2-3 mortais (família pequena, casal)",
            2: "5-7 mortais (grupo de amigos, equipe pequena)",
            3: "10-15 mortais (culto pequeno, fã-clube)",
            4: "20-30 mortais (congregação, comunidade)",
            5: "50+ mortais (culto grande, comunidade extensa)"
        },
        source_book="core"
    ),

    "influence": Advantage(
        name="Influence",
        type=AdvantageType.BACKGROUND,
        max_dots=5,
        description="Poder sobre instituições mortais específicas (polícia, mídia, igreja, etc).",
        levels={
            1: "Influência menor (pode pedir pequenos favores)",
            2: "Influência moderada (pode atrasar processos, obter informações)",
            3: "Influência significativa (pode direcionar investigações, suprimir notícias)",
            4: "Influência forte (pode controlar departamentos, criar políticas)",
            5: "Influência dominante (controla a instituição na cidade)"
        },
        source_book="core"
    ),

    "mask": Advantage(
        name="Mask",
        type=AdvantageType.BACKGROUND,
        max_dots=5,
        description="Identidade falsa com documentação. Permite operar no mundo mortal.",
        levels={
            1: "Identidade básica (ID falso, história simples)",
            2: "Identidade estabelecida (histórico de crédito, endereço)",
            3: "Identidade sólida (emprego fictício, referências)",
            4: "Identidade profunda (anos de histórico, múltiplas referências)",
            5: "Identidade impecável (resiste a investigação federal)"
        },
        source_book="core"
    ),

    "mawla": Advantage(
        name="Mawla",
        type=AdvantageType.BACKGROUND,
        max_dots=5,
        description="Mentor ou patrono Kindred. Fornece conselho, proteção ou recursos.",
        levels={
            1: "Ancilla menor ou neonate experiente",
            2: "Ancilla estabelecido",
            3: "Ancilla influente ou Elder menor",
            4: "Elder respeitado",
            5: "Elder poderoso, Primogen ou equivalente"
        },
        source_book="core"
    ),

    "resources": Advantage(
        name="Resources",
        type=AdvantageType.BACKGROUND,
        max_dots=5,
        description="Riqueza material e renda. Dinheiro, propriedades, investimentos.",
        levels={
            1: "Pobre (R$ 2.000/mês, apartamento alugado)",
            2: "Classe média (R$ 8.000/mês, carro usado)",
            3: "Confortável (R$ 25.000/mês, casa própria, carro novo)",
            4: "Rico (R$ 100.000/mês, múltiplas propriedades)",
            5: "Milionário (R$ 500.000+/mês, mansões, iates)"
        },
        source_book="core"
    ),

    "retainers": Advantage(
        name="Retainers",
        type=AdvantageType.BACKGROUND,
        max_dots=5,
        description="Servos devotados - geralmente carniçais. Servem lealmente.",
        levels={
            1: "Um retainer não-carniçal ou carniçal fraco",
            2: "Um carniçal competente ou dois fracos",
            3: "Um carniçal habilidoso ou pequeno grupo",
            4: "Carniçal excepcional ou grupo competente",
            5: "Múltiplos carniçais habilidosos ou pequena força"
        },
        source_book="core"
    ),

    "status": Advantage(
        name="Status",
        type=AdvantageType.BACKGROUND,
        max_dots=5,
        description="Posição na sociedade Kindred. Pode ser em seita, clã ou cidade.",
        levels={
            1: "Conhecido (reconhecido pela corte)",
            2: "Respeitado (voz em assuntos menores)",
            3: "Influente (consultado em decisões)",
            4: "Poderoso (parte do círculo interno)",
            5: "Dominante (líder reconhecido)"
        },
        source_book="core"
    ),
}


def get_background(background_id: str) -> Optional[Advantage]:
    """Get background by ID"""
    return BACKGROUNDS_V5.get(background_id.lower())


def get_background_description(background_id: str, dots: int) -> Optional[str]:
    """Get description for a specific level of a background"""
    bg = get_background(background_id)
    if bg and dots in bg.levels:
        return bg.levels[dots]
    return None
