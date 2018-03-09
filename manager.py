#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Date : 2018-02-21 09:20:41
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

import datetime
import Tkinter
import tkMessageBox
from tkintertable.TableModels import TableModel
from tkintertable.Tables import TableCanvas


class ManagerUI(object):
    def __init__(self, top, conn):
        self.top = top
        self.conn = conn

        self.initComponent()

        self.initTable()

        self.quitButton = Tkinter.Button(self.top, text='退出', command=self.top.quit)
        self.quitButton.pack()

    def initComponent(self):
        entryWidth = 40

        self.nameFm = Tkinter.Frame(self.top)
        self.name = Tkinter.StringVar(self.nameFm)
        self.nameLabel = Tkinter.Label(self.nameFm, text='姓名：')
        self.nameLabel.pack(side=Tkinter.LEFT)
        self.nameEntry = Tkinter.Entry(self.nameFm, width=entryWidth, textvariable=self.name)
        self.nameEntry.bind('<Return>', self.get)
        self.nameEntry.pack(side=Tkinter.LEFT)
        self.nameFm.pack()

        self.ageFm = Tkinter.Frame(self.top)
        self.age = Tkinter.StringVar(self.ageFm)
        self.ageLabel = Tkinter.Label(self.ageFm, text='年龄：')
        self.ageLabel.pack(side=Tkinter.LEFT)
        self.ageEntry = Tkinter.Entry(self.ageFm, width=entryWidth, textvariable=self.age)
        self.ageEntry.bind('<Return>', self.get)
        self.ageEntry.pack(side=Tkinter.LEFT)
        self.ageFm.pack()

        self.jointimeFm = Tkinter.Frame(self.top)
        self.jointime = Tkinter.StringVar(self.jointimeFm)
        self.jointimeLabel = Tkinter.Label(self.jointimeFm, text='加入时间：')
        self.jointimeLabel.pack(side=Tkinter.LEFT)
        self.jointimeEntry = Tkinter.Entry(self.jointimeFm, width=entryWidth, textvariable=self.jointime)
        self.jointimeEntry.bind('<Return>', self.get)
        self.jointimeEntry.pack(side=Tkinter.LEFT)
        self.jointimeFm.pack()

        self.btnfm = Tkinter.Frame(self.top)
        self.refreshButton = Tkinter.Button(self.btnfm, text='刷新', command=self.refresh)
        self.addButton = Tkinter.Button(self.btnfm, text='添加', command=self.add)
        self.getButton = Tkinter.Button(self.btnfm, text='查询', command=self.get)
        self.deleteButton = Tkinter.Button(self.btnfm, text='删除', command=self.delete)
        self.resetButton = Tkinter.Button(self.btnfm, text='重置', command=self.reset)
        self.refreshButton.pack(side=Tkinter.LEFT)
        self.addButton.pack(side=Tkinter.LEFT)
        self.getButton.pack(side=Tkinter.LEFT)
        self.deleteButton.pack(side=Tkinter.LEFT)
        self.resetButton.pack(side=Tkinter.LEFT)
        self.btnfm.pack()

    def initTable(self):
        self.tabFm = Tkinter.Frame(self.top)
        self.tabFm.pack(expand=True, fill=Tkinter.BOTH)  # 后期修改
        self.top.geometry('920x700+200+100')

        self.model = TableModel(rows=0, columns=0)  # like HTML
        self.table = TableCanvas(self.tabFm, self.model, cellwidth=120, cellbackgr='#e3f698',
                                 thefont=('Arial', 12), rowheight=22, rowheaderwidth=30,
                                 rowselectedcolor='yellow', editable=False)  # like CSS
        self.table.createTableFrame()

        self.colnames = ('ID', '姓名', '年龄', '加入时间')
        for name in self.colnames:
            self.table.addColumn(name)

        self.refresh()

    def refresh(self, ev=None):
        try:
            rs = self.conn.execute('select * from person')
            rs = rs.fetchall()

            self.model.deleteRows()
            self.table.addRows(len(rs))
            self.table.redrawTable()

            for index, row in enumerate(rs):
                for i in range(len(self.colnames)):
                    if type(row[i]) == unicode:
                        self.model.data[index][self.colnames[i]] = ('' + row[i]).encode('utf8')
                    elif type(row[i]) == datetime.date:
                        self.model.data[index][self.colnames[i]] = row[i].strftime('%Y-%m-%d')
                    else:  # long or float
                        self.model.data[index][self.colnames[i]] = str(row[i])

            self.table.autoResizeColumns()
        except Exception as e:
            tkMessageBox.showinfo('提示', '刷新失败：%s' % e)

    def add(self, ev=None):
        try:
            self.conn.execute('INSERT INTO person(NAME, AGE, JOINTIME) values("%s", %s, "%s")' %
                              (self.name.get().encode('utf8'), self.age.get(), self.jointime.get()))
            self.conn.commit()

            self.refresh()
        except Exception as e:
            tkMessageBox.showinfo('提示', '添加失败：%s' % e)

    def get(self, ev=None):
        try:
            sql = 'select * from person where 1=1'
            if self.name.get():
                sql = sql + ' AND name like "%%%s%%"' % self.name.get()
            if self.age.get():
                sql = sql + ' AND age = %s' % self.age.get()

            rs = self.conn.execute(sql)
            rs = rs.fetchall()

            self.model.deleteRows()
            self.table.addRows(len(rs))
            self.table.redrawTable()

            for index, row in enumerate(rs):
                for i in range(len(self.colnames)):
                    if type(row[i]) == unicode:
                        self.model.data[index][self.colnames[i]] = ('' + row[i]).encode('utf8')
                    elif type(row[i]) == datetime.date:
                        self.model.data[index][self.colnames[i]] = row[i].strftime('%Y-%m-%d')
                    else:  # long or float
                        self.model.data[index][self.colnames[i]] = str(row[i])

            self.table.autoResizeColumns()
        except Exception as e:
            tkMessageBox.showinfo('提示', '查询失败：%s' % e)

    def delete(self, ev=None):
        try:
            self.get()

            sql = 'DELETE FROM person where 1=1'
            if self.name.get():
                sql = sql + ' AND name like "%%%s%%"' % self.name.get()
            if self.age.get():
                sql = sql + ' AND age = %s' % self.age.get()

            if tkMessageBox.askyesnocancel('提示', '确认删除表中的记录？'):
                self.conn.execute(sql)
                self.conn.commit()
                self.refresh()
        except Exception as e:
            tkMessageBox.showinfo('提示', '删除失败：%s' % e)

    def reset(self, ev=None):
        self.name.set('')
        self.age.set('')
        self.jointime.set('')


def init(top, manager):
    ManagerUI(top, manager)
    # Tkinter.mainloop()
