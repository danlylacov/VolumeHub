from aiogram import Bot
from volume_analyze.Standard_deviation_and_Z_score.stream_analize import StandartDeviationAnalize
from DB.db import DataBase


db = DataBase()

async def send_message_interval(bot: Bot):
    print('Sched func works!')
    deviation = StandartDeviationAnalize()
    result = deviation.analize()
    for i in range(len(result)):
        if result[i][1][0] == True:

            await bot.send_message(691902762, str(db.get_action_name_by_figi(result[i][0])))