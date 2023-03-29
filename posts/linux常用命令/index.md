# Linux常用命令


## 1. 路径相关

### 1.1 pwd 显示当前路径

在终端中输入pwd命令，显示当前我们所在的位置：

```shell
ubuntu@VM-12-11-ubuntu:~$ pwd
/home/ubuntu
```

### 1.2 ls 查看当前目录

```shell
ubuntu@VM-12-11-ubuntu:~$ ls
build  c++  muduo  my-website  recipes  snap
```

可以使用如下命令让这些文件列表输出，并且显示文件相关的信息：

```shell
ubuntu@VM-12-11-ubuntu:~$ ls -l
total 24
drwxrwxr-x  4 ubuntu ubuntu 4096 Oct 31 14:07 build
drwxrwxr-x  9 ubuntu ubuntu 4096 Dec  2 14:34 c++
drwxrwxr-x  9 ubuntu ubuntu 4096 Nov  3 15:17 muduo
drwxrwxr-x 17 ubuntu ubuntu 4096 Dec  8 19:33 my-website
drwxrwxr-x 26 ubuntu ubuntu 4096 Oct 28 14:21 recipes
drwx------  3 ubuntu ubuntu 4096 Dec  8 16:14 snap
```

使用`ls -al`列出所有的文件和文件夹，这里包含隐藏目录和文件：

```shell
ubuntu@VM-12-11-ubuntu:~$ ls -al
total 96
drwxr-xr-x 14 ubuntu ubuntu  4096 Dec  8 19:16 .
drwxr-xr-x  4 root   root    4096 Oct 28 13:48 ..
-rw-------  1 ubuntu ubuntu 12973 Dec  9 14:50 .bash_history
-rw-r--r--  1 ubuntu ubuntu   220 Sep 21 16:16 .bash_logout
-rw-r--r--  1 ubuntu ubuntu  3771 Sep 21 16:16 .bashrc
drwxrwxr-x  4 ubuntu ubuntu  4096 Oct 31 14:07 build
drwxrwxr-x  9 ubuntu ubuntu  4096 Dec  2 14:34 c++
drwx------  3 ubuntu ubuntu  4096 Oct 28 14:37 .cache
-rw-rw-r--  1 ubuntu ubuntu    61 Oct 28 15:11 .gitconfig
drwxrwxr-x  3 ubuntu ubuntu  4096 Oct 28 14:37 .local
drwxrwxr-x  9 ubuntu ubuntu  4096 Nov  3 15:17 muduo
drwxrwxr-x 17 ubuntu ubuntu  4096 Dec  8 19:33 my-website
drwxrwxr-x  2 ubuntu ubuntu  4096 Sep 21 16:22 .pip
-rw-r--r--  1 ubuntu ubuntu   807 Sep 21 16:16 .profile
-rw-rw-r--  1 ubuntu ubuntu    73 Oct 28 13:48 .pydistutils.cfg
drwxrwxr-x 26 ubuntu ubuntu  4096 Oct 28 14:21 recipes
drwx------  3 ubuntu ubuntu  4096 Dec  8 16:14 snap
drwx------  2 ubuntu ubuntu  4096 Oct 28 15:09 .ssh
-rw-r--r--  1 ubuntu ubuntu     0 Oct 28 14:00 .sudo_as_admin_successful
-rw-------  1 ubuntu ubuntu     0 Oct 28 13:48 .viminfo
drwxrwxr-x  2 ubuntu ubuntu  4096 Oct 30 19:37 .vscode
drwxrwxr-x  5 ubuntu ubuntu  4096 Dec  9 09:19 .vscode-server
-rw-rw-r--  1 ubuntu ubuntu   183 Dec  8 20:32 .wget-hsts
```

其中包含.和..目录，也就是当前路径和上级目录，以.开始的文件就是隐藏文件。

### 1.3 cd 进入某个目录

#### 1.3.1 cd dir

在命令行终端中可以使用cd进入某个目录

```shell
ubuntu@VM-12-11-ubuntu:~$ cd my-website/
ubuntu@VM-12-11-ubuntu:~/my-website$ 
```

这里还有个技巧，你可以只输入文件/文件夹名字的前几个字母，然后点击tab键，让linux自动补全。

#### 1.3.2 cd ..

返回上一级目录，这时可以使用`cd ..`返回上级目录，例如：

```shell
ubuntu@VM-12-11-ubuntu:~/my-website$ cd ..
ubuntu@VM-12-11-ubuntu:~$ 
```
#### 1.3.3 cd / 与 cd ~

可以使用`cd /`命令切换到操作系统根目录，`cd`、`cd ~`命令返回到用户目录。

#### cd -

使用`cd -`命令可以回到上一个打开的目录

```shell
ubuntu@VM-12-11-ubuntu:~$ cd my-website/content/
ubuntu@VM-12-11-ubuntu:~/my-website/content$ cd -
/home/ubuntu
ubuntu@VM-12-11-ubuntu:~$ 
```

