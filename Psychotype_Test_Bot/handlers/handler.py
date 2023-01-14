from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import keyboard
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from package_database import base_questions, base_user


START = """
🌎Главное меню - /start
📔Описание проекта - /info
🚩Начать тест - /begin_test
♻Загрузить ответы - /load
🎯Узнать психотип - /psychotype
"""

INFO = """Тест типологии MBTI - это методика тестирования, которая позволяет описать и типизировать взаимодействие человека с окружающим миром.
Согласно типологии MBTI можно выделить 16 типов личности отличающихся поведенческими реакциями, степенью возбудимости и эмоциональными проявлениями.
Данный тест представляет собой модификацию KPMI, который включает в себя <b>60 вопросов (5-6 мин)</b>

Данная типология включает в себя четыре основных характеристик:

• <b>E—I — направленность жизненной энергии:</b>
Е (Еxtraversion, экстраверсия) — на внешний мир;
I (Introversion, интроверсия) — на внутренний мир;

• <b>S—N — способ ориентирования в ситуации:</b>
S (Sensing, здравый смысл) — ориентирование на конкретную информацию;
N (iNtuition, интуиция) — ориентирование на обобщённую информацию;

• <b>T—F — основа принятия решений:</b>
T (Thinking, мышление) — рациональное взвешивание альтернатив;
F (Feeling, чувство) — принятие решений на эмоциональной основе;

• <b>J—P — способ подготовки решений:</b>
J (Judging, суждение) — предпочтение планировать и заранее упорядочивать информацию;
P (Perception, восприятие) — предпочтение действовать без детальной предварительной подготовки, больше ориентируясь по обстоятельствам.
"""

NUM = 0

DICT_ANSWER = {}


class StateAnswer(StatesGroup):
    ANS_1 = State()
    ANS_2 = State()


async def start_command(message : types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id,
                           text=START,
                           reply_markup=keyboard.kb_main, parse_mode='html')


async def info_command(message : types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id,
                           text=INFO,
                           reply_markup=keyboard.kb_main, parse_mode='html')
    photo_url = "https://i.ibb.co/3CscczV/image.png"
    await bot.send_photo(chat_id=message.from_user.id, photo=photo_url)


async def begin_test_command(message : types.Message, state: FSMContext):
    global NUM, DICT_ANSWER
    await state.finish()
    await base_user.delet(message.from_user.id)

    NUM = 0

    question = await base_questions.get_question(0) # получаем вопрос
    answer = await base_questions.get_answer(0) # получаем ответы

    TEXT = f"""
🚩<b>Тест начался</b>
        
Вопрос {1}

<b>{question}</b>
A) {answer[0][0]}
B) {answer[1][0]}
    """

    await bot.send_message(text=TEXT, reply_markup=keyboard.kb_answer, chat_id=message.from_user.id, parse_mode='html')
    DICT_ANSWER['user_id'] = message.from_user.id
    await StateAnswer.ANS_1.set()


async def last_command(message : types.Message):
    global NUM
    NUM -= 1
    if NUM < 0:
        await bot.send_message(text='Вы откатились к последнему вопросу', reply_markup=keyboard.kb_answer, chat_id=message.from_user.id)
        NUM = 0
    question = await base_questions.get_question(NUM)
    answer = await base_questions.get_answer(NUM)

    TEXT = f""" 
Вопрос {NUM + 1}

<b>{question}</b>
A) {answer[0][0]}
B) {answer[1][0]}
        """
    await bot.send_message(text='✅Вы вернулись к предыдущему вопросу', chat_id=message.from_user.id)
    await bot.send_message(text=TEXT, reply_markup=keyboard.kb_answer, chat_id=message.from_user.id, parse_mode='html')
    await StateAnswer.ANS_2.set()


