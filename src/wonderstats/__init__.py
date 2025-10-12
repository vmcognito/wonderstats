from dataclasses import dataclass
from datetime import datetime


STATS_LABEL = {
    1:  "thinking_time",
    10: "number_of_turns",

    20: "civilian_victory",
    30: "science_victory",
    40: "military_victory",
    42: "political_victory",

    50: "victory_points",

    60: "vp_from_blue",
    70: "vp_from_green",
    80: "vp_from_yellow",
    90: "vp_from_purple",
    95: "vp_from_divinities",
    100: "vp_from_wonders",
    110: "vp_from_progress",
    120: "vp_from_coins",
    130: "vp_from_military",
    135: "vp_from_senate",
}


@dataclass
class Wonder:
    WONDERS = [
        'Appian Way',
        'Circus Maximus',
        'Colossus',
        'Curia Julia',
        'Divine Theater',
        'Great Library',
        'Great Lighthouse',
        'Hanging Gardens',
        'Knossos',
        'Mausoleum',
        'Piraeus',
        'Pyramids',
        'Sanctuary',
        'Sphinx',
        'Statue of Zeus',
        'Temple of Artemis'
    ]

    id: int
    name: str

    @classmethod
    def from_name(cls, name):
        id = Wonder.WONDERS.index(name)
        return Wonder(id, name)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)


@dataclass
class PlayerStat:
    player_id: str
    player_name: str

    elo: int
    went_first: bool
    thinking_time: int
    number_of_turns: int    
    
    draw: bool
    civilian_victory: bool
    science_victory: bool
    military_victory: bool
    political_victory: bool

    victory_points: int

    vp_from_blue: int
    vp_from_green: int
    vp_from_yellow: int
    vp_from_purple: int
    vp_from_divinities: int
    vp_from_wonders: int
    vp_from_progress: int
    vp_from_coins: int
    vp_from_military: int
    vp_from_senate: int

    wonders: list[Wonder]

    @property
    def is_winner(self):
        return self.civilian_victory or self.science_victory or self.military_victory or self.political_victory

    def __post_init__(self):
        self.civilian_victory = bool(self.civilian_victory)
        self.science_victory = bool(self.science_victory)
        self.military_victory = bool(self.military_victory)
        self.political_victory = bool(self.political_victory)


@dataclass
class TableStat:
    table_id: int
    player1: PlayerStat
    player2: PlayerStat
    winner: str
    time_start: datetime
    time_end: datetime
    game_type: str

    def __post_init__(self):
        self.time_start = self.time_start if isinstance(self.time_start, datetime) else self._format_date(self.time_start)
        self.time_end = self.time_end if isinstance(self.time_end, datetime) else self._format_date(self.time_end)

    def _format_date(self, date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except: pass
        try:
            return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
        except:
            raise Exception(f"Unexpected date format: {date_str}")
