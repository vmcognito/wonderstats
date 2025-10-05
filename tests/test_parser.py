import json
from pathlib import Path
import pytest

from wonderstats.parser import bgatable_to_tablestat, to_tablestat
from wonderstats.bga import load_bga


@pytest.fixture
def resource_path():
    return Path(__file__).parent / "resources"


def test_bga_v010(resource_path):
    bga = load_bga(resource_path / "bga_v0.1.0.json")
    bgatable = bga.to_bgatable()
    ts = bgatable_to_tablestat(bgatable)
    assert ts.table_id == "732730019"


def test_ts_v010(resource_path):
    with open(resource_path / "ts_v0.1.0.json", "r", encoding="utf-8") as f:
        ts_json_str = f.read()
        ts_json = json.loads(ts_json_str)
        assert ts_json["table_id"] == "732730019"

        player1 = ts_json["player1"]
        assert player1["player_id"] == "95265981"

        player2 = ts_json["player2"]
        assert player2["player_id"] == "96573208"
    
    ts = to_tablestat(ts_json)
    assert ts.table_id == "732730019"

    assert ts.player1.player_id == "95265981"
    assert ts.player1.wonders[0].id == 0

    assert ts.player2.player_id == "96573208"
    assert ts.player2.wonders[0].id == 7
