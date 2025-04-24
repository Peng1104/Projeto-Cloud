"""
The module grepolis_data.py is responsible for fetching and processing data from the Grepolis API.

The module contains the following functions:
    get_players_data: Fetches and processes player data from the Grepolis API,
    returning a DataFrame with the following columns:
    id, name, alliance_id, points, rank, towns, combat_rank, combat_points, attack_rank,
      attack_points, defense_rank, defense_points.
"""
from urllib.parse import unquote_plus
from pandas import DataFrame
import pandas as pd

__GAME_WORLD = "br137"
__COMBAT_COLUMNS = ["rank", "player_id", "points"]
__COMBAT_DYPES = {"rank": int, "player_id": int, "points": int}


def __read_data(url: str, columns: list[str], dtype: dict[str, any]) -> DataFrame:
    """
    Reads data from a CSV file at the given URL with specified columns and data types.

    Args:
        url (str): The URL of the CSV file to read.
        columns (list[str]): A list of column names to use for the DataFrame.
        dtype (dict[str, any]): A dictionary specifying the data type for each column.

    Returns:
        DataFrame: A pandas DataFrame containing the data from the CSV file.
    """
    return pd.read_csv(url, compression="gzip", sep=",", names=columns, dtype=dtype)


def __player_data() -> DataFrame:
    """
    Fetches and processes player data from the specified Grepolis game world.
    Returns:
        DataFrame: A pandas DataFrame containing player data with the following columns:
            - id (int): The player's ID.
            - name (str): The player's name, URL-decoded.
            - alliance_id (int): The ID of the player's alliance, if not in an alliance, -1.
            - points (int): The player's points.
            - rank (int): The player's rank.
            - towns (int): The number of towns the player has.
    """
    data = __read_data(
        f"http://{__GAME_WORLD}.grepolis.com/data/players.txt.gz",
        ["id", "name", "alliance_id", "points", "rank", "towns"],
        {"id": int, "name": str, "alliance_id": float,
            "points": int, "rank": int, "towns": int}
    )
    data['name'] = data['name'].apply(unquote_plus)
    data['alliance_id'] = data['alliance_id'].fillna(-1).astype(int)

    return data


def __player_combat_data() -> DataFrame:
    """
    Fetches and processes player combat data from the Grepolis game world.

    Returns:
        DataFrame: A pandas DataFrame containing the player combat data with columns renamed 
        to 'combat_rank' and 'combat_points'.
    """
    return __read_data(
        f"http://{__GAME_WORLD}.grepolis.com/data/player_kills_all.txt.gz",
        __COMBAT_COLUMNS,
        __COMBAT_DYPES
    ).rename(columns={"rank": "combat_rank", "points": "combat_points"})


def __player_attack_data() -> DataFrame:
    """
    Fetches and processes player attack data from the Grepolis game world.

    This function reads player attack data from a specified URL, processes it,
    and renames certain columns for clarity.

    Returns:
        DataFrame: A pandas DataFrame containing the processed player attack data
        with columns renamed to "attack_rank" and "attack_points".
    """
    return __read_data(
        f"http://{__GAME_WORLD}.grepolis.com/data/player_kills_att.txt.gz",
        __COMBAT_COLUMNS,
        __COMBAT_DYPES
    ).rename(columns={"rank": "attack_rank", "points": "attack_points"})


def __player_defense_data() -> DataFrame:
    """
    Fetches and processes player defense data from the Grepolis game world.

    Returns:
        DataFrame: A pandas DataFrame containing the player defense data with columns
        renamed to "defense_rank" and "defense_points".
    """
    return __read_data(
        f"http://{__GAME_WORLD}.grepolis.com/data/player_kills_def.txt.gz",
        __COMBAT_COLUMNS,
        __COMBAT_DYPES
    ).rename(columns={"rank": "defense_rank", "points": "defense_points"})


def get_players_data() -> DataFrame:
    """
    Retrieve and merge the player data, combat, attack, and defense into a single DataFrame.

    Columns:
    - id (int): The player's ID.
    - name (str): The player's name, URL-decoded.
    - alliance_id (int): The ID of the player's alliance, if not in an alliance, -1.
    - points (int): The player's points.
    - rank (int): The player's rank.
    - towns (int): The number of towns the player has.
    - combat_rank (int): The player's combat rank.
    - combat_points (int): The player's combat points.
    - attack_rank (int): The player's attack rank.
    - attack_points (int): The player's attack points.
    - defense_rank (int): The player's defense rank.
    - defense_points (int): The player's defense points.

    Returns:
        DataFrame: A DataFrame containing merged player data, sorted by rank.
    """
    return __player_data().merge(
        __player_combat_data(),
        left_on="id",
        right_on="player_id",
        how="left"
    ).merge(
        __player_attack_data(),
        left_on="id",
        right_on="player_id",
        how="left",
        suffixes=("", "_atk")
    ).merge(
        __player_defense_data(),
        left_on="id",
        right_on="player_id",
        how="left",
        suffixes=("", "_def")
    ).drop(
        columns=["player_id", "player_id_atk", "player_id_def"]
    ).sort_values(
        by='rank'
    )
