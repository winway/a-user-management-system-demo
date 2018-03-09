#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Date : 2018-02-20 23:20:44
# @Link : https://winway.github.io
# @Version : 0.1
# @Description : 这个家伙很懒，没有留下任何信息
# @History :
# @Other:
#
#      ┏┛ ┻━━━━━┛ ┻┓
#      ┃　　　　　　 ┃
#      ┃　　　━　　　┃
#      ┃　┳┛　  ┗┳　┃
#      ┃　　　　　　 ┃
#      ┃　　　┻　　　┃
#      ┃　　　　　　 ┃
#      ┗━┓　　　┏━━━┛
#        ┃　　　┃   GOD BLESS!
#        ┃　　　┃    NO BUG！
#        ┃　　　┗━━━━━━━━━┓
#        ┃　　　　　　　    ┣┓
#        ┃　　　　         ┏┛
#        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
#          ┃ ┫ ┫   ┃ ┫ ┫
#          ┗━┻━┛   ┗━┻━┛

r"""
docstring for module
"""

import Tkinter
import tkMessageBox
import sqlite3

import manager


class LoginUI(object):
    def __init__(self):
        self.top = Tkinter.Tk()

        self.userNameFm = Tkinter.Frame(self.top)
        self.userName = Tkinter.StringVar(self.userNameFm)
        self.userNameLabel = Tkinter.Label(self.userNameFm, text='用户名：')
        self.userNameLabel.pack(side=Tkinter.LEFT)
        self.userNameEntry = Tkinter.Entry(self.userNameFm, width=20, textvariable=self.userName)
        self.userNameEntry.pack(side=Tkinter.LEFT)
        self.userNameFm.pack()

        self.passwordFm = Tkinter.Frame(self.top)
        self.password = Tkinter.StringVar(self.passwordFm)
        self.passwordLabel = Tkinter.Label(self.passwordFm, text='密码：')
        self.passwordLabel.pack(side=Tkinter.LEFT)
        self.passwordEntry = Tkinter.Entry(self.passwordFm, width=20, show='*', textvariable=self.password)
        self.passwordEntry.bind('<Return>', self.login)
        self.passwordEntry.pack(side=Tkinter.LEFT)
        self.passwordFm.pack()

        self.btnfm = Tkinter.Frame(self.top)
        self.loginButton = Tkinter.Button(self.btnfm, text='登陆', command=self.login)
        self.loginButton.pack(side=Tkinter.LEFT)
        self.quitButton = Tkinter.Button(self.btnfm, text='退出', command=self.top.quit)
        self.quitButton.pack(side=Tkinter.LEFT)
        self.btnfm.pack()

        # test
        self.userName.set('admin')
        self.password.set('123456')

    def login(self, ev=None):
        if self.userName.get() == 'admin' and self.password.get() == '123456':
            conn = self.initDB()
            if conn:
                self.clear()
                manager.init(self.top, conn)
                # self.top.quit()  # 别忘了加这句话，要不然 Manager 的 quitButton 要按两次
        else:
            tkMessageBox.showinfo('提示', '用户名或密码错误')

    def initDB(self):
        try:
            conn = sqlite3.connect('data.db')
            conn.execute('''CREATE TABLE IF NOT EXISTS person(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NAME TEXT NOT NULL,
                            AGE INTEGER NOT NULL,
                            JOINTIME DATE not null);''')
            conn.commit()
            return conn
        except Exception as e:
            tkMessageBox.showinfo('提示', e)

        return None

    def clear(self):
        self.userNameFm.pack_forget()
        # self.userNameLabel.pack_forget()
        # self.userNameEntry.pack_forget()
        self.passwordFm.pack_forget()
        # self.passwordLabel.pack_forget()
        # self.passwordEntry.pack_forget()
        self.btnfm.pack_forget()
        # self.loginButton.pack_forget()
        # self.quitButton.pack_forget()


def init():
    LoginUI()
    Tkinter.mainloop()
