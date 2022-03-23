import sqlite3
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt
import sqlalchemy as sa
import base64
    
def ChangeTime(db):
    xaxis = []
    for entry in db:
        v = dt.datetime.fromtimestamp(db[entry]['integratedTime'])
        xaxis.append(dt.date(v.year, v.month, v.day))
    
    x = []
    y = []
    for j in xaxis:
        if j not in x:
            x.append(j)
            y.append(xaxis.count(j))
    
    slope = [y[0]]
    for k in range(len(x) - 1):
        slope.append(y[k + 1] - y[k])
        
    i = int((365 * (x[-1].year - x[0].year) + 30 * (x[-1].month - x[0].month) + x[-1].day - x[0].day) / 5)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = i))
    plt.plot(x, slope)
    plt.gcf().autofmt_xdate()

def DistBar(db):
    formats = []
    for entry in db:
        formats.append(db[entry]['body']['spec']['signature']['format'])
        
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

def DistTime(db):
    formats = []
    xaxis = []
    for entry in db:
        formats.append(db[entry]['body']['spec']['signature']['format'])
        v = dt.datetime.fromtimestamp(db[entry]['integratedTime'])
        xaxis.append(dt.date(v.year, v.month, v.day))
    
    labels = []
    for i in formats:
        if i not in labels:
            labels.append(i)
        
    i = int((365 * (xaxis[-1].year - xaxis[0].year) + 30 * (xaxis[-1].month - xaxis[0].month) + xaxis[-1].day - xaxis[0].day) / 5)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(labels)))
    
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
    
def Table(db):
    metadata = sa.MetaData()
    
    formats = []
    xaxis = []
    for entry in db:
        formats.append(db[entry]['body']['spec']['signature']['format'])
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
    
def TotalTime(db):
    x = []
    y = []
    for entry in db:
        v = dt.datetime.fromtimestamp(db[entry]['integratedTime'])
        x.append(dt.date(v.year, v.month, v.day))
        y.append(len(x))
        
    i = int((365 * (x[-1].year - x[0].year) + 30 * (x[-1].month - x[0].month) + x[-1].day - x[0].day) / 5)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = i))
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()

def main():
    con = sqlite3.connect('testy2.db')
    cur = con.execute('SELECT * FROM entries ORDER BY idx')

    db = {}
    for row in cur:
        db[row[0]] = json.loads(row[1])
        
    for i in db:
        db[i]['body'] = json.loads(base64.b64decode(db[i]['body']))
    
    # ChangeTime(db)
    # DistBar(db)
    # DistTime(db)
    # Table(db)
    # TotalTime(db)
                    
if __name__ == '__main__':
    main()
