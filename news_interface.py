import tkinter as tk
import requests
from tkinter import scrolledtext
import tkinter.ttk as ttk1
from datetime import date
import random


class NewsApp():
    def __init__(self):
        self.newsApp = tk.Tk()
        self.newsApp.title("Latest news update for Cryptocurrencies")
        self.newsApp.geometry('1050x800')
        self.api = requests.get(
            "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=132cabf1-5b55-43f6-9cff-ce32c8d37c3e")
        self.api_json = self.api.json()
        self.menu()
        self.newsApp.mainloop()

    def menu(self):
        self.coin_dict = dict()

        for coin in range(len(self.api_json['data'])):
            self.coin_dict[self.api_json['data'][coin]['name']
                           ] = self.api_json['data'][coin]['symbol']

        label = tk.Label(
            self.newsApp, text="Get Latest Crypto News Updates", font=('Courier', 35))
        label.place(relx=0.1, rely=0.01, relwidth=0.75, relheight=0.1)

        frame = tk.Frame(self.newsApp, bg='black', bd=3, relief=tk.SUNKEN)
        frame.place(relx=0.5, rely=0.1, relwidth=0.75,
                    relheight=0.1, anchor='n')

        self.combo = ttk1.Combobox(
            frame, width=50, height=50, font=('courier', 25))
        self.combo['value'] = ("Select Cryptocurrency",)

        for i in self.coin_dict:
            self.combo['values'] = (*self.combo['values'], i)

        self.combo.current(0)
        self.combo.place(relx=0.005, rely=0.25, relwidth=0.65, relheight=0.5)
        button = tk.Button(frame, text='GO', font=(
            'Courier', 25), command=self.clicked)
        button.place(relx=0.7, rely=0.25, relwidth=0.3, relheight=0.5,)

    def clicked(self):
        coin = self.combo.get()

        if coin == '':
            pass

        else:
            coin = self.coin_dict[coin]
            news = requests.get(
                "http://newsapi.org/v2/everything?q={}&from={}&sortBy=publishedAt&apiKey=440d055069644605bd696bf397dbe640".format(coin, date.today()))
            news_json = news.json()

            lower_frame = tk.Frame(self.newsApp, bg='black', bd=10)
            lower_frame.place(relx=0.5, rely=0.25,
                              relwidth=0.75, relheight=0.6, anchor='n')

            txt = scrolledtext.ScrolledText(
                lower_frame, width=40, height=10, wrap='word')
            txt.place(relwidth=1, relheight=1)

            j = 0
            for i in news_json['articles']:
                j = j + 1
                txt.insert(tk.INSERT, '\t\t\t\t\t\tHeadline {}'.format(
                    j) + '\n', 'headline')
                txt.insert(tk.INSERT, i['description'] + '\n\n', 'description')
                txt.insert(tk.INSERT, i['url'] + '\n\n', 'url')
                txt.tag_config('title', font=('Courier', 16, 'bold'))
                txt.tag_config('description', font=('Courier', 14))
                txt.tag_config('url', font=('Courier', 15))
