# Markdown基础语法


## 1.标题

```md
# h1 标题
## h2 标题
### h3 标题
#### h4 标题
##### h5 标题
###### h6 标题
```

## 2.注释

```md
<!-- 这是一段注释 -->
```

## 3.水平线

``` md
___:三个连续的下划线

下面两个警告：MD035/hr-style: Horizontal rule style [Expected: ___; Actual: ---]markdownlintMD035
---:三个连续的破折号
***:三个连续的星号
```

效果如下：
___

## 4.段落

Lorem ipsum dolor sit amet, graecis denique ei vel, at duo primis mandamus. Et legere ocurreret pri,
animal tacimates complectitur ad cum. Cu eum inermis inimicus efficiendi. Labore officiis his ex,
soluta officiis concludaturque ei qui, vide sensibus vim ad.

可以通过两个回车进行换行

## 5.内联 HTML 元素

## 6.强调

```md
字符**加粗**

字符*斜体*

字符~~删除线~~
```

效果如下：

* 字符**加粗**
* 字符*斜体*
* 字符~~删除线~~

## 7.引用

```md
> 引用内容
>> 多层引用
```

> 引用内容
>> 多层引用

## 8.列表

a. 无序列表

```md
* 一项内容
- 一项内容
+ 一项内容
```

效果如下：

* 1
* 2

___

b. 有序列表

```md
1. ....
2. ....
3. ....
```

效果如下：

1. 1
2. 2

___

c. 任务列表

任务列表使您可以创建带有复选框的项目列表。在支持任务列表的Markdown应用程序中，复选框将显示在内容旁边。要创建任务列表，请在任务列表项之前添加破折号-和方括号[ ]，并在[ ]前面加上空格。要选择一个复选框，请在方括号[x]之间添加 x 。

- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media

## 9.代码

a.行内代码

`c++`

```md
`c++`
```

b.缩进代码

```md
                line 1
                line 2
```

c.围栏代码块

## 10.表格

## 11.链接

### a.基本链接

```md
<https://www.baidu.com>
<xxx@xx.com>
[百度](https://www.baidu.com)
```

效果如下：

<https://www.baidu.com>

<xxx@xx.com>

[百度](https://www.baidu.com/)

加入鼠标悬浮提示: 
[百度](<https://www.baidu.com/> "百度一下")

### b.定位标记

## 12.脚注

```md
这是一个数字脚注[^1].
这是一个带标签的脚注[^label]

[^1]: 这是一个数字脚注
[^label]: 这是一个带标签的脚注
```

这是一个数字脚注[^1].

这是一个带标签的脚注[^label]

## 13.图片

```md
![图片alt](图片链接 "图片title")。
![Minion](https://octodex.github.com/images/minion.png)
```

![Minion](https://octodex.github.com/images/minion.png)

或者

```md
![Alt text](https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat")
```

![Alt text](https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat")

像链接一样, 图片也具有脚注样式的语法:

```md
![Alt text][id]
```

[id]:https://octodex.github.com/images/dojocat.jpg  "The Dojocat"

___

```md
[^1]: 这是一个数字脚注
[^label]: 这是一个带标签的脚
```

[^1]: 这是一个数字脚注
[^label]: 这是一个带标签的脚

## 14.首航缩进

全角缩进：`&emsp;`

半角缩进：`&ensp;`


---

> Author: cjt  
> URL: https://cui-jiang-tao.github.io/posts/markdown/  

