from pymystem3 import Mystem

from question_game.jaccard import jaccard
from question_game.nltk_bleu_score import sentence_bleu
from question_game.nltk_bleu_score import SmoothingFunction


stemmer = Mystem()
chencherry = SmoothingFunction()


class Question:
    """Provide a class to keep a single step in the game."""

    def __init__(self, qa_pair: tuple):
        self._question, self._ref_trans = qa_pair
        self._guesses = []  # List[Tuple(guess, mask, score), ]
        self._ref_analysis = stemmer.analyze(self._ref_trans)
        self._ref_lemmas = []
        self._ref_text = []
        self._get_ref_lemmas_and_text()
        self._guess_lemmas = ''

    def add_guess(self, guess):
        self._guess_lemmas = stemmer.lemmatize(guess)  # incl. punct. etc

        mask = self._get_mask()
        score = self._calc_score(guess)

        self._guesses.append((guess, mask, score))

    def get_question(self):
        return self._question

    def _get_ref_lemmas_and_text(self):
        """Extract lemmas and text only from reference translation."""
        for element in self._ref_analysis:
            try:
                self._ref_lemmas.append(element['analysis'][0]['lex'])
                self._ref_text.append(element['text'])
            except (KeyError, IndexError):
                pass

    def _get_guess_lemmas_and_text(self, guess):
        """Extract lemmas and text only from candidate translation."""
        lemmas = []
        text = []
        for element in stemmer.analyze(guess):
            try:
                lemmas.append(element['analysis'][0]['lex'])
                text.append(element['text'])
            except (KeyError, IndexError):
                pass
        return lemmas, text

    def _calc_score(self, guess):
        guess_lemmas, _ = self._get_guess_lemmas_and_text(guess)
        # jaccard_score = jaccard(self._ref_lemmas, guess_lemmas)
        bleu_score = sentence_bleu(references=[self._ref_lemmas],
                                   hypothesis=guess_lemmas,
                                   weights=(0.25, 0.25, 0, 0),
                                   smoothing_function=chencherry.method2
                                   )
        # return round((jaccard_score + bleu_score) / 2, 2)
        return round(bleu_score, 2)

    def _get_mask(self):
        """Return the answer with words from the guess visible."""
        masked_ref_trans = ''
        for elem in self._ref_analysis:
            try:
                lex = elem['analysis'][0]['lex']
            except (KeyError, IndexError):
                masked_ref_trans += elem['text']
            else:
                if lex in self._guess_lemmas:
                    masked_ref_trans += elem['text']
                else:
                    masked_ref_trans += '-' * len(elem['text'])
        return masked_ref_trans.strip()

    def get_status(self, answer=False) -> dict:
        """Return question, answer, guesses and masks as a dict."""
        status_data = dict([('Q', ''),
                            ('A', ''),
                            ('GuessMask', []),
                            # ('G', [])
                            ]
                           )
        status_data['Q'] = self._question
        if answer:
            status_data['A'] = self._ref_trans

        for idx, guess_mask in enumerate(self._guesses):
            guess, masked, score = guess_mask[0], guess_mask[1], guess_mask[2]
            # the guess is more or less correct, no need to show the mask
            # show chr(10003)?
            if masked.casefold() == self._ref_trans.casefold():
                status_data['GuessMask'].append(f'({score}) {guess}')
                guess_size = len(guess.split())
                ref_size = len(self._ref_trans.split())
                diff = guess_size - ref_size
                if diff > 0:
                    msg = f'ЛИШНИЕ СЛОВА ({diff}) В ПЕРЕВОДЕ!'
                    status_data['GuessMask'].append(msg)
                elif score < 1:
                    msg = f'НЕПРАВИЛЬНЫЙ ПОРЯДОК СЛОВ В ПЕРЕВОДЕ!'
                    status_data['GuessMask'].append(msg)
                else:
                    status_data['GuessMask'].append('')
            else:
                # the guess is wrong, show mask
                status_data['GuessMask'].append(f'({score}) {guess}')
                status_data['GuessMask'].append(masked)
            # else:
            #     # final report should not include masks
            #     status_data.append(f'({idx + 1}): {guess_mask[0]}')
        return status_data

    def get_status_tab_delim(self) -> str:
        """Return tab-delim question, answer, guesses as a string."""
        status_data = self._question
        status_data += '\t'
        status_data += self._ref_trans
        status_data += '\t'

        guesses = [guess[0] for guess in self._guesses]

        status_data += ' // '.join(guesses)

        return status_data
