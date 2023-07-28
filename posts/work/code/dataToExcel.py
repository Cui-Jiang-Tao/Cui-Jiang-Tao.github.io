import csv
from openpyxl import Workbook

excel_name = "808_" + input("请输入文件名称: ") + ".xlsx"

print("请等待...")

# 创建一个新的Excel工作簿
workbook = Workbook()

files_ = ['Menus_cn.bin', 'Menus_en.bin', 'ECUMenu_cn.bin']

for fileName in files_:
    try:
        # 读取文本文件，并以Tab作为分隔符
        with open(fileName, 'r', encoding='gbk') as file:
            reader = csv.reader(file, delimiter='\t')
            data = list(reader)
            # 创建第二个工作表并设置名称
            sheet = workbook.create_sheet(title=fileName.replace(".bin", ""))
            # 将数据写入第一个Excel工作表
            for row in data:
                sheet.append(row)
    except:
        print(fileName + " not find")

# 删除默认的Sheet工作表
default_sheet = workbook.get_sheet_by_name('Sheet')
workbook.remove(default_sheet)

# 保存Excel文件
workbook.save(excel_name)
