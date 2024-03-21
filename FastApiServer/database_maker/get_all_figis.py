import os

from dotenv import load_dotenv
from pandas import DataFrame
from tinkoff.invest import Client, InstrumentStatus
from tinkoff.invest.services import InstrumentsService, MarketDataService



import pandas as pd

load_dotenv()
TOKEN = os.environ['TINKOFF_API_TOKEN']


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def run():
    with Client(TOKEN) as cl:
        instruments: InstrumentsService = cl.instruments
        market_data: MarketDataService = cl.market_data
        r = DataFrame(
            instruments.shares(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_BASE).instruments,
            columns=['name', 'figi', 'ticker']
        )
        print(r.values[0])
        with open('figis.txt', 'w') as f:
            for i in range(len(r.values)):
                f.write(str(r.values[i]) + '\n')
            f.close()


if __name__ == '__main__':
    run()