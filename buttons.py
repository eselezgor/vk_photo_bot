from enum import Enum


class VkKeyboardColor(Enum):
    """ Возможные цвета кнопок """

    #: Синяя
    PRIMARY = 'primary'

    #: Белая
    DEFAULT = 'default'

    #: Красная
    NEGATIVE = 'negative'

    #: Зелёная
    POSITIVE = 'positive'


class VkKeyboardButton(Enum):
    """ Возможные типы кнопки """

    #: Кнопка с текстом
    TEXT = "text"


class VkKeyboard(object):
    """ Класс для создания клавиатуры для бота (https://vk.com/dev/bots_docs_3)
    :param one_time: Если True, клавиатура исчезнет после нажатия на кнопку
    :type one_time: bool
    """

    __slots__ = ('one_time', 'lines', 'keyboard', 'inline')

    def __init__(self, one_time=False, inline=False):
        self.one_time = one_time
        self.inline = inline
        self.lines = [[]]

        self.keyboard = {
            'one_time': self.one_time,
            'inline': self.inline,
            'buttons': self.lines
        }


def get_empty_keyboard(cls):
    """ Получить json пустой клавиатуры.
    Если отправить пустую клавиатуру, текущая у пользователя исчезнет.
    """
    keyboard = cls()
    keyboard.keyboard['buttons'] = []
    return keyboard.get_keyboard()


def add_button(self, label, color=VkKeyboardColor.DEFAULT):
    """ Добавить кнопку с текстом.
        Максимальное количество кнопок на строке - 4

    :param label: Надпись на кнопке и текст, отправляющийся при её нажатии.
    :type label: str
    :param color: цвет кнопки.
    :type color: VkKeyboardColor or str
    :param payload: Параметр для callback api
    :type payload: str or list or dict
    """

    current_line = self.lines[-1]

    if len(current_line) >= 4:
        raise ValueError('Max 4 buttons on a line')

    color_value = color

    if isinstance(color, VkKeyboardColor):
        color_value = color_value.value

    button_type = VkKeyboardButton.TEXT.value

    current_line.append({
        'color': color_value,
        'action': {
            'type': button_type,
            'label': label,
        }
    })


def add_line(self):
    """ Создаёт новую строку, на которой можно размещать кнопки.
    Максимальное количество строк - 10.
    """

    if len(self.lines) >= 10:
        raise ValueError('Max 10 lines')

    self.lines.append([])
