from data.tests import Tests
from data import db_session

"""Добавление теста в таблицу"""

db_session.global_init("db/tests.sqlite")
new_test = Tests
new_test.question = input('Вопрос')
new_test.answer_choice = input('Варианты ответа через "**"')
new_test.answer = input('Правильный ответ')
session = db_session.create_session()
session.add(new_test)
session.commit()
