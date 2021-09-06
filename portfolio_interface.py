import tkinter as tk
from datetime import date
from tkinter import messagebox, Menu
import sqlite3
import hashlib
import requests
import json
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import scrolledtext
style.use('dark_background')


class RegisterLogin():
    def __init__(self):
        self.registerPortal = tk.Tk()
        self.registerPortal.title("Login Portal")
        self.registerPortal.geometry("400x200")
        self.design_register()
        self.registerPortal.mainloop()

    def design_register(self):
        login = tk.Button(self.registerPortal, text="Login", command=self.btn_login, fg='black',
                          font="Lato 18 bold", borderwidth=4, padx="48", pady="30").pack()

        register = tk.Button(self.registerPortal, text="New User", command=self.btn_register,
                             fg='black', font="Lato 18 bold", borderwidth=4, padx="35", pady="30").pack()

    def btn_register(self):
        self.registerPortal.destroy()
        NewUser()

    def btn_login(self):
        self.registerPortal.destroy()
        LoginPage()


class NewUser():
    def __init__(self):
        self.con = sqlite3.connect('crypto.db')
        self.cursorObj = self.con.cursor()
        self.cursorObj.execute(
            "CREATE TABLE IF NOT EXISTS users(Id INTEGER, Username PRIMARY KEY, Password)")
        self.newUser = tk.Tk()
        self.newUser.title("New Account")
        self.newUser.geometry("800x500")
        self.id = 0
        self.username = ''
        self.design_newuser()
        self.newUser.mainloop()
        self.cursorObj.close()
        self.con.close()

    def design_newuser(self):
        title = tk.Label(self.newUser, text='Enter Your Details:', font=(
            'impact', 40, 'bold'), fg='black', bg='white').pack()

        space = tk.Label(self.newUser, text='', height=2).pack()

        name_title = tk.Label(self.newUser, text='User Name:', font=(
            'Goudy old style', 15, 'bold'), fg='black', bg='white').pack()

        self.name = tk.Entry(self.newUser, bg="white", fg="black",
                             font="Lato 12", borderwidth=6, relief="sunken")
        self.name.pack()

        space = tk.Label(self.newUser, text='', height=1).pack()

        password_title = tk.Label(self.newUser, text='Password:', font=(
            'Goudy old style', 15, 'bold'), fg='black', bg='white').pack()

        self.password = tk.Entry(self.newUser, show='*', bg="white",
                                 fg="black", font="Lato 12", borderwidth=6, relief="sunken")
        self.password.pack()

        space = tk.Label(self.newUser, text='', height=1).pack()

        move_to_portofolio = tk.Button(self.newUser, text='Save and move to your portfolio', command=self.btn_command, font=(
            'Goudy old style', 15), bd=0, fg='black', bg='white').pack()

    def btn_command(self):
        NewUser.username = self.name.get()
        self.passwordSTORED = self.password.get()
        self.passwordSTORED = hashlib.sha256(
            str(self.passwordSTORED).encode()).hexdigest()
        self.id += 1
        self.name.delete(0, tk.END)
        self.password.delete(0, tk.END)
        try:
            self.cursorObj.execute("Insert INTO users(Id, Username, Password) VALUES(?, ?, ?)", (
                self.id, NewUser.username, self.passwordSTORED,))
            self.con.commit()
            messagebox.showinfo(
                "Successfully Entered Your Details", "Now Login to your Portfolio")
            self.newUser.destroy()
        except:
            messagebox.showinfo(
                "Login Error", "Try again, the username already in use")


