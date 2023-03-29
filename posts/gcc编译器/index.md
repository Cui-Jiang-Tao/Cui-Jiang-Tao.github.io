# GCC编译器


* 使用gcc指令编译c代码
* 使用g++指令编译c++代码

## 1.编译过程

test.cpp

```c++
#include <iostream>

int main() {

    #ifdef DEBUG
        std::cout << "DEBUG ..." << std::endl;
    #else
      std::cout << "hello world!!!" << std::endl;
    #endif

    return 0;
}
```

1. 预处理(Pre-Processing)

-E 选项指示编译器仅对输入文件进行预处理

```g++
g++ -E test.cpp -o test.i //.i文件
```

2. 编译(Compiling)

* -S 编译选项告诉 g++ 在为 C++ 代码产生了汇编语言文件后停止编译
* g++ 产生的汇编语言文件的缺省扩展名是 .s

```g++
g++ -S test.i -o test.s //.s文件
```

3. 汇编(Assmebling)

* -c 选项告诉 g++ 仅把源代码编译为**机器语言的目标代码**
* 缺省时 g++ 建立的目标代码文件有一个 .o 的扩展名。

```g++
g++ -c test.s -o test.o //.o文件
```

4. 链接(Linking)
* -o 编译选项来为将产生的**可执行文件**用指定的文件名

```g++
g++ test.o -o test.bin  //.bin文件
```

## 2.g++编译参数

1. -g 编译带调试信息的可执行文件

```g++
# -g 选项告诉 GCC 产生能被 GNU 调试器GDB使用的调试信息，以调试程序。
# 产生带调试信息的可执行文件test
g++ -g test.cpp
```

2. -O[n] 优化源代码

```g++
## 所谓优化，例如省略掉代码中从未使用过的变量、直接将常量表达式用结果值代替等等，这些操作
会缩减目标文件所包含的代码量，提高最终生成的可执行文件的运行效率。
# -O 选项告诉 g++ 对源代码进行基本优化。这些优化在大多数情况下都会使程序执行的更快。 -O2
选项告诉 g++ 产生尽可能小和尽可能快的代码。 如-O2，-O3，-On（n 常为0–3）
# -O 同时减小代码的长度和执行时间，其效果等价于-O1
# -O0 表示不做优化
# -O1 为默认优化
# -O2 除了完成-O1的优化之外，还进行一些额外的调整工作，如指令调整等。
# -O3 则包括循环展开和其他一些与处理特性相关的优化工作。
# 选项将使编译的速度比使用 -O 时慢， 但通常产生的代码执行速度会更快。
# 使用 -O2优化源代码，并输出可执行文件
g++ -O2 test.cpp
```

3. -l 和 -L 指定库文件 | 指定库文件路径

```g++
# -l参数(小写)就是用来指定程序要链接的库，-l参数紧接着就是库名
# 在/lib和/usr/lib和/usr/local/lib里的库直接用-l参数就能链接
# 链接glog库
g++ -lglog test.cpp
# 如果库文件没放在上面三个目录里，需要使用-L参数(大写)指定库文件所在目录
# -L参数跟着的是库文件所在的目录名
# 链接mytest库，libmytest.so在/home/bing/mytestlibfolder目录下
g++ -L/home/bing/mytestlibfolder -lmytest test.cpp
```

4. -l 指定头文件搜索目录

```g++
# -I
# /usr/include目录一般是不用指定的，gcc知道去那里找，但 是如果头文件不在/usr/icnclude
里我们就要用-I参数指定了，比如头文件放在/myinclude目录里，那编译命令行就要加上-
I/myinclude 参数了，如果不加你会得到一个”xxxx.h: No such file or directory”的错
误。-I参数可以用相对路径，比如头文件在当前 目录，可以用-I.来指定。上面我们提到的–cflags参
数就是用来生成-I参数的。
g++ -I/myinclude test.cpp
```

5. -Wall 打印警告信息

```g++
# 打印出gcc提供的警告信息
g++ -Wall test.cpp
```

