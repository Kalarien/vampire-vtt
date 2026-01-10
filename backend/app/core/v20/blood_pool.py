from dataclasses import dataclass
from typing import Optional


@dataclass
class BloodPoolChange:
    old_pool: int
    new_pool: int
    max_pool: int
    change: int
    message: str


class BloodPoolManager:
    """Manages Blood Pool mechanics for V20"""

    # Generation -> Max Blood Pool
    GENERATION_BLOOD_POOL = {
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

    # Generation -> Max Blood Points per turn
    GENERATION_BLOOD_PER_TURN = {
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

    @staticmethod
    def get_max_blood_pool(generation: int) -> int:
        """Get maximum blood pool for a generation"""
        return BloodPoolManager.GENERATION_BLOOD_POOL.get(generation, 10)

    @staticmethod
    def get_blood_per_turn(generation: int) -> int:
        """Get maximum blood points spendable per turn"""
        return BloodPoolManager.GENERATION_BLOOD_PER_TURN.get(generation, 1)

    @staticmethod
    def spend_blood(
        current: int,
        amount: int,
        max_pool: int,
        generation: int
    ) -> BloodPoolChange:
        """
        Spend blood points.

        Args:
            current: Current blood pool
            amount: Amount to spend
            max_pool: Maximum blood pool
            generation: Vampire's generation

        Returns:
            BloodPoolChange with result
        """
        per_turn = BloodPoolManager.get_blood_per_turn(generation)

        if amount > per_turn:
            return BloodPoolChange(
                old_pool=current,
                new_pool=current,
                max_pool=max_pool,
                change=0,
                message=f"Cannot spend more than {per_turn} blood per turn."
            )

        if amount > current:
            return BloodPoolChange(
                old_pool=current,
                new_pool=current,
                max_pool=max_pool,
                change=0,
                message="Not enough blood!"
            )

        new_pool = current - amount

        if new_pool == 0:
            message = "Blood pool empty! Must feed immediately or enter torpor."
        elif new_pool <= 2:
            message = f"Blood pool critically low ({new_pool}). Consider feeding."
        else:
            message = f"Spent {amount} blood. Pool now at {new_pool}."

        return BloodPoolChange(
            old_pool=current,
            new_pool=new_pool,
            max_pool=max_pool,
            change=-amount,
            message=message
        )

    @staticmethod
    def gain_blood(
        current: int,
        amount: int,
        max_pool: int
    ) -> BloodPoolChange:
        """
        Gain blood points from feeding.

        Args:
            current: Current blood pool
            amount: Amount gained
            max_pool: Maximum blood pool

        Returns:
            BloodPoolChange with result
        """
        new_pool = min(current + amount, max_pool)
        actual_gain = new_pool - current

        if actual_gain < amount:
            message = f"Gained {actual_gain} blood (at maximum)."
        else:
            message = f"Gained {actual_gain} blood. Pool now at {new_pool}."

        return BloodPoolChange(
            old_pool=current,
            new_pool=new_pool,
            max_pool=max_pool,
            change=actual_gain,
            message=message
        )

    @staticmethod
    def heal_damage(
        current_pool: int,
        damage_type: str,
        amount: int = 1,
        generation: int = 13
    ) -> dict:
        """
        Heal damage using blood.

        Args:
            current_pool: Current blood pool
            damage_type: "bashing", "lethal", or "aggravated"
            amount: Health levels to heal
            generation: Vampire's generation

        Returns:
            Dict with healing result
        """
        if damage_type == "bashing":
            cost_per_level = 1
            can_heal = True
        elif damage_type == "lethal":
            cost_per_level = 1
            can_heal = True
        else:  # aggravated
            cost_per_level = 5
            can_heal = True  # Requires 5 blood and a day of rest

        total_cost = cost_per_level * amount
        per_turn = BloodPoolManager.get_blood_per_turn(generation)

        if total_cost > current_pool:
            return {
                "success": False,
                "healed": 0,
                "cost": 0,
                "message": f"Not enough blood to heal. Need {total_cost}, have {current_pool}."
            }

        if damage_type != "aggravated" and total_cost > per_turn:
            # Can only heal what blood per turn allows
            healable = per_turn // cost_per_level
            actual_cost = healable * cost_per_level
            return {
                "success": True,
                "healed": healable,
                "cost": actual_cost,
                "message": f"Healed {healable} {damage_type} damage. Can heal more next turn."
            }

        return {
            "success": True,
            "healed": amount,
            "cost": total_cost,
            "message": f"Healed {amount} {damage_type} damage for {total_cost} blood."
        }

    @staticmethod
    def boost_attribute(
        current_pool: int,
        attribute: str,
        amount: int,
        generation: int
    ) -> dict:
        """
        Boost a Physical attribute with blood.

        Args:
            current_pool: Current blood pool
            attribute: "strength", "dexterity", or "stamina"
            amount: Points to boost
            generation: Vampire's generation

        Returns:
            Dict with boost result
        """
        per_turn = BloodPoolManager.get_blood_per_turn(generation)

        if amount > per_turn:
            return {
                "success": False,
                "boost": 0,
                "cost": 0,
                "message": f"Cannot spend more than {per_turn} blood per turn."
            }

        if amount > current_pool:
            return {
                "success": False,
                "boost": 0,
                "cost": 0,
                "message": "Not enough blood."
            }

        return {
            "success": True,
            "boost": amount,
            "cost": amount,
            "message": f"Boosted {attribute} by {amount} for one turn."
        }
