import math

MU = 398600.4418       # km^3/s^2
R_EARTH = 6378.137     # km

class Orbit:
    """
    Two-body Keplerian orbit defined by semi-major axis and eccentricity.

    Parameters
    ----------
    a : float  Semi-major axis (km). Periapsis a(1 - e) must be above R_EARTH.
    e : float  Eccentricity. 0 <= e < 1 for a bound elliptical orbit.
    """

    def __init__(self, a, e):
        if not (0 <= e < 1):
            raise ValueError(f"Eccentricity must be 0 <= e < 1, got {e}.")
        r_p = a * (1 - e)
        if r_p <= R_EARTH:
            raise ValueError(
                f"Periapsis {r_p:.1f} km is inside the Earth (R = {R_EARTH} km)."
            )
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

if __name__ == "__main__":
    for a, e, name in [(6778, 0.001, "ISS-like"),
                       (24471, 0.720, "Transfer"),
                       (26560, 0.740, "Molniya-like")]:
        print(f"=== {name} ===")
        print(Orbit(a, e))
        print()