6. -w 关闭警告信息

```g++
# 关闭所有警告信息
g++ -w test.cpp
```

7. -std=c++11 设置编译标准

```g++
# 使用 c++11 标准编译 test.cpp
g++ -std=c++11 test.cpp
```

8. -o 指定输出文件名

```g++
# 指定即将产生的文件名
# 指定输出可执行文件名为test
g++ test.cpp -o test
```
9. -D 定义宏

```g++
# 在使用gcc/g++编译的时候定义宏
# 常用场景：
# -DDEBUG 定义DEBUG宏，可能文件中有DEBUG宏部分的相关信息，用个DDEBUG来选择开启或关闭
DEBUG
g++ test.cpp -DDEBUG -o test 
```

## 3.g++命令编译

```tree
.
├── include
│   └── say.h
├── main.cpp
└── src
    └── say.cpp

2 directories, 3 files
```

say.h

```c++
#pragma once    //防止重复编译
#include <iostream>
#include <string>

class Say
{
public:
    Say(std::string name) : name(name) {

    }

    void sayHello();

private:
    std::string name; 
};
```

say.cpp

```c++
#include "say.h"

void Say::sayHello() {
    std::cout << name << ": say hello!!!" << endl;
}
```

main.cpp

```c++
#include "say.h"

int main(int argc, char **argv)
{
    bool wall = 1;  //未使用的变量

    Say say("cjt");

    say.sayHello();

    return 0;
}
```

### 1. 直接编译

编译，生成可执行文件

```g++
g++ main.cpp src/say.cpp -Iinclude -o sayHello
```

增加参数编译，生成可执行文件

```g++
g++ main.cpp src/say.cpp -Iinclude -std=c++11 -o2 -Wall -o sayHello
```

### 2.生成库文件并编译

可参考：
[C++静态库与动态库](<https://www.cnblogs.com/skynet/p/3372855.html/> "C++静态库与动态库") 、
[C语言静态库VS动态库](<https://cloud.tencent.com/developer/article/1656728/> "C语言静态库VS动态库")

静态库VS动态库

静态库和动态库的载入时间是不一样的。

静态库的代码在编译的过程中已经载入到可执行文件中，所以最后生成的可执行文件相对较大。

动态库的代码在可执行程序运行时才载入内存，在编译过程中仅简单的引用，所以最后生成的可执行文件相对较小。

静态库和动态库的最大区别是，静态库链接的时候把库直接加载到程序中,而动态库链接的时候，它只是保留接口，将动态库与程序代码独立，这样就可以提高代码的可复用度和降低程序的耦合度。

静态库在程序编译时会被连接到目标代码中，程序运行时将不再需要该静态库。

动态库在程序编译时并不会被连接到目标代码中，而是在程序运行是才被载入，因此在程序运行时还需要动态库存在。

无论静态库，还是动态库，都是由.o文件创建的。因此，我们必须将源程序.cpp通过g++先编译成.o文件。

___

#### 1. 链接**静态库**生成可执行文件

```g++
#汇编生成sayHello.o文件
g++ src/say.cpp -Iinclude -c -o sayHello.o

#生成静态库libsayHello.o
ar rs libsayHello.a sayHello.o 

#链接，生成可执行文件 main
说明：-L.(静态库的所在目录，.代表当前目录)、 -lsayHello(静态库的名字sayHello)
g++ main.cpp -Iinclude -L. -lsayHello -o main

#运行可执行文件
./main
```

#### 2. 链接**动态库**生成可执行文件

```g++
#生成动态库libsayHello.so
g++ src/say.cpp -Iinclude -fPIC -shared -o libsayHello.so

#链接，生成可执行文件 main
g++ main.cpp -Iinclude -L. -lsayHello -o main

#运行可执行文件
说明: 需要指定动态库的路径
LD_LIBRARY_PATH=. ./main 
```


---

> Author: cjt  
> URL: https://cui-jiang-tao.github.io/posts/gcc%E7%BC%96%E8%AF%91%E5%99%A8/  

