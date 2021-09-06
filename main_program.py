import tkinter as tk
from news_interface import NewsApp
from market_interface import MarketApp
from portfolio_interface import RegisterLogin
import sqlite3

class MainPage:
    def __init__(self):
        self.main = tk.Tk()
        self.main.title("Main Page")
        self.design()
        self.main.mainloop()

    def design(self):
        my_portfolio = tk.Button(self.main, text="Portfolio", command=self.btn_login,
                                 fg='black', font="Lato 18 bold", borderwidth=4, padx="35", pady="30").pack()

        news = tk.Button(self.main, text="News", command=self.btn_news, fg='black',
                         font="Lato 18 bold", borderwidth=4, padx="48", pady="30").pack()

        market_stats = tk.Button(self.main, text="Market", command=self.btn_market, fg='black',
                                 font="Lato 18 bold", borderwidth=4, padx="48", pady="30").pack()

        close_app = tk.Button(self.main, text="Close", command=self.btn_close,
                              fg='black', font="Lato 28 bold", borderwidth=4, padx="15", pady="15").pack()

    def btn_login(self):
        self.main.destroy()
        registerLogin = RegisterLogin()
        MainPage()

    def btn_news(self):
        self.main.destroy()
        newsApp = NewsApp()
        MainPage()

    def btn_market(self):
        self.main.destroy()
        marketApp = MarketApp()
        MainPage()

    def btn_close(self):
        self.main.destroy()

if __name__ == "__main__":
    app = MainPage()
    print('Runtime Completed')
