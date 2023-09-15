import os
import sys
import time
import threading
import datetime
import json
import webbrowser
from platform import system

path = os.path.dirname(os.path.abspath(__file__))

def run():
    now = datetime.datetime.now()

    t= time.localtime()
    y = str(t.tm_year)
    mo = str(t.tm_mon)
    dt = str(t.tm_mday)

    dy = "sat"  # Here, the day of the week is set to Saturday
    
    now_time = time.strftime("%H%M", t)

    with open(os.path.join(path, "meetings.json")) as f:
        meeting = json.load(f)
    next_time = []
    for set_time in meeting[dy].keys():
        if now_time <= set_time:
            next_time.append(set_time)
    next_time = min(next_time)

    full_next_time = y+mo+dt+next_time
    full_next_time = datetime.datetime.strptime(full_next_time, "%Y%m%d%H%M")

    min_left = full_next_time-now
    min_left = min_left.seconds/60

    subject = meeting[dy][next_time]["subject"]
    professor = meeting[dy][next_time]["professor"]
    id = meeting[dy][next_time]["id"]
    pw = meeting[dy][next_time]["pw"]
    url = "zoommtg://zoom.us/join?confno={}&pwd={}".format(id, pw)

    if 0 <= min_left <= 5:
        print("--------------------------")
        print("[Now Datetime]",now.strftime('%Y-%m-%d %H:%M:%S'))
        print("[Next Class]",subject)
        print("[Professor]",professor)
        print("[Time Left]",int(min_left),"minute(s) left\n")
        print("{} minutes left until the class start".format(int(min_left)))
        print("------------------------")
        pf = system()
        if pf=="Darwin":
            os.system("osascript -e 'display notification \"{} minute(s) left until the class starts. The class link opens\"'".format(int(min_left)))
            os.system('afplay quite-impressed.m4r')
        webbrowser.open(url)
        sys.exit()  # Program exits after opening the Zoom link

    threading.Timer(2.5, run).start()

run()
