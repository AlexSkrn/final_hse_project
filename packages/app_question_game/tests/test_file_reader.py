import io
import pytest

from app_question_game.processing.file_reader import (
    read_file,
    read_cat_file,
    read_bitext_file,
    )


@pytest.mark.parametrize(
    'test_input',
    [(''),
     ('\t'),
     ]
    )
def test_read_file(test_input):
    with pytest.raises(ValueError):
        f = io.BytesIO(bytes(test_input, 'utf-8'))
        read_file(f)


@pytest.mark.parametrize(
    'test_input',
    [('aaa\tbbb\t')]
    )
def test_read_cat_file(test_input):
    with pytest.raises(ValueError):
        read_cat_file(test_input)
