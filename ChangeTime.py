import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

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