import matplotlib.pyplot as plt
import numpy as np

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
