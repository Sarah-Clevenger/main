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
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = int((x[-1] - x[0]).days / 5)))
    plt.plot(x, slope, '.')
    plt.gcf().autofmt_xdate()
    plt.title('Total Change in Count Over Time')
    plt.xlabel('Time')
    plt.ylabel('Count')
