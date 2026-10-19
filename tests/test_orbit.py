"""Tests for orbit_class.py: geometry, energy, angular momentum, vis-viva and validation."""
import math
import pytest

from orbit_class import Orbit, MU

# The three reference orbits used throughout Week 1
ISS = (6778.0, 0.001)
TRANSFER = (24471.0, 0.720)
MOLNIYA = (26560.0, 0.740)
ALL_ORBITS = [ISS, TRANSFER, MOLNIYA]


# ---------- geometry and period ----------

def test_circular_orbit_periapsis_equals_apoapsis():
    orbit = Orbit(6778.0, 0.0)
    assert orbit.periapsis == pytest.approx(orbit.apoapsis)


@pytest.mark.parametrize("a, e, expected_min", [
    (6778.0, 0.0, 92.56),      # ISS-like
    (24471.0, 0.72, 634.95),   # transfer orbit
    (26560.0, 0.74, 717.96),   # Molniya, about 12 h
])
def test_period(a, e, expected_min):
    assert Orbit(a, e).period_min == pytest.approx(expected_min, abs=0.01)


def test_periapsis_and_apoapsis_molniya():
    orbit = Orbit(*MOLNIYA)
    assert orbit.periapsis == pytest.approx(6905.6, abs=0.1)
    assert orbit.apoapsis == pytest.approx(46214.4, abs=0.1)


# ---------- energy and angular momentum ----------

def test_energy_negative_and_matches_formula():
    orbit = Orbit(6778.0, 0.0)
    assert orbit.specific_energy < 0
    assert orbit.specific_energy == pytest.approx(-MU / (2 * 6778.0))
    assert orbit.specific_energy == pytest.approx(-29.40, abs=0.01)   # hand value


def test_angular_momentum_circular_equals_sqrt_mu_r():
    orbit = Orbit(6778.0, 0.0)
    assert orbit.angular_momentum == pytest.approx(math.sqrt(MU * 6778.0))


def test_angular_momentum_iss_hand_value():
    assert Orbit(*ISS).angular_momentum == pytest.approx(51978, abs=1)


# ---------- vis-viva ----------

def test_transfer_orbit_speeds():
    orbit = Orbit(*TRANSFER)
    assert orbit.periapsis_speed == pytest.approx(10.00, abs=0.01)
    assert orbit.apoapsis_speed == pytest.approx(1.63, abs=0.01)


def test_speed_at_radius_matches_periapsis_speed():
    orbit = Orbit(*TRANSFER)
    assert orbit.speed_at_radius(orbit.periapsis) == pytest.approx(orbit.periapsis_speed)


@pytest.mark.parametrize("radius", [5000.0, 50000.0])
def test_speed_outside_orbit_raises(radius):
    with pytest.raises(ValueError, match="outside orbit range"):
        Orbit(*TRANSFER).speed_at_radius(radius)


# ---------- conservation laws (hold for ANY valid orbit) ----------

@pytest.mark.parametrize("a, e", ALL_ORBITS)
def test_energy_conserved(a, e):
    orbit = Orbit(a, e)
    eps_p = orbit.periapsis_speed**2 / 2 - MU / orbit.periapsis
    eps_a = orbit.apoapsis_speed**2 / 2 - MU / orbit.apoapsis
    assert eps_p == pytest.approx(eps_a, rel=1e-12)
    assert eps_p == pytest.approx(orbit.specific_energy, rel=1e-12)


@pytest.mark.parametrize("a, e", ALL_ORBITS)
def test_angular_momentum_conserved(a, e):
    # At periapsis and apoapsis, velocity is perpendicular to r, so h = r * v
    orbit = Orbit(a, e)
    assert orbit.periapsis * orbit.periapsis_speed == pytest.approx(orbit.angular_momentum, rel=1e-12)
    assert orbit.apoapsis * orbit.apoapsis_speed == pytest.approx(orbit.angular_momentum, rel=1e-12)


@pytest.mark.parametrize("a, e", ALL_ORBITS)
def test_faster_at_periapsis(a, e):
    orbit = Orbit(a, e)
    assert orbit.periapsis_speed > orbit.apoapsis_speed      # Kepler's second law


# ---------- validation ----------

@pytest.mark.parametrize("a, e, reason", [
    (7000.0, 1.5, "Eccentricity"),         # hyperbolic
    (7000.0, 1.0, "Eccentricity"),         # parabolic
    (7000.0, -0.1, "Eccentricity"),        # negative
    (6000.0, 0.0, "inside the Earth"),     # circular orbit below the surface
    (6000.0, 0.5, "inside the Earth"),     # a below Earth radius
    (7000.0, 0.5, "inside the Earth"),     # a above Earth radius, periapsis 3,500 km
])
def test_invalid_orbits_raise(a, e, reason):
    with pytest.raises(ValueError, match=reason):
        Orbit(a, e)