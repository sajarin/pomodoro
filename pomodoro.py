"""
    A timer + RNG for skinnerian reinforcement.

    User input:
        1. a way to start the timer
        2. a way to specify how long each task is
        3. a way to reset session history

    Output:
        1. a countdown timer
        2. an alert if you get the reward
        3. a history of the session

    Usage:
        pomodoro.py [options]

    Options:
        -h, --help  Show this help message and exit
"""

import os
import time
import random
import argparse
import tkinter as tk
from tkinter import messagebox
from datetime import date


def main():
    """
        Output: gui
    """
    handle_args()
    config_contents = {
            'length_of_tasks_in_minutes': 0,
            'num_of_tasks_done': 0
            }
    stats_contents = {
            'datetime': "",
            'num_of_tasks_done': 0
            }
    config = "config.txt"
    stats = "statistics.txt"
    with open(config, "r") as handle:
        lines = []
        for line in handle:
            lines.append(line.split(",")[1].strip())
        print("Time between each session:", lines[0], "\n# of sessions done:",
              lines[1])
        config_contents['length_of_tasks_in_minutes'] = float(lines[0])
        config_contents['num_of_tasks_done'] = int(lines[1])

    task_length_in_seconds = int(
            60*config_contents['length_of_tasks_in_minutes'])

    with open(stats, "r") as handle:
        lines = []
        raw_lines = handle.readlines()[-2:]
        for line in raw_lines:
            lines.append(line.split(",")[1].strip())
        stats_contents['datetime'] = str(lines[0])
        print(stats_contents['datetime'])
        if is_today(stats_contents['datetime']):
            stats_contents['num_of_tasks_done'] = int(lines[1])
        else:
            stats_contents['num_of_tasks_done'] = 0
        print(stats_contents['num_of_tasks_done'])

    while True:
        run_timer(task_length_in_seconds)
        config_contents['num_of_tasks_done'] += 1
        stats_contents['num_of_tasks_done'] += 1
        update_config(config_contents, config)
        update_statistics(stats_contents, stats, config_contents[
                                                          'num_of_tasks_done'])
        # set new date to today's to avoid duplication of log entries
        stats_contents['datetime'] = date.today().strftime("%m/%d/%y")
        reward_prob = get_reward_probability(config_contents)
        is_reward = check_reward(reward_prob)
        if is_reward:
            reward_alert()


def handle_args() -> None:
    # handle script arguments
    parser = argparse.ArgumentParser(description='A timer + rng for skinnerian\
                                     reinforcement')
    parser.parse_args()


def run_timer(seconds: int) -> None:
    """
        decrement seconds and pass to print_timer()
    """
    while seconds > 0:
        print_timer(seconds)
        time.sleep(1)
        seconds -= 1


def print_timer(seconds_left: int) -> None:
    """
        prints to the console how much time is left
    """
    minutes, seconds = divmod(seconds_left, 60)
    min_sec_format = '{:02d}:{:02d}'.format(minutes, seconds)
    print(min_sec_format, end='\r')


def check_reward(reward_prob: float) -> bool:
    """
        returns true if rng < reward_prob
    """
    rng = random.random()
    if rng < reward_prob:
        return True
    else:
        return False


def update_config(contents: dict, config: str) -> None:
    """Writes to the config file the current number of tasks done"""

    with open(config, "w") as handle:
        for elem in contents.keys():
            line = elem.upper() + ", " + str(contents[elem]).upper() + '\n'
            handle.write(line)


def update_statistics(contents: dict, statistics: str, cur_tasks: int) -> None:
    """
        Writes to the statistics file the current number of tasks done and date
    """
    keys = list(contents.keys())
    tasks_line = keys[1].upper() + ", " + str(contents['num_of_tasks_done']
                                              ).upper() + '\n'
    date_line = keys[0].upper() + ", " + date.today().strftime(
                                                             "%m/%d/%y") + '\n'

    # if date logged is today's, then edit 'num_of_tasks_done' line only
    if is_today(contents['datetime']):
        truncate_last_line_in_file(statistics)
        with open(statistics, 'a', encoding='utf8') as handle:
            handle.write('\n' + tasks_line)
    # new date, new entry in log file and first task of the day
    else:
        tasks_line = keys[1].upper() + ", 1" + '\n'
        with open(statistics, "a") as handle:
            handle.write(date_line)
            handle.write(tasks_line)


def is_today(saved_datetime: str) -> bool:
    """Checks if today is the same date as the one logged"""
    if saved_datetime == date.today().strftime("%m/%d/%y"):
        return True
    return False


def truncate_last_line_in_file(filename: str) -> None:
    """Finds and removes the last line in a file"""

    with open(filename, "rb+") as handle:
        handle.seek(0, os.SEEK_END)
        pos = handle.tell() - 1
        while pos > 0 and handle.read(1) != b"\n":
            pos -= 1
            handle.seek(pos, os.SEEK_SET)
        if pos > 0:
            handle.seek(pos - 1, os.SEEK_SET)
            handle.truncate()


def get_reward_probability(config_contents: dict) -> float:
    """
        returns the probability of a reward given number of tasks done

        n.b assuming 4hrs * 30d = 120hrs to habit formation, reward prob should
        be close to zero after 120 hours worth of tasks has passed (this is
                irregardless of the decay function)
    """

    task_length_in_seconds = config_contents['length_of_tasks_in_minutes']
    num_of_tasks_done = config_contents['num_of_tasks_done']
    total_time_spent = task_length_in_seconds*num_of_tasks_done / 60
    reward_prob = -0.00792 * total_time_spent + 1
    return reward_prob


def reward_alert() -> None:
    """
       popup if reward
    """
    root = tk.Tk()
    root.attributes('-topmost', 1)
    root.withdraw()
    messagebox.showwarning(
            'You got a Reward!',
            'Close when you\'re ready to start the timer again')


main()
