from typing import List, Optional
from pydantic import BaseModel


class DisciplinePowerV20(BaseModel):
    name: str
    level: int
    description: str
    system: str


class DisciplineV20(BaseModel):
    name: str
    description: str
    powers: List[DisciplinePowerV20]


DISCIPLINES_V20: dict[str, DisciplineV20] = {
    "animalism": DisciplineV20(
        name="Animalism",
        description="Comunhão sobrenatural com a Besta e os animais.",
        powers=[
            DisciplinePowerV20(name="Feral Whispers", level=1, description="Comunica-se com animais.", system="Manipulation + Animal Ken, dif 6."),
            DisciplinePowerV20(name="Beckoning", level=2, description="Convoca animais da área.", system="Charisma + Survival, dif 6."),
            DisciplinePowerV20(name="Quell the Beast", level=3, description="Acalma a Besta em vampiros ou aterroriza mortais.", system="Manipulation + Intimidation, dif 7."),
            DisciplinePowerV20(name="Subsume the Spirit", level=4, description="Possui o corpo de um animal.", system="Manipulation + Animal Ken, dif 8."),
            DisciplinePowerV20(name="Drawing Out the Beast", level=5, description="Transfere a Besta para outro.", system="Manipulation + Self-Control, dif 8."),
        ]
    ),
    "auspex": DisciplineV20(
        name="Auspex",
        description="Percepção sobrenatural e poderes psíquicos.",
        powers=[
            DisciplinePowerV20(name="Heightened Senses", level=1, description="Sentidos sobre-humanos.", system="Percepção aumentada, pode causar sobrecarga."),
            DisciplinePowerV20(name="Aura Perception", level=2, description="Vê auras emocionais.", system="Perception + Empathy, dif 8."),
            DisciplinePowerV20(name="The Spirit's Touch", level=3, description="Lê impressões psíquicas de objetos.", system="Perception + Empathy, dif varia."),
            DisciplinePowerV20(name="Telepathy", level=4, description="Lê e projeta pensamentos.", system="Intelligence + Subterfuge, dif Willpower."),
            DisciplinePowerV20(name="Psychic Projection", level=5, description="Projeção astral.", system="Perception + Occult, dif varia."),
        ]
    ),
    "celerity": DisciplineV20(
        name="Celerity",
        description="Velocidade e reflexos sobre-humanos.",
        powers=[
            DisciplinePowerV20(name="Celerity 1-5", level=1, description="Cada ponto adiciona uma ação extra por turno.", system="Gaste 1 blood point por turno para ativar."),
        ]
    ),
    "chimerstry": DisciplineV20(
        name="Chimerstry",
        description="Criação de ilusões. Exclusiva dos Ravnos.",
        powers=[
            DisciplinePowerV20(name="Ignis Fatuus", level=1, description="Cria ilusão estática de um sentido.", system="Perception + Alertness, dif 6."),
            DisciplinePowerV20(name="Fata Morgana", level=2, description="Cria ilusão estática multi-sensorial.", system="Intelligence + Subterfuge, dif 6."),
            DisciplinePowerV20(name="Apparition", level=3, description="Ilusões podem se mover.", system="Intelligence + Subterfuge, dif 7."),
            DisciplinePowerV20(name="Permanency", level=4, description="Torna ilusões permanentes.", system="Gasta Willpower."),
            DisciplinePowerV20(name="Horrid Reality", level=5, description="Ilusões podem causar dano real.", system="Manipulation + Subterfuge, dif Perception + Self-Control."),
        ]
    ),
    "dementation": DisciplineV20(
        name="Dementation",
        description="Transmissão e manipulação de loucura. Exclusiva dos Malkavians.",
        powers=[
            DisciplinePowerV20(name="Passion", level=1, description="Intensifica emoções do alvo.", system="Charisma + Empathy, dif Humanity."),
            DisciplinePowerV20(name="The Haunting", level=2, description="Causa alucinações sutis.", system="Manipulation + Subterfuge, dif Perception + Self-Control."),
            DisciplinePowerV20(name="Eyes of Chaos", level=3, description="Vê padrões ocultos e verdades.", system="Perception + Occult, dif varia."),
            DisciplinePowerV20(name="Voice of Madness", level=4, description="Causa frenesi ou Rotschreck.", system="Manipulation + Empathy, dif Willpower."),
            DisciplinePowerV20(name="Total Insanity", level=5, description="Causa loucura permanente.", system="Manipulation + Intimidation, dif Willpower."),
        ]
    ),
    "dominate": DisciplineV20(
        name="Dominate",
        description="Controle mental através do olhar.",
        powers=[
            DisciplinePowerV20(name="Command", level=1, description="Dá uma ordem de uma palavra.", system="Manipulation + Intimidation, dif Willpower."),
            DisciplinePowerV20(name="Mesmerize", level=2, description="Implanta comandos complexos.", system="Manipulation + Leadership, dif Willpower."),
            DisciplinePowerV20(name="The Forgetful Mind", level=3, description="Apaga e altera memórias.", system="Wits + Subterfuge, dif Willpower."),
            DisciplinePowerV20(name="Conditioning", level=4, description="Torna alvo suscetível a comandos.", system="Charisma + Leadership, vários testes."),
            DisciplinePowerV20(name="Possession", level=5, description="Toma controle total do corpo.", system="Charisma + Intimidation, dif 7."),
        ]
    ),
    "fortitude": DisciplineV20(
        name="Fortitude",
        description="Resistência sobrenatural a dano.",
        powers=[
            DisciplinePowerV20(name="Fortitude 1-5", level=1, description="Cada ponto adiciona dado de absorção contra todos os danos.", system="Pode absorver dano agravado."),
        ]
    ),
    "necromancy": DisciplineV20(
        name="Necromancy",
        description="Magia de morte e comunicação com mortos.",
        powers=[
            DisciplinePowerV20(name="Insight", level=1, description="Vê fantasmas e detecta morte.", system="Perception + Occult, dif 5."),
            DisciplinePowerV20(name="Summon Soul", level=2, description="Convoca espírito de morto.", system="Perception + Occult, dif Willpower do fantasma."),
            DisciplinePowerV20(name="Compel Soul", level=3, description="Comanda espíritos convocados.", system="Manipulation + Occult, dif Willpower."),
            DisciplinePowerV20(name="Haunting", level=4, description="Liga fantasma a local ou objeto.", system="Manipulation + Occult, dif 7."),
            DisciplinePowerV20(name="Torment", level=5, description="Causa dano a espíritos.", system="Stamina + Empathy, dif Willpower."),
        ]
    ),
    "obfuscate": DisciplineV20(
        name="Obfuscate",
        description="Ocultação e invisibilidade.",
        powers=[
            DisciplinePowerV20(name="Cloak of Shadows", level=1, description="Invisível se imóvel em sombras.", system="Sem teste se imóvel."),
            DisciplinePowerV20(name="Unseen Presence", level=2, description="Invisível mesmo em movimento.", system="Wits + Stealth para ações chamativas."),
            DisciplinePowerV20(name="Mask of a Thousand Faces", level=3, description="Altera aparência percebida.", system="Manipulation + Acting, dif 7."),
            DisciplinePowerV20(name="Vanish from Mind's Eye", level=4, description="Desaparece mesmo sendo observado.", system="Charisma + Stealth, dif Willpower."),
            DisciplinePowerV20(name="Cloak the Gathering", level=5, description="Estende Obfuscate a outros.", system="Afeta até Stealth + 1 pessoas."),
        ]
    ),
    "obtenebration": DisciplineV20(
        name="Obtenebration",
        description="Controle de sombras. Exclusiva dos Lasombra.",
        powers=[
            DisciplinePowerV20(name="Shadow Play", level=1, description="Manipula sombras.", system="Wits + Occult, dif 7."),
            DisciplinePowerV20(name="Shroud of Night", level=2, description="Cria escuridão sobrenatural.", system="Manipulation + Occult, dif 7."),
            DisciplinePowerV20(name="Arms of the Abyss", level=3, description="Cria tentáculos de sombra.", system="Manipulation + Occult, dif 7."),
            DisciplinePowerV20(name="Black Metamorphosis", level=4, description="Transforma-se em criatura de sombras.", system="Manipulation + Courage, dif 7."),
            DisciplinePowerV20(name="Tenebrous Form", level=5, description="Torna-se sombra intangível.", system="Nenhum teste."),
        ]
    ),
    "potence": DisciplineV20(
        name="Potence",
        description="Força sobrenatural.",
        powers=[
            DisciplinePowerV20(name="Potence 1-5", level=1, description="Cada ponto adiciona dado de dano e sucesso automático em Strength.", system="Sempre ativo."),
        ]
    ),
    "presence": DisciplineV20(
        name="Presence",
        description="Controle emocional e carisma sobrenatural.",
        powers=[
            DisciplinePowerV20(name="Awe", level=1, description="Atrai atenção positiva.", system="Charisma + Acting, dif 7."),
            DisciplinePowerV20(name="Dread Gaze", level=2, description="Causa terror paralisante.", system="Charisma + Intimidation, dif Courage + 4."),
            DisciplinePowerV20(name="Entrancement", level=3, description="Cria devoção temporária.", system="Appearance + Empathy, dif Willpower."),
            DisciplinePowerV20(name="Summon", level=4, description="Convoca alguém irresistivelmente.", system="Charisma + Subterfuge, dif 5."),
            DisciplinePowerV20(name="Majesty", level=5, description="Inspira reverência absoluta.", system="Charisma + Intimidation, dif Courage + 4."),
        ]
    ),
    "protean": DisciplineV20(
        name="Protean",
        description="Transformação física. Tradicionalmente Gangrel.",
        powers=[
            DisciplinePowerV20(name="Eyes of the Beast", level=1, description="Vê perfeitamente no escuro.", system="Sem teste."),
            DisciplinePowerV20(name="Feral Claws", level=2, description="Garras que causam dano agravado.", system="1 blood point."),
            DisciplinePowerV20(name="Earth Meld", level=3, description="Funde-se com a terra.", system="Sem teste."),
            DisciplinePowerV20(name="Shape of the Beast", level=4, description="Transforma-se em lobo ou morcego.", system="1 blood point."),
            DisciplinePowerV20(name="Mist Form", level=5, description="Transforma-se em névoa.", system="1 blood point."),
        ]
    ),
    "quietus": DisciplineV20(
        name="Quietus",
        description="Assassinato silencioso. Exclusiva dos Assamitas.",
        powers=[
            DisciplinePowerV20(name="Silence of Death", level=1, description="Cria zona de silêncio.", system="Sem teste."),
            DisciplinePowerV20(name="Scorpion's Touch", level=2, description="Transforma sangue em veneno.", system="Willpower, dif 6."),
            DisciplinePowerV20(name="Dagon's Call", level=3, description="Causa hemorragia interna.", system="Stamina + Medicine, dif 6."),
            DisciplinePowerV20(name="Baal's Caress", level=4, description="Sangue causa dano agravado.", system="Willpower + Occult, dif 6."),
            DisciplinePowerV20(name="Taste of Death", level=5, description="Cospe sangue corrosivo.", system="Dexterity + Athletics para acertar."),
        ]
    ),
    "serpentis": DisciplineV20(
        name="Serpentis",
        description="Poderes de serpente. Exclusiva dos Setitas.",
        powers=[
            DisciplinePowerV20(name="Eyes of the Serpent", level=1, description="Olhar paralisante.", system="Willpower, dif 9."),
            DisciplinePowerV20(name="Tongue of the Asp", level=2, description="Língua bifurcada venenosa.", system="1 blood point."),
            DisciplinePowerV20(name="Skin of the Adder", level=3, description="Pele escamosa, pode se espremer.", system="1 blood point."),
            DisciplinePowerV20(name="Form of the Cobra", level=4, description="Transforma-se em cobra.", system="1 blood point."),
            DisciplinePowerV20(name="Heart of Darkness", level=5, description="Remove coração para proteção.", system="Ritual de uma noite."),
        ]
    ),
    "thaumaturgy": DisciplineV20(
        name="Thaumaturgy",
        description="Magia de sangue dos Tremere.",
        powers=[
            DisciplinePowerV20(name="Path of Blood (A Taste for Blood)", level=1, description="Determina geração de vitae.", system="Perception + Occult, dif 7."),
            DisciplinePowerV20(name="Path of Blood (Blood Rage)", level=2, description="Força vampiro a gastar sangue.", system="Dexterity + Occult, dif Willpower."),
            DisciplinePowerV20(name="Path of Blood (Blood of Potency)", level=3, description="Aumenta geração temporariamente.", system="Stamina + Occult, dif 8."),
            DisciplinePowerV20(name="Path of Blood (Theft of Vitae)", level=4, description="Rouba sangue à distância.", system="Intelligence + Occult, dif Willpower."),
            DisciplinePowerV20(name="Path of Blood (Cauldron of Blood)", level=5, description="Ferve sangue no alvo.", system="Willpower, dif Humanity."),
        ]
    ),
    "vicissitude": DisciplineV20(
        name="Vicissitude",
        description="Modelagem de carne e osso. Exclusiva dos Tzimisce.",
        powers=[
            DisciplinePowerV20(name="Malleable Visage", level=1, description="Altera própria aparência.", system="Dexterity + Body Crafts, dif 6."),
            DisciplinePowerV20(name="Fleshcraft", level=2, description="Modela carne alheia.", system="Dexterity + Body Crafts, dif 5."),
            DisciplinePowerV20(name="Bonecraft", level=3, description="Modela ossos.", system="Strength + Body Crafts, dif 6."),
            DisciplinePowerV20(name="Horrid Form", level=4, description="Transforma em monstro de guerra.", system="Stamina + Survival, dif 6."),
            DisciplinePowerV20(name="Bloodform", level=5, description="Transforma em poça de sangue.", system="1+ blood points."),
        ]
    ),
}


def get_discipline_v20(discipline_id: str) -> Optional[DisciplineV20]:
    """Get V20 discipline by ID"""
    return DISCIPLINES_V20.get(discipline_id.lower().replace(" ", "_"))
