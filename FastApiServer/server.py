import threading

from fastapi import FastAPI

from db import DataBase
from scheduler import run_scheduled_task
from stream_parser.parser import StreamParser

app = FastAPI()


@app.get("/")
def main():
    return {'ok': True}


@app.get("/get_anomal_volumes")
def get_anomal_volumes():
    db = DataBase()
    request = {}
    anomal_volumes = db.get_anomal_volume_notes()
    for anomal_volume in anomal_volumes:
        request[anomal_volume[0]] = {
            'action_name': anomal_volume[1],
            'price_change': anomal_volume[2],
            'day_price_change': anomal_volume[3],
            'price': anomal_volume[4],
            'volume': anomal_volume[5],
            'time': anomal_volume[6]
        }
    return request


@app.get("/delete_anomal_volume/{id}")
def delete_anomal_volume(id: int):
    try:
        db = DataBase()
        db.delete_anomal_volume_note(id)
        return {id: 'deleted'}
    except:
        return {id: 'mistake!'}


@app.get("/get_hour_data/{figi}")
def get_hour_data(figi: str):
    try:
        db = DataBase()
        request = db.get_last_hour_prices(figi)

        return request

    except:
        return None


@app.get('/get_order_book_percent/{figi}')
def get_order_book_percent(figi: str):
    parser = StreamParser(figi)
    ask, bid = parser.count_percent_of_trades()
    return {'ask': ask, 'bid': bid}


@app.get('/get_figi_by_action_name/{name}')
def get_figi_by_action_name(name: str):
    db = DataBase()
    return str(db.get_figi_by_action_name(name))


threading.Thread(target=run_scheduled_task, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
