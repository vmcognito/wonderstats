import json
from pathlib import Path
import pytest

from tests.resources import expected_values
from wonderstats.parser import bgatable_to_tablestat, to_tablestat, to_json_str
from wonderstats.bga import load_bga


SKIPIF_COND = False


@pytest.fixture
def resource_path():
    return Path(__file__).parent / "resources"


@pytest.mark.skipif(SKIPIF_COND, reason="Manually skipped.")
def test_bga_v010(resource_path):
    bga = load_bga(resource_path / "bga_v0.1.0.json")
    bgatable = bga.to_bgatable()
    ts = bgatable_to_tablestat(bgatable)
    assert ts.table_id == "732730019"


@pytest.mark.skipif(SKIPIF_COND, reason="Manually skipped.")
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


@pytest.mark.skipif(SKIPIF_COND, reason="Manually skipped.")
def test_abandoned_bga_v010(resource_path):
    bga = load_bga(resource_path / "bga_abandoned_game_v0.1.2.json")
    bgatable = bga.to_bgatable()
    ts = bgatable_to_tablestat(bgatable)
    assert ts.table_id == "729690472"


@pytest.mark.skipif(SKIPIF_COND, reason="Manually skipped.")
def test_to_json_str(resource_path):
    bga = load_bga(resource_path / "bga_v0.1.0.json")
    bgatable = bga.to_bgatable()
    ts = bgatable_to_tablestat(bgatable)

    ts_string = to_json_str(ts)    
    assert ts_string == expected_values.ts_str
    assert ts == to_tablestat(json.loads(ts_string))


@pytest.mark.skipif(SKIPIF_COND, reason="Manually skipped.")
def test_to_ts_from_bga_old_data(resource_path):
    bga = load_bga(resource_path / "bga_old_data.json")
    bgatable = bga.to_bgatable()
    ts = bgatable_to_tablestat(bgatable)
    assert ts.table_id == "329371663"


@pytest.mark.skipif(SKIPIF_COND, reason="Manually skipped.")
def test_parsing_v015(resource_path):
    bga = load_bga(resource_path / "bga_v0.1.5.json")
    bgatable = bga.to_bgatable()
    ts = bgatable_to_tablestat(bgatable)
    assert ts.table_id == "712162886"