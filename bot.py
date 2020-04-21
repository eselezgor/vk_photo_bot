import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard
from defs import add_button


def main():
    vk_session = vk_api.VkApi(
        token='ab948e1d036b8d2e340bd6e2e66799330708cb59317956632f06a93d4f18f2ad6d89d51cb6683f0479cbd')

    longpoll = VkBotLongPoll(vk_session, 194151011)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
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
            elif text == 'Рассылка фото':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=('Извините, эта функция пока не поддерживается'),
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
                keyboard = add_button(keyboard, 'Фото по категориям', new_line=False)
                keyboard = add_button(keyboard, 'Рассылка фото')
                keyboard = add_button(keyboard, 'Тесты про фотографию')
                keyboard = add_button(keyboard, 'Рассылка интересных фактов про фото')
                keyboard = add_button(keyboard, 'Игры на внимательность')

                up = VkUpload(vk)
                mes = up.photo_messages('static/img/cities/pic{}.jpg'.format(str(1)))[0]
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=('Здравствуйте, {}'.format(response[0]['first_name'])),
                                 attachment=f"photo{mes['owner_id']}_{mes['id']}",
                                 keyboard=keyboard.get_keyboard(),
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
