import os
import re
from lxml import etree
import shutil


def has_file(directory, file_name):
    for root, dirs, files in os.walk(directory):
        if file_name in files:
            return True
    return False


# 待查找的文件夹路径
folder_path_ = './_Htmls/'
folder_path = './Htmls/'
folder_path_en = './ens/'

if os.path.exists(folder_path):
    shutil.rmtree(folder_path)
os.makedirs(os.path.dirname(folder_path), exist_ok=True)

# 定义正则表达式规则
pattern_en = re.compile(r'^EN_.*')
pattern_cn = re.compile(r'^CN_.*')

input_index = open("index.bin", 'r', encoding='utf-8')
index_set = set()

while True:
    line = input_index.readline()
    line = line.replace("\n", "")
    if len(line) == 0:
        break
    index_set.add(line)

input_index.close()

for file_name in os.listdir(folder_path_):
    str_name = file_name.replace(".html", "").replace("EN_", "").replace("CN_", "")
    if not str_name in index_set:
        pass
    else:
        # 使用shutil.copy()复制文件
        shutil.copy(folder_path_ + file_name, folder_path)
        print("copy ", file_name)

cnt = 0
map_td = {}
set_files = set()
for file_name in os.listdir(folder_path):
    str_name = file_name.replace("EN_", "").replace("CN_", "")
    if os.path.exists(folder_path + "EN_" + str_name) and os.path.exists(folder_path + "CN_" + str_name):
        html_cn = etree.parse(folder_path + "CN_" + str_name, etree.HTMLParser())
        html_en = etree.parse(folder_path + "EN_" + str_name, etree.HTMLParser())
        # 获取所有td标签内容
        tds_cn = html_cn.xpath('/html/body/table/tr/td')
        tds_en = html_en.xpath('/html/body/table/tr/td')

        i_ = 0
        while i_ < len(tds_cn):
            str_cn = str(tds_cn[i_].text).strip()
            str_en = str(tds_en[i_].text).strip()
            if str_cn and str_cn != 'None':
                if str_en and str_en != 'None':
                    map_td[str_cn] = str_en
                else:
                    map_td[str_cn] = str_cn
            i_ += 1
    else:
        set_files.add(file_name)
        print(file_name, end="\t")
        cnt += 1


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


print("\n总数：", cnt)

if cnt:
    if os.path.exists(folder_path_en):
        shutil.rmtree(folder_path_en)
    os.makedirs(os.path.dirname(folder_path_en), exist_ok=True)

for file_name in set_files:
    if file_name.find("CN_") == 0:
        file_name_en = file_name.replace("CN_", "EN_")
        html = etree.parse(folder_path + file_name, etree.HTMLParser())
        tds = html.xpath('/html/body/table/tr/td')

        tds_en = []
        i_ = 0
        while i_ < len(tds):
            str_td = str(tds[i_].text).strip()
            if str_td and str_td != 'None':
                if str_td in map_td.keys():
                    tds_en.append(map_td[str_td])
                else:
                    tds_en.append("")
            else:
                tds_en.append("")
            i_ += 1

        output_html = open(folder_path_en + file_name_en, 'w', encoding='utf-8')
        writeHtml(tds_en, file_name_en, output_html)
        output_html.close()
