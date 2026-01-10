from dataclasses import dataclass
from enum import Enum
from typing import Optional
from .dice import V5DiceRoller, V5DiceRoll


class FrenzyType(Enum):
    FURY = "fury"  # Rage frenzy - attack source of anger
    HUNGER = "hunger"  # Hunger frenzy - feed on nearest
    TERROR = "terror"  # Fear frenzy - flee from source


@dataclass
class FrenzyCheckResult:
    success: bool
    roll: V5DiceRoll
    frenzy_type: Optional[FrenzyType]
    difficulty: int
    message: str


class FrenzyManager:
    """Handles Frenzy mechanics for V5"""

    # Base difficulties by trigger
    FRENZY_DIFFICULTIES = {
        "smell_of_blood": 2,
        "taste_of_blood": 3,
        "life_threatening_danger": 3,
        "humiliation": 3,
        "physical_provocation": 3,
        "loved_one_threatened": 4,
        "mortal_wound": 4,
        "fire_nearby": 3,
        "fire_touching": 4,
        "sunlight_exposure": 4,
        "hunger_5": 4,
    }

    @staticmethod
    def calculate_frenzy_pool(willpower: int, humanity: int) -> int:
        """
        Calculate the dice pool for resisting frenzy.

        Args:
            willpower: Current Willpower (undamaged boxes)
            humanity: Current Humanity score

        Returns:
            Dice pool size
        """
        return willpower + (humanity // 3)

    @staticmethod
    def get_frenzy_difficulty(
        trigger: str,
        hunger: int = 0,
        clan_brujah: bool = False
    ) -> int:
        """
        Get the difficulty for a frenzy check.

        Args:
            trigger: The triggering event
            hunger: Current Hunger level
            clan_brujah: If character is Brujah (easier to frenzy)

        Returns:
            Difficulty number
        """
        base_difficulty = FrenzyManager.FRENZY_DIFFICULTIES.get(trigger, 3)

        # Hunger increases difficulty
        if hunger >= 4:
            base_difficulty += 1
        if hunger >= 5:
            base_difficulty += 1

        # Brujah have harder time resisting rage frenzy
        if clan_brujah and trigger in ["humiliation", "physical_provocation", "loved_one_threatened"]:
            base_difficulty += 2

        return min(base_difficulty, 6)  # Cap at 6

    @staticmethod
    def determine_frenzy_type(trigger: str) -> FrenzyType:
        """Determine what type of frenzy is triggered"""
        terror_triggers = ["fire_nearby", "fire_touching", "sunlight_exposure", "life_threatening_danger"]
        hunger_triggers = ["smell_of_blood", "taste_of_blood", "hunger_5"]

        if trigger in terror_triggers:
            return FrenzyType.TERROR
        elif trigger in hunger_triggers:
            return FrenzyType.HUNGER
        else:
            return FrenzyType.FURY

    @staticmethod
    def resist_frenzy(
        willpower: int,
        humanity: int,
        trigger: str,
        hunger: int = 0,
        clan_brujah: bool = False,
        spend_willpower: bool = False
    ) -> FrenzyCheckResult:
        """
        Attempt to resist frenzy.

        Args:
            willpower: Current Willpower (undamaged boxes)
            humanity: Current Humanity score
            trigger: What triggered the frenzy
            hunger: Current Hunger level
            clan_brujah: If character is Brujah
            spend_willpower: If spending Willpower for reroll

        Returns:
            FrenzyCheckResult with outcome
        """
        pool = FrenzyManager.calculate_frenzy_pool(willpower, humanity)
        difficulty = FrenzyManager.get_frenzy_difficulty(trigger, hunger, clan_brujah)
        frenzy_type = FrenzyManager.determine_frenzy_type(trigger)

        # Make the roll
        roll = V5DiceRoller.roll(pool, hunger=0, difficulty=difficulty)

        if roll.margin >= 0:
            return FrenzyCheckResult(
                success=True,
                roll=roll,
                frenzy_type=None,
                difficulty=difficulty,
                message=f"Resisted {frenzy_type.value} frenzy! ({roll.successes} successes vs difficulty {difficulty})"
            )
        else:
            return FrenzyCheckResult(
                success=False,
                roll=roll,
                frenzy_type=frenzy_type,
                difficulty=difficulty,
                message=f"Failed to resist! Entering {frenzy_type.value} frenzy. ({roll.successes} successes vs difficulty {difficulty})"
            )

    @staticmethod
    def ride_the_wave(willpower: int, humanity: int) -> bool:
        """
        Attempt to 'Ride the Wave' - maintain some control during frenzy.
        Requires Willpower + Humanity/3 vs 4

        Returns:
            True if successful
        """
        pool = FrenzyManager.calculate_frenzy_pool(willpower, humanity)
        roll = V5DiceRoller.roll(pool, hunger=0, difficulty=4)
        return roll.margin >= 0
