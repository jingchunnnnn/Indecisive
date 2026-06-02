import pytest

from app.services.safety import trim_remarks, validate_lat_lng, validate_radius


def test_invalid_lat_lng_rejected():
    with pytest.raises(ValueError):
        validate_lat_lng(91, 103.8)
    with pytest.raises(ValueError):
        validate_lat_lng(1.3, 181)


def test_radius_above_50000_rejected():
    with pytest.raises(ValueError):
        validate_radius(50001)


def test_long_remarks_trimmed_safely():
    assert len(trim_remarks("x" * 500)) == 300
