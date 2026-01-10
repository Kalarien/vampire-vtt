from typing import List, Optional
from pydantic import BaseModel


class ClanV20(BaseModel):
    name: str
    nickname: str
    disciplines: List[str]
    weakness: str
    description: str
    organization: str


CLANS_V20: dict[str, ClanV20] = {
    "assamite": ClanV20(
        name="Assamite",
        nickname="Assassins",
        disciplines=["Celerity", "Obfuscate", "Quietus"],
        weakness="Vício em vitae Kindred. Teste Self-Control (dif 4 + BP consumido) ou viciado.",
        description="Assassinos silenciosos e diablerists, ligados por um código antigo.",
        organization="Alamut, o Ninho da Águia, é sua fortaleza."
    ),
    "brujah": ClanV20(
        name="Brujah",
        nickname="Rabble",
        disciplines=["Celerity", "Potence", "Presence"],
        weakness="Dificuldade para resistir ao Frenesi é 2 maior que o normal.",
        description="Rebeldes apaixonados e guerreiros-estudiosos.",
        organization="Organização frouxa, unidos por ideais."
    ),
    "followers_of_set": ClanV20(
        name="Followers of Set",
        nickname="Setites",
        disciplines=["Obfuscate", "Presence", "Serpentis"],
        weakness="Sensibilidade extrema à luz. +2 dano de luz solar, -1 dado em luz forte.",
        description="Corruptores e tentadores servindo o deus Set.",
        organization="Templos dedicados à adoração de Set."
    ),
    "gangrel": ClanV20(
        name="Gangrel",
        nickname="Outlanders",
        disciplines=["Animalism", "Fortitude", "Protean"],
        weakness="Cada frenesi causa uma característica animal permanente.",
        description="Nômades bestiais conectados à natureza selvagem.",
        organization="Independentes, raramente se reúnem."
    ),
    "giovanni": ClanV20(
        name="Giovanni",
        nickname="Necromancers",
        disciplines=["Dominate", "Necromancy", "Potence"],
        weakness="Mordida causa dano agravado extra, não pode selar feridas com lambida.",
        description="Família incestuosa de necromantes e empresários.",
        organization="Estrutura familiar rígida, La Famiglia."
    ),
    "lasombra": ClanV20(
        name="Lasombra",
        nickname="Keepers",
        disciplines=["Dominate", "Obtenebration", "Potence"],
        weakness="Sem reflexo. Não pode ser fotografado ou gravado.",
        description="Mestres das sombras e líderes do Sabbat.",
        organization="Núcleo da liderança Sabbat."
    ),
    "malkavian": ClanV20(
        name="Malkavian",
        nickname="Lunatics",
        disciplines=["Auspex", "Dementation", "Obfuscate"],
        weakness="Todos os Malkavians têm um derangement permanente.",
        description="Videntes amaldiçoados com insight e loucura.",
        organization="A Rede da Loucura os conecta."
    ),
    "nosferatu": ClanV20(
        name="Nosferatu",
        nickname="Sewer Rats",
        disciplines=["Animalism", "Obfuscate", "Potence"],
        weakness="Aparência 0. Não pode aumentar. Quebra a Máscara ao ser visto.",
        description="Corretores de informação amaldiçoados com aparência horrenda.",
        organization="Warrens sob cidades, comunidades unidas."
    ),
    "ravnos": ClanV20(
        name="Ravnos",
        nickname="Deceivers",
        disciplines=["Animalism", "Chimerstry", "Fortitude"],
        weakness="Vício em um pecado específico. Deve indulgir ou ganhar derangement.",
        description="Ilusionistas e viajantes com inclinação criminosa.",
        organization="Famílias e bandos nômades."
    ),
    "toreador": ClanV20(
        name="Toreador",
        nickname="Degenerates",
        disciplines=["Auspex", "Celerity", "Presence"],
        weakness="Entrancement. Pode ficar perdido contemplando beleza.",
        description="Artistas e sensualistas obcecados com beleza.",
        organization="Salões, galerias, círculos artísticos."
    ),
    "tremere": ClanV20(
        name="Tremere",
        nickname="Warlocks",
        disciplines=["Auspex", "Dominate", "Thaumaturgy"],
        weakness="Começa um passo Blood Bound ao clã. Anciões controlam através do sangue.",
        description="Feiticeiros de sangue organizados em pirâmide rígida.",
        organization="Estrutura piramidal rígida de Viena."
    ),
    "tzimisce": ClanV20(
        name="Tzimisce",
        nickname="Fiends",
        disciplines=["Animalism", "Auspex", "Vicissitude"],
        weakness="Deve descansar com 2+ punhados de terra natal ou perde dados.",
        description="Modeladores de carne e antigos senhores da Europa Oriental.",
        organization="Voivodas ancestrais, espinha dorsal do Sabbat."
    ),
    "ventrue": ClanV20(
        name="Ventrue",
        nickname="Blue Bloods",
        disciplines=["Dominate", "Fortitude", "Presence"],
        weakness="Só pode se alimentar de tipo específico de vítima.",
        description="Aristocratas e líderes naturais da Camarilla.",
        organization="Liderança central da Camarilla."
    ),

    # === BLOODLINES ===
    "baali": ClanV20(
        name="Baali",
        nickname="Demons",
        disciplines=["Daimoinon", "Obfuscate", "Presence"],
        weakness="Fé verdadeira causa dano extra. Símbolos sagrados repelem.",
        description="Adoradores de demônios e forças sombrias primordiais.",
        organization="Cultos secretos, covens dispersos."
    ),
    "daughters_of_cacophony": ClanV20(
        name="Daughters of Cacophony",
        nickname="Sirens",
        disciplines=["Fortitude", "Melpominee", "Presence"],
        weakness="Ouvem música constantemente. Dificuldade em se concentrar.",
        description="Cantoras sobrenaturais com vozes mágicas.",
        organization="Corais e performances artísticas."
    ),
    "samedi": ClanV20(
        name="Samedi",
        nickname="Zombies",
        disciplines=["Fortitude", "Necromancy", "Thanatosis"],
        weakness="Aparência de cadáver em decomposição. Cheiro de morte.",
        description="Necromantes com aparência de mortos-vivos.",
        organization="Conexões com o Hecata/Giovanni."
    ),
}


def get_clan_v20(clan_id: str) -> Optional[ClanV20]:
    """Get V20 clan by ID"""
    return CLANS_V20.get(clan_id.lower().replace(" ", "_"))


def get_clans_by_sect(sect: str) -> dict[str, ClanV20]:
    """Get all clans typically associated with a sect"""
    camarilla = ["brujah", "gangrel", "malkavian", "nosferatu", "toreador", "tremere", "ventrue"]
    sabbat = ["lasombra", "tzimisce"]
    independent = ["assamite", "followers_of_set", "giovanni", "ravnos"]

    if sect.lower() == "camarilla":
        return {k: v for k, v in CLANS_V20.items() if k in camarilla}
    elif sect.lower() == "sabbat":
        return {k: v for k, v in CLANS_V20.items() if k in sabbat}
    elif sect.lower() == "independent":
        return {k: v for k, v in CLANS_V20.items() if k in independent}
    return {}
