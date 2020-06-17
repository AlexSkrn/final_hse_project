"""Provide tests for the Game class methods."""

import pytest

from question_game.qa_game import QAGame


def test_init():
    game = QAGame()
    assert game._questions == []
    assert game._cur_q_idx == -1


def test_game():
    q1 = [("As a photographer he favors", "Он фотограф и предпочитает")]
    game = QAGame()
    game.add_bitext_from_list(q1, 'somefilename')
    expected = {'Q': "As a photographer he favors",
                'A': '',
                'GuessMask': []
                }
    assert game.get_question() == expected


def test_get_question_returns_empty_list():
    q1 = [("As a photographer he favors", "Он фотограф и предпочитает")]
    game = QAGame()
    game.add_bitext_from_list(q1, 'somefilename')
    game.get_question()
    assert game.get_question() == []


# def test_eval_guess_returns_none():
#     game = QAGame()
#     with pytest.raises(IndexError):
#         res = game.evaluate_guess("Как фотограф он предпочитает")
    # expected = {'Q': '', 'A': '', 'GuessMask': []}
    # assert res == expected


def test_eval_guess():
    q1 = [("As a photographer he favors",
           "Он фотограф и предпочитает")
          ]
    game = QAGame()
    game.add_bitext_from_list(q1, 'somefilename')
    res = game.evaluate_guess("Он предпочитает")

    assert res['Q'] == "As a photographer he favors"
    assert res['A'] == ''  # empty string
    assert "Он предпочитает" in res['GuessMask'][0]
    assert "предпочитает" in res['GuessMask'][1]
    assert "портрет" not in res['GuessMask'][1]
    assert "-" in res['GuessMask'][1]


def test_get_questiomn_online_qa_returns_question():
    random_qa_pair = ('In his letter, John Paul II',
                      'В своем письме Иоанн Павел I'
                      )
    game = QAGame()
    res = game.get_question(online_qa=random_qa_pair)
    assert res == [random_qa_pair[0]]


def test_get_questiomn_online_qa_returns_question():
    random_qa_pair = ('In his letter, John Paul II',
                      'В своем письме Иоанн Павел I'
                      )
    game = QAGame()
    res = game.get_question(online_qa=random_qa_pair)
    expected = {'Q': random_qa_pair[0],
                'A': '',
                'GuessMask': []
                }
    assert res == expected


def test_get_questiomn_online_qa_updates_index():
    random_qa_pair = ('In his letter, John Paul II',
                      'В своем письме Иоанн Павел I'
                      )
    game = QAGame()
    game.get_question(online_qa=random_qa_pair)
    assert game._cur_q_idx == 0


def test_get_question_saves_question_object():
    random_qa_pair = ('In his letter, John Paul II',
                      'В своем письме Иоанн Павел I'
                      )
    game = QAGame()
    game.get_question(online_qa=random_qa_pair)
    assert game._questions[0]._question == 'In his letter, John Paul II'
    assert game._questions[0]._ref_trans == 'В своем письме Иоанн Павел I'


def test_show_answer():
    game = QAGame()
    random_qa_pair = ('In his letter, John Paul II',
                      'В своем письме Иоанн Павел I'
                      )
    game.get_question(online_qa=random_qa_pair)
    res = game.show_answer()
    assert res['Q'] == 'In his letter, John Paul II'
    assert res['A'] == 'В своем письме Иоанн Павел I'


def test_set_topics_user_provided_file():
    game = QAGame()
    game.set_topics('file_1.txt', reset=True)
    game.set_topics('file_2.txt', reset=True)
    res = game.get_topics()
    assert res == ['file_2.txt']


# def test_get_question_online():
#     with patch('question_game.qa_game.Game') as MockQAGameClass:
#         qa_game = MockQAGameClass.return_value
#         qa_game._online_questions = ["As a photographer he favors"]
#         qa_pair.answer = "Он фотограф и предпочитает"
#         game = Game()
#         assert game.get_online_question() == ["As a photographer he favors"]
#         assert len(game._qa_pairs) == 1
#         assert len(game._guesses) == 1
#         assert len(game._masks) == 1
