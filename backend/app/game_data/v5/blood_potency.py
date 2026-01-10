from pydantic import BaseModel
from typing import Optional


class BloodPotencyLevel(BaseModel):
    level: int
    blood_surge: int
    mend_amount: int
    power_bonus: int
    rouse_reroll: int
    bane_severity: int
    feeding_penalty: str


BLOOD_POTENCY_TABLE: dict[int, BloodPotencyLevel] = {
    0: BloodPotencyLevel(
        level=0,
        blood_surge=1,
        mend_amount=1,
        power_bonus=0,
        rouse_reroll=0,
        bane_severity=0,
        feeding_penalty="Sem penalidade. Sangue animal sustenta."
    ),
    1: BloodPotencyLevel(
        level=1,
        blood_surge=2,
        mend_amount=1,
        power_bonus=0,
        rouse_reroll=0,
        bane_severity=2,
        feeding_penalty="Sem penalidade. Sangue animal sustenta."
    ),
    2: BloodPotencyLevel(
        level=2,
        blood_surge=2,
        mend_amount=2,
        power_bonus=1,
        rouse_reroll=0,
        bane_severity=2,
        feeding_penalty="Sangue animal não sustenta mais."
    ),
    3: BloodPotencyLevel(
        level=3,
        blood_surge=3,
        mend_amount=2,
        power_bonus=1,
        rouse_reroll=1,
        bane_severity=3,
        feeding_penalty="Sangue animal não sustenta. Bolsas de sangue reduzem apenas 1 Hunger."
    ),
    4: BloodPotencyLevel(
        level=4,
        blood_surge=3,
        mend_amount=3,
        power_bonus=2,
        rouse_reroll=1,
        bane_severity=3,
        feeding_penalty="Sangue animal e bolsas não sustentam. Deve drenar ou matar para reduzir Hunger abaixo de 2."
    ),
    5: BloodPotencyLevel(
        level=5,
        blood_surge=4,
        mend_amount=3,
        power_bonus=2,
        rouse_reroll=2,
        bane_severity=4,
        feeding_penalty="Deve drenar ou matar para reduzir Hunger. Mortais comuns não sustentam abaixo de Hunger 2."
    ),
    6: BloodPotencyLevel(
        level=6,
        blood_surge=4,
        mend_amount=4,
        power_bonus=3,
        rouse_reroll=2,
        bane_severity=4,
        feeding_penalty="Deve drenar e matar para se alimentar. Apenas sangue de qualidade excepcional satisfaz."
    ),
    7: BloodPotencyLevel(
        level=7,
        blood_surge=5,
        mend_amount=4,
        power_bonus=3,
        rouse_reroll=3,
        bane_severity=5,
        feeding_penalty="Deve matar para se alimentar. Apenas Kindred, lobisomens ou sangue sobrenatural satisfaz."
    ),
    8: BloodPotencyLevel(
        level=8,
        blood_surge=5,
        mend_amount=5,
        power_bonus=4,
        rouse_reroll=3,
        bane_severity=5,
        feeding_penalty="Apenas sangue sobrenatural satisfaz. Kindred preferido."
    ),
    9: BloodPotencyLevel(
        level=9,
        blood_surge=6,
        mend_amount=5,
        power_bonus=4,
        rouse_reroll=4,
        bane_severity=6,
        feeding_penalty="Apenas sangue Kindred satisfaz."
    ),
    10: BloodPotencyLevel(
        level=10,
        blood_surge=6,
        mend_amount=6,
        power_bonus=5,
        rouse_reroll=5,
        bane_severity=6,
        feeding_penalty="Apenas sangue de Kindred potente (BP 2+) satisfaz."
    ),
}


# Geração -> Blood Potency inicial
GENERATION_TO_BLOOD_POTENCY = {
    16: 0,  # Thin-Blood
    15: 0,  # Thin-Blood
    14: 0,  # Thin-Blood / Fledgling
    13: 1,  # Fledgling
    12: 1,  # Neonate
    11: 2,  # Neonate
    10: 2,  # Ancillae
    9: 3,   # Ancillae
    8: 4,   # Elder
    7: 5,   # Elder
    6: 6,   # Methuselah
    5: 7,   # Methuselah
    4: 8,   # Antediluvian
    3: 9,   # Antediluvian
    2: 10,  # Caine's Childer
}


# Blood Potency máxima por geração
GENERATION_MAX_BLOOD_POTENCY = {
    16: 0,
    15: 0,
    14: 1,
    13: 2,
    12: 3,
    11: 4,
    10: 5,
    9: 6,
    8: 7,
    7: 8,
    6: 9,
    5: 10,
    4: 10,
    3: 10,
    2: 10,
}


def get_blood_potency_info(level: int) -> BloodPotencyLevel:
    """Retorna informações do Blood Potency."""
    return BLOOD_POTENCY_TABLE.get(level, BLOOD_POTENCY_TABLE[0])


def get_starting_blood_potency(generation: int) -> int:
    """Retorna o Blood Potency inicial baseado na geração."""
    return GENERATION_TO_BLOOD_POTENCY.get(generation, 1)


def get_max_blood_potency(generation: int) -> int:
    """Retorna o Blood Potency máximo baseado na geração."""
    return GENERATION_MAX_BLOOD_POTENCY.get(generation, 5)


def calculate_blood_surge_pool(base_pool: int, blood_potency: int) -> int:
    """Calcula pool com Blood Surge ativo."""
    bp_info = get_blood_potency_info(blood_potency)
    return base_pool + bp_info.blood_surge


def can_feed_on_animals(blood_potency: int) -> bool:
    """Verifica se o vampiro pode se alimentar de animais."""
    return blood_potency <= 1


def can_use_blood_bags(blood_potency: int) -> bool:
    """Verifica se o vampiro pode usar bolsas de sangue efetivamente."""
    return blood_potency <= 2
