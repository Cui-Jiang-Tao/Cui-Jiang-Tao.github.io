# makefile的简单例子


## 示例

树形结构：

```shell
ubuntu@VM-12-11-ubuntu:~/c++/makefile$ tree
.
├── factorial.cpp
├── functions.h
├── main.cpp
├── Makefile
└── printHello.cpp

0 directories, 5 files
```

functions.h

```c++
#ifndef FUNCTIONS_H
#define FUNCTIONS_H
#include <iostream>
void printHello();
int factorial(int n);
#endif
```

factorial.cpp

```c++
#include "functions.h"

int factorial(int n) {
  if (n == 1) {
    return 1;
  } else {
    return n * factorial(n - 1);
  }
}
```

main.cpp

```c++
#include "functions.h"

using namespace std;

int main() {
    printHello();

    cout << "This is main：" << endl;
    cout << "The factorial of 5 is：" << factorial(5) << endl;
}
```

printHello.cpp

```c++
#include "functions.h"

using namespace std;

void printHello() {
    int i;
    cout << "Hello World!" << endl;
}
```

## 版本 1

```makefile
## VERSION 1
hello: main.cpp printHello.cpp factorial.cpp
	g++ -o hello main.cpp printHello.cpp factorial.cpp
```

第一个版本比较简单：

* hello的生成依赖于：main.cpp printHello.cpp factorial.cpp
* 通过：g++ -o hello main.cpp printHello.cpp factorial.cpp 来生成hello这个目标

## 版本 2

```makefile
CXX = g++
TARGET = hello
OBJ = main.o printHello.o factorial.o

$(TARGET) : $(OBJ)
	$(CXX) -o $(TARGET) $(OBJ)

main.o : main.cpp
	$(CXX) -c main.cpp

printHello.o : printHello.cpp
	$(CXX) -c printHello.cpp

factorial.o : factorial.cpp
	$(CXX) -c factorial.cpp
```

首先定义了3个变量，CXX、TARGET、OBJ；然后再说明定义的TARGET变量依赖于OBJ这个变量，如果OBJ变量更新的化，使用命令(`$(CXX) -o $(TARGET) $(OBJ)`)重新生成CXX。而OBJ变量依赖于main.o printHello.o factorial.o这三个文件，然后make会根据后面的解释生成这三个文件。

make生成：

```shell
ubuntu@VM-12-11-ubuntu:~/c++/makefile$ make
g++ -c main.cpp
g++ -c printHello.cpp
g++ -c factorial.cpp
g++ -o hello main.o printHello.o factorial.o
```

## 版本 3

```makefile
CXX = g++
TARGET = hello
OBJ = main.o printHello.o factorial.o

# 增加了一条编译选项
CXXFLAGS = -c -Wall

$(TARGET) : ${OBJ}
	${CXX} -o $@ $^

%.o : %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

.PHONY : clear
clear : 
	rm -f *.o $(TARGET)
```

其中，`$@` 代表的就是 `$(TARGET)`，`$^` 代表的就是 `${OBJ}`

```makefile
$(TARGET) : ${OBJ}
	${CXX} -o $@ $^
```

如下的命令是将所以的.cpp文件生成对应的.o文件，以`$(CXX) $(CXXFLAGS) $< -o $@`命令的方式生成。

```makefile
%.o : %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@
```

这条命令是删除对应`*.o`文件和`$(TARGET)`文件

```makefile
.PHONY : clear
clear : 
	rm -f *.o $(TARGET)
```

其中`.PHONY : clear`用来避免歧义

可以通过 `make clear`来执行：

```shell
ubuntu@VM-12-11-ubuntu:~/c++/makefile$ make clear
rm -f *.o hello
```

## 版本 4

```makefile
CXX = g++
TARGET = hello
SRC = $(wildcard *.cpp)
OBJ = $(patsubst %.cpp, %.o, ${SRC})

CXXFLAGS = -c -Wall

$(TARGET) : ${OBJ}
	${CXX} -o $@ $^

%.o : %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

.PHONY : clear
clear : 
	rm -f *.o $(TARGET)
```

`SRC = $(wildcard *.cpp)`，将所有当前目录的.cpp 都放到SRC变量中。

`OBJ = $(patsubst %.cpp, %.o, ${SRC})`，将SRC所有的.cpp文件 替换为.o文件

---

> Author: cjt  
> URL: https://cui-jiang-tao.github.io/posts/makefile/  