class LoginPage():
    def __init__(self):
        self.con = sqlite3.connect('crypto.db')
        self.cursorObj = self.con.cursor()
        self.loginPortal = tk.Tk()
        self.loginPortal.title('Login Page')
        self.loginPortal.geometry('500x500')
        self.usernameStored = ''
        self.design_login()
        self.loginPortal.mainloop()

    def design_login(self):
        frame = tk.LabelFrame(self.loginPortal, text="Login to your portfolio {}".format(date.today()), font="Lato 30 bold",
                              fg='white', padx=50, pady=50).pack()

        title = tk.Label(frame, text='Login Here', font=(
            'impact', 40, 'bold'), fg='black', bg='white').place(x=130, y=20)

        desc = tk.Label(frame, text='Login to your Portfolio Account', font=(
            'Goudy old style', 15, 'bold'), fg='black', bg='white').place(x=100, y=100)

        user = tk.Label(frame, text='User Name:', font=(
            'Goudy old style', 15, 'bold'), fg='black', bg='white').place(x=100, y=130)
        self.user_name = tk.Entry(
            frame, bg="white", fg="black", font="Lato 12", borderwidth=6, relief="sunken")
        self.user_name.place(x=100, y=160, height=30, width=240)

        password = tk.Label(frame,  text='Password:', font=(
            'Goudy old style', 15), fg='black', bg='white').place(x=100, y=200)
        self.user_password = tk.Entry(
            frame, show='*', bg="white", fg="black", font="Lato 12", borderwidth=6, relief="sunken")
        self.user_password.place(x=100, y=230, height=30, width=240)

        login = tk.Button(frame, command=self.btn_command, text="Login", font=(
            'Goudy old style', 15)).place(x=150, y=300, width=150, height=40)

    def btn_command(self):
        self.username2 = self.user_name.get()
        self.passwordSTORED2 = self.user_password.get()
        self.passwordSTORED2 = hashlib.sha256(
            str(self.passwordSTORED2).encode()).hexdigest()
        try:
            self.user_name.delete(0, tk.END)
            self.user_password.delete(0, tk.END)
            self.cursorObj.execute("SELECT * FROM users")
            users = self.cursorObj.fetchall()
            names = [users[i][1] for i in range(len(users))]
            passwords = [users[i][2] for i in range(len(users))]
            if (self.username2 in names) and (self.passwordSTORED2 in passwords):
                LoginPage.usernameStored = self.username2
                self.loginPortal.destroy()
                Portfolio()
            else:
                messagebox.showinfo("Login Error", "Try again")
        except:
            messagebox.showinfo(
                "Login Error", """Try again, or maybe you don't have an account if so close the window and you will
                be redirected to the main page to create an account""")


