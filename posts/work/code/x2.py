from googletrans import Translator
from lxml import etree
from datetime import datetime
import os
import re
import shutil
import time


def writeHtml(tds, file_name, output_html):
    output_html.write("<!DOCTYPE html>\n")
    output_html.write("<html>\n")
    output_html.write("<head>\n")
    output_html.write("<title>" + file_name.replace(".html", "") + "</title>\n")
    output_html.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n")
    output_html.write("<link rel=\"stylesheet\" href=\"../style.css\">\n")
    # output_html.write("<link rel=\"stylesheet\" href=\"../style.min.css\">\n")
    output_html.write("</head>\n")
    output_html.write("<body>\n")
    output_html.write("<table>\n")

    i = 0
    len_ = len(tds)
    while i < len_:
        output_html.write("<tr>\n")
        if tds[i]:
            output_html.write("<td>" + tds[i] + "</td>\n")
        else:
            output_html.write("<td></td>\n")

        if tds[i + 1]:
            output_html.write("<td>" + tds[i + 1] + "</td>\n")
        else:
            output_html.write("<td></td>\n")
        output_html.write("</tr>\n")
        i += 2

    output_html.write("</table>\n")
    output_html.write("</body>\n")
    output_html.write("</html>\n")


# 待查找的文件夹路径
folder_path = './Htmls/'
output_path = './translate/'
languages_path = './languages/'

# if os.path.exists(output_path):
# #     shutil.rmtree(output_path)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# 21 种语言
languages = {
    # "CN": "zh-CN",
    # "TW": "zh-tw",
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


languages_maps = {
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

for key in languages_maps:
    input_file = open(languages_path + key + '.bin', 'r', encoding='utf-8')
    while True:
        line = input_file.readline()
        line = line.replace("\n", "")
        if len(line) == 0:
            break
        pair_ = line.split("::")
        languages_maps[key][pair_[0]] = pair_[1]
    input_file.close()


err_set_en = set()
err_set_cn = set()


def translate_language(tds, dest, source_language):
    tds_ = []
    err_cnt = 0

    for td in tds:
        if str(td.text).strip() and str(td.text).strip() != 'None':
            try:
                tds_.append(languages_maps[dest][str(td.text).upper().strip()])
            except:
                if source_language == "CN":
                    err_set_cn.add(str(td.text).strip())
                else:
                    err_set_en.add(str(td.text).strip())
                err_cnt += 1
        else:
            tds_.append("")

    if err_cnt:
        raise Exception()

    return tds_


# 定义正则表达式规则
pattern_en = re.compile(r'^EN_.*')
pattern_cn = re.compile(r'^CN_.*')

error_files = set()

# 遍历文件夹中所有文件
for file_name in os.listdir(folder_path):
    # 判断文件名是否符合正则表达式规则
    if pattern_en.match(file_name):
        for (key, val) in languages.items():
            new_file_name = file_name.replace("EN_", key + "_")
            output_html = open(output_path + new_file_name, 'w', encoding='utf-8')
            html = etree.parse(folder_path + file_name, etree.HTMLParser())
            # 获取所有td标签内容
            tds = html.xpath('/html/body/table/tr/td')
            print(datetime.now(), file_name, " to ", new_file_name)
            try:
                writeHtml(translate_language(tds, key, "EN"), new_file_name, output_html)
            except:
                error_files.add(file_name)
            output_html.close()
        print("")
        os.remove(folder_path + file_name)
    elif pattern_cn.match(file_name):
        new_file_name = file_name.replace("CN_", "TW_")
        output_html = open(output_path + new_file_name, 'w', encoding='utf-8')
        html = etree.parse(folder_path + file_name, etree.HTMLParser())
        # 获取所有td标签内容
        tds = html.xpath('/html/body/table/tr/td')
        print(datetime.now(), file_name, " to ", new_file_name)
        try:
            writeHtml(translate_language(tds, 'TW', "CN"), new_file_name, output_html)
        except:
            error_files.add(file_name)
        output_html.close()
        shutil.move(folder_path + file_name, output_path)

if len(err_set_cn) != 0:
    output_error = open("./error_cn.bin", 'w', encoding='utf-8')
    for err_ in err_set_cn:
        output_error.write(err_ + "\n")
    output_error.close()

if len(err_set_en) != 0:
    output_error = open("./error_en.bin", 'w', encoding='utf-8')
    for err_ in err_set_en:
        output_error.write(err_ + "\n")
    output_error.close()

if len(err_set_cn) != 0 or len(err_set_en) != 0:
    print("translate error size :", len(err_set_cn) + len(err_set_en))

for error in error_files:
    print("translate error file: ", error)
