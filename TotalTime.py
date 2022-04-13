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

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = int((x[-1] - x[0]).days / 5)))
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.title('Total Count Over Time Graph')
    plt.xlabel('Time')
    plt.ylabel('Count')
