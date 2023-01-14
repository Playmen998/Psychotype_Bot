from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb1 = KeyboardButton('/start')
kb2 = KeyboardButton('/info')
kb3 = KeyboardButton('/begin_test')
kb4 = KeyboardButton('/load')
kb5 = KeyboardButton('/psychotype')

kb_main.add(kb2, kb3).add(kb4, kb5)

kb_answer = ReplyKeyboardMarkup(resize_keyboard=True)
kb_two1 = KeyboardButton('A')
kb_two2 = KeyboardButton('B')
kb_two3 = KeyboardButton('/Вернуть_вопрос')
kb_two4 = KeyboardButton('/Сохранить_ответы')

kb_answer.add(kb_two1, kb_two2).add(kb_two3,kb_two4)

ikb_psychotype = InlineKeyboardMarkup(row_width=1)
ib1 = InlineKeyboardButton(text = '👍Сильные стороны',
                           callback_data= 'force')
ib2 = InlineKeyboardButton(text = '👎Слабые стороны',
                           callback_data= 'weak')
ib3 = InlineKeyboardButton(text = '👫Отношения',
                           callback_data= 'relationship')
ib4 = InlineKeyboardButton(text = '🔨Профессии',
                           callback_data= 'profession')
ikb_psychotype.add(ib1).add(ib2).add(ib3).add(ib4)