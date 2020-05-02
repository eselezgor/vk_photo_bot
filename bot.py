import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard
from defs import add_button, add_mailing, mailing_check, get_photo, del_mailing
import os.path
from data import db_session, mailing


def main():
    vk_session = vk_api.VkApi(
        token='ab948e1d036b8d2e340bd6e2e66799330708cb59317956632f06a93d4f18f2ad6d89d51cb6683f0479cbd')

    db_session.global_init("db/mailing.sqlite")
    id = mailing_check()
    if not id == '':
        vk = vk_session.get_api()
        vk.messages.send(user_id=id,
                         message=('Здравствуйте! Рассылка фото'),
                         attachment=random.choice(get_photo(-194151011, 271928593)),
                         random_id=random.randint(0, 2 ** 64))

    longpoll = VkBotLongPoll(vk_session, 194151011)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            main_menu = True
            main_menu_text = False
            vk = vk_session.get_api()
            response = vk.users.get(user_id=event.obj.message['from_id'])
            text = event.obj.message['text']
            keyboard = VkKeyboard(one_time=True)

            if text == 'Фото по категориям':
                keyboard = add_button(keyboard, 'Города', new_line=False)
                keyboard = add_button(keyboard, 'Игры')
                keyboard = add_button(keyboard, 'Горы')
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=('Выберите категорию'),
                                 keyboard=keyboard.get_keyboard(),
                                 random_id=random.randint(0, 2 ** 64))
                main_menu = False

            elif text == 'Города' or text == 'Горы' or text == 'Игры':
                up = VkUpload(vk)
                if text == 'Города':
                    group = 'cities'
                elif text == 'Горы':
                    group = 'mountains'
                else:
                    group = 'games'

                # Подсчёт количества файлов в папке
                path = 'static/img/{}'.format(group)
                num_files = len([f for f in os.listdir(path)
                                 if os.path.isfile(os.path.join(path, f))])

                mes = up.photo_messages('static/img/{}/pic{}.jpg'.format(group, str(random.randint(1, num_files))))[0]
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=(''),
                                 attachment=f"photo{mes['owner_id']}_{mes['id']}",
                                 random_id=random.randint(0, 2 ** 64))

            elif text == 'Рассылка фото':
                keyboard = add_button(keyboard, 'Каждый день', new_line=False)
                keyboard = add_button(keyboard, 'Два раза в неделю')
                keyboard = add_button(keyboard, 'Раз в неделю')
                keyboard = add_button(keyboard, 'Отписаться от рассылки')
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=('Выберите частоту'),
                                 keyboard=keyboard.get_keyboard(),
                                 random_id=random.randint(0, 2 ** 64))
                main_menu = False

            elif text == 'Каждый день' or text == 'Два раза в неделю' or text == 'Раз в неделю':
                db_session.global_init("db/mailing.sqlite")

                if text == 'Каждый день':
                    times_a_week = 7
                elif text == 'Два раза в неделю':
                    times_a_week = 2
                else:
                    times_a_week = 1

                session = db_session.create_session()
                text_message = 'Вы подписались на рассылку фото {}. Чтобы отменить рассылку, выберите "Отисаться от' \
                               ' рассылки" в меню "Рассылка фото"'.format(text.lower())
                for user in session.query(mailing.Mailing).all():
                    if user.id == event.obj.message['from_id']:
                        del_mailing(event.obj.message['from_id'])
                        text_message = 'Вы поменяли частоту рассылки на {}. Чтобы отменить рассылку, выберите ' \
                                       '"Отисаться от рассылки" в меню "Рассылка фото"'.format(text.lower())
                        break
                add_mailing(event.obj.message['from_id'], times_a_week)
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=(text_message),
                                 random_id=random.randint(0, 2 ** 64))

            elif text == 'Отписаться от рассылки':
                del_mailing(event.obj.message['from_id'])
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=('Вы отписались от рассылки'),
                                 random_id=random.randint(0, 2 ** 64))

            elif text == 'Тесты про фотографию':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=('Извините, эта функция пока не поддерживается'),
                                 random_id=random.randint(0, 2 ** 64))

            elif text == 'Рассылка интересных фактов про фото':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=('Извините, эта функция пока не поддерживается'),
                                 random_id=random.randint(0, 2 ** 64))

            elif text == 'Игры на внимательность':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=('Извините, эта функция пока не поддерживается'),
                                 random_id=random.randint(0, 2 ** 64))
            else:
                main_menu_text = True

            if main_menu:
                keyboard = add_button(keyboard, 'Фото по категориям', new_line=False)
                keyboard = add_button(keyboard, 'Рассылка фото')
                keyboard = add_button(keyboard, 'Тесты про фотографию')
                keyboard = add_button(keyboard, 'Рассылка интересных фактов про фото')
                keyboard = add_button(keyboard, 'Игры на внимательность')

                if main_menu_text:
                    up = VkUpload(vk)
                    mes = up.photo_messages('static/img/cities/pic{}.jpg'.format(str(1)))[0]
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=('Здравствуйте, {}'.format(response[0]['first_name'])),
                                     attachment=f"photo{mes['owner_id']}_{mes['id']}",
                                     keyboard=keyboard.get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=('Выберите категорию'),
                                     keyboard=keyboard.get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
