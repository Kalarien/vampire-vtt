from typing import Dict, List, Optional


MERITS_V20: Dict[str, Dict] = {
    # PHYSICAL
    "acute_senses": {"name": "Acute Senses", "type": "physical", "cost": 1, "description": "+2 em testes envolvendo o sentido escolhido."},
    "ambidextrous": {"name": "Ambidextrous", "type": "physical", "cost": 1, "description": "Sem penalidade por usar mão não-dominante."},
    "catlike_balance": {"name": "Catlike Balance", "type": "physical", "cost": 1, "description": "+2 em testes de equilíbrio."},
    "eat_food": {"name": "Eat Food", "type": "physical", "cost": 1, "description": "Pode comer e digerir comida normal."},
    "huge_size": {"name": "Huge Size", "type": "physical", "cost": 4, "description": "+1 Health level, +1 dado em Intimidation física."},
    "light_sleeper": {"name": "Light Sleeper", "type": "physical", "cost": 2, "description": "Acorda facilmente durante o dia."},

    # SOCIAL
    "natural_leader": {"name": "Natural Leader", "type": "social", "cost": 1, "description": "+2 em Leadership."},
    "pitiable": {"name": "Pitiable", "type": "social", "cost": 1, "description": "Outros querem protegê-lo."},
    "prestigious_sire": {"name": "Prestigious Sire", "type": "social", "cost": 1, "description": "Sire é conhecido e respeitado."},

    # MENTAL
    "common_sense": {"name": "Common Sense", "type": "mental", "cost": 1, "description": "ST avisa sobre ideias estúpidas."},
    "concentration": {"name": "Concentration", "type": "mental", "cost": 1, "description": "Ignora distrações em ações mentais."},
    "eidetic_memory": {"name": "Eidetic Memory", "type": "mental", "cost": 2, "description": "Lembra de tudo que viu/leu."},
    "iron_will": {"name": "Iron Will", "type": "mental", "cost": 3, "description": "+3 contra Dominate e poderes de controle."},
    "time_sense": {"name": "Time Sense", "type": "mental", "cost": 1, "description": "Sempre sabe a hora exata."},

    # SUPERNATURAL
    "medium": {"name": "Medium", "type": "supernatural", "cost": 2, "description": "Pode ver e falar com fantasmas."},
    "oracular_ability": {"name": "Oracular Ability", "type": "supernatural", "cost": 3, "description": "Recebe visões proféticas."},
    "spirit_mentor": {"name": "Spirit Mentor", "type": "supernatural", "cost": 3, "description": "Guiado por um espírito ancestral."},
    "true_faith": {"name": "True Faith", "type": "supernatural", "cost": 7, "description": "Pode repelir vampiros com fé."},
}


FLAWS_V20: Dict[str, Dict] = {
    # PHYSICAL
    "addiction": {"name": "Addiction", "type": "physical", "cost": 1, "description": "Viciado em substância no sangue."},
    "bad_sight": {"name": "Bad Sight", "type": "physical", "cost": 1, "description": "+2 dificuldade em testes de visão."},
    "disfigured": {"name": "Disfigured", "type": "physical", "cost": 2, "description": "Cicatrizes ou deformidades. +2 dificuldade social."},
    "lame": {"name": "Lame", "type": "physical", "cost": 3, "description": "Movimento reduzido, -2 em Dexterity."},
    "mute": {"name": "Mute", "type": "physical", "cost": 4, "description": "Não pode falar."},
    "one_arm": {"name": "One Arm", "type": "physical", "cost": 3, "description": "Penalidades em ações que requerem duas mãos."},

    # SOCIAL
    "enemy": {"name": "Enemy", "type": "social", "cost": 1, "description": "Inimigo mortal ou sobrenatural."},
    "hunted": {"name": "Hunted", "type": "social", "cost": 4, "description": "Caçado ativamente por inquisidores."},
    "infamous_sire": {"name": "Infamous Sire", "type": "social", "cost": 1, "description": "Sire é odiado ou desprezado."},
    "sire_bond": {"name": "Sire's Resentment", "type": "social", "cost": 1, "description": "Sire odeia você."},

    # MENTAL
    "amnesia": {"name": "Amnesia", "type": "mental", "cost": 2, "description": "Não lembra de seu passado mortal."},
    "compulsion": {"name": "Compulsion", "type": "mental", "cost": 1, "description": "Compulsão irracional."},
    "nightmares": {"name": "Nightmares", "type": "mental", "cost": 1, "description": "Pesadelos terríveis afetam descanso."},
    "phobia": {"name": "Phobia", "type": "mental", "cost": 2, "description": "Medo irracional de algo comum."},
    "short_fuse": {"name": "Short Fuse", "type": "mental", "cost": 2, "description": "+2 dificuldade para resistir frenzy."},
    "territorial": {"name": "Territorial", "type": "mental", "cost": 2, "description": "Extremamente protetor de seu território."},
    "vengeful": {"name": "Vengeful", "type": "mental", "cost": 2, "description": "Não descansa até vingar-se."},

    # SUPERNATURAL
    "beacon_of_the_unholy": {"name": "Beacon of the Unholy", "type": "supernatural", "cost": 2, "description": "True Faith detecta você facilmente."},
    "can_not_cross_running_water": {"name": "Can't Cross Running Water", "type": "supernatural", "cost": 3, "description": "Não pode atravessar água corrente."},
    "cast_no_reflection": {"name": "Cast No Reflection", "type": "supernatural", "cost": 1, "description": "Não tem reflexo."},
    "cursed": {"name": "Cursed", "type": "supernatural", "cost": 1, "description": "Amaldiçoado por forças sobrenaturais."},
    "eerie_presence": {"name": "Eerie Presence", "type": "supernatural", "cost": 2, "description": "Mortais sentem algo errado."},
    "magic_susceptibility": {"name": "Magic Susceptibility", "type": "supernatural", "cost": 2, "description": "+2 dificuldade para resistir magia."},
    "repelled_by_crosses": {"name": "Repelled by Crosses", "type": "supernatural", "cost": 3, "description": "Cruzes o repelem."},
    "touch_of_frost": {"name": "Touch of Frost", "type": "supernatural", "cost": 1, "description": "Toque sempre frio como gelo."},
}


def get_merit_v20(merit_id: str) -> Optional[Dict]:
    """Get V20 merit by ID"""
    return MERITS_V20.get(merit_id.lower().replace(" ", "_"))


def get_flaw_v20(flaw_id: str) -> Optional[Dict]:
    """Get V20 flaw by ID"""
    return FLAWS_V20.get(flaw_id.lower().replace(" ", "_"))


def get_merits_by_type(merit_type: str) -> Dict[str, Dict]:
    """Get all merits of a specific type"""
    return {k: v for k, v in MERITS_V20.items() if v["type"] == merit_type}


def get_flaws_by_type(flaw_type: str) -> Dict[str, Dict]:
    """Get all flaws of a specific type"""
    return {k: v for k, v in FLAWS_V20.items() if v["type"] == flaw_type}