## 2. 文件相关

### 2.1 mkdir 创建目录

使用mkdir命令创建一个文件夹

```shell
mkdir workspace
```

### 2.2 touch 创建文件

```shell
ubuntu@VM-12-11-ubuntu:~$ touch workspace/test.txt
ubuntu@VM-12-11-ubuntu:~$ tree workspace/
workspace/
└── test.txt

0 directories, 1 file
```

### 2.3 mv 命令

#### 2.3.1 文件重命名

```shell
ubuntu@VM-12-11-ubuntu:~$ mv workspace/test.txt workspace/newFile.txt
ubuntu@VM-12-11-ubuntu:~$ tree workspace/
workspace/
└── newFile.txt

0 directories, 1 file
```

#### 2.3.2 移动文件

```shell
ubuntu@VM-12-11-ubuntu:~/workspace$ mv newFile.txt ~
ubuntu@VM-12-11-ubuntu:~/workspace$ cd ../
ubuntu@VM-12-11-ubuntu:~$ ll
-rw-rw-r--  1 ubuntu ubuntu     0 Dec  9 15:07 newFile.txt
```

还原：

```shell
ubuntu@VM-12-11-ubuntu:~/workspace$ mv ../newFile.txt .
ubuntu@VM-12-11-ubuntu:~/workspace$ ll
total 8
drwxrwxr-x  2 ubuntu ubuntu 4096 Dec  9 15:14 ./
drwxr-xr-x 15 ubuntu ubuntu 4096 Dec  9 15:14 ../
-rw-rw-r--  1 ubuntu ubuntu    0 Dec  9 15:07 newFile.txt
```

### 2.4 cp 拷贝文件/目录

```shell
ubuntu@VM-12-11-ubuntu:~/workspace$ cp newFile.txt copy_newFile.txt
ubuntu@VM-12-11-ubuntu:~/workspace$ tree
.
├── copy_newFile.txt
└── newFile.txt

0 directories, 2 files
```

### 2.5 rm 删除文件

```shell
ubuntu@VM-12-11-ubuntu:~/workspace$ rm copy_newFile.txt 
ubuntu@VM-12-11-ubuntu:~/workspace$ tree
.
└── newFile.txt

0 directories, 1 file
```

需要注意的是，rm可以直接删除一个文件，但是如果你想要删除整个文件夹中所有内容，那么你需要使用-rf选项：

```shell
ubuntu@VM-12-11-ubuntu:~$ rm -rf workspace/
```

### 2.6 tar 命令

linux中有很多.tar.gz的压缩包文件，解压这些压缩包文件需要用到tar命令

```shell
tar xzf VMwareTools-10.3.10-13959562.tar.gz
```

直接 tar xzf 文件名.tar.gz就可以解压出文件。

## 3. 查找

### 3.1 find 文件查找

命令格式：find (目录) [-type d | f] (文件夹 | 文件) -name （名称，可使用正则表达式）

当前my-website目录结构：

```shell
ubuntu@VM-12-11-ubuntu:~/my-website$ ls -l
total 104
-rw-rw-r--  1 ubuntu ubuntu  6661 Oct 28 15:13 404.html
drwxrwxr-x  2 ubuntu ubuntu  4096 Oct 28 15:13 archetypes
drwxrwxr-x  2 ubuntu ubuntu  4096 Dec  8 14:56 categories
-rw-rw-r--  1 ubuntu ubuntu  4962 Dec  9 09:33 config.toml
drwxrwxr-x  4 ubuntu ubuntu  4096 Oct 28 15:13 content
drwxrwxr-x  2 ubuntu ubuntu  4096 Oct 28 15:13 css
drwxrwxr-x  4 ubuntu ubuntu  4096 Oct 28 15:13 imgs
-rw-rw-r--  1 ubuntu ubuntu 16845 Oct 28 15:13 index.html
-rw-rw-r--  1 ubuntu ubuntu  5845 Oct 28 15:13 index.xml
drwxrwxr-x  2 ubuntu ubuntu  4096 Oct 28 15:13 js
drwxrwxr-x  6 ubuntu ubuntu  4096 Oct 28 15:13 lib
drwxrwxr-x  3 ubuntu ubuntu  4096 Oct 28 15:13 page
drwxrwxr-x 12 ubuntu ubuntu  4096 Oct 28 15:13 posts
drwxrwxr-x 12 ubuntu ubuntu  4096 Dec  8 21:12 public
drwxrwxr-x  3 ubuntu ubuntu  4096 Oct 28 15:13 resources
-rw-rw-r--  1 ubuntu ubuntu  3650 Oct 28 15:13 sitemap.xml
drwxrwxr-x  2 ubuntu ubuntu  4096 Oct 28 15:13 svg
drwxrwxr-x 10 ubuntu ubuntu  4096 Oct 28 15:13 tags
drwxrwxr-x  3 ubuntu ubuntu  4096 Dec  8 14:55 themes
```

#### 3.1.1 根据名字查找文件

