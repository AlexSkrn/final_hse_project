# Requires Spacy
# pip install -U spacy
# pip install -U spacy-lookups-data
# python -m spacy download en_core_web_sm
import os
import string
from time import time

import spacy
import pandas as pd


def remove_punc(text) -> str:
    """Return de-punctuated text as string."""
    punct_exclude = set(string.punctuation)
    return ''.join(char for char in text if char not in punct_exclude)


def remove_numbers(text) -> str:
    """Return de-numericised text."""
    return ' '.join(token for token in text.split(' ') if not token.isdigit())


def lemmatize(text) -> str:
    """Return lemmatized text, while skipping some POSes as string."""
    doc = nlp(text)
    pos_list = ['PROPN', 'VERB', 'NOUN', 'ADJ']
    return ' '.join([token.lemma_ for token in doc if token.pos_ in pos_list])


def preprocess(text) -> str:
    """Return text as a preprocessed string."""
    return lemmatize(text).casefold()


if __name__ == '__main__':
    DATA_DIR = 'wiki-matrix-data'
    SRC_FILENAME = 'cleaned_bitext.tsv'
    TRG_FILENAME = 'lemmatized_pos_en.txt'

    print(f'Reading data from file {DATA_DIR}/{SRC_FILENAME}')
    df = pd.read_csv(os.path.join(DATA_DIR, SRC_FILENAME), sep='\t')

    nlp = spacy.load('en_core_web_sm')

    # ###########################################
    # example = """Čachtice has received the status of a town in 1392, but it was later degraded back to a village."""
    # example = """And of course the virus would love the cell so much in 1980."""
    # print(preprocess(example))
    # ###########################################
    lemmatized_df = pd.DataFrame()

    print('Processing data... Wait!')
    t0 = time()
    lemmatized_df['en'] = df['en'].map(preprocess)
    print(f'Done in {time() - t0} seconds')

    print(f'Saving to {DATA_DIR}/{TRG_FILENAME}')
    lemmatized_df.to_csv(os.path.join(DATA_DIR, TRG_FILENAME), index=False)
