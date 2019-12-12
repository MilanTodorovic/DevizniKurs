import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
import datetime as dt
import numpy as np
import DB

lst = DB.read_db()
print(lst)
np_nbs = np.array(lst[0])
np_erste = np.array(lst[1])
np_raiff = np.array(lst[2])

dates = []
for l in lst[3]:
    for d in l:
        dates.append(d)

x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]

fig, ax = plt.subplots(1)

fig.autofmt_xdate()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())

red_patch = mpatches.Patch(color='red', label='Raiffeisen')
blue_patch = mpatches.Patch(color='blue', label='Erste')
yellow_patch = mpatches.Patch(color='yellow', label='NBS')

plt.legend(handles=[red_patch, blue_patch, yellow_patch])

plt.plot(x,np_nbs,'y-')
plt.plot(x,np_erste,'b-')
plt.plot(x,np_raiff,'r-')

plt.grid(b=True, which='major', color='b', linestyle='-')

plt.title('Prodajna efektiva')

plt.show()
