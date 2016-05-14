import csv
import json
import sys
import os
import time
import numpy as np
from datetime import datetime
from datetime import timedelta
from collections import defaultdict


airport_loc = {}
flight_times = defaultdict(list)
flight_delays = defaultdict(lambda: (0, 0.0, 0.0))
mon_year_del = defaultdict(lambda: (0, 0.0)) # (orig, dest, month, year) --> list of delay vals
dow_del = defaultdict(lambda: (0, 0.0)) # (orig, dest, day_of_week) --> list of delay vals
time_del = defaultdict(lambda: (0, 0.0)) # (orig, dest, time_of_day) --> list of delay vals

# read in any initial delay file
def readInit(fname, dictionary):
    with open(fname) as fil:
        reader = csv.reader(fil)
        next(reader, None)

        for d in reader:
            key = tuple(d[:-2])
            curr = dictionary[key]
            num, tot = int(d[-2]), float(d[-1])
            dictionary[key] = (curr[0] + num, curr[1] + tot)

def main():
    # read in initial price delay file
    with open(price_delay_init) as flight_f:
        reader = csv.reader(flight_f)
        flight_heading = next(reader, None)

        for f in reader:
            key = tuple(f[:-3])
            fd = flight_delays[key]
            num, tot, maxD = int(f[-3]), float(f[-2]), float(f[-1])
            newMaxD = max(maxD, fd[2])
            flight_delays[key] = (fd[0] + num, fd[1] + tot, newMaxD)


    # read in all intial delay files
    readInit(mon_year_init, mon_year_del)
    readInit(dow_init, dow_del)
    readInit(time_init, time_del)

    with open(airport_file) as f:
        reader = csv.reader(f)
        next(reader, None)

        # get lat long values for airports
        for loc in reader:
            airport_loc[loc[0]] = (loc[1], loc[2])

    price_f = output_path + "clean_price_data.csv"
    m_y_f = output_path + "mon_year_delays.csv"
    dow_f = output_path + "dow_delays.csv"
    time_f = output_path + "time_delays.csv"

    # combine all values and write to final output files
    with open(price_f, 'wb') as fout:
        writer = csv.writer(fout)

        new_heading = flight_heading[:-3]
        new_heading.append("avg_delay")
        new_heading.append("max_delay")
        writer.writerow(new_heading)

        for entry in flight_delays:
            row = list(entry)
            fd = flight_delays[entry]
            num, tot, maxD = fd
            avg_delay = (tot/num) if num > 0 else 0.0
            
            row.append(format(avg_delay, '.2f'))
            row.append(maxD)
            writer.writerow(row)

    fout.close()

    with open(m_y_f, 'wb') as fout:
        writer = csv.writer(fout)

        writer.writerow(["Origin", "Org_Lat", "Org_Lon", "Dest", "Dest_Lat", "Dest_Lon", "Month", "Year", "Avg_Delay"])

        for entry in mon_year_del:
            if entry[0] not in airport_loc or entry[1] not in airport_loc:
                continue
            row = [entry[0]]
            row += list(airport_loc[entry[0]])
            row.append(entry[1])
            row += list(airport_loc[entry[1]])
            row.append(entry[2])
            row.append(entry[3])
            myd = mon_year_del[entry]
            num, tot = myd
            avg_delay = (tot/num) if num > 0 else 0.0
            row.append(format(avg_delay, '.2f'))
            writer.writerow(row)

    fout.close()

    with open(dow_f, 'wb') as fout:
        writer = csv.writer(fout)

        writer.writerow(["Origin", "Org_Lat", "Org_Lon", "Dest", "Dest_Lat", "Dest_Lon", "Day_Of_Week", "Avg_Delay"])

        for entry in dow_del:
            if entry[0] not in airport_loc or entry[1] not in airport_loc:
                continue
            row = [entry[0]]
            row += list(airport_loc[entry[0]])
            row.append(entry[1])
            row += list(airport_loc[entry[1]])
            row.append(entry[2])
            dd = dow_del[entry]
            num, tot = dd
            avg_delay = (tot/num) if num > 0 else 0.0
            row.append(format(avg_delay, '.2f'))
            writer.writerow(row)

    fout.close()

    with open(time_f, 'wb') as fout:
        writer = csv.writer(fout)

        writer.writerow(["Origin", "Org_Lat", "Org_Lon", "Dest", "Dest_Lat", "Dest_Lon", "Time_Of_Day", "Avg_Delay"])

        for entry in time_del:
            if entry[0] not in airport_loc or entry[1] not in airport_loc:
                continue
            row = [entry[0]]
            row += list(airport_loc[entry[0]])
            row.append(entry[1])
            row += list(airport_loc[entry[1]])
            row.append(entry[2])
            td = time_del[entry]
            num, tot = td
            avg_delay = (tot/num) if num > 0 else 0.0
            row.append(format(avg_delay, '.2f'))
            writer.writerow(row)

    fout.close()


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print 'Usage: python price_delay_clean2.py price_delay_init mon_year_init dow_init time_init airport_loc output_dir'
    price_delay_init = sys.argv[1]
    mon_year_init = sys.argv[2]
    dow_init = sys.argv[3]
    time_init = sys.argv[4]
    airport_file = sys.argv[5]
    output_path = sys.argv[6]
    main()