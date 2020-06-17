"""Provides test for the Question class methods."""

from question_game.question import Question


def test_get_mask_1():
    qa_pair = Question(('John, Paul II.', 'Иоанн, Павел II.'))
    qa_pair.add_guess(guess='текст')
    res = qa_pair._get_mask()
    assert res == '-----, ----- II.'


def test_get_mask_2():
    q = 'Cuba used to be the Caribbean gem'
    a = 'Когда-то Куба была жемчужиной Карибского моря'
    guess = 'Куба было жемчужиной Карибского бассейна'
    qa_pair = Question((q, a))
    qa_pair.add_guess(guess)
    res = qa_pair._get_mask()
    assert 'когда-то' not in res.lower()


def test_calc_score():
    question = Question(('John, Paul II.', 'Иоанн, Павел II.'))
    res = question._calc_score('Павел')
    assert isinstance(res, float)
    res = question._calc_score('')
    assert isinstance(res, float)
