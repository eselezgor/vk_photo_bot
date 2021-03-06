import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from data.mailing import Mailing
from data.tests import Tests
from data import db_session
import datetime
import random


def get_photo(owner, album):
    """Список id всех фото из альбома"""

    login, password = '79037726038', 'password'
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)

    vk = vk_session.get_api()
    photo = vk.photos.get(owner_id=-owner, album_id=album)
    all_id = []
    for item in photo['items']:
        all_id += [f"photo{item['owner_id']}_{item['id']}"]
    return all_id


def add_mailing(id, how_often):
    """Добавление пользователя в список рассылок"""

    mail = Mailing()
    mail.id = id
    mail.how_often = how_often
    mail.next_send = datetime.datetime.now() + datetime.timedelta(days=(7 / how_often))
    session = db_session.create_session()
    session.add(mail)
    session.commit()


def del_mailing(id):
    session = db_session.create_session()
    session.query(Mailing).filter(Mailing.id == id).delete()
    session.commit()


def mailing_check():
    """Проверка рассылки"""

    session = db_session.create_session()
    for mail in session.query(Mailing).all():
        if mail.next_send <= datetime.datetime.now():
            mail.next_send = datetime.datetime.now() + datetime.timedelta(days=(7 / mail.how_often))
            return mail.id
    return ''


def get_random_test():
    """Получение случайного теста"""

    session = db_session.create_session()
    id_count = len(session.query(Tests).all())
    print(session.query(Tests))
    test = session.query(Tests).filter(Tests.id == random.randint(1, id_count + 1)).first()
    return [test.question, test.answer_choice, test.answer]


def add_button(keyboard, text, new_line=True):
    """Добавение кнопки в клавиатуру"""

    keyboard = keyboard
    if new_line:
        keyboard.add_line()
    keyboard.add_button(text, color=VkKeyboardColor.DEFAULT)
    return keyboard
