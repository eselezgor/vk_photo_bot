import vk_api


def get_photo(owner, album):
    login, password = '79037726038', 'perf2004@@lo'
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


def photo_messages(photos):
    """ Загрузка изображений в сообщения
    :param photos: путь к изображению(ям) или file-like объект(ы)
    :type photos: str, list
    """
    login, password = '79037726038', 'password'
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)

    vk = vk_session.get_api()
    print(vk.photos.getMessagesUploadServer())
    url = vk.photos.getMessagesUploadServer()['upload_url']
    print(photos)
    photo_files = vk.open_files(photos)
    response = vk._vk.http.post(url, files=photo_files)
    vk.close_files(photo_files)

    response = vk.method('photos.saveMessagesPhoto', response.json())

    return response
