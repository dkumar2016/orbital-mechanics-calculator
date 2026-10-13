""" Project: satellite file parser

Problem statement

Task: Read a text file listing satellites, and for each valid one report its orbit class, orbital radius, circular speed and period.

Input file (data/satellites.txt): one satellite per line, in the form NORAD_ID NAME ALTITUDE_KM, for example 25544 ISS 408. The first item is the ID, the last item is the altitude, and anything between them is the name. Create about 10 lines yourself from real satellites you know. Include deliberately bad lines: a blank line, a line with a missing altitude, a non-numeric altitude, and a negative altitude.

Rules:

A bad line must not crash the program. It is skipped, and the reason is recorded.
Use your Day 1 functions (classify_orbit, orbital_radius, orbital_period_min) by importing them from calculator.py. Do not copy the code.
Add a new function circular_speed_km_s(altitude) to calculator.py, with the same validation as the others, and a self-check that compares it with your hand calculation.

Outputs:

A table printed to the console.
output/satellites.csv with columns: id, name, altitude_km, orbit_class, radius_km, speed_km_s, period_min.
output/satellites.json with the same data.
A skipped-lines report: line number, line text and reason. """



import csv
import json
import math
import os


from calculator import (
    
    classify_orbit,
    orbital_radius,
    orbital_period_min,
    circular_speed_km_s,
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_DIR, "data", "satellites.txt")
OUTPUT_CSV = os.path.join(BASE_DIR, "output", "satellites.csv")
OUTPUT_JSON = os.path.join(BASE_DIR, "output", "satellites.json")

FIELDS = ["id", "name", "altitude_km", "orbit_class", "radius_km", "speed_km_s", "period_min"]

def parse_line(line):

    """Parse 'ID NAME... ALTITUDE_KM' into a dict. Raise ValueError if invalid."""
    parts = line.strip().split()
    
    if len(parts) <3:
        raise ValueError(f"too few fields (Need ID, name, altitude): {line!r}")

    try:
        sat_id = int(parts[0])
    except ValueError:
        raise ValueError(f"invalid ID - ID is not a whole number: {parts[0]!r}") from None

    try:
        altitude = float(parts[-1])
    except ValueError:
        raise ValueError(f"invalid altitude - altitude is not a number: {parts[-1]!r}") from None

    if not math.isfinite(altitude):
        raise ValueError(f"invalid altitude - altitude must be a finite number: {parts[-1]!r}")
    if altitude <= 0:
        raise ValueError(f"invalid altitude - altitude must be positive: {parts[-1]!r}")

    name = " ".join(parts[1:-1])

    return {
        "id": sat_id,
        "name": name,
        "altitude_km": altitude
    }


def read_satellites(path):
    good, bad = [], []
    with open(path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                good.append(parse_line(line))
            except ValueError as err:
                bad.append({"line_number": line_number,
                            "line": line.rstrip("\n"),
                            "reason": str(err)})
    return good, bad

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Could not load JSON: file not found: {path}")
    except json.JSONDecodeError as err:
        print(f"Could not load JSON: invalid JSON in {path}: {err}")
    return None


def build_record(satellite):
    altitude_km = satellite["altitude_km"]
    return {
        "id": satellite["id"],
        "name": satellite["name"],
        "altitude_km": altitude_km,
        "orbit_class": classify_orbit(altitude_km),
        "radius_km": orbital_radius(altitude_km),
        "speed_km_s": circular_speed_km_s(altitude_km),
        "period_min": orbital_period_min(altitude_km),
    }


def round_record(record):
    rounded = dict(record)
    rounded["radius_km"] = round(record["radius_km"], 2)
    rounded["speed_km_s"] = round(record["speed_km_s"], 3)
    rounded["period_min"] = round(record["period_min"], 2)
    return rounded

def save_csv(records, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)


def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)



def print_table(records):
    header = (f"{'ID':>6}  {'Name':<15}{'Alt (km)':>9}  {'Class':<7}"
              f"{'Radius (km)':>12}{'Speed (km/s)':>13}{'Period (min)':>13}")
    print(header)
    print("-" * len(header))
    for r in records:
        print(f"{r['id']:>6}  {r['name']:<15}{r['altitude_km']:>9.1f}  {r['orbit_class']:<7}"
              f"{r['radius_km']:>12.2f}{r['speed_km_s']:>13.3f}{r['period_min']:>13.2f}")


def print_skipped(bad):
    print(f"\nSkipped lines ({len(bad)}):")
    for b in bad:
        print(f"  line {b['line_number']}: {b['line']!r} -> {b['reason']}")


def main():
    good, bad = read_satellites(INPUT_PATH)
    print(f"Read {len(good)} valid and {len(bad)} invalid lines from {INPUT_PATH}\n")

    records = [round_record(build_record(s)) for s in good]
    print_table(records)
    print_skipped(bad)

    save_csv(records, OUTPUT_CSV)
    save_json(records, OUTPUT_JSON)
    print(f"\nSaved {OUTPUT_CSV}\nSaved {OUTPUT_JSON}")


if __name__ == "__main__":
    main()