```shell
ubuntu@VM-12-11-ubuntu:~/my-website$ sudo find . -type f -name *.txt
./themes/FixIt/layouts/robots.txt
./themes/FixIt/layouts/index.txt
```

加sudo的原因是有些文件夹的访问可能需要管理员权限。

#### 3.1.2 根据名字查找目录

```shell
ubuntu@VM-12-11-ubuntu:~/my-website$ sudo find . -type d -name imgs
./imgs
./content/imgs
./public/imgs
```

#### 3.1.3 根据名字查找目录或文件

```shell
ubuntu@VM-12-11-ubuntu:~/my-website$ sudo find . -name *.txt
./themes/FixIt/layouts/robots.txt
./themes/FixIt/layouts/index.txt
```

#### 3.1.4 根据文件大小查找

```shell
ubuntu@VM-12-11-ubuntu:~/my-website$ sudo find . -size +1M
./.git/objects/pack/pack-baf6b2db7c80e5a63c106624efaf9c594488c31b.pack
./themes/FixIt/assets/lib/mermaid/mermaid.min.js
./themes/FixIt/assets/lib/lunr/lunr.segmentit.js
./themes/FixIt/.git/objects/pack/pack-cdb6d7f116069d8fc2ef2a77a3b30240576af855.pack
./public/.git/objects/pack/pack-6d1ce01d615acf91d67d8d57ee7c16dff4f27d36.pack
```

```shell
ubuntu@VM-12-11-ubuntu:~/my-website$ sudo find . -size +700k
./.git/objects/pack/pack-baf6b2db7c80e5a63c106624efaf9c594488c31b.pack
./themes/FixIt/assets/lib/mermaid/mermaid.min.js
./themes/FixIt/assets/lib/mapbox-gl/mapbox-gl.js
./themes/FixIt/assets/lib/gitalk/gitalk.min.js
./themes/FixIt/assets/lib/lunr/lunr.segmentit.js
./themes/FixIt/assets/lib/echarts/echarts.min.js
./themes/FixIt/.git/objects/pack/pack-cdb6d7f116069d8fc2ef2a77a3b30240576af855.pack
./public/.git/objects/pack/pack-6d1ce01d615acf91d67d8d57ee7c16dff4f27d36.pack
```

#### 3.1.5 根据名字查找目录文件，忽略大小写

```shell
ubuntu@VM-12-11-ubuntu:~/my-website$ sudo find . -type d -iname content
./content
```

### 3.2 grep 命令

find是查找文件，那么grep则是查找文件中的内容字段。

grep家族总共有三个：grep，egrep，fgrep，其常用选项有：

-E ：开启扩展（Extend）的正则表达式。
-i ：忽略大小写（ignore case）。
-v ：反过来（invert），只打印没有匹配的，而匹配的反而不打印。
-n ：显示行号
-w ：被匹配的文本只能是单词，而不能是单词中的某一部分，如文本中有liker，而我搜寻的只是like，就可以使用-w选项来避免匹配 liker
-c ：显示总共有多少行被匹配到了，而不是显示被匹配到的内容，注意如果同时使用-cv选项是显示有多少行没有被匹配到。
-o ：只显示被模式匹配到的字符串。
--color :将匹配到的内容以颜色高亮显示。
-A n：显示匹配到的字符串所在的行及其后n行，after
-B n：显示匹配到的字符串所在的行及其前n行，before
-C n：显示匹配到的字符串所在的行及其前后各n行，context

以main.cpp为例：

```c++
#include <iostream>
#include <string>

class X {
public:
	explicit X(std::string str) : str_(str) { };

private:
	std::string str_;
};

int main() {
	X x1("hello");
	//X x2(std::string("hello"));

	return 0;
}
```

#### 3.2.1 查找某字符串

```shell
ubuntu@VM-12-11-ubuntu:~/c++/test_demo$ grep "hello" ./main.cpp 
        X x1("hello");
        //X x2(std::string("hello"));
```

#### 3.2.2 查找某字符串前后行内容

显示匹配到的字符串所在的行及其**后n行**：

```shell
ubuntu@VM-12-11-ubuntu:~/c++/test_demo$ grep -A 2 "main" ./main.cpp 
int main() {
        X x1("hello");
        //X x2(std::string("hello"));
```

显示匹配到的字符串所在的行及其**前n行**：

```shell
ubuntu@VM-12-11-ubuntu:~/c++/test_demo$ grep -B 3 "main" ./main.cpp 
        std::string str_;
};

int main() {
```

显示匹配到的字符串所在的行及其**前后各n行**：

```shell
ubuntu@VM-12-11-ubuntu:~/c++/test_demo$ grep -C 3 "main" ./main.cpp 
        std::string str_;
};

int main() {
        X x1("hello");
        //X x2(std::string("hello"));

```

---

> Author: cjt  
> URL: https://cui-jiang-tao.github.io/posts/linux%E5%B8%B8%E7%94%A8%E5%91%BD%E4%BB%A4/  

