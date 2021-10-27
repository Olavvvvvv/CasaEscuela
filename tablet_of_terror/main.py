from datetime import datetime as dt
from numpy import random as r
import pandas as pd
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


def generate_prompt(cache):
    '''
    Generate a prompt, probably have it sent to the tablet as well
    '''
    time = lambda x: dt.strptime(x, '%H:%M:%S').time()
    people = ('Emma;ze;haar',
              'Dylan;hij;zijn',
              'Dagmar;ze;haar',
              'Olav;hij;zijn',
              'Sonja;ze;haar',
              'Floris;hij;zijn',
              'Bas;hij;zijn',
              'Wendel;ze;haar')

    variables = ['X', 'Y', 'Z', 'Q']

    with open('prompts.csv', 'r', encoding='utf8') as f:
        df = f.readlines()[1:]
    
    id_not_in_cache = False  # used to check if prompt id was generated before

    while not id_not_in_cache:
        prompt = r.choice(df)  # randomly select a prompt
        prompt = prompt.rstrip().split(';')  # split into columns
        
        if dt.now().time() < time('11:30:00') and not int(prompt[3]):
            # check if it is a morning-only prompt, and only keep it if it is before 11:30
            continue
        elif dt.now().time() > time('11:30:00') and int(prompt[3]):
            # if it is not a morning-only prompt and it is before 11:30, continue
            continue

        if prompt[0] not in cache:  # check if id in cache
            id_not_in_cache = True
            cache.append(prompt[0])  # if not, add to cache

    ptext = prompt[1]
    pvalency = int(prompt[2])  # number of people that are part of the prompt

    victims = r.choice(people, size=pvalency, replace=False)
    for victim, var in zip(victims, variables[:pvalency]):
        name = victim.split(';')[0]
        rel = victim.split(';')[1]
        pos = victim.split(';')[2]
        ptext = ptext.replace(f'{var}_rel', rel)  # insert appropriate pronoun
        ptext = ptext.replace(f'{var}_pos', pos)  # insert appropriate pos.prn.
        ptext = ptext.replace(var, name)
        if 'LETTER' in ptext:
            letter = r.choice([letter for letter in 'ABDEFGHKLMNOPRSTVZ'])
            ptext = ptext.replace('LETTER', letter)

    return cache, ptext


def check_times(cache, alarm_times):
    '''
    :list alarm_times: list of alarm times
    check every second whether an alarm should be sounded or not
    '''
    c1 = 0  # counts the number of prompts
    c2 = 0  # counts the number of seconds
    while c1 < len(alarm_times):  # while not all prompts have happened
        if c2 in alarm_times:  # if the current second is in alarm_times
            cache, ptext = generate_prompt(cache)
            print(f"[{dt.now().strftime('%H:%M:%S')}] {ptext}")
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
    cache = []
    for _ in range(d):  # repeat for each day
        wait(btime)  # wait until the starting time
        print(f"[{dt.now().strftime('%H:%M:%S')}] Go!")
        # generate new random times for that day:
        times = generate_alarm_times(n, rtime, btime=btime, etime=etime)
        check_times(cache, times)  # and check them


if __name__ == '__main__':
    n = int(sys.argv[1])  # number of prompts
    rtime = int(sys.argv[2])  # minimum amount of time between prompts
    d = int(sys.argv[3])  # number of days the thing is repeated
    btime = sys.argv[4]  # start time
    etime = sys.argv[5]  # end time

    main(n, rtime, d=d, btime=btime, etime=etime)
