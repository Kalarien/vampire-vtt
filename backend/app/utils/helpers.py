import uuid
import random
from typing import List, Tuple
from datetime import datetime


def generate_uuid() -> str:
    """Generate a new UUID string"""
    return str(uuid.uuid4())


def roll_d10() -> int:
    """Roll a single d10"""
    return random.randint(1, 10)


def roll_dice(count: int) -> List[int]:
    """Roll multiple d10s"""
    return [roll_d10() for _ in range(count)]


def format_datetime(dt: datetime) -> str:
    """Format datetime for display"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_date(dt: datetime) -> str:
    """Format date for display"""
    return dt.strftime("%Y-%m-%d")


def calculate_blood_pool_max(generation: int) -> int:
    """Calculate maximum blood pool based on generation (V20)"""
    blood_pool_table = {
        3: 100,
        4: 50,
        5: 40,
        6: 30,
        7: 20,
        8: 15,
        9: 14,
        10: 13,
        11: 12,
        12: 11,
        13: 10,
        14: 10,
        15: 10,
    }
    return blood_pool_table.get(generation, 10)


def calculate_blood_per_turn(generation: int) -> int:
    """Calculate blood points usable per turn based on generation (V20)"""
    blood_per_turn_table = {
        3: 20,
        4: 10,
        5: 8,
        6: 6,
        7: 5,
        8: 4,
        9: 3,
        10: 2,
        11: 1,
        12: 1,
        13: 1,
        14: 1,
        15: 1,
    }
    return blood_per_turn_table.get(generation, 1)


def count_v5_successes(dice: List[int]) -> Tuple[int, bool, int]:
    """
    Count successes for V5 dice roll.
    Returns: (successes, has_critical_pair, tens_count)
    """
    successes = sum(1 for d in dice if d >= 6)
    tens = sum(1 for d in dice if d == 10)

    # Critical pairs (each pair of 10s = +2 successes instead of +2)
    critical_pairs = tens // 2
    bonus_successes = critical_pairs * 2  # Each pair adds 2 extra (4 total per pair instead of 2)

    total_successes = successes + bonus_successes
    has_critical = critical_pairs > 0

    return total_successes, has_critical, tens


def count_v20_successes(dice: List[int], difficulty: int) -> Tuple[int, bool]:
    """
    Count successes for V20 dice roll.
    Returns: (net_successes, is_botch)
    """
    successes = sum(1 for d in dice if d >= difficulty)
    ones = sum(1 for d in dice if d == 1)

    net_successes = successes - ones

    # Botch: no successes and at least one 1
    is_botch = successes == 0 and ones > 0

    return max(0, net_successes), is_botch


def get_health_levels_v20() -> List[str]:
    """Get V20 health level names in order"""
    return [
        "bruised",
        "hurt",
        "injured",
        "wounded",
        "mauled",
        "crippled",
        "incapacitated",
    ]


def get_willpower_max_v5(composure: int, resolve: int) -> int:
    """Calculate V5 willpower max from attributes"""
    return composure + resolve


def get_health_max_v5(stamina: int) -> int:
    """Calculate V5 health max from stamina"""
    return stamina + 3


def validate_game_version(version: str) -> bool:
    """Validate game version string"""
    return version in ("v5", "v20")
