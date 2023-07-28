import os
import shutil


folder_path = './OperateGuides/'
folder_output_path = './OperateGuides_utf-8/'

if os.path.exists(folder_output_path):
    shutil.rmtree(folder_output_path)
os.makedirs(os.path.dirname(folder_output_path), exist_ok=True)

# 遍历文件夹中所有文件
for file_name in os.listdir(folder_path):
    # 打开GBK编码的文件
    with open(folder_path + file_name, "r", encoding="gbk") as file:
        gbk_data = file.read()

    # 将文本从GBK编码转换为UTF-8编码
    utf8_data = gbk_data.encode("utf-8")

    # 写入UTF-8编码的文件
    with open(folder_output_path + file_name, "w", encoding="utf-8") as file:
        file.write(utf8_data.decode("utf-8"))

