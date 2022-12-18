import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime
import logging
import multiprocessing.dummy as mp



# Artist, Album, Name, Date
def read_csv(filename: str) -> dict:
    dates: dict = {}

    for cols in csv.reader(open(filename, "r")):
        date_str = cols[3]
        if not date_str:
            continue
        
        d = datetime.strptime(date_str, "%d %b %Y %H:%M")#.date()

        artist = cols[0]

        if d not in dates.keys():
            dates[d] = {}
        
        if artist not in dates[d].keys():
            dates[d][artist] = 0

        dates[d][artist] += 1
    
    return dates

def get_dates_cum(dates: dict) -> dict:
    current_artist_numbers = {}
    dates_cum = {}

    for date in sorted(dates):

        for artist in dates[date]:
            if artist not in current_artist_numbers.keys():
                current_artist_numbers[artist] = 0
            
            current_artist_numbers[artist] += dates[date][artist]
        
        dates_cum[date] = current_artist_numbers.copy()
    
    return dates_cum;

logging.basicConfig(level=logging.INFO)
filename = input("Name of csv file? ")

logging.info("Reading CSV")
csvstuff = read_csv(filename)
logging.info("Converting to cum")
cum = get_dates_cum(csvstuff)
cum_sorted = sorted(cum)

amount_of_artists = len(cum[cum_sorted[-1]])

#x = np.empty(0, datetime)
#y = np.empty(0, dict)

logging.info("Doing append stuff")
#for date in sorted(cum):
#    x = np.append(x, date)
#
#    y = np.append(y, cum[date])

x = np.array(cum_sorted, datetime)
y = np.fromiter(
    map(
        lambda date: cum[date],
        cum_sorted
    ),
    dict,
    len(cum_sorted)
)

logging.info("Plotting the actual stuff")

#y_axes = np.empty((len(y[-1]), len(x)), int)
#y_axes = []


y_axes = np.fromiter(
    map(
        lambda artist: (
            np.fromiter(
                map(
                    lambda time: time[artist] if artist in time else 0,
                    y
                ),
                int,
                len(y)
            )
        ),
        y[-1]
    ),
    np.ndarray,
    len(y[-1])
)

y_axes = np.stack(y_axes)

#i = 0
#for artist in y[-1]:
#    axis = map(lambda t: t[artist] if artist in t else 0, y)
#    y_axes[i] = np.fromiter(map(lambda t: t[artist] if artist in t else 0, y), int, count=len(y))
#    i += 1
#    #plt.plot(x, l, label=artist, mouseover=True)

logging.info("Turning it into an array")

y_axes = np.array(y_axes)
y_axes = y_axes.transpose()
plt.plot(x, y_axes)
plt.ioff()
plt.show()