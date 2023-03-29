# Hugo的安装和FixIt 主题


推荐使用 Hugo extended 版本

* 由于这个主题的一些特性需要将  SCSS 转换为  CSS, 推荐使用 Hugo extended 版本来获得更好的使用体验。


[主题参考](https://fixit.lruihao.cn/zh-cn/theme-documentation-basics/)

## ubuntu 如何安装snap

也就说你的Ubuntu没有安装snap。 你可能需要自己手动安装它，运行命令 `sudo apt update && sudo apt install snapd` ，apt命令将会更新软件包索引并安装snapd。

## 安装hugo

默认情况下，Hugo 在 Ubuntu 20.04 默认存储库中不可用。 现在使用 Snap 安装 Hugo：

```shell
sudo snap install hugo
```

## 使用Hugo创建一个站点

由于是用snap安装的Hugo，我们在Hugo相关命令前要加上`snap run`：

```shell
snap run hugo new site my_website
```

这样就在/home下创建了一个my_website的文件夹，里面保存了Hugo生成网站的文件。

## 安装主题

```shell
git clone https://github.com/hugo-fixit/FixIt.git themes/FixIt
```

## 测试网站

```shell
snap run hugo server -D
```

在浏览器中输入localhost:1313可以预览网站。

## 生成网站

接下来我们要生成静态页面

```shell
snap run hugo
```

---

> Author: cjt  
> URL: https://cui-jiang-tao.github.io/posts/hugo%E6%90%AD%E5%BB%BA/  

