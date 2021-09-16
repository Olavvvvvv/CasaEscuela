from datetime import datetime as dt
import time
import random
import sys


def wait(wtime, verbose=False):
    '''
    :str wtime: time in hh:mm:ss format, do nothing until time is reached
    '''
    while True:
        # get the current time
        ctime = dt.now().strftime('%H:%M:%S')
        # if the current time matches the waiting time
        if ctime == wtime:
            break  # break the loop
        elif verbose:
            print(ctime)
        time.sleep(1)  # else wait one second


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

    # if rest time and n are incompatible with the time delta
    if n * rtime >= time_delta:
        while n * rtime >= time_delta:
            rtime -= 1  # lower rest time until it is compatible

    times = []
    
    while len(times) < n:  # while not enough times have been generated
        new_time = random.randint(1, time_delta)  # generate a new time
        # check whether no other time falls within one rtime unit of the new time
        ntime_range = {n for n in range(new_time - rtime, new_time + rtime)}
        # if there is
        if len(set(times).intersection(ntime_range)) > 0:
            continue  # try again
        else:
            times.append(new_time)  # else save the new time
    return times


def generate_prompt():
    '''
    Generate a prompt, probably have it sent to the tablet as well
    '''
    pass


def check_times(alarm_times):
    '''
    :list alarm_times: list of alarm times
    check every second whether an alarm should be sounded or not
    '''
    c1 = 0  # counts the number of prompts
    c2 = 0  # counts the number of seconds
    while c1 < len(alarm_times):  # while not all prompts have happened
        if c2 in alarm_times:  # if the current second is in alarm_times
            generate_prompt()
            c1 += 1  # update the number of prompts
        c2 += 1  # update the seconds
        time.sleep(1)  # wait another second


def main(n, rtime, d=3, btime='10:00:00', etime='03:00:00'):
    '''
    :int n: amount of alarms per day
    :int rtime: minimum amount of seconds between each alarm 
    :int d: amount of days the code is run
    :str btime: time in hh:mm:ss format from when the thing starts
    :str btime: time in hh:mm:ss format until when the thing goes
    '''
    for _ in range(d):  # repeat for each day
        wait(btime)  # wait until the starting time
        print(f"[{dt.now().strftime('%H:%M:%S')}] Go!")
        # generate new random times for that day:
        times = generate_alarm_times(n, rtime, btime=btime, etime=etime)
        check_times(times)  # and check them


if __name__ == '__main__':
    n = int(sys.argv[1])
    rtime = int(sys.argv[2])
    d = int(sys.argv[3])
    btime = sys.argv[4]
    etime = sys.argv[5]

    main(n, rtime, d=d, btime=btime, etime=etime)
