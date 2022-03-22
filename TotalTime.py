import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

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