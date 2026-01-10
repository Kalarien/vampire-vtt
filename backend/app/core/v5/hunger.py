from typing import Tuple
from dataclasses import dataclass
from enum import Enum


class FeedingResult(Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    KILLED = "killed"
    FAILED = "failed"


@dataclass
class HungerChange:
    old_hunger: int
    new_hunger: int
    change: int
    message: str


class HungerManager:
    """Manages Hunger mechanics for V5"""

    MIN_HUNGER = 0
    MAX_HUNGER = 5

    @staticmethod
    def increase_hunger(current: int, amount: int = 1) -> HungerChange:
        """
        Increase hunger (failed Rouse Check, etc)

        Args:
            current: Current hunger level
            amount: Amount to increase

        Returns:
            HungerChange with result
        """
        new_hunger = min(current + amount, HungerManager.MAX_HUNGER)
        change = new_hunger - current

        if new_hunger >= HungerManager.MAX_HUNGER:
            message = "Hunger at maximum! Risk of frenzy!"
        else:
            message = f"Hunger increased to {new_hunger}"

        return HungerChange(
            old_hunger=current,
            new_hunger=new_hunger,
            change=change,
            message=message
        )

    @staticmethod
    def decrease_hunger(
        current: int,
        amount: int = 1,
        blood_potency: int = 1,
        is_animal: bool = False,
        is_bagged: bool = False
    ) -> HungerChange:
        """
        Decrease hunger from feeding.

        Args:
            current: Current hunger level
            amount: Base amount to reduce
            blood_potency: Vampire's Blood Potency
            is_animal: If feeding from animal
            is_bagged: If feeding from blood bags

        Returns:
            HungerChange with result
        """
        min_hunger = 0

        # Blood Potency restrictions
        if blood_potency >= 2 and is_animal:
            return HungerChange(
                old_hunger=current,
                new_hunger=current,
                change=0,
                message="Animal blood no longer sustains you."
            )

        if blood_potency >= 3 and is_bagged:
            amount = 1  # Bagged blood only reduces 1 at BP 3+

        if blood_potency >= 4:
            min_hunger = 2  # Can't reduce below 2 without killing

        # Animal blood can't reduce below 1
        if is_animal:
            min_hunger = max(min_hunger, 1)

        new_hunger = max(current - amount, min_hunger)
        change = current - new_hunger

        if change == 0:
            message = "Feeding provides no relief."
        elif new_hunger == 0:
            message = "Hunger completely sated."
        else:
            message = f"Hunger reduced to {new_hunger}"

        return HungerChange(
            old_hunger=current,
            new_hunger=new_hunger,
            change=-change,
            message=message
        )

    @staticmethod
    def slake_hunger(current: int, kill: bool = False, blood_potency: int = 1) -> HungerChange:
        """
        Fully slake hunger (draining/killing a mortal).

        Args:
            current: Current hunger level
            kill: Whether the victim was killed
            blood_potency: Vampire's Blood Potency

        Returns:
            HungerChange with result
        """
        if kill:
            # Killing allows full reduction even at high BP
            new_hunger = 0
            message = "Hunger fully sated. The victim is dead."
        else:
            # Just draining has BP limits
            if blood_potency >= 4:
                new_hunger = 1
                message = "Hunger reduced to 1. Killing required to fully sate."
            else:
                new_hunger = 0
                message = "Hunger fully sated from draining."

        return HungerChange(
            old_hunger=current,
            new_hunger=new_hunger,
            change=current - new_hunger,
            message=message
        )

    @staticmethod
    def is_starving(hunger: int) -> bool:
        """Check if vampire is at maximum hunger"""
        return hunger >= HungerManager.MAX_HUNGER

    @staticmethod
    def frenzy_difficulty(hunger: int) -> int:
        """Get base frenzy difficulty based on hunger"""
        if hunger <= 1:
            return 2
        elif hunger <= 3:
            return 3
        elif hunger == 4:
            return 4
        else:
            return 5  # Very hard to resist at Hunger 5
