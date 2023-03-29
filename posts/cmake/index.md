# CMake


前言

* CMake是一个跨平台的安装编译工具，可以用简单的语句来描述所有平台的安装(编译过程)。
* CMake可以说已经成为大部分C++开源项目标配

## 1. 语法特性介绍

* 基本语法格式：指令(参数 1 参数 2...)
  * 参数使用括弧括起
  * 参数之间使用空格或分号分开
* 指令是大小写无关的，参数和变量是大小写相关的

```cmake
set(HELLO hello.cpp)
add_executable(hello main.cpp hello.cpp)
ADD_EXECUTABLE(hello main.cpp ${HELLO})
```

* 变量使用${}方式取值，但是在 IF 控制语句中是直接使用变量名

## 2. 重要指令和CMake常用变量

* cmake_minimum_required - 指定CMake的最小版本要求
  * 语法： `cmake_minimum_required(VERSION versionNumber [FATAL_ERROR])`

  ```camke
  # CMake最小版本要求为2.8.3
  cmake_minimum_required(VERSION 2.8.3)
  ```

* project - 定义工程名称，并可指定工程支持的语言
  * 语法： `project(projectname [CXX] [C] [Java])`

  ```g++
  # 指定工程名为HELLOWORLD
  project(HELLOWORLD)
  ```

* set - 显式的定义变量
  * 语法：`set(VAR [VALUE] [CACHE TYPE DOCSTRING [FORCE]])`

  ```g++
  # 定义SRC变量，其值为sayHello.cpp hello.cpp
  set(SRC sayHello.cpp hello.cpp)
  ```

* include_directories - 向工程添加多个特定的头文件搜索路径 --->相当于指定g++编译器的-I参数
  * 语法： `include_directories([AFTER|BEFORE] [SYSTEM] dir1 dir2 ...)`

  ```g++
  # 将/usr/include/myincludefolder 和 ./include 添加到头文件搜索路径
  include_directories(/usr/include/myincludefolder ./include)
  ```

* link_directories - 向工程添加多个特定的库文件搜索路径 --->相当于指定g++编译器的-L参数
  * 语法： `link_directories(dir1 dir2 ...)`

  ```g++
  # 将/usr/lib/mylibfolder 和 ./lib 添加到库文件搜索路径
  link_directories(/usr/lib/mylibfolder ./lib)
  ```

* add_library - 生成库文件
  * 语法： `add_library(libname [SHARED|STATIC|MODULE] [EXCLUDE_FROM_ALL] source1 source2 ... sourceN)`

  ```g++
  # 通过变量 SRC 生成 libhello.so 共享库
  add_library(hello SHARED ${SRC})
  ```

* add_compile_options - 添加编译参数
  * 语法：`add_compile_options()`

  ```g++
  # 添加编译参数 -Wall -std=c++11 -O2
  add_compile_options(-Wall -std=c++11 -O2)
  ```

* add_executable - 生成可执行文件
  * 语法：`add_executable(exename source1 source2 ... sourceN)`

  ```g++
  # 编译main.cpp生成可执行文件main
  add_executable(main main.cpp)
  ```

* target_link_libraries - 为 target 添加需要链接的共享库 --->相同于指定g++编译器-l参数
  * 语法： `target_link_libraries(target library1<debug | optimized> library2...)`

  ```g++
  # 将hello动态库文件链接到可执行文件main
  target_link_libraries(main hello)
  ```

* add_subdirectory - 向当前工程添加存放源文件的子目录，并可以指定中间二进制和目标二进制
存放的位置
  * 语法： `add_subdirectory(source_dir [binary_dir] [EXCLUDE_FROM_ALL])`

  ```g++
  # 添加src子目录，src中需有一个CMakeLists.txt
  add_subdirectory(src)
  ```

* aux_source_directory - 发现一个目录下所有的源代码文件并将列表存储在一个变量中，这个指令临时被用来自动构建源文件列表
  * 语法： `aux_source_directory(dir VARIABLE)`

  ```g++
  # 定义SRC变量，其值为当前目录下所有的源代码文件
  aux_source_directory(. SRC)
  # 编译SRC变量所代表的源代码文件，生成main可执行文件
  add_executable(main ${SRC})
  ```

## 3. CMake常用变量

* CMAKE_C_FLAGS gcc编译选项
* CMAKE_CXX_FLAGS g++编译选项

  ```g++
  # 在CMAKE_CXX_FLAGS编译选项后追加-std=c++11
  set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
  ```

* CMAKE_BUILD_TYPE 编译类型(Debug, Release)
  
  ```g++
  # 设定编译类型为debug，调试时需要选择debug
  set(CMAKE_BUILD_TYPE Debug)
  # 设定编译类型为release，发布时需要选择release
  set(CMAKE_BUILD_TYPE Release)
  ```

* CMAKE_BINARY_DIR
* PROJECT_BINARY_DIR
* _BINARY_DIR

  ```g++
  1. 这三个变量指代的内容是一致的。
  2. 如果是 in source build，指的就是工程顶层目录。
  3. 如果是 out-of-source 编译,指的是工程编译发生的目录。
  4. PROJECT_BINARY_DIR 跟其他指令稍有区别，不过现在，你可以理解为他们是一致的。
  ```

