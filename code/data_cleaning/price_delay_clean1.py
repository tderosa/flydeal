import csv
import json
import sys
import os
import time
import numpy as np
from datetime import datetime
from datetime import timedelta
from collections import defaultdict


flight_times = defaultdict(list)
flight_delays = defaultdict(lambda: (0, 0.0, 0.0))
mon_year_del = defaultdict(lambda: (0, 0.0)) # (orig, dest, month, year) --> list of delay vals
dow_del = defaultdict(lambda: (0, 0.0)) # (orig, dest, day_of_week) --> list of delay vals
time_del = defaultdict(lambda: (0, 0.0)) # (orig, dest, time_of_day) --> list of delay vals
expected_heading = ["YEAR","MONTH","DAY_OF_MONTH","ORIGIN","DEST","CRS_DEP_TIME","DEP_DELAY", ""]


def main():
    # Read in flight data
    fjson = open(flight_data_path, 'r')
    json_data = json.loads(fjson.read())

    # store (from_airport, to_airport) --> time
    for entry in json_data['data']:
        dt = datetime.fromtimestamp(entry['departure_time'])
        flight_times[(entry['from_airport'], entry['to_airport'])].append(dt.replace(year=1900, month=1, day=1))
        

    delay_files = os.listdir(to_clean_path)
    for fname in delay_files:
        path = to_clean_path + fname
        print "cleaning " + fname
        with open(path) as f:
            data = csv.reader(f)
            heading = next(data, None)

            assert (heading == expected_heading), "csv format incorrect"

            for d in data:
                delay = float(d[6]) if (d[6] != "") else 0.0
                dt = dt.combine(datetime(int(d[0]), int(d[1]), int(d[2])), datetime.strptime(d[5], "%H%M").time())

                myd = mon_year_del[(d[3], d[4], dt.month, dt.year)]
                mon_year_del[(d[3], d[4], dt.month, dt.year)] = (myd[0] + 1, myd[1] + delay)
                dd = dow_del[(d[3], d[4], dt.weekday())]
                dow_del[(d[3], d[4], dt.weekday())] = (dd[0] + 1, dd[1] + delay)
                td = time_del[(d[3], d[4], dt.hour)] 
                time_del[(d[3], d[4], dt.hour)] = (td[0] + 1, td[1] + delay)

                flight_key = (d[3], d[4])
                if flight_key in flight_times:
                    delay_time = datetime.strptime(d[5], "%H%M")
                    for f_time in flight_times[flight_key]:
                        if abs((delay_time - f_time).total_seconds()) <= 900:
                            fd = flight_delays[(d[3], d[4], f_time)]
                            maxD = max(fd[2], delay)
                            flight_delays[(d[3], d[4], f_time)] = (fd[0] + 1, fd[1] + delay, maxD)



    price_f = output_path + "clean_price_data_init.csv"
    m_y_f = output_path + "m_y_delays_init.csv"
    dow_f = output_path + "dow_delays_init.csv"
    time_f = output_path + "time_delays_init.csv"

    openas = "wb" if overwrite else "a"
    with open(price_f, openas) as fout:
        writer = csv.writer(fout)

        if overwrite:
            new_heading = json_data['data'][0].keys()
            new_heading.append("num_delays")
            new_heading.append("total_delay")
            new_heading.append("max_delay")
            writer.writerow(new_heading)

        for entry in json_data['data']:
            dt = datetime.fromtimestamp(entry['departure_time'])
            key = (entry['from_airport'], entry['to_airport'], dt.replace(year=1900, month=1, day=1))

            row = []
            for k in entry.keys():
                row.append(entry[k])

            row += list(flight_delays[key])
            writer.writerow(row)

    fout.close()

    with open(m_y_f, openas) as fout:
        writer = csv.writer(fout)

        if overwrite:
            new_heading = json_data['data'][0].keys()
            new_heading.append("num_delay")
            new_heading.append("avg_delays")
            writer.writerow(new_heading)

        for entry in mon_year_del:
            row = list(entry + mon_year_del[entry])
            writer.writerow(row)

    fout.close()

    with open(dow_f, openas) as fout:
        writer = csv.writer(fout)

        if overwrite:
            new_heading = json_data['data'][0].keys()
            new_heading.append("num_delay")
            new_heading.append("avg_delays")
            writer.writerow(new_heading)

        for entry in dow_del:
            row = list(entry + dow_del[entry])
            writer.writerow(row)

    fout.close()

    with open(time_f, openas) as fout:
        writer = csv.writer(fout)

        if overwrite:
            new_heading = json_data['data'][0].keys()
            new_heading.append("num_delay")
            new_heading.append("avg_delays")
            writer.writerow(new_heading)

        for entry in time_del:
            row = list(entry + time_del[entry])
            writer.writerow(row)

    fout.close()



if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Usage: python price_delay_clean1.py flight_data to_clean_dir_path output_dir_path overwrite?<0/1>'
    flight_data_path = sys.argv[1]
    to_clean_path = sys.argv[2]
    output_path = sys.argv[3]
    overwrite = int(sys.argv[4])
    main()