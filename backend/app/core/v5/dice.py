import random
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class V5RollResult(Enum):
    BESTIAL_FAILURE = "bestial_failure"
    FAILURE = "failure"
    SUCCESS = "success"
    CRITICAL = "critical"
    MESSY_CRITICAL = "messy_critical"


@dataclass
class V5DiceRoll:
    regular_dice: List[int]
    hunger_dice: List[int]
    difficulty: int
    successes: int
    regular_tens: int
    hunger_tens: int
    hunger_ones: int
    critical_pairs: int
    result_type: V5RollResult
    margin: int


class V5DiceRoller:
    """
    V5 Dice Mechanics:
    - Pool of d10s, some replaced by Hunger Dice (red)
    - 6+ = 1 success
    - Pair of 10s = Critical (+2 extra successes)
    - If critical includes Hunger 10 = Messy Critical
    - Failure + Hunger 1 = Bestial Failure
    """

    @staticmethod
    def roll(pool: int, hunger: int = 0, difficulty: int = 1) -> V5DiceRoll:
        """
        Roll a V5 dice pool.

        Args:
            pool: Total number of dice to roll
            hunger: Number of dice that are Hunger Dice (max = pool)
            difficulty: Number of successes needed

        Returns:
            V5DiceRoll with all results
        """
        if pool <= 0:
            pool = 1

        hunger = min(hunger, pool)
        regular_count = pool - hunger

        # Roll the dice
        regular_dice = [random.randint(1, 10) for _ in range(regular_count)]
        hunger_dice = [random.randint(1, 10) for _ in range(hunger)]

        # Count basic successes (6+)
        regular_successes = sum(1 for d in regular_dice if d >= 6)
        hunger_successes = sum(1 for d in hunger_dice if d >= 6)
        base_successes = regular_successes + hunger_successes

        # Count special results
        regular_tens = sum(1 for d in regular_dice if d == 10)
        hunger_tens = sum(1 for d in hunger_dice if d == 10)
        total_tens = regular_tens + hunger_tens
        hunger_ones = sum(1 for d in hunger_dice if d == 1)

        # Calculate criticals (pairs of 10s give +2 extra successes each)
        critical_pairs = total_tens // 2
        total_successes = base_successes + (critical_pairs * 2)

        margin = total_successes - difficulty

        # Determine result type
        if margin >= 0:
            if critical_pairs > 0:
                if hunger_tens > 0:
                    result_type = V5RollResult.MESSY_CRITICAL
                else:
                    result_type = V5RollResult.CRITICAL
            else:
                result_type = V5RollResult.SUCCESS
        else:
            if hunger_ones > 0:
                result_type = V5RollResult.BESTIAL_FAILURE
            else:
                result_type = V5RollResult.FAILURE

        return V5DiceRoll(
            regular_dice=regular_dice,
            hunger_dice=hunger_dice,
            difficulty=difficulty,
            successes=total_successes,
            regular_tens=regular_tens,
            hunger_tens=hunger_tens,
            hunger_ones=hunger_ones,
            critical_pairs=critical_pairs,
            result_type=result_type,
            margin=margin
        )

    @staticmethod
    def rouse_check(reroll: bool = False) -> Tuple[bool, List[int]]:
        """
        Rouse Check: 1d10, 6+ = success (no Hunger gain)
        Blood Potency allows reroll on fail

        Args:
            reroll: Whether to reroll on failure (Blood Potency bonus)

        Returns:
            Tuple of (success, list of dice rolled)
        """
        dice = [random.randint(1, 10)]
        success = dice[0] >= 6

        if not success and reroll:
            reroll_die = random.randint(1, 10)
            dice.append(reroll_die)
            success = reroll_die >= 6

        return (success, dice)

    @staticmethod
    def frenzy_check(willpower: int, humanity: int, difficulty: int = 3) -> V5DiceRoll:
        """
        Frenzy Check: Willpower + Humanity/3 vs difficulty

        Args:
            willpower: Current Willpower (undamaged boxes)
            humanity: Current Humanity score
            difficulty: Difficulty of frenzy trigger (default 3)

        Returns:
            V5DiceRoll result (no hunger dice in frenzy checks)
        """
        pool = willpower + (humanity // 3)
        return V5DiceRoller.roll(pool, hunger=0, difficulty=max(1, difficulty))

    @staticmethod
    def remorse_check(humanity: int, stains: int) -> Tuple[bool, V5DiceRoll]:
        """
        Remorse Check: Roll Humanity - Stains (min 1)
        1+ success = keep Humanity, remove Stains
        0 successes = lose 1 Humanity, remove Stains

        Args:
            humanity: Current Humanity
            stains: Number of Stains accumulated

        Returns:
            Tuple of (success, V5DiceRoll)
        """
        pool = max(1, humanity - stains)
        roll = V5DiceRoller.roll(pool, hunger=0, difficulty=1)
        success = roll.successes >= 1
        return (success, roll)

    @staticmethod
    def willpower_roll(willpower: int, difficulty: int = 1) -> V5DiceRoll:
        """
        Simple Willpower roll (no hunger dice).

        Args:
            willpower: Willpower pool
            difficulty: Difficulty

        Returns:
            V5DiceRoll
        """
        return V5DiceRoller.roll(willpower, hunger=0, difficulty=difficulty)

    @staticmethod
    def contested_roll(
        attacker_pool: int,
        attacker_hunger: int,
        defender_pool: int,
        defender_hunger: int = 0
    ) -> dict:
        """
        Contested roll between two characters.

        Returns:
            Dict with attacker_roll, defender_roll, and winner
        """
        attacker_roll = V5DiceRoller.roll(attacker_pool, attacker_hunger, difficulty=0)
        defender_roll = V5DiceRoller.roll(defender_pool, defender_hunger, difficulty=0)

        if attacker_roll.successes > defender_roll.successes:
            winner = "attacker"
            margin = attacker_roll.successes - defender_roll.successes
        elif defender_roll.successes > attacker_roll.successes:
            winner = "defender"
            margin = defender_roll.successes - attacker_roll.successes
        else:
            winner = "tie"
            margin = 0

        return {
            "attacker_roll": attacker_roll,
            "defender_roll": defender_roll,
            "winner": winner,
            "margin": margin
        }
