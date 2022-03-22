import sqlite3
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt
import math
import sqlalchemy as sa
import base64
import sys

def TotalTime(db):
    x = []
    y = []
    for entry in db:
        v = dt.datetime.fromtimestamp(db[entry]['IntegratedTime'])
        x.append(dt.date(v.year, v.month, v.day))
        y.append(len(x))
        
    i = int((365 * (x[-1].year - x[0].year) + 30 * (x[-1].month - x[0].month) + x[-1].day - x[0].day) / 5)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = i))
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    
def ChangeTime(db):
    x = []
    yaxis = []
    for entry in db:
        v = dt.datetime.fromtimestamp(db[entry]['IntegratedTime'])
        x.append(dt.date(v.year, v.month, v.day))
        yaxis.append(len(x))
    
    y = []
    for k in x:
        n = 1
        result  = 0
        for m in range(0, n + 1):
            sign = (-1)**m
            coefficient = math.comb(n, m)
            entry = yaxis[-1 - m]
            result += sign * coefficient * entry
        y.append(result)
        
    i = int((365 * (x[-1].year - x[0].year) + 30 * (x[-1].month - x[0].month) + x[-1].day - x[0].day) / 5)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = i))
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    
def DistTime(db):
    formats = []
    xaxis = []
    for entry in db:
        formats.append(db[entry]['Body']['RekordObj']['signature']['format'])
        v = dt.datetime.fromtimestamp(db[entry]['IntegratedTime'])
        xaxis.append(dt.date(v.year, v.month, v.day))
    
    labels = []
    for i in formats:
        if i not in labels:
            labels.append(i)
        
    i = int((365 * (xaxis[-1].year - xaxis[0].year) + 30 * (xaxis[-1].month - xaxis[0].month) + xaxis[-1].day - xaxis[0].day) / 5)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(xaxis)))
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = i))
    for m in range(len(labels)):
        x = []
        y = []
        for n in range(len(formats)):
            if formats[n] == labels[m]:
                x.append(xaxis[n])
                y.append(len(x))
        plt.plot(x, y, label = labels[m], color = colors[m])
    plt.gcf().autofmt_xdate()
    plt.legend()

def DistBar(db):
    formats = []
    for entry in db:
        formats.append(db[entry]['Body']['RekordObj']['signature']['format'])
        # formats.append(db[entry]['spec']['signature']['format'])
        
    x = []
    y = []
    for i in formats:
        if i not in y:
            y.append(i)
            x.append(formats.count(i))

    x, y = zip(*sorted(zip(x, y)))
    colors = plt.cm.rainbow(np.linspace(0, 1, len(x)))
    
    plt.barh(y, x, color = colors)
    plt.title('Formats')
    plt.xlabel('Count')
    plt.ylabel('Type')
    plt.show()
    
def Table(db):
    metadata = sa.MetaData()
    
    formats = []
    xaxis = []
    for entry in db:
        formats.append(db[entry]['Body']['RekordObj']['signature']['format'])
        v = dt.datetime.fromtimestamp(db[entry]['IntegratedTime'])
        xaxis.append(dt.date(v.year, v.month, v.day))
    
    labels = []
    for i in formats:
        if i not in labels:
            labels.append(i)
    
    times = []
    count = []
    total = []
    for m in range(len(labels)):
        x = []
        y = []
        for n in range(len(formats)):
            if formats[n] == labels[m]:
                x.append(xaxis[n])
                y.append(len(x))
        times.append(x)
        count.append(y)
        total.append(y[-1])
    
    table = sa.Table('table', metadata, 
        sa.Column('type', sa.String, primary_key = True),
        sa.Column('time', sa.DateTime, nullable = False),
        sa.Column('count', sa.Integer, key = 'count'), 
        sa.Column('total', sa.Integer, nullable = False))

def main():
    con = sqlite3.connect('testy2.db')
    # con = sqlite3.connect('test.db')
    cur = con.execute('SELECT * FROM entries ORDER BY idx')

    db = {}
    for row in cur:
        db[row[0]] = json.loads(row[1])
        
    # target = sys.stdin.readline()
    # target = sys.stdin.readline()

    # while True:
    #     target = sys.stdin.readline()
    #     target = sys.stdin.readline()
    #     payload = json.loads(target)
    #     payload['body'] = json.loads(base64.b64decode(payload['body']))
    
    # Table(db)
    # DistBar(db)
    # TotalTime(db)
    # DistTime(db)
    # ChangeTime(db)
                    
if __name__ == '__main__':
    main()