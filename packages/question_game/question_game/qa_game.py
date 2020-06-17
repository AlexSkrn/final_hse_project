"""This module contains a class to handle a user-provided bitext."""
import io

from question_game.question import Question


class QAGame:
    """Provide a class to keep the state of the game of questions."""

    def __init__(self):
        self._questions = []
        self._cur_q_idx = -1
        self.filename = ''
        self._selected_topics = []

    def set_topics(self, topics=None, reset=False):
        if topics:
            if reset and isinstance(topics, str):
                self._selected_topics = [topics]
            elif reset and isinstance(topics, list):
                self._selected_topics = topics
            elif isinstance(topics, str):
                self._selected_topics.append(topics)
            elif isinstance(topics, list):
                self._selected_topics.extend(topics)
        elif reset:
            self._selected_topics = []
            self._questions = []
            self._cur_q_idx = -1

    def get_topics(self):
        return self._selected_topics

    def add_bitext_from_list(self, bitext: list, filename: str):
        self._questions = [Question(q) for q in bitext]
        self._cur_q_idx = -1
        self.set_topics(filename, reset=True)
        self.filename = filename

    def _add_question(self, qa):
        """Add a qa pair to questions list."""
        self._questions.append(Question(qa))

    def get_question(self, online_qa=None):
        if online_qa:
            self._add_question(online_qa)
        self._cur_q_idx += 1
        try:
            q = self._questions[self._cur_q_idx].get_status(answer=False)
        except IndexError:
            return []
        return q

    def evaluate_guess(self, guess: str) -> dict:
        """Return a dict ( 'Q': '', 'GuessMask': [] ) ]."""
        try:
            self._questions[self._cur_q_idx].add_guess(guess.strip())
        except IndexError:
            return {}
            # raise
        else:
            return self._questions[self._cur_q_idx].get_status(answer=False)

    def show_answer(self) -> list:
        if self._cur_q_idx == -1:
            return []
        try:
            return self._questions[self._cur_q_idx].get_status(answer=True)
        except IndexError:
            return []

    def get_printable_report(self) -> list:
        return [q.get_status_tab_delim()
                for q in self._questions[:self._cur_q_idx + 1]
                ]

    def get_bytes_io_object(self, data: list):   # move outside?
        str_io_obj = io.StringIO()
        for question in data:
            str_io_obj.write(question)
            str_io_obj.write('\n')

        byte_io_obj = io.BytesIO()
        byte_io_obj.write(str_io_obj.getvalue().encode('utf-8'))
        byte_io_obj.seek(0)

        str_io_obj.close()

        return byte_io_obj

    def get_bytes_io_report(self):
        """Return a bytesIO object containing the report."""
        return self.get_bytes_io_object(self.get_printable_report())
