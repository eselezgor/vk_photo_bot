from data import db_session
db_session.global_init("db/tests.sqlite")
session = db_session.create_session()
from data.tests import Tests

"""Добавление теста в таблицу"""

new_test = Tests
new_test.question = input('Вопрос')
new_test.answer_choice = input('Варианты ответа через "**"')
new_test.answer = input('Правильный ответ')
session.add(new_test)
session.commit()
