# C标准库


## 1. 头文件stdio.h

### 1.1 fopen函数

C 库函数 `FILE *fopen(const char *filename, const char *mode)` 使用给定的模式 mode 打开 filename 所指向的文件。

```c
#include <stdio.h>

FILE *fopen(const char *filename, const char *mode)
```

调用fopen函数，成功返回一个 FILE 指针，失败则返回 NULL，且设置全局变量 errno 来标识错误。

* filename：表示要打开的文件名称。
* mode：表示文件的访问模式。

文件的访问模式：

| 模式     | 描述        |
| :---          |    :----:   |
| "r"          | 打开一个用于读取的文件。该文件必须存在。 |
| "w"             | 创建一个用于写入的空文件。如果文件名称与已存在的文件相同，则会删除已有文件的内容，文件被视为一个新的空文件。 |
| "a"             | 追加到一个文件。写操作向文件末尾追加数据。如果文件不存在，则创建文件。 |
| "r+"             | 打开一个用于更新的文件，可读取也可写入。该文件必须存在。 |
| "w+"             | 创建一个用于读写的空文件。 |
| "a+"             | 	打开一个用于读取和追加的文件。 |

写入文件file.txt：We are in 2022

```c
#include <stdio.h>
#include <stdlib.h>
 
int main()
{
   FILE * fp;
 
   fp = fopen ("./file/file.txt", "w+");
   fprintf(fp, "%s %s %s %d", "We", "are", "in", 2022);
   
   fclose(fp);
   
   return(0);
}
```

显示文件file.txt的内容：

```c
#include <stdio.h>

int main ()
{
   FILE *fp;
   int c;
  
   fp = fopen("file.txt","r");
   while(1)
   {
      c = fgetc(fp);
      if( feof(fp) )
      { 
          break ;
      }
      printf("%c", c);
   }
   fclose(fp);
   return(0);
}
```

### 1.2 fclose函数

C 库函数 `int fclose(FILE *stream)` 关闭流 stream。刷新所有的缓冲区。

调用fclose函数，如果流成功关闭，则该方法返回零。如果失败，则返回 EOF。

* stream：这是指向 FILE 对象的指针，该 FILE 对象指定了要被关闭的流。

### 1.3 fwrite函数

C 库函数 `size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream)` 把 ptr 所指向的数组中的数据写入到给定流 stream 中。

```c
#include <stdio.h>

size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream)
```

调用fwrite，如果成功返回一个size_t对象，表示元素的总数(nmemb)，该对象是一个整型数据类型。

* ptr：这是指向要被写入的元素数组的指针。
* size：这是要被写入的每个元素的大小，以字节为单位。
* nmemb：这是元素的个数，每个元素的大小为 size 字节。
* stream：这是指向 FILE 对象的指针，该 FILE 对象指定了一个输出流。

```c
#include<stdio.h>
 
int main ()
{
   FILE *fp;
   char str[] = "This is data!";
 
   fp = fopen( "./file/file.txt" , "w" );
//    fwrite(str, sizeof(str) , 1, fp );    //两种方式
   fwrite(str, 1, sizeof(str), fp );
 
   fclose(fp);
  
   return(0);
}
```


---

> Author: cjt  
> URL: https://cui-jiang-tao.github.io/posts/c%E6%A0%87%E5%87%86%E5%BA%93/  

