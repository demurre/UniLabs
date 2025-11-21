import random
from typing import List, Tuple, Dict
from datetime import datetime, timedelta


class SecurityQuestion:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer.lower().strip()

    def check_answer(self, provided_answer: str) -> bool:
        """Checks the user's answer."""
        return provided_answer.lower().strip() == self.answer


SECURITY_QUESTIONS = [
    SecurityQuestion("What is your favorite number?", "1"),
    SecurityQuestion("When did you approximately create your account (year)?", "2025"),
    SecurityQuestion("City where you were born?", "City"),
    SecurityQuestion("Favorite sport?", "Basketball"),
    SecurityQuestion("What is your favorite day of the week?", "RPG"),
    SecurityQuestion("What is your favorite day of the week?", "Sunday"),
    SecurityQuestion("Favorite color?", "White"),
    SecurityQuestion("Favorite season?", "Summer"),
    SecurityQuestion("Favorite season?", "Electro"),
    SecurityQuestion("Year you graduated from school?", "2022"),
]


class QuestionSession:
    """Question answering session with retry timer."""

    REPEAT_PERIOD_MINUTES = 3

    QUESTIONS_PER_ITERATION = 4

    def __init__(self, username: str):
        self.username = username
        self.current_questions: List[SecurityQuestion] = []
        self.correct_answers = 0
        self.session_start_time = None
        self.last_session_time = None
        self.select_random_questions()

    def select_random_questions(self):
        """Selects 4 random questions from 10."""
        self.current_questions = random.sample(
            SECURITY_QUESTIONS, self.QUESTIONS_PER_ITERATION
        )
        self.correct_answers = 0

    def can_start_new_session(self) -> bool:
        """Checks if the retry period (3 minutes) has passed."""
        if self.last_session_time is None:
            return True

        time_passed = datetime.now() - self.last_session_time
        return time_passed >= timedelta(minutes=self.REPEAT_PERIOD_MINUTES)

    def start_session(self) -> bool:
        """Starts a new question session."""
        if not self.can_start_new_session():
            time_left = (
                self.last_session_time
                + timedelta(minutes=self.REPEAT_PERIOD_MINUTES)
                - datetime.now()
            )
            minutes = int(time_left.total_seconds() / 60)
            seconds = int(time_left.total_seconds() % 60)
            return False, f"Wait {minutes}m {seconds}s before next iteration"

        self.select_random_questions()
        self.session_start_time = datetime.now()
        return True, "Question session started"

    def submit_answer(self, question_index: int, answer: str) -> Tuple[bool, str]:
        """Checks the answer to a question."""
        if question_index < 0 or question_index >= len(self.current_questions):
            return False, "Invalid question index"

        question = self.current_questions[question_index]
        if question.check_answer(answer):
            self.correct_answers += 1
            return True, "Correct!"
        else:
            return False, f"Incorrect. Correct answer: {question.answer}"

    def end_session(self) -> Tuple[int, int, bool]:
        """Ends the session and returns the results."""
        self.last_session_time = datetime.now()
        passed = self.correct_answers >= (self.QUESTIONS_PER_ITERATION * 0.75)
        return self.correct_answers, self.QUESTIONS_PER_ITERATION, passed

    def get_current_question(self) -> Dict:
        """Returns the current question for answering."""
        if not self.current_questions:
            return {"error": "No questions available"}

        question = self.current_questions[0]
        return {
            "text": question.question,
            "total": len(self.current_questions),
            "current": 1,
        }

    def get_remaining_time(self) -> int:
        """Returns the remaining time until the next allowed session (in seconds)."""
        if self.last_session_time is None:
            return 0

        time_passed = datetime.now() - self.last_session_time
        remaining = timedelta(minutes=self.REPEAT_PERIOD_MINUTES) - time_passed

        if remaining.total_seconds() <= 0:
            return 0
        return int(remaining.total_seconds())


class QuestionManager:
    """Manager for question sessions for multiple users."""

    def __init__(self):
        self.sessions: Dict[str, QuestionSession] = {}

    def get_session(self, username: str) -> QuestionSession:
        """Gets or creates a session for the user."""
        if username not in self.sessions:
            self.sessions[username] = QuestionSession(username)
        return self.sessions[username]

    def start_session(self, username: str) -> Tuple[bool, str]:
        """Starts a new question session for the user."""
        session = self.get_session(username)
        return session.start_session()

    def submit_answer(self, username: str, question_index: int, answer: str):
        """Submits an answer to a question."""
        session = self.get_session(username)
        return session.submit_answer(question_index, answer)

    def end_session(self, username: str):
        """Ends the question session."""
        session = self.get_session(username)
        return session.end_session()

    def verify_user_security(self, username: str) -> Tuple[bool, str]:
        """
        Verifies the user through the security system.
        Returns (passed, message)
        """
        session = self.get_session(username)

        can_start, message = session.start_session()
        if not can_start:
            return False, message

        return True, "Session ready to launch"


question_manager = QuestionManager()
