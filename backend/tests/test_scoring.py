import unittest
import pytest
from app.utils import generate_throw_for_score
from app.schemas import Throw
from app import constants as c


class TestGenerateThrowForScore(unittest.TestCase):
    def test_single_zone(self):
        """Test generating a single score throw."""
        for zone in range(1, 21):
            throw = generate_throw_for_score(zone, c.SINGLE)
            assert isinstance(throw, Throw)
            assert (c.OUTER_BULL_RADIUS <= throw.radius <= c.INNER_TRIPLE_RADIUS) or (
                c.OUTER_TRIPLE_RADIUS <= throw.radius <= c.INNER_DOUBLE_RADIUS
            )
            assert throw.angle >= 0
            assert throw.angle <= 360

    def test_double_zone(self):
        """Test generating a double score throw."""
        for zone in range(1, 21):
            throw = generate_throw_for_score(zone, c.DOUBLE)
            assert isinstance(throw, Throw)
            assert c.INNER_DOUBLE_RADIUS <= throw.radius <= c.OUTER_DOUBLE_RADIUS
            assert throw.angle >= 0
            assert throw.angle <= 360

    def test_triple_zone(self):
        """Test generating a triple score throw."""
        for zone in range(1, 21):
            throw = generate_throw_for_score(zone, c.TRIPLE)
            assert isinstance(throw, Throw)
            assert c.INNER_TRIPLE_RADIUS <= throw.radius <= c.OUTER_TRIPLE_RADIUS
            assert throw.angle >= 0
            assert throw.angle <= 360

    def test_inner_bullseye(self):
        """Test generating an inner bullseye throw."""
        throw = generate_throw_for_score(50, "bull")
        for zone in range(1, 21):
            # TODO This is incorrect
            throw = generate_throw_for_score(zone, c.TRIPLE)
            assert isinstance(throw, Throw)
            assert throw.radius <= c.INNER_BULL_RADIUS
            assert throw.angle >= 0
            assert throw.angle <= 360

    def test_outer_bullseye(self):
        """Test generating an outer bullseye throw."""
        throw = generate_throw_for_score(25, "bull")
        assert isinstance(throw, Throw)
        assert c.INNER_BULL_RADIUS <= throw.radius <= c.OUTER_BULL_RADIUS
        assert throw.angle >= 0
        assert throw.angle <= 360

    def test_invalid_multiplier(self):
        """Test handling of invalid multiplier."""
        with pytest.raises(ValueError):
            generate_throw_for_score(5, "quadruple")

    def test_invalid_zone(self):
        """Test handling of invalid zone."""
        with pytest.raises(ValueError):
            generate_throw_for_score(21, c.SINGLE)

    def test_invalid_bullseye_zone(self):
        """Test handling of invalid bullseye zone."""
        with pytest.raises(ValueError):
            generate_throw_for_score(30, "bull")
