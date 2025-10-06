
from wonderstats import STATS_LABEL, PlayerStat, TableStat, Wonder
from wonderstats.bga import BGATable


def bgatable_to_tablestat(bgatable: BGATable):
    players = _get_players_stats(bgatable)
    winner_array = [player for player in players if player.is_winner]
    winner = None
    if winner_array.count == 1:
        winner = winner_array[0].player_id

    return TableStat(
        bgatable.table_id,
        players[0],
        players[1],
        winner, 
        bgatable.time_start,
        bgatable.time_end,
        _get_game_type(bgatable)
    )

def _get_players_stats(bgatable: BGATable):
    players = {}
    for stat in bgatable.results:
        player_id = stat["id"]
        player_name = stat["name"]
        values_by_stats_label = {
            field : 0 if str(key) not in stat["stats"] else int(stat["stats"][str(key)])
            for key, field in STATS_LABEL.items()
        }

        wonders_dict = []
        if player_name in bgatable.wonders:
            wonders_dict = bgatable.wonders[player_name]

        player = PlayerStat(
            player_id=player_id,
            player_name=player_name,
            elo=bgatable.elos[player_name],
            went_first=bgatable.went_first == player_name,
            draw=stat["tie"],
            wonders=[Wonder.from_name(wonder) for wonder in wonders_dict],
            **values_by_stats_label
        )
        players[player_name] = player

    return [players[name] for name in sorted(players.keys())]

def _get_game_type(bgatable: BGATable):
    game_type = []
    if bgatable.agora:
        game_type.append("A")
    if bgatable.pantheon:
        game_type.append("P")
    
    if len(game_type) == 0:
        game_type = ["B"]

    return "".join(game_type)


def to_tablestat(ts_json):
    player1_json = ts_json.pop("player1")
    player2_json = ts_json.pop("player2")

    wonders1_json = player1_json.pop("wonders")
    wonders2_json = player2_json.pop("wonders")

    wonders1 = [Wonder(**w) for w in wonders1_json]
    wonders2 = [Wonder(**w) for w in wonders2_json]

    ts = TableStat(
        **ts_json,
        player1=PlayerStat(**player1_json, wonders=wonders1),
        player2=PlayerStat(**player2_json, wonders=wonders2)
    )
    
    return ts