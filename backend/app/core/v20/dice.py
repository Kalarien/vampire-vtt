import random
from dataclasses import dataclass
from enum import Enum
from typing import List


class V20RollResult(Enum):
    BOTCH = "botch"
    FAILURE = "failure"
    SUCCESS = "success"
    EXCEPTIONAL = "exceptional"


@dataclass
class V20DiceRoll:
    dice: List[int]
    difficulty: int
    successes: int
    ones: int
    tens: int
    specialty_rerolls: List[int]
    result_type: V20RollResult


class V20DiceRoller:
    """
    V20 Dice Mechanics:
    - Pool of d10s
    - Roll >= difficulty = 1 success
    - 10s count as success and may reroll with specialty
    - 1s subtract from successes
    - 0 successes with any 1s = Botch
    - 5+ successes = Exceptional success
    """

    @staticmethod
    def roll(
        pool: int,
        difficulty: int = 6,
        specialty: bool = False,
        willpower: bool = False
    ) -> V20DiceRoll:
        """
        Roll a V20 dice pool.

        Args:
            pool: Number of dice to roll
            difficulty: Target number (usually 6)
            specialty: If character has relevant specialty (10s reroll)
            willpower: If spending Willpower for automatic success

        Returns:
            V20DiceRoll with all results
        """
        if pool <= 0:
            pool = 1

        difficulty = max(2, min(10, difficulty))  # Clamp difficulty 2-10

        # Roll initial dice
        dice = [random.randint(1, 10) for _ in range(pool)]

        # Count results
        ones = sum(1 for d in dice if d == 1)
        tens = sum(1 for d in dice if d == 10)
        successes = sum(1 for d in dice if d >= difficulty)

        # Specialty rerolls for 10s
        specialty_rerolls = []
        if specialty and tens > 0:
            specialty_rerolls = [random.randint(1, 10) for _ in range(tens)]
            for reroll in specialty_rerolls:
                if reroll >= difficulty:
                    successes += 1
                if reroll == 1:
                    ones += 1

        # Add Willpower automatic success
        if willpower:
            successes += 1

        # Subtract 1s from successes
        net_successes = successes - ones

        # Determine result type
        if net_successes <= 0:
            if ones > 0 and successes == 0:
                result_type = V20RollResult.BOTCH
                net_successes = 0
            else:
                result_type = V20RollResult.FAILURE
                net_successes = 0
        elif net_successes >= 5:
            result_type = V20RollResult.EXCEPTIONAL
        else:
            result_type = V20RollResult.SUCCESS

        return V20DiceRoll(
            dice=dice,
            difficulty=difficulty,
            successes=net_successes,
            ones=ones,
            tens=tens,
            specialty_rerolls=specialty_rerolls,
            result_type=result_type
        )

    @staticmethod
    def extended_roll(
        pool: int,
        difficulty: int,
        target_successes: int,
        max_rolls: int = 10,
        specialty: bool = False
    ) -> dict:
        """
        Extended roll - accumulate successes over multiple rolls.

        Args:
            pool: Dice pool
            difficulty: Target number
            target_successes: Total successes needed
            max_rolls: Maximum number of rolls allowed
            specialty: If specialty applies

        Returns:
            Dict with all rolls and final result
        """
        rolls = []
        total_successes = 0
        botched = False

        for i in range(max_rolls):
            roll = V20DiceRoller.roll(pool, difficulty, specialty)
            rolls.append(roll)

            if roll.result_type == V20RollResult.BOTCH:
                botched = True
                break

            total_successes += roll.successes

            if total_successes >= target_successes:
                break

        return {
            "rolls": rolls,
            "total_successes": total_successes,
            "target": target_successes,
            "success": total_successes >= target_successes and not botched,
            "botched": botched,
            "rolls_taken": len(rolls)
        }

    @staticmethod
    def resisted_roll(
        attacker_pool: int,
        defender_pool: int,
        difficulty: int = 6,
        attacker_specialty: bool = False,
        defender_specialty: bool = False
    ) -> dict:
        """
        Resisted roll between two characters.

        Returns:
            Dict with both rolls and result
        """
        attacker_roll = V20DiceRoller.roll(attacker_pool, difficulty, attacker_specialty)
        defender_roll = V20DiceRoller.roll(defender_pool, difficulty, defender_specialty)

        net_successes = attacker_roll.successes - defender_roll.successes

        if net_successes > 0:
            winner = "attacker"
        elif net_successes < 0:
            winner = "defender"
            net_successes = abs(net_successes)
        else:
            winner = "tie"
            net_successes = 0

        return {
            "attacker_roll": attacker_roll,
            "defender_roll": defender_roll,
            "winner": winner,
            "net_successes": net_successes
        }

    @staticmethod
    def damage_roll(
        damage_pool: int,
        difficulty: int = 6,
        is_aggravated: bool = False
    ) -> dict:
        """
        Damage roll.

        Args:
            damage_pool: Number of damage dice
            difficulty: Usually 6
            is_aggravated: If damage is aggravated

        Returns:
            Dict with damage information
        """
        roll = V20DiceRoller.roll(damage_pool, difficulty)

        return {
            "roll": roll,
            "damage_dealt": roll.successes,
            "damage_type": "aggravated" if is_aggravated else "lethal",
            "botched": roll.result_type == V20RollResult.BOTCH
        }

    @staticmethod
    def soak_roll(
        stamina: int,
        fortitude: int = 0,
        damage_type: str = "lethal"
    ) -> dict:
        """
        Soak roll to reduce damage.

        Args:
            stamina: Stamina attribute
            fortitude: Fortitude discipline level
            damage_type: "bashing", "lethal", or "aggravated"

        Returns:
            Dict with soak information
        """
        if damage_type == "bashing":
            pool = stamina
            difficulty = 6
        elif damage_type == "lethal":
            pool = fortitude  # Only Fortitude soaks lethal
            difficulty = 6
        else:  # aggravated
            pool = fortitude  # Only Fortitude soaks aggravated
            difficulty = 6

        if pool <= 0:
            return {
                "roll": None,
                "damage_soaked": 0,
                "can_soak": False
            }

        roll = V20DiceRoller.roll(pool, difficulty)

        return {
            "roll": roll,
            "damage_soaked": roll.successes,
            "can_soak": True
        }