* CMAKE_SOURCE_DIR
* PROJECT_SOURCE_DIR
* _SOURCE_DIR

  ```g+=
  1. 这三个变量指代的内容是一致的,不论采用何种编译方式,都是工程顶层目录。
  2. 也就是在 in source build时,他跟 CMAKE_BINARY_DIR 等变量一致。
  3. PROJECT_SOURCE_DIR 跟其他指令稍有区别,现在,你可以理解为他们是一致的。
  ```

* CMAKE_C_COMPILER：指定C编译器
* CMAKE_CXX_COMPILER：指定C++编译器
* EXECUTABLE_OUTPUT_PATH：可执行文件输出的存放路径
* LIBRARY_OUTPUT_PATH：库文件输出的存放路径

## 4. CMake编译工程

CMake目录结构：项目主目录存在一个CMakeLists.txt文件

**两种方式设置编译规则：**

1. 包含源文件的子文件夹**包含**CMakeLists.txt文件，主目录的CMakeLists.txt通过add_subdirectory
添加子目录即可；
2. 包含源文件的子文件夹**未包含**CMakeLists.txt文件，子目录编译规则体现在主目录的CMakeLists.txt中；

### 4.1 编译流程

在 linux 平台下使用 CMake 构建C/C++工程的流程如下:

* 手动编写 CMakeLists.txt。
* 执行命令 cmake PATH 生成 Makefile ( PATH 是顶层CMakeLists.txt 所在的目录 )。
* 执行命令 make 进行编译。

```g++
# important tips
. # 表示当前目录
./ # 表示当前目录
.. # 表示上级目录
../ # 表示上级目录
```

### 4.2 两种构建方式

* **内部构建(in-source build)**：不推荐使用

内部构建会在同级目录下产生一大堆中间文件，这些中间文件并不是我们最终所需要的，和工程源文件放在一起会显得杂乱无章。

```g++
## 内部构建
# 在当前目录下，编译本目录的CMakeLists.txt，生成Makefile和其他文件
cmake .
# 执行make命令，生成target
make
```

* **外部构建(out-of-source build)**：推荐使用

将编译输出文件与源文件放到不同目录中

```g++
## 外部构建
# 1. 在当前目录下，创建build文件夹
mkdir build
# 2. 进入到build文件夹
cd build
# 3. 编译上级目录的CMakeLists.txt，生成Makefile和其他文件
cmake ..
# 4. 执行make命令，生成target
make
```

## 5. CMake代码实践

### 5.1 简单CMake工程

test.cpp

```c++
#include <iostream>

int main() {

    std::cout << "hello world!!!" << std::endl;

    return 0;
}
```

CMakeLists.txt

```g++
# Set the minimum version of CMake that can be used
cmake_minimum_required(VERSION 3.0)

# Set the project name
project (TEST)

# Add an executable
add_executable(test_cmake test.cpp)
```

### 5.2 多级目录工程 - 直接编译

```tree

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

CMakeLists.txt

```g++
# Set the minimum version of CMake that can be used
cmake_minimum_required(VERSION 3.0)

#project name
project(SAYHELLO)

#head file pat
include_directories(include)

#生成可执行文件
add_executable(sayHello main.cpp src/say.cpp)
```

### 5.3 多级目录工程 - 生成库编译

```g++
# Set the minimum version of CMake that can be used
cmake_minimum_required(VERSION 3.0)

#project name
project(SAYHELLO_LIBRARY)

#add compile options - 添加编译参数
add_compile_options(-std=c++11 -Wall)

#set CMAKE_BUILD_TYPE 编译类型(Debug)
set(CMAKE_BUILD_TYPE Debug)

# set output binary path
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/bin)

############################################################

# Create a library
############################################################
#Generate the static library from the library sources
add_library(say_lib STATIC src/say.cpp)
target_include_directories(say_lib PUBLIC ${PROJECT_SOURCE_DIR}/include)

############################################################

# Create an executable
############################################################
# Add an executable with the above sources
add_executable(sayHello main.cpp)

# link the new sayHello target with the say_lib target
target_link_libraries(sayHello say_lib)
```

## 6. 搭配 vs code

```tree
.
├── CMakeLists.txt
├── build
├── include
│   └── say.h
├── main.cpp
└── src
    └── say.cpp

3 directories, 4 files
```

launch.json

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [

        
        {
            "name": "(gdb) Attach",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/c++/build/bin/sayHello",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ],
            "preLaunchTask": "Build",
            "miDebuggerPath": "/usr/bin/gdb"
        }

    ]
}
```

tasks.json

```json
{
    "version": "2.0.0",
    "options": {
        "cwd": "${workspaceFolder}/c++/build"
    },
    "tasks": [
        {
            "type": "shell",
            "label": "cmake",
            "command": "cmake",
            "args":[
                ".."
            ]
        },
        {
            "label": "make",
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "command": "make",
            "args": [

            ]
        },
        {
            "label": "Build",
            "dependsOrder": "sequence",
            "dependsOn": [
                "cmake",
                "make"
            ]
        }
    ],
}
```


---

> Author: cjt  
> URL: https://cui-jiang-tao.github.io/posts/cmake/  