async def state_answer_1(message : types.Message, state: FSMContext):
    global NUM, DICT_ANSWER
    NUM += 1
    if NUM == 60:
        DICT_ANSWER['num'] = NUM
        DICT_ANSWER[f'q{NUM}'] = message.text
        no_answer = await base_user.insert(DICT_ANSWER)
        NUM = 0
        await state.finish()
        text = """
✅Вы прошли тест 
Для того, чтобы узнать свой психотип нажмите команду 
/psychotype
        """
        return await bot.send_message(text=text, chat_id=message.from_user.id, reply_markup=keyboard.kb_main)

    question = await base_questions.get_question(NUM)
    answer = await base_questions.get_answer(NUM)

    TEXT = f""" 
Вопрос {NUM + 1}

<b>{question}</b>
A) {answer[0][0]}
B) {answer[1][0]}
    """

    await bot.send_message(text=TEXT, reply_markup=keyboard.kb_answer, chat_id=message.from_user.id, parse_mode='html')

    DICT_ANSWER['num'] = NUM
    DICT_ANSWER[f'q{NUM}'] = message.text
    await StateAnswer.ANS_2.set()

async def state_answer_2(message : types.Message, state: FSMContext):
    global NUM,DICT_ANSWER
    NUM += 1
    if NUM == 60:
        DICT_ANSWER['num'] = NUM
        DICT_ANSWER[f'q{NUM}'] = message.text
        await base_user.insert(DICT_ANSWER)
        NUM = 0
        await state.finish()
        text = """
✅Вы прошли тест 
Для того, чтобы узнать свой психотип нажмите команду 
/psychotype
                """
        return await bot.send_message(text= text, chat_id=message.from_user.id, reply_markup=keyboard.kb_main)

    question = await base_questions.get_question(NUM)
    answer = await base_questions.get_answer(NUM)

    TEXT = f""" 
Вопрос {NUM + 1}

<b>{question}</b>
A) {answer[0][0]}
B) {answer[1][0]}
    """

    await bot.send_message(text=TEXT, reply_markup=keyboard.kb_answer, chat_id=message.from_user.id, parse_mode='html')

    DICT_ANSWER['num'] = NUM
    DICT_ANSWER[f'q{NUM}'] = message.text
    await StateAnswer.ANS_1.set()



async def safe_command(message : types.Message, state: FSMContext):
    global DICT_ANSWER, NUM
    DICT_ANSWER['num'] = NUM
    NUM = 0
    await base_user.insert(DICT_ANSWER)
    await bot.send_message(text='✅Ваши ответы сохранены', reply_markup=keyboard.kb_main, chat_id=message.from_user.id)
    await bot.send_message(text=START, chat_id=message.from_user.id)
    await state.finish()


async def load_command(message : types.Message):
    global NUM, DICT_ANSWER
    DICT_ANSWER = {}
    try:
        NUM = await base_user.select_num(message.from_user.id)
        if NUM == 60:
            text = """
<b>Вы уже прошли весь тест</b>
🎯Посмотреть результаты:
/psychotype
🚩Начать заново:
/begin_test
                    """
            return await bot.send_message(text=text, chat_id=message.from_user.id, parse_mode='html')
        DICT_ANSWER['user_id'] = message.from_user.id

        question = await base_questions.get_question(NUM)  # получаепм вопрос
        answer = await base_questions.get_answer(NUM)  # получаем ответы
        TEXT = f"""
✅<b>Вы загрузили последние ответы</b>
    
Вопрос {NUM+1}

<b>{question}</b>
A) {answer[0][0]}
B) {answer[1][0]}
    """

        await bot.send_message(text=TEXT, reply_markup=keyboard.kb_answer, chat_id=message.from_user.id, parse_mode='html')
        await StateAnswer.ANS_1.set()
    except:
        await bot.send_message(text='⛔Нет сохраненных данных', reply_markup=keyboard.kb_main, chat_id=message.from_user.id)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'], state="*")
    dp.register_message_handler(info_command, commands=['info', 'help'], state="*")
    dp.register_message_handler(begin_test_command, commands=['begin_test'], state="*")
    dp.register_message_handler(last_command, commands=['Вернуть_вопрос'], state="*")
    dp.register_message_handler(safe_command, commands=['Сохранить_ответы'], state="*")
    dp.register_message_handler(state_answer_1, Text(equals = ['A','B']), state=StateAnswer.ANS_1)
    dp.register_message_handler(state_answer_2,Text(equals = ['A','B']), state=StateAnswer.ANS_2)
    dp.register_message_handler(load_command, commands=['load'], state="*")


