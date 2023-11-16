import os
from aiogram import Bot, Dispatcher, executor, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv.main import load_dotenv
from tg_bot.apsched import send_message_interval
from volume_analyze.Standard_deviation_and_Z_score.stream_analize import StandartDeviationAnalize
from aiogram.types import ParseMode
from adminDB import UsersDataBase
from keyboards import start_keyboard, payment_keyboard



load_dotenv()
API_TOKEN = os.environ['BOT_TOKEN']


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)




@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    db = UsersDataBase()
    db.add_user(userid=message.from_user.id, username=message.from_user.username)
    await bot.send_message(message.chat.id, "Привет! Это бот VolumeHub", reply_markup=start_keyboard)

@dp.message_handler(content_types=['text'])
async def menu(message: types.Message):
    if message.text == 'ℹО ботеℹ':
        db = UsersDataBase()
        await bot.send_message(message.chat.id, str(db.get_about_bot_text()))

    if message.text == '📌Подписка📌':
        db = UsersDataBase()
        await bot.send_message(message.chat.id, str(db.get_subscription_text()), reply_markup=payment_keyboard)


@dp.message_handler(lambda c: c.data)
def get_payment_link(callback_query: types.CallbackQuery):
    if callback_query.data == '30':
        bot.send_message(callback_query.from_user.id, 'Ссылка на оплату 30 дней')
    if callback_query.data == '90':
        bot.send_message(callback_query.from_user.id, 'Ссылка на оплату 30 дней')
    if callback_query.data == '90':
        bot.send_message(callback_query.from_user.id, 'Ссылка на оплату 30 дней')




@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    deviation = StandartDeviationAnalize()
    result = deviation.analize()
    await bot.send_message(691902762, result)


# Функция для отправки сообщения через бота
async def send_message_to_user(chat_id, text, photo_path=None):
    if photo_path:
        with open(photo_path, 'rb') as photo:
            await bot.send_photo(chat_id, photo, caption=text, parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.send_message(chat_id, text, parse_mode=ParseMode.MARKDOWN)



def run_bot():
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(send_message_interval, trigger='interval', seconds=60, kwargs={'bot': bot})
    scheduler.start()
    print('sheduler started!')

    executor.start_polling(dp, skip_updates=True)
    print('бот запущен!')


if __name__ == "__main__":
    run_bot()
