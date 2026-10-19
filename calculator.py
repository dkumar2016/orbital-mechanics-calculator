"""Circular-orbit calculator: classify an orbit by altitude and compute its
radius, circular speed and period.

Run directly for a demo report:  py calculator.py
Run the tests from the repo root: pytest -v
"""

import math

earth_radius_km = 6378.137  # Earth's equatorial radius in kilometers
geo_altitude_km = 35786     # GEO altitude in kilometers
leo_max_altitude_km = 2000  # LEO upper limit (inclusive)
geo_band_km = 200           # GEO band: +/- 200 km around GEO altitude
mu = 398600.4418            # Earth's gravitational parameter in km^3/s^2


def validate_altitude(altitude):
    """Raise ValueError if altitude is not a positive number (km)."""
    if altitude <= 0:
        raise ValueError(f"Altitude must be positive (km), got {altitude}.")


def classify_orbit(altitude):
    """Return 'LEO', 'MEO', 'GEO' or 'Beyond GEO' for an altitude in km."""
    validate_altitude(altitude)
    if altitude <= leo_max_altitude_km:
        return "LEO"
    elif altitude <= geo_altitude_km - geo_band_km:
        return "MEO"
    elif altitude <= geo_altitude_km + geo_band_km:
        return "GEO"
    else:
        return "Beyond GEO"


def orbital_radius(altitude):
    """Orbital radius in km: Earth's radius plus altitude."""
    validate_altitude(altitude)
    return earth_radius_km + altitude


def orbital_period_min(altitude):
    """Circular-orbit period in MINUTES."""
    radius = orbital_radius(altitude)
    period_seconds = 2 * math.pi * math.sqrt(radius**3 / mu)
    return period_seconds / 60


def circular_speed_km_s(altitude):
    """Circular-orbit speed in km/s."""
    radius = orbital_radius(altitude)
    return math.sqrt(mu / radius)


def print_report(altitude):
    """Print class, radius, speed and period for one altitude, or the error."""
    try:
        orbit_class = classify_orbit(altitude)
        radius = orbital_radius(altitude)
        speed = circular_speed_km_s(altitude)
        period = orbital_period_min(altitude)
        print(f"Altitude: {altitude} km -> Orbit Class: {orbit_class}, Orbital Radius: {radius:.2f} km, "
              f"Speed: {speed:.3f} km/s, Orbital Period: {period:.2f} minutes")
    except ValueError as e:
        print(f"Altitude: {altitude} km -> Error: {e}")


if __name__ == "__main__":
    print("Report:")
    for altitude in [400, 2000, 2001, 20200, 35786, 50000, 0, -5]:
        print_report(altitude)