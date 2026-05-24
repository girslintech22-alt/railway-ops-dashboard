import json
from pathlib import Path

from processing.route_processor import (
    extract_route_data,
    process_all_route_snapshots,
    save_processed_route_data,
)


def load_sample_snapshot() -> dict:
    sample_path = Path("data/raw/sample1.json")
    return json.loads(sample_path.read_text(encoding="utf-8"))


def test_valid_route_extraction() -> None:
    snapshot = load_sample_snapshot()
    records = extract_route_data(snapshot)

    assert records
    first = records[0]
    assert first["trainNumber"] == "12951"
    assert first["trainName"] == "New Delhi Tejas Rajdhani Express"
    assert first["trainType"] == "Rajdhani Express"
    assert "stationCode" in first


def test_missing_optional_fields() -> None:
    snapshot = {
        "data": {
            "train": {"trainNumber": "11111", "trainName": "Test", "type": "Express"},
            "route": [
                {
                    "sequence": 1,
                    "stationCode": "ABC",
                    "stationName": "Alpha",
                    "isHalt": 1,
                    "day": 1,
                }
            ],
        }
    }

    records = extract_route_data(snapshot)
    assert len(records) == 1
    assert records[0]["scheduledArrival"] is None
    assert records[0]["platform"] is None


def test_malformed_route_payloads() -> None:
    malformed = {"data": {"train": {"trainNumber": "12951"}, "route": "bad-type"}}
    records = extract_route_data(malformed)
    assert records == []


def test_duplicate_prevention() -> None:
    snapshot = {
        "data": {
            "train": {"trainNumber": "22222", "trainName": "Dup Train", "type": "Rajdhani"},
            "route": [
                {"sequence": 1, "stationCode": "AAA", "stationName": "A", "day": 1},
                {"sequence": 1, "stationCode": "AAA", "stationName": "A", "day": 1},
            ],
        }
    }
    records = extract_route_data(snapshot)
    assert len(records) == 1


def test_processed_output_generation(tmp_path: Path) -> None:
    output_file = tmp_path / "route_segments.json"

    snapshot = load_sample_snapshot()
    records = extract_route_data(snapshot)
    save_processed_route_data(records, str(output_file))

    assert output_file.exists()
    loaded = json.loads(output_file.read_text(encoding="utf-8"))
    assert isinstance(loaded, list)
    assert loaded


def test_process_all_route_snapshots_local_files(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    sample = load_sample_snapshot()
    (raw_dir / "sample.json").write_text(json.dumps(sample), encoding="utf-8")

    output_file = tmp_path / "processed" / "route_segments.json"
    records = process_all_route_snapshots(raw_dir=raw_dir, output_path=str(output_file))

    assert output_file.exists()
    assert records
