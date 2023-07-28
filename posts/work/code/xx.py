from googletrans import Translator
import os
import re
from lxml import etree
import shutil
import time
from datetime import datetime

translator = Translator()
error_cnt = 0

folder_path = './Htmls/'
languages_path = './languages/'
parse_cn_and_en_path = './parse_cn_and_en/'

# 21 种语言
languages = {
    "CN": "zh-CN",
    "TW": "zh-tw",
    "CZ": "cs",
    "DE": "de",
    "EL": "el",
    "EN": "en",
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


set_td_cn = set()
set_td_en = set()

if not os.path.exists(parse_cn_and_en_path):
    if os.path.exists(languages_path):
        shutil.rmtree(languages_path)
    os.makedirs(os.path.dirname(languages_path), exist_ok=True)
    os.makedirs(os.path.dirname(parse_cn_and_en_path), exist_ok=True)

    # 定义正则表达式规则
    pattern_en = re.compile(r'^EN_.*')
    pattern_cn = re.compile(r'^CN_.*')

    path_list = os.listdir(folder_path)
    size_ = len(path_list)
    cur_index = 0
    for file_name in path_list:
        cur_index += 1
        print(datetime.now(), "总数: ", size_, "当前: ", cur_index, " analysis: ", file_name)

        html = etree.parse(folder_path + file_name, etree.HTMLParser())
        # 获取所有td标签内容
        tds = html.xpath('/html/body/table/tr/td')

        i_ = 0
        while i_ < len(tds):
            str_ = str(tds[i_].text).strip()
            if str_ and str_ != 'None':
                # 解析中文的
                if pattern_cn.match(file_name):
                    set_td_cn.add(str_)
                elif pattern_en.match(file_name):
                    set_td_en.add(str_)
            i_ += 1

    parse_output_file_cn = open(parse_cn_and_en_path + 'cn.bin', 'w', encoding='utf-8')
    parse_output_file_en = open(parse_cn_and_en_path + 'en.bin', 'w', encoding='utf-8')
    for str_cn in set_td_cn:
        parse_output_file_cn.write(str_cn + "\n")
    parse_output_file_cn.close()
    for str_en in set_td_en:
        parse_output_file_en.write(str_en + "\n")
    parse_output_file_en.close()

    index_output_cn = open(parse_cn_and_en_path + 'index_cn.bin', 'w', encoding='utf-8')
    index_output_cn.write("1\n")
    index_output_cn.close()

    index_output_en = open(parse_cn_and_en_path + 'index_en.bin', 'w', encoding='utf-8')
    index_output_en.write("1\n")
    index_output_en.close()

set_td_cn.clear()
set_td_en.clear()

parse_input_file_cn = open(parse_cn_and_en_path + 'cn.bin', 'r', encoding='utf-8')
parse_input_file_en = open(parse_cn_and_en_path + 'en.bin', 'r', encoding='utf-8')

index_input_cn = open(parse_cn_and_en_path + 'index_cn.bin', 'r', encoding='utf-8')
parse_index_cn = int(index_input_cn.readline().replace("\n", ""))
index_input_cn.close()

index_input_en = open(parse_cn_and_en_path + 'index_en.bin', 'r', encoding='utf-8')
parse_index_en = int(index_input_en.readline().replace("\n", ""))
index_input_en.close()

parse_input_file_index_cn = 0
while True:
    line = parse_input_file_cn.readline().replace("\n", "")
    parse_input_file_index_cn += 1
    if len(line) == 0:
        break

    if parse_input_file_index_cn < parse_index_cn:
        continue

    set_td_cn.add(line)
parse_input_file_cn.close()

parse_input_file_index_en = 0
while True:
    line = parse_input_file_en.readline().replace("\n", "")
    parse_input_file_index_en += 1
    if len(line) == 0:
        break

    if parse_input_file_index_en < parse_index_en:
        continue

    set_td_en.add(line)
parse_input_file_en.close()


def translateByGoogle(set_tds, source_language):
    # 长度 13
    li_str = ""
    li_cnt = 0
    td_cnt = len(set_tds)
    td_cut_index = 0

    for str_td in set_tds:
        li_str += str_td + "\n"
        li_cnt += 1
        td_cut_index += 1
        if td_cut_index >= td_cnt or li_cnt >= 13:
            print(source_language, " translate to: ", end=" ")
            for (key, val) in languages.items():
                str_mode = 'w'
                if os.path.exists(languages_path + key + '.bin'):
                    str_mode = 'a'
                output_file = open(languages_path + key + '.bin', str_mode, encoding='utf-8')
                write_data = ""
                li_data = ""

                if source_language == 'CN':
                    if key == 'CN':
                        write_data = li_str
                        write_data = write_data.rstrip("\n")
                        li_data = str.split(li_str.rstrip("\n"), '\n')
                    elif key == 'TW':
                        write_data = translate_language_google(li_str, val)
                        li_data = str.split(li_str.rstrip("\n"), '\n')
                    else:
                        output_file.close()
                        continue
                else:
                    if key == 'CN' or key == 'TW':
                        output_file.close()
                        continue

                    write_data = translate_language_google(li_str, val)
                    li_data = str.split(li_str.rstrip("\n"), '\n')

                print(key, end=" ")
                write_data_li = str.split(write_data, '\n')
                i_ = 0
                while i_ < len(write_data_li):
                    output_file.write(
                        li_data[i_].upper() + "::" + write_data_li[i_][:1].upper() + write_data_li[i_][1:] + "\n")
                    i_ += 1
                output_file.close()

            path_index = parse_cn_and_en_path + 'index_en.bin'
            parse_index = parse_index_en
            if source_language == 'CN':
                path_index = parse_cn_and_en_path + 'index_cn.bin'
                parse_index = parse_index_cn
            index_output = open(path_index, 'w', encoding='utf-8')
            index_output.write(str(td_cut_index + parse_index) + "\n")
            index_output.close()
            print(datetime.now(), "\t总数：", td_cnt, "当前：", td_cut_index)
            print("\n")
            li_str = ""
            li_cnt = 0


translateByGoogle(set_td_cn, "CN")
translateByGoogle(set_td_en, "EN")
