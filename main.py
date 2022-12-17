import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime
import logging


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


x = []
y = []

logging.info("Doing append stuff")
for date in sorted(cum):
    x.append(date)

    y.append(cum[date])

logging.info("Plotting the actual stuff")
for artist in y[-1]:
    l = list(map(lambda t: t[artist] if artist in t else 0, y))
    plt.plot(x, l, label=artist, mouseover=True)


plt.show()