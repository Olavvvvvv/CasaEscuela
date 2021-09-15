from datetime import datetime as dt
import time
import random


def wait(wtime, verbose=False):
    '''
    :str wtime: time in hh:mm:ss format, do nothing until time is reached
    '''
    while True:
        # get the current
        ctime = dt.now().strftime('%H:%M:%S')
        if ctime == wtime:
            break
        elif verbose:
            print(ctime)
        time.sleep(1)


def generate_alarm_times(n, rtime, btime='10:00:00', etime='03:00:00'):
    '''
    :int n: amount of alarms per day
    :int rtime: rest time in seconds following each alarm
    :str btime: begin time in hh:mm:ss format
    :str etime: end time in hh:mm:ss format
    '''
    # get the amount of seconds between btime and etime
    btime = dt.strptime(btime, '%H:%M:%S')
    etime = dt.strptime(etime, '%H:%M:%S')
    time_delta = etime - btime
    time_delta = time_delta.seconds

    times = []
    # TODO: test whether the amount of alarms with the rest time is even
    #       possible with the given time frame
    while len(times) < n:
        new_time = random.randint(1, time_delta)
        ntime_range = {n for n in range(new_time - rtime, new_time + rtime)}
        if len(set(times).intersection(ntime_range)) > 0:
            continue
        else:
            times.append(new_time)
    return times

def check_times(alarm_times):
    """
    :list alarm_times: list of alarm times
    check every second whether an alarm should be sounded or not
    """
    c1 = 0
    c2 = 1
    while c1 < len(alarm_times):
        if c2 in alarm_times:
            # TODO: Fix the line below
            print(f"drink at {dt.now().strftime('%H:%M:%S')}!")
            c1 += 1
        c2 += 1
        time.sleep(1)

def main(n, rtime, d=3, btime='10:00:00', etime='03:00:00'):
    '''
    :int n: amount of alarms per day
    :int rtime: minimum amount of seconds between each alarm 
    :int d: amount of days the code is run
    :str btime: time in hh:mm:ss format from when the thing starts
    :str btime: time in hh:mm:ss format until when the thing goes
    '''
    for _ in range(d):
        wait(btime)
        print(f"[{dt.now().strftime('%H:%M:%S')}] Go!")
        times = generate_alarm_times(n, rtime, btime=btime, etime=etime)
        check_times(times)


main(20, 1800)  # give twenty alarms with a minimum of 1800 seconds between each
