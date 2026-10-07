# orbital-mechanics-calculator

A small Python tool that classifies a satellite's orbit (LEO, MEO, GEO or Beyond GEO) from its altitude, and computes the orbital radius and circular-orbit period. Includes input validation, built-in self-checks and physics sanity checks.

## Problem

Given a satellite's altitude above Earth's surface in kilometres, report which orbit class it belongs to, and for a circular orbit at that altitude report the orbital radius and period.

**Input:** one altitude in km.
**Output:** an orbit class label, an orbital radius (km) and an orbital period (minutes).

**Classification rules** (these are conventions, see Limitations):

| Altitude (km) | Class |
|---|---|
| up to 2,000 (inclusive) | LEO |
| above 2,000 up to 35,586 | MEO |
| above 35,586 up to 35,986 (GEO altitude +/- 200 km) | GEO |
| above 35,986 | Beyond GEO |

Zero or negative altitudes are rejected with a `ValueError`.

## Approach

- `validate_altitude(altitude)`: the single place where the "altitude must be positive" rule lives. Every other function calls it.
- `classify_orbit(altitude)`: returns the orbit class using the boundaries above.
- `orbital_radius(altitude)`: Earth radius plus altitude.
- `orbital_period_min(altitude)`: period of a circular two-body orbit in minutes.
- `run_self_checks()`: asserts the expected class for boundary and typical altitudes, confirms invalid inputs raise errors, and checks two known periods.
- `print_report(altitude)`: prints class, radius and period for one altitude, or the error message if the input is invalid.

Period formula for a circular two-body orbit:

```
T = 2 * pi * sqrt(a^3 / mu)
```

where `a` is the orbital radius (Earth radius + altitude) and `mu` is Earth's gravitational parameter.

## Constants and units

| Constant | Value | Unit |
|---|---|---|
| Earth radius (equatorial) | 6,378.137 | km |
| GEO altitude | 35,786 | km |
| mu (Earth) | 398,600.4418 | km^3/s^2 |
| LEO upper limit | 2,000 | km |
| GEO band | +/- 200 | km |

Distances are in km, periods in minutes. Altitude is measured above the equatorial radius of a spherical Earth.

## Setup and run

Requires Python 3. There are no external packages (only the standard library `math` module).

```
git clone git@github.com:dkumar2016/orbital-mechanics-calculator.git
cd orbital-mechanics-calculator
py calculator.py
```

## Example output

```
self-checks:
physics sanity check:
  400 km period: 92.56 min (expected ~92.5)
  GEO period:    1436.07 min (expected ~1436)
All 8 classification checks and 2 physics checks passed successfully.

Report:
Altitude: 400 km -> Orbit Class: LEO, Orbital Radius: 6778.14 km, Orbital Period: 92.56 minutes
Altitude: 2000 km -> Orbit Class: LEO, Orbital Radius: 8378.14 km, Orbital Period: 127.20 minutes
Altitude: 2001 km -> Orbit Class: MEO, Orbital Radius: 8379.14 km, Orbital Period: 127.22 minutes
Altitude: 20200 km -> Orbit Class: MEO, Orbital Radius: 26578.14 km, Orbital Period: 718.70 minutes
Altitude: 35786 km -> Orbit Class: GEO, Orbital Radius: 42164.14 km, Orbital Period: 1436.07 minutes
Altitude: 50000 km -> Orbit Class: Beyond GEO, Orbital Radius: 56378.14 km, Orbital Period: 2220.37 minutes
Altitude: 0 km -> Error: Altitude must be positive (km), got 0.
Altitude: -5 km -> Error: Altitude must be positive (km), got -5.
```

## Validation

**Automated self-checks** (`run_self_checks`) run every time the program starts and stop with an `AssertionError` if anything is wrong:

- 400 km is LEO and 2,000 km is LEO (upper boundary inclusive).
- 2,001 km is MEO (just past the boundary) and 20,200 km is MEO (a GPS-like altitude).
- 35,786 km is GEO and 50,000 km is Beyond GEO.
- 0 km and -5 km raise `ValueError`.

**Physics sanity checks** against known results:

| Case | Program | Expected |
|---|---|---|
| 400 km (ISS-like) | 92.56 min | about 92.5 min |
| 35,786 km (GEO) | 1,436.07 min | one sidereal day, about 1,436 min (23 h 56 min) |

**Hand calculation, GEO:**

- a = 6,378.137 + 35,786 = 42,164.137 km
- a^3 = 7.496 x 10^13 km^3
- a^3 / mu = 7.496 x 10^13 / 398,600.4418 = 1.8806 x 10^8 s^2
- sqrt(a^3 / mu) = 13,713.4 s
- T = 2 * pi * 13,713.4 = 86,164 s = 1,436.07 min

**Hand calculation, 400 km:**

- a = 6,378.137 + 400 = 6,778.137 km
- a^3 = 3.114 x 10^11 km^3
- a^3 / mu = 781,256 s^2
- sqrt(a^3 / mu) = 883.9 s
- T = 2 * pi * 883.9 = 5,553.6 s = 92.56 min

Hand results match the program output.

## Limitations

- Orbit-class boundaries are conventions. Different sources use different cut-offs (for example, some put the LEO limit at 1,000 km or 2,000 km).
- The period assumes a circular, two-body orbit. It ignores J2 (Earth's oblateness), atmospheric drag and third-body effects.
- Altitude is taken above a spherical Earth with the equatorial radius. Real altitude depends on latitude and the orbit's shape.
- The tool takes one altitude at a time and does not handle elliptical orbits.

## Next steps

The next project, `orbit-state-vector-toolkit`, extends this to full orbital elements and state vectors.