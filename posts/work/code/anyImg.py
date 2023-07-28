import os
import glob


def create_imgs(file_path: str, split: bytes):
    f_read = open(file_path, 'rb')
    img_bytes = f_read.read()
    f_read.close()
    imgs = img_bytes.split(split)
    imgs.pop(0)
    str_add = b""
    for img in imgs:
        if len(img) < 0x400:
            str_add = img + split
            continue
        img = str_add + img
        str_add = b""
        img = split + img
        flag_jpg = 1
        index0 = img.find(b".jpg")
        if index0 == -1:
            flag_jpg = 0
            index0 = img.find(b".png")
        if index0 == -1:
            print(f"error---{file_path}")
        path = img[:index0 + 4]
        dirs = path.split(b"/")
        cur_path = "imgs//"
        for di in dirs[:-1]:
            cur_path = cur_path + di.decode('utf-8')
            if not os.path.exists(cur_path):
                os.mkdir(cur_path)
            cur_path = cur_path + "//"
        img_name = dirs[-1].decode('utf-8')
        img_start = img.find(b"\xff\xd8\xff") if flag_jpg else img.find(b"\x89\x50\x4e\x47")
        img_end = img.rfind(b"\xff\xd9") + 2 if flag_jpg else img.rfind(b"\xae\x42\x60\x82") + 4
        with open(f"{cur_path}{img_name}", 'wb') as f:
            if img_start == -1 or img_end == -1:
                f.write(img)
            else:
                f.write(img[img_start:img_end])


def get_split_and_create_imgs(file_path: str):
    f_read = open(file_path, 'rb')
    img_bytes = f_read.read()
    f_read.close()
    first_img = img_bytes.find(b".jpg")
    if first_img == -1:
        first_img = img_bytes.find(b".png")
    if first_img == -1:
        print(f"error---{file_path}")
    path0 = first_img - 1
    while img_bytes[path0] != 0x2e:
        path0 -= 1
    path = b"./" + img_bytes[path0:first_img].split(b"/")[1]
    create_imgs(file_path, path)


files = glob.glob("files//*.bin")
for file in files:
    get_split_and_create_imgs(file)
