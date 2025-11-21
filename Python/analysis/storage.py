import json
import os
from typing import Dict

DATA_FILE = "users.json"

ACCESS_LEVELS = {0: "USER", 1: "MODERATOR", 2: "ADMIN"}


def make_initial_data() -> Dict:
    """
    Creates initial data with 6 users and 3 access levels.
    """
    return {
        "ADMIN": {
            "password": "",
            "locked": False,
            "restriction": True,
            "access_level": 2,  # ADMIN
            "questions_completed": 0,
        },
        "moderator1": {
            "password": "",
            "locked": False,
            "restriction": True,
            "access_level": 1,  # MODERATOR
            "questions_completed": 0,
        },
        "user1": {
            "password": "",
            "locked": False,
            "restriction": True,
            "access_level": 0,  # USER
            "questions_completed": 0,
        },
        "user2": {
            "password": "",
            "locked": False,
            "restriction": True,
            "access_level": 0,  # USER
            "questions_completed": 0,
        },
        "user3": {
            "password": "",
            "locked": False,
            "restriction": True,
            "access_level": 0,  # USER
            "questions_completed": 0,
        },
        "user4": {
            "password": "",
            "locked": False,
            "restriction": True,
            "access_level": 0,  # USER
            "questions_completed": 0,
        },
    }


def load_data(path: str = DATA_FILE) -> Dict:
    """Loads data from JSON file."""
    if not os.path.exists(path):
        data = make_initial_data()
        save_data(data, path)
        return data
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: Dict, path: str = DATA_FILE) -> None:
    """Saves data to JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_access_level_name(level: int) -> str:
    """Returns access level name."""
    return ACCESS_LEVELS.get(level, "UNKNOWN")


def get_user_access_level(data: Dict, username: str) -> int:
    """Returns user access level."""
    if username in data:
        return data[username].get("access_level", 0)
    return -1


def set_user_access_level(data: Dict, username: str, level: int) -> bool:
    """Changes user access level."""
    if username in data and level in ACCESS_LEVELS:
        data[username]["access_level"] = level
        return True
    return False
