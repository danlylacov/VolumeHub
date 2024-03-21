import threading
import time
from datetime import datetime

import schedule

from db import DataBase
from volume_analyze.Standard_deviation_and_Z_score import stream_analyze

lock = threading.Lock()


def add_anomal_note(result):
    for i in range(len(result)):
        if result[i][1][0] is not True:
            continue
        with lock:
            db = DataBase()
            db.add_anomal_volume_note(
                str(db.get_action_name_by_figi(result[i][0])),
                float(db.get_price_change(result[i][0])),
                float(db.get_day_change(result[i][0])),
                float(db.get_last_price(result[i][0])),
                int(db.get_last_volume(result[i][0])),
                "(" + str(int(datetime.utcnow().hour) + 3) + ":" + str(datetime.utcnow().minute) + ")" +
                str(datetime.utcnow()).split(' ')[0]
            )


def scheduled_task():
    print('Sched func works!')
    print(datetime.now())

    deviation_1_lising = stream_analyze.StandartDeviationAnalize(z=8, listing=1)
    result_1 = deviation_1_lising.analize()

    deviation_2_lising = stream_analyze.StandartDeviationAnalize(z=9, listing=2)
    result_2 = deviation_2_lising.analize()

    deviation_3_lising = stream_analyze.StandartDeviationAnalize(z=10, listing=3)
    result_3 = deviation_3_lising.analize()

    add_anomal_note(result_1)
    add_anomal_note(result_2)
    add_anomal_note(result_3)




def run_scheduled_task():
    schedule.every().minute.at(":05").do(scheduled_task)
    while True:
        schedule.run_pending()
        time.sleep(1)
