from datetime import datetime
import re
import json
from bs4 import BeautifulSoup


def get_wonders(game_logs):
    wonders = {}

    pattern = r"'(.*)(( gets the last Wonder of the round )|( selected Wonder ))“(.*)”'"
    for log in game_logs:
        match = re.search(pattern, log)
        if match:
            player_name = match.group(1)
            wonder_name = match.group(5)
            player_wonders = []
            if player_name in wonders:
                player_wonders = wonders[player_name]
            player_wonders.append(wonder_name.replace('The ', ''))
            wonders[player_name] = player_wonders

    return wonders


def parse_replay_html(replay_html_content: str):
    replay_soup = BeautifulSoup(replay_html_content, features="html.parser")
    replay_dict = {}

    game_logs: list[str] = list(map(lambda string: repr(string), replay_soup.find(id="replaylogs").strings))
    replay_dict["wonders"] = get_wonders(game_logs)
    replay_dict["went_first"] = get_went_first(game_logs)
    elos = get_elos(replay_soup)
    
    results_dict = None
    for script in replay_soup.find_all("script"):
        stats_line = script.find(string=re.compile('"stats"'))
        if stats_line:
            gamelogs_line = re.search(r'g_archive_mode = (.*);g_gamelogs = (.*)', stats_line).group(2)
            results_value = re.search(r'"result"\:(\[[^\]]*\])', gamelogs_line).group(1)
            results_dict = json.loads(results_value)
            break
    
    if results_dict is None:
        raise Exception("Error getting game stats.")

    replay_dict["results"] = results_dict
    replay_dict["elos"] = { result["name"] : elos[f"player_elo_{result["player"]}"] for result in results_dict }
    replay_dict["players"] = [{ "player_id" : result["player"], "name" : result["name"] } for result in results_dict ]
    return replay_dict


def get_elos(replay_soup):
    return { elo_span.get("id"): int(elo_span.text) for elo_span in replay_soup.find_all(class_="gamerank_value") }


def get_went_first(game_logs):
    went_first = None
    for log in game_logs:
        m = re.search(r"'(.*) selected Wonder", log)
        if m:
            went_first = m.group(1)
            break
    
    if not went_first:
        raise Exception("Error getting 'went_first' data.")
    return went_first


def format_datetime(datetime_str):
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

