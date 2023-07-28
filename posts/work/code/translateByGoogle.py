from googletrans import Translator
from lxml import etree
from datetime import datetime
import os
import re
import shutil
import time

translator = Translator()
error_cnt = 0


def translate_language_google_old(tds, dest):
    tds_ = []

    for td in tds:
        if str(td.text).strip() and str(td.text).strip() != 'None':

            while True:
                try:
                    tds_.append(translator.translate(str(td.text).strip(), dest).text)
                    break
                except:
                    time.sleep(10)
                    continue
        else:
            tds_.append("")

    return tds_


def translate_language_google(tds, dest):
    tds_ = []
    str_data = ""

    for td in tds:
        if str(td.text).strip() and str(td.text).strip() != 'None':
            str_data += str(td.text).strip() + "\n"
            tds_.append(str(td.text).strip())
        else:
            tds_.append("")

    while True:
        try:
            str_data = translator.translate(str_data, dest).text
            time.sleep(1)
            break
        except:
            global error_cnt
            error_cnt += 1
            print(datetime.now(), "translate error:", error_cnt)
            time.sleep(60)

    str_li = str.split(str_data, "\n")
    j = 0
    for i in range(len(tds_)):
        if tds_[i]:
            tds_[i] = str_li[j]
            j += 1

    return tds_


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

# 定义正则表达式规则
pattern_en = re.compile(r'^EN_.*')
pattern_cn = re.compile(r'^CN_.*')

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
            writeHtml(translate_language_google(tds, val), new_file_name, output_html)
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
        writeHtml(translate_language_google(tds, 'zh-tw'), new_file_name, output_html)
        output_html.close()
        shutil.move(folder_path + file_name, output_path)