class Portfolio(LoginPage):
    def __init__(self):
        self.con = sqlite3.connect('crypto.db')
        self.cursorObj = self.con.cursor()
        self.cursorObj.execute("CREATE TABLE IF NOT EXISTS {}(symbol TEXT PUBLIC KEY, amount INTEGER, price REAL)".format(
            LoginPage.usernameStored))
        self.con.commit()
        self.pycrypto = tk.Tk()
        self.pycrypto.title("{}'s Portfolio".format(
            LoginPage.usernameStored.title()))
        self.coins = []
        self.pie = []
        self.pie_size = []
        self.app_header()
        self.my_portfolio()
        self.app_nav()
        self.pycrypto.mainloop()
        self.cursorObj.close()
        self.con.close()

    def reset(self):
        for cell in self.pycrypto.winfo_children():
            cell.destroy()
        self.app_header()
        self.my_portfolio()
        self.app_nav()

    def app_nav(self):
        def clear_all():
            self.cursorObj.execute("DELETE FROM coin")
            self.con.commit()

            messagebox.showinfo("Portfolio Notification",
                                "Portfolio Cleared - Add New Coins")
            reset()

        def close_app():
            pycrypto.destroy()

        menu = Menu(self.pycrypto)
        file_item = Menu(menu)
        file_item.add_command(label='Clear Portfolio', command=clear_all)
        file_item.add_command(label='Close App', command=close_app)
        menu.add_cascade(label="File", menu=file_item)
        self.pycrypto.config(menu=menu)

    def my_portfolio(self):
        api_request = requests.get(
            "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=5000&convert=USD&CMC_PRO_API_KEY=132cabf1-5b55-43f6-9cff-ce32c8d37c3e")
        api = json.loads(api_request.content)

        def font_color(amount):
            if amount < 0:
                return "red"
            else:
                return "green"

        def insert_coin():
            self.cursorObj.execute("INSERT INTO {}(symbol, price, amount) VALUES(?, ?, ?)".format(
                LoginPage.usernameStored), (symbol_text.get(), price_text.get(), amount_text.get(),))
            self.con.commit()
            messagebox.showinfo("Portfolio Notification",
                                "Coin Added to Portfolio Successfully!")
            self.reset()

        def update_coin():
            self.cursorObj.execute("UPDATE {} SET price=?, amount=? WHERE symbol=?".format(
                LoginPage.usernameStored), (price_update.get(), amount_update.get(), symbol_update.get(),))
            self.con.commit()
            messagebox.showinfo("Portfolio Notification",
                                "Coin Updated to Portfolio Successfully!")
            self.reset()

        def delete_coin():
            self.cursorObj.execute("DELETE FROM {} WHERE symbol=?".format(
                LoginPage.usernameStored), (port_id_delete.get(),))
            self.con.commit()
            messagebox.showinfo("Portfolio Notification",
                                "Coin Deleted from Portfolio Successfully!")
            self.reset()

        self.cursorObj.execute(
            "SELECT * FROM {}".format(LoginPage.usernameStored))
        self.coins = self.cursorObj.fetchall()

        total_pl = 0
        coin_row = 1
        total_current_value = 0
        total_amount_paid = 0

        for i in range(0, 500):
            for coin in self.coins:
                if api["data"][i]["symbol"] == coin[0]:
                    total_paid = coin[1] * coin[2]
                    current_value = coin[1] * \
                        api["data"][i]["quote"]["USD"]["price"]
                    total_current_value += current_value
                    pl_percoin = api["data"][i]["quote"]["USD"]["price"] - \
                        float(coin[2])
                    total_pl_coin = pl_percoin * coin[1]

                    total_pl += total_pl_coin
                    total_amount_paid += total_paid

                    name = tk.Label(self.pycrypto, text=api["data"][i]["symbol"], bg="white", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                    name.grid(row=coin_row, column=1)

                    price = tk.Label(self.pycrypto, text="${0:.2f}".format(
                        api["data"][i]["quote"]["USD"]["price"]), bg="white", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                    price.grid(row=coin_row, column=2)

                    no_coins = tk.Label(self.pycrypto, text=coin[1], bg="white", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                    no_coins.grid(row=coin_row, column=3)

                    amount_paid = tk.Label(self.pycrypto, text="${0:.2f}".format(
                        total_paid), bg="white", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                    amount_paid.grid(row=coin_row, column=4)

                    current_val = tk.Label(self.pycrypto, text="${0:.2f}".format(current_value), bg="white", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                    current_val.grid(row=coin_row, column=5)

                    pl_coin = tk.Label(self.pycrypto, text="${0:.2f}".format(pl_percoin), bg="white", fg=font_color(
                        pl_percoin), font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                    pl_coin.grid(row=coin_row, column=6)

                    totalpl = tk.Label(self.pycrypto, text="${0:.2f}".format(total_pl_coin), bg="white", fg=font_color(
                        total_pl_coin), font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                    totalpl.grid(row=coin_row, column=7)

                    coin_row += 1

        totalcurrentvalue = tk.Label(self.pycrypto, text="${0:.2f}".format(total_current_value), bg="gray", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
        totalcurrentvalue.grid(row=coin_row, column=5)

        totalpl = tk.Label(self.pycrypto, text="${0:.2f}".format(total_pl), bg="white", fg=font_color(float("{0:.2f}".format(
            total_pl))), font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
        totalpl.grid(row=coin_row, column=7)

        totalamountpaid = tk.Label(self.pycrypto, text="${0:.2f}".format(
            total_amount_paid), bg="gray", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
        totalamountpaid.grid(row=coin_row, column=4)

        api = ""
        # Insert data

        symbol_text = tk.Entry(self.pycrypto, borderwidth=2, relief="groove")
        symbol_text.grid(row=coin_row + 1, column=1)

        price_text = tk.Entry(self.pycrypto, borderwidth=2, relief="groove")
        price_text.grid(row=coin_row + 1, column=2)

        amount_text = tk.Entry(self.pycrypto, borderwidth=2, relief="groove")
        amount_text.grid(row=coin_row + 1, column=3)

        add_coin = tk.Button(self.pycrypto, text="Add Coin", command=insert_coin, bg="cyan",
                             fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
        add_coin.grid(row=coin_row + 1, column=4)

        # update data
        symbol_update = tk.Entry(self.pycrypto, borderwidth=2, relief="groove")
        symbol_update.grid(row=coin_row + 2, column=1)

        price_update = tk.Entry(self.pycrypto, borderwidth=2, relief="groove")
        price_update.grid(row=coin_row + 2, column=2)

        amount_update = tk.Entry(self.pycrypto, borderwidth=2, relief="groove")
        amount_update.grid(row=coin_row + 2, column=3)

        update_coin = tk.Button(self.pycrypto, text="Update Coin", command=update_coin, bg="cyan",
                                fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
        update_coin.grid(row=coin_row + 2, column=4)

        # delete coin
        port_id_delete = tk.Entry(
            self.pycrypto, borderwidth=2, relief="groove")
        port_id_delete.grid(row=coin_row + 3, column=1)

        delete_coin = tk.Button(self.pycrypto, text="Delete Coin", command=delete_coin, bg="cyan",
                                fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
        delete_coin.grid(row=coin_row + 3, column=4)

        refresh = tk.Button(self.pycrypto, text="Refresh", command=self.reset, bg="cyan",
                            fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
        refresh.grid(row=coin_row + 1, column=7)

        chart_button = tk.Button(self.pycrypto, text="Pie", command=self.chart, fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
        chart_button.grid(row=coin_row + 2, column=7)

    def app_header(self):
        name = tk.Label(self.pycrypto, text="Coin Name", bg="#000000", fg="white",
                        font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
        name.grid(row=0, column=1)

        price = tk.Label(self.pycrypto, text="Price", bg="#000000", fg="white",
                         font="Lato 12 bold",  padx="5", pady="5", borderwidth=2, relief="groove")
        price.grid(row=0, column=2)

        no_coins = tk.Label(self.pycrypto, text="Coin Owned", bg="#000000", fg="white",
                            font="Lato 12 bold",  padx="5", pady="5", borderwidth=2, relief="groove")
        no_coins.grid(row=0, column=3)

        amount_paid = tk.Label(self.pycrypto, text="Total Amount Paid", bg="#000000", fg="white",
                               font="Lato 12 bold",  padx="5", pady="5", borderwidth=2, relief="groove")
        amount_paid.grid(row=0, column=4)

        current_val = tk.Label(self.pycrypto, text="Current Value", bg="#000000", fg="white",
                               font="Lato 12 bold",  padx="5", pady="5", borderwidth=2, relief="groove")
        current_val.grid(row=0, column=5)

        pl_coin = tk.Label(self.pycrypto, text="P/L Per Coin", bg="#000000", fg="white",
                           font="Lato 12 bold",  padx="5", pady="5", borderwidth=2, relief="groove")
        pl_coin.grid(row=0, column=6)

        totalpl = tk.Label(self.pycrypto, text="Total P/L With coin", bg="#000000", fg="white",
                           font="Lato 12 bold",  padx="5", pady="5", borderwidth=2, relief="groove")
        totalpl.grid(row=0, column=7)

    def chart(self):
        labels = [coin[0] for coin in self.coins]
        sizes = [coin[1] for coin in self.coins]
        coinsShare = plt.pie(sizes, autopct='%1.0f%%', shadow=True)
        plt.gcf().canvas.set_window_title('Your Coins')
        plt.legend(labels, loc="best")
        # Equal aspect ratio ensures that self.pie is drawn as a circle.
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
