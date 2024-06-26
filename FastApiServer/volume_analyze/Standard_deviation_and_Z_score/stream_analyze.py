from volume_analyze.Standard_deviation_and_Z_score.standart_deviation import StandartDeviation
from stream_parser.parser import StreamParser
from db import DataBase


class StandartDeviationAnalize(object):


    def __init__(self, z: float, listing: int, interval: int = 1):
        '''
        Конструктор класса

        :param interval: интервал рассматриваемых свеч в мин, default: 1
        '''
        self.db = DataBase()
        self.figis = self.db.get_figis(listing=listing)
        self.interval = interval
        self.z = z


    def analize(self): # -> list
        '''
        функция вычисления является ли зн-е объёма в настоящий момент аномальным
        :return: список со структурой list: [ [str: figi, bool: аномальное ли] , [..], .. ]
        '''
        result = []
        for i in range(len(self.figis)):
            figi = self.figis[i]
            historic_data = self.db.get_historic_data(figi)

            try:

                stream_parser = StreamParser(figi, 1)
                stream_data = stream_parser.parse()

                if stream_data != None:
                    self.db.delete_first_candle(figi)
                    self.db.insert_data(figi, stream_data)
                    standart_dev = StandartDeviation(historic_data, stream_data['volume'], z_limit=self.z)
                    result.append([figi, standart_dev.result])

                else:
                    result.append([figi, (None, None)])

            except:
                result.append([figi, (None, None)])

        return result









