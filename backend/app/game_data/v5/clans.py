from typing import List, Optional
from pydantic import BaseModel


class ClanV5(BaseModel):
    name: str
    nickname: str
    description: str
    disciplines: List[str]
    bane: str
    compulsion: str
    source_book: str


CLANS_V5: dict[str, ClanV5] = {
    # === CORE RULEBOOK ===
    "brujah": ClanV5(
        name="Brujah",
        nickname="Rabble",
        description="Rebeldes apaixonados e idealistas violentos. Outrora filósofos-reis, agora são ativistas, anarquistas e guerreiros. Sua paixão é tanto sua força quanto sua maldição.",
        disciplines=["Celerity", "Potence", "Presence"],
        bane="Os Brujah são propensos ao frenesi. Subtraia 2 da dificuldade para resistir ao frenesi provocado por raiva.",
        compulsion="Rebelião - O Brujah deve se opor a qualquer coisa que perceba como opressão, não importa o custo.",
        source_book="core"
    ),
    "gangrel": ClanV5(
        name="Gangrel",
        nickname="Ferals",
        description="Vampiros bestiais conectados à natureza selvagem. Nômades e solitários, os Gangrel são os mais próximos de suas Bestas - e os mais confortáveis com ela.",
        disciplines=["Animalism", "Fortitude", "Protean"],
        bane="Em frenesi, ganham características animais. Cada frenesi adiciona ou piora uma característica até a próxima lua cheia.",
        compulsion="Impulsos Ferais - Devem agir por instinto: fugir, atacar ou congelar. Não podem usar habilidades sociais complexas.",
        source_book="core"
    ),
    "malkavian": ClanV5(
        name="Malkavian",
        nickname="Lunatics",
        description="Profetas insanos tocados por uma maldição de loucura. Cada Malkavian sofre de pelo menos uma condição mental, mas muitos acreditam que sua loucura os conecta a verdades ocultas.",
        disciplines=["Auspex", "Dominate", "Obfuscate"],
        bane="Aflito com pelo menos um tipo de transtorno mental que não pode ser curado.",
        compulsion="Delírio - A realidade se torna distorcida por sua loucura. Sofrem penalidades em testes de percepção e podem agir de forma errática.",
        source_book="core"
    ),
    "nosferatu": ClanV5(
        name="Nosferatu",
        nickname="Sewer Rats",
        description="Horrendamente deformados, os Nosferatu são mestres da informação que vivem nas sombras. Sua aparência monstruosa os força a se esconder, mas isso os tornou observadores incomparáveis.",
        disciplines=["Animalism", "Obfuscate", "Potence"],
        bane="Aparência horrenda. Automaticamente falham em qualquer teste Social que envolva aparência. Quebram a Máscara simplesmente sendo vistos.",
        compulsion="Criptofilia - Obcecados em aprender segredos. Devem buscar informações ocultas mesmo quando arriscado.",
        source_book="core"
    ),
    "toreador": ClanV5(
        name="Toreador",
        nickname="Degenerates",
        description="Artistas e hedonistas obcecados com beleza. Os Toreador são os vampiros mais próximos da humanidade, cultivando arte, moda e cultura - mas também podem ser superficiais e cruéis.",
        disciplines=["Auspex", "Celerity", "Presence"],
        bane="Podem ficar fascinados por beleza, incapazes de agir enquanto contemplam algo esteticamente agradável.",
        compulsion="Obsessão - Fixam-se em algo belo ou interessante, ignorando tudo mais ao redor.",
        source_book="core"
    ),
    "tremere": ClanV5(
        name="Tremere",
        nickname="Warlocks",
        description="Feiticeiros de sangue, estudiosos do oculto. Os Tremere eram uma casa hermética de magos que se tornaram vampiros através de rituais proibidos. Sua estrutura piramidal foi destruída pela Segunda Inquisição.",
        disciplines=["Auspex", "Blood Sorcery", "Dominate"],
        bane="Não podem criar Laços de Sangue em outros, apenas recebê-los. Têm dificuldade em criar carniçais.",
        compulsion="Perfeccionismo - Devem completar a tarefa atual com perfeição antes de fazer qualquer outra coisa.",
        source_book="core"
    ),
    "ventrue": ClanV5(
        name="Ventrue",
        nickname="Blue Bloods",
        description="Aristocratas e líderes natos, os Ventrue consideram-se os governantes naturais da sociedade vampírica. Sua ambição é igualada apenas por seu senso de dever e tradição.",
        disciplines=["Dominate", "Fortitude", "Presence"],
        bane="Só podem se alimentar de um tipo específico de mortal (determinado na criação).",
        compulsion="Arrogância - Devem dominar e liderar em qualquer situação. Não podem aceitar ordens ou parecer fracos.",
        source_book="core"
    ),
    "caitiff": ClanV5(
        name="Caitiff",
        nickname="Trash",
        description="Vampiros sem clã, desprezados pela sociedade Kindred. Seja por sangue diluído ou mistério do Abraço, os Caitiff não pertencem a nenhuma linhagem reconhecida.",
        disciplines=[],
        bane="Sem bane específico, mas XP custa mais para aumentar Disciplinas.",
        compulsion="Nenhuma compulsão de clã.",
        source_book="core"
    ),
    "thin_blood": ClanV5(
        name="Thin-Blood",
        nickname="Duskborn",
        description="Vampiros de 14ª ou 15ª geração, tão distantes de Caim que mal são vampiros. Podem andar ao sol brevemente, comer comida, mas também são fracos e desprezados.",
        disciplines=["Thin-Blood Alchemy"],
        bane="Múltiplas limitações: não podem criar carniçais, Laços de Sangue fracos, etc.",
        compulsion="Nenhuma.",
        source_book="core"
    ),

    # === CAMARILLA BOOK ===
    "banu_haqim": ClanV5(
        name="Banu Haqim",
        nickname="Assassins / Judges",
        description="Juízes e assassinos, guardiões de uma lei antiga. Recentemente aceitos na Camarilla após séculos de conflito, os Banu Haqim buscam julgar os indignos - especialmente outros vampiros.",
        disciplines=["Blood Sorcery", "Celerity", "Obfuscate"],
        bane="Viciados em sangue vampírico. Ao provar vitae de outro Kindred, devem resistir ou tentar beber mais.",
        compulsion="Julgamento - Devem punir aqueles que violam seu código pessoal de honra.",
        source_book="camarilla"
    ),

    # === ANARCH BOOK ===
    "ministry": ClanV5(
        name="The Ministry",
        nickname="Setites / Serpents",
        description="Tentadores e corruptores, os antigos Seguidores de Set agora se chamam Ministério. Acreditam que a libertação vem através da indulgência e da quebra de tabus.",
        disciplines=["Obfuscate", "Presence", "Protean"],
        bane="Queimados por luz forte. Sofrem dano agravado de luz solar e penalidades em iluminação intensa.",
        compulsion="Transgressão - Devem tentar outros a quebrar seus próprios princípios ou tabus.",
        source_book="anarch"
    ),

    # === CHICAGO BY NIGHT / OUTROS ===
    "lasombra": ClanV5(
        name="Lasombra",
        nickname="Keepers / Magisters",
        description="Mestres das sombras, antigos pilares do Sabbat. Muitos Lasombra recentemente desertaram para a Camarilla, trazendo seu domínio sobre a escuridão e sua ambição implacável.",
        disciplines=["Dominate", "Oblivion", "Potence"],
        bane="Sem reflexo. Tecnologia frequentemente falha em sua presença (câmeras, microfones, etc).",
        compulsion="Crueldade - Devem provar superioridade através de qualquer meio, humilhando ou prejudicando outros.",
        source_book="chicago_by_night"
    ),
    "hecata": ClanV5(
        name="Hecata",
        nickname="The Family",
        description="A união dos clãs da morte: Giovanni, Cappadocianos, Samedi, e outros. Necromantes e negociantes, os Hecata tratam com os mortos como outros tratam com dinheiro.",
        disciplines=["Auspex", "Fortitude", "Oblivion"],
        bane="Mordida dolorosa. Vítimas sofrem dano extra e não sentem prazer, apenas dor.",
        compulsion="Morbidez - Obcecados com morte e os mortos. Devem interagir com cadáveres, fantasmas ou moribundos.",
        source_book="cults_of_the_blood_gods"
    ),

    # === PLAYERS GUIDE / COMPANION ===
    "ravnos": ClanV5(
        name="Ravnos",
        nickname="Daredevils",
        description="Viajantes e ilusionistas, amaldiçoados pela inquietude após a destruição de seu Antediluviano. Os poucos Ravnos que restam são incapazes de permanecer em um lugar por muito tempo.",
        disciplines=["Animalism", "Obfuscate", "Presence"],
        bane="Não podem dormir no mesmo lugar duas vezes seguidas. Dano solar persiste por mais tempo.",
        compulsion="Tentando o Destino - Devem assumir riscos desnecessários, apostando tudo em chances mínimas.",
        source_book="core_v5_companion"
    ),
    "salubri": ClanV5(
        name="Salubri",
        nickname="Soul Thieves / Cyclops",
        description="Curandeiros perseguidos quase até a extinção pelos Tremere. Os Salubri possuem um terceiro olho místico e poderes de cura, mas seu sangue é viciante para outros vampiros.",
        disciplines=["Auspex", "Dominate", "Fortitude"],
        bane="Terceiro olho se abre ao usar Disciplinas. Seu sangue é viciante - quem prova quer mais.",
        compulsion="Empatia Afetiva - Sobrecarregados pelo sofrimento alheio. Devem ajudar os que sofrem.",
        source_book="core_v5_companion"
    ),
    "tzimisce": ClanV5(
        name="Tzimisce",
        nickname="Dragons / Fiends",
        description="Metamorfos territoriais, mestres da carne e osso. Os Tzimisce são antigos senhores da Europa Oriental que valorizam território e transformação acima de tudo.",
        disciplines=["Animalism", "Dominate", "Protean"],
        bane="Devem dormir cercados por terra de sua terra natal ou de um território significativo.",
        compulsion="Cobiça - Devem possuir o que desejam. Não podem descansar enquanto algo cobiçado pertence a outro.",
        source_book="core_v5_companion"
    ),
}


def get_clan(clan_id: str) -> Optional[ClanV5]:
    """Get clan by ID"""
    return CLANS_V5.get(clan_id.lower())


def get_clans_by_source(source: str) -> dict[str, ClanV5]:
    """Get all clans from a specific source book"""
    return {k: v for k, v in CLANS_V5.items() if v.source_book == source}


def get_clans_with_discipline(discipline: str) -> dict[str, ClanV5]:
    """Get all clans that have a specific discipline"""
    return {k: v for k, v in CLANS_V5.items() if discipline in v.disciplines}
