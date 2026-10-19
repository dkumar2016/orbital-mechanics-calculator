"""Tests for parse_satellites.py: line parsing, file reading, records and file output."""
import csv
import pytest

from parse_satellites import (
    FIELDS,
    INPUT_PATH,
    parse_line,
    read_satellites,
    build_record,
    round_record,
    save_csv,
    save_json,
    load_json,
)


# ---------- parse_line: valid lines ----------

def test_parse_simple_line():
    assert parse_line("25544 ISS 408") == {"id": 25544, "name": "ISS", "altitude_km": 408.0}


def test_parse_name_with_spaces():
    sat = parse_line("43013 NOAA 20 824")
    assert sat["name"] == "NOAA 20"
    assert sat["altitude_km"] == 824.0


def test_parse_ignores_extra_whitespace():
    assert parse_line("  48274   STARLINK-3001   550  \n")["name"] == "STARLINK-3001"


# ---------- parse_line: invalid lines ----------

@pytest.mark.parametrize("line, reason", [
    ("", "too few fields"),
    ("12345 ONLYNAME", "too few fields"),
    ("ABC ISS 408", "ID is not a whole number"),
    ("99999 BADSAT abc", "altitude is not a number"),
    ("54321 NEGSAT -5", "altitude must be positive"),
    ("54321 ZEROSAT 0", "altitude must be positive"),
    ("11111 INFSAT inf", "must be a finite number"),
    ("22222 NANSAT nan", "must be a finite number"),
])
def test_parse_invalid_lines(line, reason):
    with pytest.raises(ValueError, match=reason):
        parse_line(line)


# ---------- read_satellites: the real data file ----------

def test_read_data_file_counts():
    good, bad = read_satellites(INPUT_PATH)
    assert len(good) == 10
    assert len(bad) == 4


def test_skipped_lines_have_number_text_and_reason():
    _, bad = read_satellites(INPUT_PATH)
    for entry in bad:
        assert set(entry) == {"line_number", "line", "reason"}
        assert entry["line_number"] >= 1
        assert entry["reason"]          # not empty


# ---------- build_record and round_record ----------

def test_build_record_iss():
    record = build_record({"id": 25544, "name": "ISS", "altitude_km": 408.0})
    assert set(record) == set(FIELDS)
    assert record["orbit_class"] == "LEO"
    assert record["radius_km"] == pytest.approx(6786.137, abs=0.001)
    assert record["speed_km_s"] == pytest.approx(7.664, abs=0.001)
    assert record["period_min"] == pytest.approx(92.72, abs=0.01)


def test_round_record_does_not_change_original():
    record = build_record({"id": 25544, "name": "ISS", "altitude_km": 408.0})
    rounded = round_record(record)
    assert rounded["speed_km_s"] == round(record["speed_km_s"], 3)
    assert record["speed_km_s"] != rounded["speed_km_s"]   # original keeps full precision


# ---------- file output (tmp_path = temporary folder from pytest) ----------

def test_json_round_trip(tmp_path):
    records = [round_record(build_record(parse_line("25544 ISS 408")))]
    path = tmp_path / "out" / "sats.json"
    save_json(records, str(path))
    assert load_json(str(path)) == records


def test_csv_has_header_and_rows(tmp_path):
    records = [round_record(build_record(parse_line(l)))
               for l in ["25544 ISS 408", "41866 GOES-16 35786"]]
    path = tmp_path / "out" / "sats.csv"
    save_csv(records, str(path))
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert list(rows[0].keys()) == FIELDS
    assert len(rows) == 2
    assert rows[1]["orbit_class"] == "GEO"


def test_load_json_missing_file_returns_none(tmp_path):
    assert load_json(str(tmp_path / "does_not_exist.json")) is None