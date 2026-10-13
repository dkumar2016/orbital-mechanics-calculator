#Problem statement: Orbit Altitude Classifier

#Task: Write a Python program that takes a satellite's altitude above Earth's surface (in km) and reports which orbit class it belongs to.

#Inputs: One altitude value in kilometres.

#Outputs: One of four labels: LEO, MEO, GEO or Beyond GEO.


#Rules:

#Altitude (km)	Label
#Up to 2,000	LEO
#Above 2,000 up to 35,586	MEO
#35,586 to 35,986 (within 200 km of 35,786)	GEO
#Above 35,986	Beyond GEO
#Invalid input: Zero or negative altitudes must be rejected with a clear error message.
#Constants: Earth's radius (6,378.137 km) and the GEO altitude (35,786 km) should be defined once, not typed repeatedly.
#Checks: The program must test itself against at least these altitudes: 400, 2,000, 2,001, 20,200, 35,786 and 50,000 km, plus 0 and -5 as invalid inputs.
#Output when run: It prints the result for each test altitude.
#Stretch (optional): Also report the orbital radius (Earth's radius plus altitude) and the circular-orbit period. Sanity check: 400 km should give about 92.5 minutes, and GEO about 1,436 minutes.


#solution:

import math

earth_radius_km = 6378.137  # Earth's radius in kilometers
geo_altitude_km = 35786  # GEO altitude in kilometers
leo_max_altitude_km = 2000
geo_band_km = 200
mu = 398600.4418  # Standard gravitational parameter for Earth in km^3/s^2


def validate_altitude(altitude):
    """Raise ValueError if altitude is not a positive number (km)."""
    if altitude <= 0:
        raise ValueError(f"Altitude must be positive (km), got {altitude}.")


def classify_orbit(altitude):
    validate_altitude(altitude)
    if altitude <= leo_max_altitude_km:
        return "LEO"
    elif altitude <= geo_altitude_km - geo_band_km:
        return "MEO"
    elif geo_altitude_km - geo_band_km < altitude <= geo_altitude_km + geo_band_km:
        return "GEO"
    else:
        return "Beyond GEO"


def orbital_radius(altitude):
    validate_altitude(altitude)
    return earth_radius_km + altitude


def orbital_period_min(altitude):
    """Circular-orbit period in MINUTES."""
    validate_altitude(altitude)
    radius = orbital_radius(altitude)
    period_seconds = 2 * math.pi * math.sqrt(radius**3 / mu)
    return period_seconds / 60


def circular_speed_km_s(altitude):
    """Circular-orbit speed in km/s."""
    validate_altitude(altitude)
    radius = orbital_radius(altitude)
    return math.sqrt(mu / radius)


def run_self_checks():
    print("self-checks:")
    test_cases = [
        (400, "LEO"),
        (2000, "LEO"),
        (2001, "MEO"),
        (20200, "MEO"),
        (35786, "GEO"),
        (50000, "Beyond GEO"),
        (0, ValueError),
        (-5, ValueError),
    ]

    for altitude, expected in test_cases:
        try:
            result = classify_orbit(altitude)
            assert result == expected, f"Test failed for altitude {altitude}: expected {expected}, got {result}"
        except ValueError as e:
            assert expected == ValueError, f"Test failed for altitude {altitude}: expected {expected}, got ValueError: {e}"

    print("physics checks:")
    leo_min = orbital_period_min(400)
    geo_min = orbital_period_min(geo_altitude_km)
    assert abs(leo_min - 92.5) < 1, f"LEO period sanity check failed: expected ~92.5 minutes, got {leo_min:.2f} minutes"
    assert abs(geo_min - 1436) < 1, f"GEO period sanity check failed: expected ~1436 minutes, got {geo_min:.2f} minutes"
    print(f"  400 km period: {leo_min:.2f} min (expected ~92.5)")
    print(f"  GEO period:    {geo_min:.2f} min (expected ~1436)")

    # Speed vs hand calculations (docs/hand_calculations.md)
    speed_cases = [
        (400, 7.669),
        (20200, 3.873),
        (35786, 3.075),
    ]
    for altitude, expected_speed in speed_cases:
        actual_speed = circular_speed_km_s(altitude)
        assert abs(actual_speed - expected_speed) < 0.01, (
            f"Speed check failed at {altitude} km: "
            f"expected {expected_speed} km/s, got {actual_speed:.3f} km/s"
        )
        print(f"  {altitude} km speed: {actual_speed:.3f} km/s (hand value {expected_speed})")

    for altitude in (0, -5):
        try:
            circular_speed_km_s(altitude)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Expected ValueError for altitude {altitude} km")

    # Consistency: speed * period = circumference (2*pi*r), at every valid altitude
    for altitude in [400, 2000, 2001, 20200, 35786, 50000]:
        lhs = circular_speed_km_s(altitude) * orbital_period_min(altitude) * 60
        rhs = 2 * math.pi * orbital_radius(altitude)
        assert math.isclose(lhs, rhs, rel_tol=1e-9), f"v*T != 2*pi*r at {altitude} km"

    print("All classification and physics checks passed successfully.")


def print_report(altitude):
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
    run_self_checks()
    print("\nReport:")
    for altitude in [400, 2000, 2001, 20200, 35786, 50000, 0, -5]:
        print_report(altitude)