from datetime import datetime, timedelta
import os
import traceback
from datetime import timedelta

from dotenv.main import load_dotenv
from tinkoff.invest import Client, CandleInterval, TradeDirection
from tinkoff.invest.utils import now


class StreamParser(object):

    def __init__(self, figi: str, interval: int = 1):
        '''
        Конструктор класса
        :param figis: figi акций, по котромым необходимо получить свечи
        :param interval: интервал получаемых свечей в мин, default = 5
        '''
        load_dotenv()
        self.TOKEN = os.environ['TINKOFF_API_TOKEN']
        self.figi = figi
        self.interval = interval

    def parse(self):  # str, int -> HistoricCandle
        '''
           функция для получения свечи по акции в данный момент

           arguments:
               figi - figi-номер акции(содержится в файле figi.txt)
               interval - интервал требуемой свечи в мин(default: 5)

           :return:
               свеча в формате - HistoricCandle(открытие, верхняя граница, нижняя граница, закрытие, объём, время, завершена(bool))

               !!!ВАЖНО: в свече указано время по часовому поясу UTC+00.00
               '''

        interval = self.interval

        intervals = {
            1: CandleInterval.CANDLE_INTERVAL_1_MIN,
            5: CandleInterval.CANDLE_INTERVAL_5_MIN,
            2: CandleInterval.CANDLE_INTERVAL_2_MIN,
            3: CandleInterval.CANDLE_INTERVAL_3_MIN,
            10: CandleInterval.CANDLE_INTERVAL_10_MIN,
            15: CandleInterval.CANDLE_INTERVAL_15_MIN,
            30: CandleInterval.CANDLE_INTERVAL_30_MIN,
            60: CandleInterval.CANDLE_INTERVAL_HOUR,
            120: CandleInterval.CANDLE_INTERVAL_2_HOUR,
            1440 : CandleInterval.CANDLE_INTERVAL_DAY
        }
        interval_method = intervals[interval]


        try:
            with Client(self.TOKEN) as client:  # подключение по токену

                for candle in client.get_all_candles(  # вызов метода получения свечи
                        figi=self.figi,
                        from_=now() - timedelta(minutes=interval),
                        interval=interval_method,
                ):
                    return self.parse_candle_data(candle)
        except:
            return {'open': None, 'high': None, 'low': None,
                    'close': None, 'volume': None, 'time': None}

    @staticmethod
    def parse_candle_data(candle):
        DEVIDER = 1000000000
        return {
            'open': float(candle.open.units) + (candle.open.nano / DEVIDER),
            'high': float(candle.high.units) + (candle.high.nano / DEVIDER),
            'low': float(candle.low.units) + (candle.low.nano / DEVIDER),
            'close': float(candle.close.units) + (candle.close.nano / DEVIDER),
            'volume': int(candle.volume),
            'time': str(candle.time)
        }

    def get_order_book(self):
        with Client(self.TOKEN) as client:
            book = None
            try:
                book = client.market_data.get_order_book(figi=self.figi, depth=50)
            except Exception:
                traceback.print_exc(10)

            return book

    def get_buy_sell_percent_in_order_book(self):
        book = self.get_order_book()
        if not book:
            return

        ask_sum, bid_sum = 0, 0
        for order in book.asks:
            ask_sum += order.quantity
        for order in book.bids:
            bid_sum += order.quantity
        if ask_sum + bid_sum != 0:
            ask_percent = (ask_sum / (ask_sum + bid_sum)) * 100
            bid_percent = 100 - ask_percent
        else:
            ask_percent = 0
            bid_percent = 0

        return round(ask_percent), round(bid_percent)


    def get_last_trades(self):
        with Client(self.TOKEN) as client:
            trades = None
            try:
                trades = client.market_data.get_last_trades(figi=self.figi, from_=now()-timedelta(minutes=1), to=now(), instrument_id=self.figi)
            except Exception:
                traceback.print_exc(10)

            return trades.trades

    def count_percent_of_trades(self):
        request = self.get_last_trades()
        buy_lots, sell_lots = 0, 0
        for trade in request:
            if trade.direction == TradeDirection.TRADE_DIRECTION_BUY:
                buy_lots += trade.quantity
            if trade.direction == TradeDirection.TRADE_DIRECTION_SELL:
                sell_lots += trade.quantity

        buy_persent = (buy_lots / (buy_lots+sell_lots)) * 100
        sell_persent = 100 - buy_persent

        return int(buy_persent) , int(sell_persent)




