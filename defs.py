import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def get_photo(owner, album):
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


def add_button(keyboard, text, new_line=True):
    keyboard = keyboard
    if new_line:
        keyboard.add_line()
    keyboard.add_button(text, color=VkKeyboardColor.DEFAULT)
    return keyboard
