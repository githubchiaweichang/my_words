# coding: utf-8

import requests
import re
import csv
import time
import progressbar


def remain_chinese(data):
    rule = re.compile(r"[^\u4e00-\u9fa5]")
    data = rule.sub('', data)
    return data


def replace_punctuation_with_delimiter(data, delimiter):
    # translator = str.maketrans('', '', string.punctuation)
    punctuation_list = ['"', '\\', '\n', '.', '，', ')',
                        '(', '；', ';', '、', ' ']
    for punctuation in punctuation_list:
        data = data.replace(punctuation, delimiter).strip()

    data = data.split(",")
    data = list(filter(None, data))
    return delimiter.join(data)


def get_word_url(word):
    url = "https://quizlet.com/webapi/3.2/suggestions/definition?"
    param_list = [
        'limit=10',
        'word=' + word,
        'defLang=zh-TW',
        'localTermId=-1',
        'wordLang=en',
    ]
    return url + "&".join(param_list)


def get_meanings(word):
    url = get_word_url(word)
    suggestions = requests.get(url).json()
    suggestions = suggestions['responses'][0]['data']['suggestions']['suggestions']

    meaning_list = []
    for suggestion in suggestions:
        meanings = suggestion['text']
        meanings = replace_punctuation_with_delimiter(meanings, ',')
        meanings = [remain_chinese(m) for m in meanings.split(',')]
        meanings = list(filter(None, meanings))
        meaning_list.append(','.join(meanings))
    return meaning_list


def get_file_line_count(filename):
    with open(filename, encoding="utf-8") as f:
        file_line_count = sum(1 for _ in f)
    return file_line_count


def main(old_filename, new_filename, filter_word):
    data_table = []
    new_filename_index = 0
    with open(old_filename, newline='', encoding="utf-8") as csvfile:
        rows = csv.reader(csvfile)
        # rows = [['say']]
        with progressbar.ProgressBar(
            max_value=get_file_line_count(old_filename)
        ) as bar:

            for index, row in enumerate(rows):
                bar.update(index)
                time.sleep(0.0001)
                word = row[0]
                data = get_meanings(word.rsplit(filter_word)[0])
                data = sorted(data, key=len)
                data_table.append([word, data[-1] if data else "NotFoundAnyMeanings"])

                if len(data_table) >= 1000:
                    with open(new_filename + str(new_filename_index) + ".csv",
                              'w', newline='', encoding="utf-8") as csvfile:
                        csv.writer(csvfile).writerows(data_table)

                    data_table = []
                    new_filename_index = new_filename_index + 1
                    print("save index = {}".format(new_filename_index))

    with open(new_filename, 'w', newline='', encoding="utf-8") as csvfile:
        csv.writer(csvfile).writerows(data_table)


if __name__ == '__main__':
    main(
        old_filename="gre_words.csv",
        new_filename="new.csv",
        filter_word="--0"
    )
# bug
# if  csv file have empty line