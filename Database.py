import sqlite3
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt
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
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = int((x[-1] - x[0]).days / 5)))
    plt.plot(x, slope, '.')
    plt.gcf().autofmt_xdate()
    plt.title('Total Change in Count Over Time')
    plt.xlabel('Time')
    plt.ylabel('Count')

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
    plt.title('Distribution of Formats')
    plt.xlabel('Count')
    plt.ylabel('Format')

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
        
    colors = plt.cm.rainbow(np.linspace(0, 1, len(labels)))
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = int((xaxis[-1] - xaxis[0]).days / 5)))
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
    plt.title('Distribution Formats Over Time')
    plt.xlabel('Time')
    plt.ylabel('Count')
    
def TotalTime(db):
    x = []
    y = []
    for entry in db:
        v = dt.datetime.fromtimestamp(db[entry]['integratedTime'])
        x.append(dt.date(v.year, v.month, v.day))
        y.append(len(x))

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = int((x[-1] - x[0]).days / 5)))
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.title('Total Count Over Time Graph')
    plt.xlabel('Time')
    plt.ylabel('Count')

def main():
    con = sqlite3.connect('testy2.db')
    cur = con.execute('SELECT * FROM entries ORDER BY idx')

    db = {}
    for row in cur:
        db[row[0]] = json.loads(row[1])
        
    for i in db:
        db[i]['body'] = json.loads(base64.b64decode(db[i]['body']))
    
    figures = [ChangeTime, DistBar, DistTime, TotalTime]
    for t in figures:
        plt.figure()
        t(db)
                    
if __name__ == '__main__':
    main()
