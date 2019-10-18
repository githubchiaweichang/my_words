# coding: utf-8
import requests

import ast
import json
import re

import string

import csv


def remain_chinese(data):
    rule = re.compile(r"[^\u4e00-\u9fa5]")
    data = rule.sub('', data)
    return data


def replace_punctuation(data):
    # translator = str.maketrans('', '', string.punctuation)
    punctuation_list = ['\\', '.', '，', ')', '(', '；', ';', '、', ',']
    for punctuation in punctuation_list:
        data = data.replace(punctuation, ' ').strip()

    data = data.strip()
    data = ",".join(data.split())

    # data = data.translate(translator).strip()
    return data


def get_word_url(word):
    url = "https://quizlet.com/webapi/3.2/suggestions/definition?"
    param_list = [
        'limit=10',
        'word=' + word,
        'defLang=zh-TW',
        'localTermId=-1',
        'wordLang=en',
    ]

    url = url + "&".join(param_list)

    return url


def get_meanings(word):
    url = get_word_url(word)
    r = requests.get(url)
    r.encoding = "unicode_escape"

    meanings_text = r.text
    meanings_text = meanings_text.replace('""', '"')

    # # print(meanings_text)

    text_list = json.loads(replace_punctuation(meanings_text), strict=False)['responses'][0]['data']['suggestions']['suggestions']
    dst_list = []
    for word in text_list:
        dst_list.append(remain_chinese(word['text']))
    return dst_list


filename = "gre_words.CSV"
filter_word = "--0"

data_table = []
import time
import progressbar

with open(filename, encoding="utf-8") as f:
    file_line_count = sum(1 for _ in f)


with open(filename, newline='', encoding="utf-8") as csvfile:
    rows = csv.reader(csvfile)
    # rows = [['bed'], ['dog']]
    with progressbar.ProgressBar(max_value=file_line_count) as bar:
        for index, row in enumerate(rows):
            # # print(row)
            bar.update(index)
            time.sleep(0.0001)
            word = row[0].rsplit(filter_word)[0]
            # print(word)
            data = get_meanings(word)
            data_table.append([word, data[0] if data else "NotFoundAnyMeanings"])

print(data_table)

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data_table)
