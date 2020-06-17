# https://docs.sqlalchemy.org/en/13/core/
# https://flask-sqlalchemy.palletsprojects.com/
import random

from sqlalchemy import func
from sqlalchemy import desc

from app_question_game.db import db


class BitextModel(db.Model):
    __tablename__ = 'bitext'
    id = db.Column(db.Integer, primary_key=True)
    en = db.Column(db.String)
    ru = db.Column(db.String)
    cat = db.Column(db.String)

    def __init__(self, en, ru, cat):
        self.en = en
        self.ru = ru
        self.cat = cat

    def save_to_db(self):
        """Upsert (update or insert) data into db."""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def save_all_to_db(data):
        """Bulk upsert (update or insert) data into db."""
        rows = []
        for row in data:
            row = BitextModel(*row)
            rows.append(row)
        db.session.add_all(rows)
        db.session.commit()

    @classmethod
    def get_categories_counts(cls):
        """Return all distinct categories and number of elements in each.

        SELECT cat, COUNT(*) as c
        FROM bitext
        GROUP BY cat
        ORDER BY c DESC;
        """
        res = db.session.query(
                   cls.cat,
                   func.count(cls.cat).label('count')
                   ).group_by(cls.cat).order_by(desc('count'))
        return list(res)

    @classmethod
    def category_exists(cls, category):
        """Check if category exists.

        SELECT DISTINCT cat
        FROM bitext;
        """
        return category in db.session.query(cls.cat).distinct()

    @classmethod
    def random_line(cls, cat):
        """Return a random en-ru pair for the given category.

        First, get indexes for the given category:
        SELECT bitext.id AS bitext_id
        FROM bitext
        WHERE bitext.cat = %(cat_1)s;

        Then choose a random index and query by it:
        SELECT en, ru
        FROM bitext
        WHERE id=rand_idx;
        """
        idx = list(db.session.query(cls.id).filter_by(cat=cat))
        rand_idx = random.choice(idx)[0]
        res = db.session.query(cls.en, cls.ru).filter_by(id=rand_idx)
        return list(res)[0]
