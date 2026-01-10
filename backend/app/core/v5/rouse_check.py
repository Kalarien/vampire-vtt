from dataclasses import dataclass
from typing import List, Optional
from .dice import V5DiceRoller


@dataclass
class RouseCheckResult:
    success: bool
    dice: List[int]
    hunger_increase: int
    rerolled: bool
    message: str


class RouseChecker:
    """Handles Rouse Check mechanics"""

    @staticmethod
    def perform_rouse_check(
        blood_potency: int = 1,
        current_hunger: int = 0
    ) -> RouseCheckResult:
        """
        Perform a Rouse Check.

        Args:
            blood_potency: Vampire's Blood Potency (determines reroll ability)
            current_hunger: Current Hunger level

        Returns:
            RouseCheckResult with all details
        """
        # Blood Potency determines number of allowed rerolls
        from ..v5 import BLOOD_POTENCY_TABLE
        bp_info = BLOOD_POTENCY_TABLE.get(blood_potency)
        can_reroll = bp_info.rouse_reroll > 0 if bp_info else False

        success, dice = V5DiceRoller.rouse_check(reroll=can_reroll)
        rerolled = len(dice) > 1

        if success:
            return RouseCheckResult(
                success=True,
                dice=dice,
                hunger_increase=0,
                rerolled=rerolled,
                message="Rouse Check successful. No Hunger gain."
            )
        else:
            if current_hunger >= 5:
                return RouseCheckResult(
                    success=False,
                    dice=dice,
                    hunger_increase=0,
                    rerolled=rerolled,
                    message="Rouse Check failed! Already at maximum Hunger - must resist Hunger Frenzy!"
                )
            else:
                return RouseCheckResult(
                    success=False,
                    dice=dice,
                    hunger_increase=1,
                    rerolled=rerolled,
                    message=f"Rouse Check failed. Hunger increases by 1."
                )

    @staticmethod
    def multiple_rouse_checks(
        count: int,
        blood_potency: int = 1,
        current_hunger: int = 0
    ) -> List[RouseCheckResult]:
        """
        Perform multiple Rouse Checks (e.g., for high-level powers).

        Args:
            count: Number of Rouse Checks to perform
            blood_potency: Vampire's Blood Potency
            current_hunger: Current Hunger level

        Returns:
            List of RouseCheckResult
        """
        results = []
        hunger = current_hunger

        for _ in range(count):
            result = RouseChecker.perform_rouse_check(blood_potency, hunger)
            results.append(result)
            hunger += result.hunger_increase

        return results
