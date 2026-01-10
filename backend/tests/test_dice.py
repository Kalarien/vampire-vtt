import pytest
from app.core.v5.dice import V5DiceRoller
from app.core.v20.dice import V20DiceRoller


class TestV5DiceRoller:
    """Tests for V5 dice roller"""

    def test_roll_basic(self):
        """Test basic dice rolling"""
        result = V5DiceRoller.roll(5, 0, 1)
        assert len(result.regular_dice) == 5
        assert len(result.hunger_dice) == 0
        assert all(1 <= d <= 10 for d in result.regular_dice)

    def test_roll_with_hunger(self):
        """Test rolling with hunger dice"""
        result = V5DiceRoller.roll(5, 2, 1)
        assert len(result.regular_dice) == 3
        assert len(result.hunger_dice) == 2

    def test_roll_hunger_caps_at_pool(self):
        """Test that hunger dice can't exceed pool"""
        result = V5DiceRoller.roll(3, 5, 1)
        assert len(result.regular_dice) == 0
        assert len(result.hunger_dice) == 3

    def test_success_counting(self):
        """Test success counting logic"""
        # Mock dice results
        result = V5DiceRoller.roll(10, 0, 1)
        # Successes are 6+
        assert result.successes >= 0
        assert result.is_success == (result.successes >= result.difficulty)

    def test_rouse_check(self):
        """Test rouse check"""
        success, dice = V5DiceRoller.rouse_check()
        assert len(dice) == 1
        assert isinstance(success, bool)
        assert success == (dice[0] >= 6)

    def test_rouse_check_reroll(self):
        """Test rouse check with reroll"""
        success, dice = V5DiceRoller.rouse_check(reroll=True)
        assert len(dice) == 2


class TestV20DiceRoller:
    """Tests for V20 dice roller"""

    def test_roll_basic(self):
        """Test basic V20 dice rolling"""
        result = V20DiceRoller.roll(5, 6)
        assert len(result.dice) == 5
        assert all(1 <= d <= 10 for d in result.dice)

    def test_difficulty_affects_success(self):
        """Test that difficulty affects success counting"""
        # With a high difficulty, fewer successes
        result_easy = V20DiceRoller.roll(10, 3)
        result_hard = V20DiceRoller.roll(10, 9)
        # Can't directly compare since it's random, but verify structure
        assert isinstance(result_easy.successes, int)
        assert isinstance(result_hard.successes, int)

    def test_botch_detection(self):
        """Test botch detection structure"""
        result = V20DiceRoller.roll(1, 6)
        assert isinstance(result.is_botch, bool)
        # A botch requires: 0 successes and at least one 1
        if result.is_botch:
            assert result.successes == 0
            assert 1 in result.dice

    def test_ones_and_tens_counting(self):
        """Test counting of ones and tens"""
        result = V20DiceRoller.roll(10, 6)
        ones_count = sum(1 for d in result.dice if d == 1)
        tens_count = sum(1 for d in result.dice if d == 10)
        assert result.ones_count == ones_count
        assert result.tens_count == tens_count


class TestV5MessyCritical:
    """Tests for messy critical detection"""

    def test_messy_critical_structure(self):
        """Test that messy critical flag exists"""
        result = V5DiceRoller.roll(10, 5, 1)  # High hunger increases chance
        assert hasattr(result, 'is_messy_critical')
        assert isinstance(result.is_messy_critical, bool)


class TestV5BestialFailure:
    """Tests for bestial failure detection"""

    def test_bestial_failure_structure(self):
        """Test that bestial failure flag exists"""
        result = V5DiceRoller.roll(5, 5, 5)  # High difficulty, high hunger
        assert hasattr(result, 'is_bestial_failure')
        assert isinstance(result.is_bestial_failure, bool)
