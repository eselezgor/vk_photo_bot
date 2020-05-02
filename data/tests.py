import sqlalchemy
from .db_session import SqlAlchemyBase


class Tests(SqlAlchemyBase):
    """Таблица с тестами"""

    __tablename__ = 'tests'

    question = sqlalchemy.Column(sqlalchemy.String)
    answer_choice = sqlalchemy.Column(sqlalchemy.String)  # Четыре варианта ответа через **
    answer = sqlalchemy.Column(sqlalchemy.String)
