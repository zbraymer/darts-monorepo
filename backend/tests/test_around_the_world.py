import pytest
from app.game import AroundTheWorldGame
from app.schemas import ThrowTriplet, Throw
from app.utils import calculate_score
from unittest.mock import patch


@pytest.fixture
def game():
    """Creates a new game instance for testing."""
    return AroundTheWorldGame(mode="single")


def test_initialize_game(game):
    """Test that a game initializes correctly."""
    assert game.current_target == 1
    assert game.throw_count == 0
    assert not game.is_complete


@patch("app.utils.calculate_score")
def test_process_valid_throws(mock_calculate_score, game):
    """Test multiple valid throws advancing the target immediately."""
    mock_calculate_score.side_effect = [
        Throw(zone=1, multiplier="single"),
        Throw(zone=2, multiplier="single"),
        Throw(zone=3, multiplier="single"),
    ]

    throws = ThrowTriplet(
        throws=[
            Throw(zone=1, multiplier="single"),
            Throw(zone=2, multiplier="single"),
            Throw(zone=3, multiplier="single"),
        ]
    )

    result = game.process_throws(throws)

    assert result["message"] == "Turn processed."
    assert game.current_target == 4  # Should be targeting 4 next
    assert game.throw_count == 3  # Three throws taken


@patch("app.utils.calculate_score")
def test_process_invalid_throws(mock_calculate_score, game):
    """Test invalid throws that do not advance the target."""
    mock_calculate_score.side_effect = [
        Throw(zone=5, multiplier="single"),
        Throw(zone=7, multiplier="single"),
        Throw(zone=9, multiplier="single"),
    ]

    throws = ThrowTriplet(
        throws=[
            Throw(zone=5, multiplier="single"),
            Throw(zone=7, multiplier="single"),
            Throw(zone=9, multiplier="single"),
        ]
    )

    result = game.process_throws(throws)

    assert result["message"] == "Turn processed."
    assert game.current_target == 1  # Should still be targeting 1
    assert game.throw_count == 3  # Three throws taken


@patch("app.utils.calculate_score")
def test_complete_game(mock_calculate_score, game):
    """Test that the game correctly completes when reaching target 20."""
    for i in range(1, 21):
        mock_calculate_score.return_value = Throw(zone=i, multiplier="single")
        throws = ThrowTriplet(throws=[Throw(zone=i, multiplier="single")] * 3)
        game.process_throws(throws)

    assert game.is_complete
    assert game.current_target == 20  # Should end on 20
    assert game.throw_count == 60  # 3 darts per target


@patch("app.utils.calculate_score")
def test_already_completed_game(mock_calculate_score, game):
    """Ensure no additional processing occurs once the game is complete."""
    game.is_complete = True

    throws = ThrowTriplet(
        throws=[
            Throw(zone=10, multiplier="single"),
            Throw(zone=15, multiplier="single"),
            Throw(zone=20, multiplier="single"),
        ]
    )

    result = game.process_throws(throws)

    assert result["message"] == "Game is already completed."
    assert game.current_target == 1  # Should remain unchanged
    assert game.throw_count == 0  # No throws should be counted
