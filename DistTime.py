import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import numpy as np

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
