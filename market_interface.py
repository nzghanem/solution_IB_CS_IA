import requests
import json
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import qgrid
from datetime import date
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import scrolledtext
import tkinter.ttk as ttk1
from matplotlib import style
style.use('dark_background')


class MarketApp():
    def __init__(self):
        self.marketApp = tk.Tk()
        self.marketApp.title("Latest market update for Cryptocurrencies")
        self.marketApp.geometry('1050x800')

        # data gathering
        self.page2 = requests.get(
            'https://coinmarketcap.com/currencies/bitcoin/historical-data/')
        self.soup2 = BeautifulSoup(self.page2.content, 'html.parser')

        self.api = requests.get(
            "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=132cabf1-5b55-43f6-9cff-ce32c8d37c3e")
        self.api_json = self.api.json()

        market_stats = self.soup2.find_all(class_='cmc-link')
        self.market_data = [item.get_text() for item in market_stats]
        del self.market_data[4:]
        self.market_labels = ['Cryptocurrencies:',
                              'Markets:', 'Market Cap:', '24h Vol:']

        # initialization functions
        # self.df = self.get_binance_bars()
        self.graphs()
        self.marketApp.mainloop()

    def get_binance_bars(self, symbol, interval, startTime, endTime):

        url = "https://api.binance.com/api/v3/klines"

        startTime = str(int(startTime.timestamp() * 1000))
        endTime = str(int(endTime.timestamp() * 1000))
        limit = '1000'

        req_params = {"symbol": symbol, 'interval': interval,
                      'startTime': startTime, 'endTime': endTime, 'limit': limit}

        df = pd.DataFrame(json.loads(
            requests.get(url, params=req_params).text))

        if (len(df.index) == 0):
            return None

        df = df.iloc[:, 0:6]
        df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']

        df.open = df.open.astype("float")
        df.high = df.high.astype("float")
        df.low = df.low.astype("float")
        df.close = df.close.astype("float")
        df.volume = df.volume.astype("float")

        df['adj_close'] = df['close']

        df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.datetime]
        print(df)
        return df

    def graphs(self):
        canvas = tk.Canvas(self.marketApp)
        frame = tk.LabelFrame(canvas, text="Global Market statistics up to {}".format(date.today()), font="Lato 30 bold",
                              fg='black', padx=50, pady=50)
        frame.pack(padx=10, pady=10)
        self.marketApp.title("Market Statistics")
        self.marketApp.geometry('630x800')

        scroll = tk.Scrollbar(
            self.marketApp, orient='vertical', command=canvas.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(fill=tk.BOTH, expand=1)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        for i in range(len(self.market_data)):
            tk.Label(self.marketApp, text='{} {}'.format(
                self.market_labels[i], self.market_data[i]), font=(16), fg='black', bg='white').pack()

        self.get_binance_bars('ETHUSDT', '12h', dt.datetime(
            2020, 11, 1), dt.datetime(2020, 11, 23))

        months = [dt.datetime(2020, i, 1) for i in range(1, 13)]
        months.append(dt.datetime(2021, 1, 1))

        df_list = [self.get_binance_bars(
            'ETHUSDT', '1h', months[i], months[i + 1] - dt.timedelta(0, 1)) for i in range(0, len(months) - 1)]

        df = pd.concat(df_list)
        f1 = Figure(figsize=(5, 5), dpi=100)
        a = f1.add_subplot(111)
        r = df['close'].astype('float')
        a.plot(r)

        total_market_share = 0
        for i in range(len(self.api_json['data'])):
            coin_market_share = self.api_json['data'][i]['quote']['USD']['market_cap']
            total_market_share += coin_market_share

        name = [self.api_json['data'][i]['name']
                for i in range(len(self.api_json['data']))]
        market_share = [round(((self.api_json['data'][i]['quote']['USD']['market_cap'] /
                                total_market_share) * 100), 3) for i in range(len(self.api_json['data']))]

        name4 = name[:4]
        market_share4 = market_share[:4]
        name4.insert(4, 'other')
        market_share4.insert(4, round(sum(market_share[4:]), 3))

        f2 = Figure(figsize=(5, 5), dpi=100)
        a = f2.add_subplot(111)
        a.pie(market_share4, labels=name4, autopct='%1.0f%%', shadow=True)

        r1 = FigureCanvasTkAgg(f1, frame)
        r1.get_tk_widget().pack()
        r1.draw()

        r2 = FigureCanvasTkAgg(f2, frame)
        r2.get_tk_widget().pack()
        r2.draw()

        def on_frame_resized(self, event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.marketApp.bind('<Configure>', on_frame_resized)
