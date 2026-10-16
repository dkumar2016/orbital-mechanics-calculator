import math

MU = 398600.4418       # km^3/s^2
R_EARTH = 6378.137     # km

class Orbit:
    """
    Two-body Keplerian orbit defined by semi-major axis and eccentricity.

    Parameters
    ----------
    a : float  Semi-major axis (km). Must be > R_EARTH.
    e : float  Eccentricity. 0 <= e < 1 for a bound elliptical orbit.
    """

    def __init__(self, a, e):
        if a <= R_EARTH:
            raise ValueError(f"Semi-major axis must be > Earth radius ({R_EARTH} km), got {a}.")
        if not (0 <= e < 1):
            raise ValueError(f"Eccentricity must be 0 <= e < 1, got {e}.")
        self.a = a
        self.e = e


    @property
    def periapsis(self):
        """Periapsis radius (km) — closest point to Earth's centre."""
        return self.a * (1 - self.e)

    @property
    def apoapsis(self):
        """Apoapsis radius (km) — farthest point from Earth's centre."""
        return self.a * (1 + self.e)

    @property
    def period_min(self):
        """Orbital period (minutes)."""
        return 2 * math.pi * math.sqrt(self.a**3 / MU) / 60

    @property
    def specific_energy(self):
        """Specific orbital energy (km^2/s^2). Always negative for a bound orbit."""
        return -MU / (2 * self.a)

    @property
    def angular_momentum(self):
        """Magnitude of specific angular momentum (km^2/s)."""
        return math.sqrt(MU * self.a * (1 - self.e**2))

    def speed_at_radius(self, r):
        """
        Speed (km/s) at any radius r (km) using vis-viva.
        Raises ValueError if r is outside [periapsis, apoapsis].
        """
        if not (self.periapsis - 1e-6 <= r <= self.apoapsis + 1e-6):
            raise ValueError(
                f"Radius {r:.1f} km is outside orbit range "
                f"[{self.periapsis:.1f}, {self.apoapsis:.1f}] km."
            )
        return math.sqrt(MU * (2/r - 1/self.a))

    @property
    def periapsis_speed(self):
        """Speed at periapsis (km/s) — fastest point."""
        return self.speed_at_radius(self.periapsis)

    @property
    def apoapsis_speed(self):
        """Speed at apoapsis (km/s) — slowest point."""
        return self.speed_at_radius(self.apoapsis)

    def __repr__(self):
        return (
            f"Orbit(a={self.a:.1f} km, e={self.e:.4f})\n"
            f"  Periapsis:        {self.periapsis:.1f} km  |  speed: {self.periapsis_speed:.3f} km/s\n"
            f"  Apoapsis:         {self.apoapsis:.1f} km  |  speed: {self.apoapsis_speed:.3f} km/s\n"
            f"  Period:           {self.period_min:.2f} min\n"
            f"  Specific energy:  {self.specific_energy:.2f} km^2/s^2\n"
            f"  Angular momentum: {self.angular_momentum:.1f} km^2/s"
        )

def run_checks():
    print("Running Orbit class checks...\n")

    # Check 1: circular orbit — periapsis equals apoapsis
    iss = Orbit(6778.0, 0.0)
    assert abs(iss.periapsis - iss.apoapsis) < 0.001, "Circular orbit: periapsis != apoapsis"
    print(f"ISS circular: period = {iss.period_min:.2f} min  (expected ~92.6)")
    assert abs(iss.period_min - 92.6) < 0.5

    # Check 2: energy is negative and matches formula
    assert iss.specific_energy < 0, "Specific energy must be negative for bound orbit"
    expected_energy = -MU / (2 * 6778.0)
    assert abs(iss.specific_energy - expected_energy) < 0.001

    # Check 3: vis-viva at periapsis and apoapsis of transfer orbit
    transfer = Orbit(24471.0, 0.720)
    v_p = transfer.periapsis_speed
    v_a = transfer.apoapsis_speed
    print(f"Transfer periapsis speed: {v_p:.3f} km/s  (expected ~10.00)")
    print(f"Transfer apoapsis speed:  {v_a:.3f} km/s  (expected ~1.63)")
    assert abs(v_p - 10.00) < 0.1
    assert abs(v_a - 1.63) < 0.05

    # Check 4: energy conservation — same energy at periapsis and apoapsis
    eps_p = 0.5 * v_p**2 - MU / transfer.periapsis
    eps_a = 0.5 * v_a**2 - MU / transfer.apoapsis
    assert abs(eps_p - eps_a) < 0.001, \
        f"Energy not conserved: {eps_p:.4f} vs {eps_a:.4f}"
    print("Energy conservation check passed ✓")

    # Check 5: invalid inputs raise ValueError
    try:
        Orbit(6000.0, 0.5)   # a < R_EARTH
    except ValueError:
        pass
    else:
        raise AssertionError("Should have raised ValueError for a < R_EARTH")

    try:
        Orbit(7000.0, 1.5)   # e >= 1
    except ValueError:
        pass
    else:
        raise AssertionError("Should have raised ValueError for e >= 1")

    print("\nAll checks passed.")

if __name__ == "__main__":
    run_checks()

    print("\n--- Three test orbits ---\n")
    for a, e, name in [(6778, 0.001, "ISS-like"),
                       (24471, 0.720, "Transfer"),
                       (26560, 0.740, "Molniya-like")]:
        print(f"=== {name} ===")
        print(Orbit(a, e))
        print()

