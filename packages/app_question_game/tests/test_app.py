import pytest

from app_question_game.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_main(client):
    response = client.get('/main')
    assert bytes("Упражнения для", encoding='utf8') in response.data
