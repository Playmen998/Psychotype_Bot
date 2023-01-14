from aiogram import executor
from create_bot import dp
from handlers import handler
from package_database import base_questions, base_user
from callbacks import callback




async def on_startup(_):
    print('Бот запущен')
    await base_questions.db_start()
    await base_user.db_start()

handler.register_handlers_client(dp)
callback.register_callback_client(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup = on_startup)