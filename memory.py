# coding: utf-8

import requests
import re
import csv
import time
import progressbar

import os


my_words_path = "my_words/"
database_path = "database/output.csv"


def get_all_unmemorized_words(data_path):
    unmemorized_words = []
    if data_path[-1] == '/':
        raise AssertionError("Should be a dir!, but not implement")
    else:
        with open(data_path, newline='', encoding="utf-8") as csvfile:
            for row in csv.reader(csvfile):
                unmemorized_words.append(row[0].strip('--0'))
    return unmemorized_words


def get_all_my_words(data_path):
    my_words = []
    if data_path[-1] == '/':
        for dirPath, dirNames, filenames in os.walk(data_path):
            # print(dirPath)
            for f in filenames:
                filename = os.path.join(dirPath, f)
                with open(filename, newline='', encoding="utf-8") as csvfile:
                    for row in csv.reader(csvfile):
                        if len(row) == 0:
                            continue
                        if '#' not in row[0]:
                            continue
                        my_words.append(row[0].strip('#'))
    else:
        raise AssertionError("Should be a file!, but not implement")

    return my_words


def get_file_line_count(filename):
    with open(filename, encoding="utf-8") as f:
        file_line_count = sum(1 for _ in f)
    return file_line_count


from datetime import datetime


def log_to_file_if_update(filename, task_num, total_word_nums):
    with open(filename, 'r', newline='', encoding="utf-8") as csvfile:
        lines = [row for row in csv.reader(csvfile)]
        last_task_num = int(lines[-1][1])

    if task_num != last_task_num:
        now_time = datetime.now().isoformat(timespec='seconds')
        with open(filename, 'a', newline='', encoding="utf-8") as csvfile:
            csv.writer(csvfile).writerow([now_time, task_num, total_word_nums])


# import numpy as np
import matplotlib.pyplot as plt


def plot_data(filename):
    with open(filename, 'r', newline='', encoding="utf-8") as csvfile:
        x = []
        y = []
        z = []
        for row in csv.reader(csvfile):
            x.append(row[0])
            y.append(int(row[1]))
            z.append(int(row[2]))
        # x = np.linspace(0, 10, 1000)
        # y = np.sin(x)
        # z = np.cos(x**2)
        plt.figure(figsize=(8, 4))
        plt.plot(x, y, label="my")
        plt.plot(x, z, label="total")
        # plt.xlabel("Time(s)")
        # plt.ylabel("Volt")
        # plt.title("PyPlot First Example")
        # plt.ylim(-1.2, 1.2)
        plt.legend()
        plt.show()


def main():
    total_word_nums = get_file_line_count(database_path)

    database = get_all_unmemorized_words(database_path)
    my_words = list(set(get_all_my_words(my_words_path)))

    task_num = 0
    for my_word in my_words:
        if my_word in database:
            task_num = task_num + 1
    log_to_file_if_update('data.log', task_num, total_word_nums)
    plot_data('data.log')


if __name__ == '__main__':
    main()
