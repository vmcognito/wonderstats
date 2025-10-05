from dataclasses import dataclass
from datetime import datetime
import json

from wonderstats.bga import parser


@dataclass
class BGATable:
    table_id: str
    time_start: datetime
    time_end: datetime
    went_first: str
    elos: dict
    results: dict
    wonders: dict
    pantheon: bool
    agora: bool
    players: dict


@dataclass
class BGAData:
    table_json: dict
    replay_html: str

    @property
    def table_id(self) -> str:
        return self.table_json["data"]["id"]

    def to_bgatable(self) -> BGATable:
        table_data = self.table_json["data"]
        table_result = table_data["result"]
        table_options = table_data["options"]
        for key in table_options:
            option = table_options[key]
            if option["name"] == "Expansion: Pantheon":
                pantheon = option["values"][int(option["value"])]["name"] == "Yes"
            if option["name"] == "Expansion: Agora":
                agora= option["values"][int(option["value"])]["name"] == "Yes"

        bga_table = BGATable(
            **parser.parse_replay_html(self.replay_html),
            table_id=self.table_id,
            time_start=parser.format_datetime(table_result["time_start"]),
            time_end=parser.format_datetime(table_result["time_end"]),
            pantheon=pantheon,
            agora=agora
        )
        return bga_table


def load_bga(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        file_content = f.read()
        return BGAData(**json.loads(file_content))
