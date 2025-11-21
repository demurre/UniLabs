import json
import os
from datetime import datetime, timedelta
from typing import Tuple, Dict


class DemowareManager:
    """
    Manager for handling Demoware limitations.

    Functionality:
    - Get information about demo version status
    - Check time limitations
    - Get list of available features
    - User count limitations
    - Functionality limitations
    """

    DEMOWARE_CONFIG = {
        "type": "Demoware",
        "max_users": 6,  # Maximum 6 users
        "max_sessions_per_day": 10,  # Maximum 10 sessions per day
        "session_duration_minutes": 30,  # Duration of one session
        "file_format_restriction": "BMP",  # Only BMP files
        "encryption_algorithm": "Vigenere",  # Encryption algorithm
    }

    AVAILABLE_FEATURES = {
        "authentication": {
            "enabled": True,
            "description": "User authentication",
            "limitation": "Maximum 6 users",
        },
        "password_change": {
            "enabled": True,
            "description": "Password change",
            "limitation": "No limitations",
        },
        "security_questions": {
            "enabled": True,
            "description": "Security system (questions)",
            "limitation": "3 min retry period",
        },
        "access_control": {
            "enabled": True,
            "description": "Access level management",
            "limitation": "3 levels (USER, MODERATOR, ADMIN)",
        },
        "file_upload": {
            "enabled": True,
            "description": "File upload",
            "limitation": "BMP format only",
        },
        "encryption": {
            "enabled": True,
            "description": "Data encryption",
            "limitation": "Vigenere cipher",
        },
        "user_management": {
            "enabled": True,
            "description": "User management",
            "limitation": "Maximum 6 users",
        },
        "advanced_analytics": {
            "enabled": False,
            "description": "Advanced analytics",
            "limitation": "Not available in demo version",
        },
        "bulk_import": {
            "enabled": False,
            "description": "Bulk data import",
            "limitation": "Not available in demo version",
        },
        "api_access": {
            "enabled": False,
            "description": "API access",
            "limitation": "Not available in demo version",
        },
    }

    def __init__(self, data_file: str = "demoware_sessions.json"):
        """Initializes Demoware manager."""
        self.data_file = data_file
        self.sessions = self._load_sessions()

    def _load_sessions(self) -> Dict:
        """Loads session data."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError):
                return {}
        return {}

    def _save_sessions(self) -> None:
        """Saves session data."""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.sessions, f, ensure_ascii=False, indent=2)

    def get_demoware_info(self) -> Dict:
        """Returns information about demo version."""
        return {
            "type": self.DEMOWARE_CONFIG["type"],
            "max_users": self.DEMOWARE_CONFIG["max_users"],
            "max_sessions_per_day": self.DEMOWARE_CONFIG["max_sessions_per_day"],
            "session_duration_minutes": self.DEMOWARE_CONFIG[
                "session_duration_minutes"
            ],
            "file_format_restriction": self.DEMOWARE_CONFIG["file_format_restriction"],
            "encryption_algorithm": self.DEMOWARE_CONFIG["encryption_algorithm"],
        }

    def start_session(self, username: str) -> Tuple[bool, str]:
        """
        Starts new session for user.
        Checks daily session limit.
        """
        today = datetime.now().strftime("%Y-%m-%d")

        if username not in self.sessions:
            self.sessions[username] = {}

        user_sessions = self.sessions[username]
        today_sessions = [s for s in user_sessions.values() if s.get("date") == today]

        if len(today_sessions) >= self.DEMOWARE_CONFIG["max_sessions_per_day"]:
            return (
                False,
                f"Exceeded daily session limit ({self.DEMOWARE_CONFIG['max_sessions_per_day']})",
            )

        session_id = f"{username}_{len(user_sessions)}"
        self.sessions[username][session_id] = {
            "start_time": datetime.now().isoformat(),
            "date": today,
            "status": "active",
        }
        self._save_sessions()

        return (
            True,
            f"Session started. Duration: {self.DEMOWARE_CONFIG['session_duration_minutes']} minutes",
        )

    def end_session(self, username: str, session_id: str) -> Tuple[bool, str]:
        """Ends user session."""
        if username in self.sessions and session_id in self.sessions[username]:
            self.sessions[username][session_id]["status"] = "closed"
            self.sessions[username][session_id]["end_time"] = datetime.now().isoformat()
            self._save_sessions()
            return True, "Session ended"
        return False, "Session not found"

    def check_file_format(self, filepath: str) -> Tuple[bool, str]:
        """Checks if file has allowed format (BMP)."""
        if not filepath.lower().endswith(".bmp"):
            return (
                False,
                f"File must be in {self.DEMOWARE_CONFIG['file_format_restriction']} format",
            )
        return True, "File format is supported"

    def get_available_features(self) -> Dict:
        """Returns list of available features in demo version."""
        enabled_features = {
            name: feature
            for name, feature in self.AVAILABLE_FEATURES.items()
            if feature["enabled"]
        }
        return enabled_features

    def get_disabled_features(self) -> Dict:
        """Returns list of unavailable features in demo version."""
        disabled_features = {
            name: feature
            for name, feature in self.AVAILABLE_FEATURES.items()
            if not feature["enabled"]
        }
        return disabled_features

    def is_feature_enabled(self, feature_name: str) -> bool:
        """Checks if feature is enabled."""
        return self.AVAILABLE_FEATURES.get(feature_name, {}).get("enabled", False)

    def get_feature_info(self, feature_name: str) -> Dict:
        """Returns information about feature."""
        return self.AVAILABLE_FEATURES.get(feature_name, {})

    def get_session_count_today(self, username: str) -> int:
        """Returns number of user sessions today."""
        today = datetime.now().strftime("%Y-%m-%d")
        if username not in self.sessions:
            return 0

        today_sessions = [
            s for s in self.sessions[username].values() if s.get("date") == today
        ]
        return len(today_sessions)

    def get_remaining_sessions_today(self, username: str) -> int:
        """Returns number of remaining sessions today."""
        used = self.get_session_count_today(username)
        remaining = self.DEMOWARE_CONFIG["max_sessions_per_day"] - used
        return max(0, remaining)

    def get_demo_status_message(self, username: str) -> str:
        """Returns demo version status message."""
        remaining = self.get_remaining_sessions_today(username)
        return (
            f"Demoware version\n"
            f"Users: 1/{self.DEMOWARE_CONFIG['max_users']}\n"
            f"Sessions today: {self.get_session_count_today(username)}"
            f"/{self.DEMOWARE_CONFIG['max_sessions_per_day']}\n"
            f"Remaining: {remaining} sessions\n"
            f"Session duration: {self.DEMOWARE_CONFIG['session_duration_minutes']} minutes"
        )


demoware_manager = DemowareManager()
