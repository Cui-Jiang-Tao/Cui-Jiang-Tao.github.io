from googletrans import Translator
import os
import time
from datetime import datetime


translator = Translator()
error_cnt = 0

languages_by_en_path = './languages_by_en/'
parse_en_path = './parse_en/'

os.makedirs(os.path.dirname(languages_by_en_path), exist_ok=True)

parse_en_map = {}

# 18 种语言
languages = {
    "CZ": "cs",
    "DE": "de",
    "EL": "el",
    "ES": "es",
    "FA": "fa",
    "FR": "fr",
    "HE": "he",
    "ID": "id",
    "IT": "it",
    "KR": "ko",
    "PL": "pl",
    "PT": "pt",
    "RU": "ru",
    "TH": "th",
    "TR": "tr",
    "VN": "vi",
    "NL": "nl",
    "SV": "sv"
}


def translate_language_google(str_data, dest):
    while True:
        try:
            str_data = translator.translate(str_data, dest).text
            time.sleep(2)
            break
        except:
            global error_cnt
            error_cnt += 1
            print(datetime.now(), "translate error:", error_cnt)
            time.sleep(60)
    return str_data


parse_input_file_en = open(parse_en_path + 'en.bin', 'r', encoding='utf-8')
index_input_en = open(parse_en_path + 'index_en.bin', 'r', encoding='utf-8')
parse_index_en = int(index_input_en.readline().replace("\n", ""))
index_input_en.close()

parse_input_file_index_en = 0
while True:
    line = parse_input_file_en.readline().replace("\n", "")
    parse_input_file_index_en += 1
    if len(line) == 0:
        break

    if parse_input_file_index_en < parse_index_en:
        continue

    li_ = line.split("::")
    parse_en_map[li_[0]] = li_[1]
parse_input_file_en.close()


def translateByGoogle(map_tds, source_language):
    # 长度 13
    li_str_key = ""
    li_str_val = ""
    li_cnt = 0
    td_cnt = len(map_tds)
    td_cut_index = 0

    for str_td_key, str_td_val in map_tds.items():
        li_str_val += str_td_val + "\n"
        li_str_key += str_td_key + "\n"
        li_cnt += 1
        td_cut_index += 1
        if td_cut_index >= td_cnt or li_cnt >= 13:
            print(source_language, " translate to: ", end=" ")
            for (key, val) in languages.items():
                str_mode = 'w'
                if os.path.exists(languages_by_en_path + key + '.bin'):
                    str_mode = 'a'
                output_file = open(languages_by_en_path + key + '.bin', str_mode, encoding='utf-8')

                print(key, end=" ")
                write_data = translate_language_google(li_str_val, val)
                li_data = str.split(li_str_key.rstrip("\n"), '\n')

                write_data_li = str.split(write_data, '\n')
                i_ = 0
                while i_ < len(write_data_li):
                    output_file.write(
                        li_data[i_].upper() + "::" + write_data_li[i_][:1].upper() + write_data_li[i_][1:] + "\n")
                    i_ += 1
                output_file.close()

            path_index = parse_en_path + 'index_en.bin'
            index_output = open(path_index, 'w', encoding='utf-8')
            index_output.write(str(td_cut_index + parse_index_en) + "\n")
            index_output.close()
            print(datetime.now(), "\t总数：", td_cnt, "当前：", td_cut_index)
            print("\n")
            li_str_key = ""
            li_str_val = ""
            li_cnt = 0


translateByGoogle(parse_en_map, "EN")
