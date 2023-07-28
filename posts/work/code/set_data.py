import os
import shutil

# 21 种语言
languages = {
    "CN": {},
    "TW": {},
    "CZ": {},
    "DE": {},
    "EL": {},
    "EN": {},
    "ES": {},
    "FA": {},
    "FR": {},
    "HE": {},
    "ID": {},
    "IT": {},
    "KR": {},
    "PL": {},
    "PT": {},
    "RU": {},
    "TH": {},
    "TR": {},
    "VN": {},
    "NL": {},
    "SV": {}
}

languages_path = './languages/'
languages_path_xx = './languages/languages/'


def set_my_map(path):
    for language in languages.keys():
        my_map_ = languages[language]
        input_file = open(path + language + '.bin', 'r', encoding='utf-8')
        while True:
            line = input_file.readline()
            line = line.replace("\n", "")
            if len(line) == 0:
                break
            pair_ = line.split("::")
            my_map_[pair_[0]] = pair_[1]
        input_file.close()


if os.path.exists(languages_path_xx):
    set_my_map(languages_path_xx)
    shutil.rmtree(languages_path_xx)

set_my_map(languages_path)


for language in languages.keys():
    my_map_ = languages[language]
    output_file = open(languages_path + language + '.bin', 'w', encoding='utf-8')
    list_ = []
    for key, val in my_map_.items():
        list_.append(key + "::" + val)
    for li_ in sorted(list_):
        output_file.write(li_ + "\n")
    output_file.close()
