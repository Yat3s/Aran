# -*- coding: utf-8 -*-

import sqlite3

def executeSQL(sql):
    print sql
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()

def createTable():
    executeSQL('create table user (id varchar(20) primary key, name varchar(20), sso varchar(30))')

def insertUser(id, name, sso):
    executeSQL('insert into user (id, name, sso) values (\'' + id + '\', \'' + name + '\', \'' + sso + '\')')

def querySSO(id):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('select sso from user where id=?', (id, ))
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values

def loadAllUser():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('select * from user')
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values
