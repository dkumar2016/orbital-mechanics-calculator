# Tests for calculator.py: classification, validation and circular-orbit physics

import math
import pytest

from calculator import (
    classify_orbit,
    orbital_radius,
    orbital_period_min,
    circular_speed_km_s,
)

MU = 398600.4418  # km^3/s^2


@pytest.mark.parametrize("altitude, expected", [
    (400, "LEO"),
    (2000, "LEO"),         # boundary: inclusive
    (2001, "MEO"),         # just above the boundary
    (20200, "MEO"),        # GPS
    (35786, "GEO"),
    (50000, "Beyond GEO"),
])
def test_classification(altitude, expected):
    assert classify_orbit(altitude) == expected

#Test for invalid altitude

@pytest.mark.parametrize("func", [classify_orbit, orbital_radius, orbital_period_min, circular_speed_km_s])
@pytest.mark.parametrize("altitude", [0, -5])
def test_invalid_altitude_raises(func, altitude):
    with pytest.raises(ValueError):
        func(altitude)
    
# Periods against known results (hand calculations in docs/hand_calculations.md)
@pytest.mark.parametrize("altitude, expected_min", [
    (400, 92.56),       # ISS-like
    (35786, 1436.07),   # GEO: one sidereal day
])
def test_period_known_values(altitude, expected_min):
    assert orbital_period_min(altitude) == pytest.approx(expected_min, abs=0.01)


# Circular speeds against hand calculations
@pytest.mark.parametrize("altitude, expected_km_s", [
    (400, 7.669),
    (20200, 3.873),
    (35786, 3.075),
])
def test_speed_hand_values(altitude, expected_km_s):
    assert circular_speed_km_s(altitude) == pytest.approx(expected_km_s, abs=0.001)


#Consistency - distance in one period equals the circumference (v * T = 2 pi r)

@pytest.mark.parametrize("altitude", [400, 2000, 2001, 20200, 35786, 50000])
def test_consistency_v_times_T(altitude):
    v = circular_speed_km_s(altitude)          # km/s
    T_s = orbital_period_min(altitude) * 60    # minutes -> seconds
    r = orbital_radius(altitude)               # km
    assert v * T_s == pytest.approx(2 * math.pi * r, rel=1e-9)