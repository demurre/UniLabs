import json
import os
from datetime import datetime, timedelta
from typing import Tuple, Dict, Optional
from captcha_generator import captcha_generator


class CaptchaSession:
    """
    User CAPTCHA session.
    """

    RETRY_DELAY_SECONDS = 300

    MAX_ATTEMPTS = 3

    def __init__(self, username: str):
        self.username = username
        self.captcha_text = None
        self.session_start_time = None
        self.last_verification_time = None
        self.attempts_count = 0
        self.is_verified = False
        self.generate_new_captcha()

    def generate_new_captcha(self) -> None:
        """Generates new CAPTCHA."""
        image, text = captcha_generator.generate()
        self.captcha_text = text
        self.attempts_count = 0
        self.is_verified = False

    def can_retry_captcha(self) -> bool:
        """Checks if user can retry CAPTCHA verification."""
        if self.last_verification_time is None:
            return True

        time_passed = datetime.now() - self.last_verification_time
        return time_passed >= timedelta(seconds=self.RETRY_DELAY_SECONDS)

    def get_retry_remaining_time(self) -> int:
        """
        Returns remaining time until next CAPTCHA retry (in seconds).
        0 means retry is allowed.
        """
        if self.last_verification_time is None:
            return 0

        time_passed = datetime.now() - self.last_verification_time
        remaining = timedelta(seconds=self.RETRY_DELAY_SECONDS) - time_passed

        if remaining.total_seconds() <= 0:
            return 0
        return int(remaining.total_seconds())

    def verify_captcha(self, user_input: str) -> Tuple[bool, str]:
        """
        Verifies text entered by user for CAPTCHA.
        Returns (success, message)
        """
        self.attempts_count += 1

        if captcha_generator.verify(user_input):
            self.is_verified = True
            self.last_verification_time = datetime.now()
            return True, "CAPTCHA verified successfully!"

        remaining_attempts = self.MAX_ATTEMPTS - self.attempts_count

        if remaining_attempts <= 0:
            self.generate_new_captcha()
            return False, "Maximum attempts exhausted. Generating new CAPTCHA."

        return False, f"Incorrect. Remaining attempts: {remaining_attempts}"

    def can_attempt_verification(self) -> bool:
        """Checks if there are attempts available for CAPTCHA input."""
        return self.attempts_count < self.MAX_ATTEMPTS

    def start_session(self) -> Tuple[bool, str]:
        """
        Starts new CAPTCHA verification session.
        Checks retry timer.
        """
        if not self.can_retry_captcha():
            remaining = self.get_retry_remaining_time()
            minutes = remaining // 60
            seconds = remaining % 60
            return (
                False,
                f"Wait {minutes}m {seconds}s before next CAPTCHA verification",
            )

        self.generate_new_captcha()
        self.session_start_time = datetime.now()
        return True, "CAPTCHA session started"


class CaptchaManager:
    """
    Manager for handling CAPTCHA sessions for multiple users.
    """

    def __init__(self, data_file: str = "captcha_sessions.json"):
        self.data_file = data_file
        self.sessions: Dict[str, CaptchaSession] = {}
        self._load_sessions()

    def _load_sessions(self) -> None:
        """Loads session data from file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for username in data.keys():
                        self.sessions[username] = CaptchaSession(username)
            except (IOError, json.JSONDecodeError):
                pass

    def _save_sessions(self) -> None:
        """Saves session data to file."""
        data = {}
        for username, session in self.sessions.items():
            data[username] = {
                "last_verification_time": (
                    session.last_verification_time.isoformat()
                    if session.last_verification_time
                    else None
                ),
                "is_verified": session.is_verified,
            }

        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def get_session(self, username: str) -> CaptchaSession:
        """Gets or creates CAPTCHA session for user."""
        if username not in self.sessions:
            self.sessions[username] = CaptchaSession(username)
        return self.sessions[username]

    def start_verification(self, username: str) -> Tuple[bool, str]:
        """
        Starts CAPTCHA verification for user.
        Returns (success, message)
        """
        session = self.get_session(username)
        success, message = session.start_session()

        if success:
            self._save_sessions()

        return success, message

    def verify_captcha(self, username: str, user_input: str) -> Tuple[bool, str]:
        """
        Verifies user CAPTCHA input.
        Returns (success, message)
        """
        session = self.get_session(username)
        success, message = session.verify_captcha(user_input)

        if success:
            self._save_sessions()

        return success, message

    def is_verified(self, username: str) -> bool:
        """Checks if user has passed CAPTCHA verification in current session."""
        session = self.get_session(username)
        return session.is_verified

    def get_captcha_image(self, username: str):
        """Returns current CAPTCHA image for user."""
        session = self.get_session(username)
        return captcha_generator.get_current_image()

    def reset_session(self, username: str) -> None:
        """Resets user session."""
        if username in self.sessions:
            self.sessions[username] = CaptchaSession(username)
            self._save_sessions()


captcha_manager = CaptchaManager()
