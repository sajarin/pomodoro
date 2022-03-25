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
        --version   Show version and exit
"""

import time
import random
import tkinter as tk
from tkinter import messagebox


def main():
    """
        Output: gui
    """
    config_contents = {
            'length_of_tasks_in_minutes': 0,
            'num_of_tasks_done': 0
            }
    config = "config.txt"
    with open(config, "r") as handle:
        lines = []
        for line in handle:
            lines.append(line.split(",")[1].strip())
        print(lines)
        config_contents['length_of_tasks_in_minutes'] = float(lines[0])
        config_contents['num_of_tasks_done'] = int(lines[1])

    task_length_in_seconds = int(
            60*config_contents['length_of_tasks_in_minutes'])

    while True:
        run_timer(task_length_in_seconds)
        config_contents['num_of_tasks_done'] += 1
        update_config(config_contents, config)
        reward_prob = get_reward_probability(config_contents)
        is_reward = check_reward(reward_prob)
        if is_reward:
            reward_alert()


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

    print(seconds_left, end='\r')


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


def get_reward_probability(config_contents: dict) -> float:
    """
        returns the probability of a reward given number of tasks done

        n.b assuming 4hrs * 30d = 120hrs to habit formation, reward prob should
        be close to zero after 120 hours worth of tasks has passed (this is
                irregardless of the decay function)
    """

    task_length_in_seconds = config_contents['length_of_tasks_in_minutes']
    num_of_tasks_done = config_contents['num_of_tasks_done']
    total_time_spent = task_length_in_seconds*num_of_tasks_done / (60 * 60)
    reward_prob = -0.000792 * total_time_spent + 1
    return reward_prob


def reward_alert() -> None:
    """
       popup if reward 
    """
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning(
            'You got a Reward!', 
            'Close when you\'re ready to start the timer again')


main()
