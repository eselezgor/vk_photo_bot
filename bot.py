import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_api import VkUpload


def main():
    vk_session = vk_api.VkApi(
        token='ab948e1d036b8d2e340bd6e2e66799330708cb59317956632f06a93d4f18f2ad6d89d51cb6683f0479cbd')

    longpoll = VkBotLongPoll(vk_session, 194151011)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()

            response = vk.users.get(user_id=event.obj.message['from_id'])
            up = VkUpload(vk)

            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=('Здравствуйте, {}'.format(response[0]['first_name'])),
                             attachment=up.photo_messages('static/img/cities/pic{}.jpg'.format(str(1))),
                             random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
