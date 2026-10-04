from src.pipeline import confidence_score
from src.schemas import Critique


def test_confidence_weighted_sum():
    c = Critique(
        adequacy=1.0,
        fluency=1.0,
        consistency=1.0,
        terminology=1.0,
        error_free=1.0,
        errors=[],
    )
    assert confidence_score(c) == 1.0


def test_confidence_bounds():
    c = Critique(
        adequacy=0.0,
        fluency=0.0,
        consistency=0.0,
        terminology=0.0,
        error_free=0.0,
        errors=["bad"],
    )
    assert confidence_score(c) == 0.0
