# Git


## 1. 配置

```git
git config --global user.name "Your Name"
git config --global user.email "email@example.com"

#设置远程仓库
git remote add origin git@github.com:vstk771/gitTest.git
```

注意：

git config命令的--global参数，用了这个参数，表示你这台机器上所有的Git仓库都会使用这个配置，当然也可以对某个仓库指定不同的用户名和Email地址。

## 2.创建版本库

通过git init命令把这个目录变成Git可以管理的仓库：

```git
git init
```

## 3. 时光穿梭机

### 3.1 版本回退

在仓库创建一个文件test.txt

```txt
hello world
```

```git
git add test.txt
git commit -m "first commit" 
```

提交之后，我们修改test.txt的内容: Hello World!!!

git status命令可以让我们时刻掌握仓库当前的状态

```git
git status
```

git diff顾名思义就是查看difference，显示的格式正是Unix通用的diff格式，*先对比暂存区，如果暂存区是空的，再对比版本库的*。

```git
git diff test.txt
```

在Git中，我们用git log命令查看提交日志(只显示到HEAD的)：

```git
git log
```

现在，我们要把当前版本回退到上一个版本，就可以使用git reset命令：

```git
git reset --hard HEAD^
```

Git提供了一个命令git reflog用来记录你的每一次命令：

```git
git reflog
```

通过 git reflog 查看命令历史，以便确定要回到未来的哪个版本

```git
$ git reflog
5a14f64 (HEAD -> master) HEAD@{0}: reset: moving to HEAD^
6507263 HEAD@{1}: commit: second commit
5a14f64 (HEAD -> master) HEAD@{2}: commit (initial): first commit

$ git reset --hard 6507263
```

### 3.2 工作区与暂存区

1. 工作区（Working Directory）

就是版本库的文件夹目录

2. 版本库（Repository）

工作区有一个隐藏目录.git，这个不算工作区，而是Git的版本库。

Git的版本库里存了很多东西，其中最重要的就是称为stage（或者叫index）的暂存区，还有Git为我们自动创建的第一个分支master，以及指向master的一个指针叫HEAD。

把文件往Git版本库里添加的时候，是分两步执行的：

第一步是用git add把文件添加进去，实际上就是把文件修改添加到暂存区；

第二步是用git commit提交更改，实际上就是把暂存区的所有内容提交到当前分支。

因为我们创建Git版本库时，Git自动为我们创建了唯一一个master分支，所以，现在，git commit就是往master分支上提交更改。

可以简单理解为，需要提交的文件修改通通放到暂存区，然后，一次性提交暂存区的所有修改。

### 3.3 管理修改

第一次修改 -> git add -> 第二次修改 -> git commit

Git管理的是修改，当你用git add命令后，在工作区的第一次修改被放入暂存区，准备提交，但是，在工作区的第二次修改并没有放入暂存区，所以，git commit只负责把暂存区的修改提交了，也就是第一次的修改被提交了，第二次的修改不会被提交。

总结：每次修改，如果不用git add到暂存区，那就不会加入到commit中；

### 3.4 撤销修改

命令git checkout -- test.txt意思就是，把test.txt文件在工作区的修改全部撤销，这里有两种情况：

* 一种是test.txt自修改后还没有被放到暂存区，现在，撤销修改就回到和版本库一模一样的状态；
* 一种是test.txt已经添加到暂存区后，又作了修改，现在，撤销修改就回到添加到暂存区后的状态。

第一种情况：

1. 版本库的test.txt文件的内容 : Hello World!!!1111
2. 暂存区是空的
3. 工作区的内容：Hello World!!!2222

```git
git checkout -- test.txt
```

现在，撤销修改就回到和版本库一模一样的状态；

第二种情况

1. 版本库的test.txt文件的内容：Hello World!!!1111
2. 暂存区的test.text文件的内容：Hello World!!!2222
3. 工作区的内容：Hello World!!!3333

```git
git checkout -- test.txt
```

现在，撤销修改就回到添加到暂存区后的状态，但暂存区的数据不会撤销。

用命令`git reset HEAD <file>`可以把暂存区的修改撤销掉（unstage），重新放回工作区：

```git
git reset HEAD test.txt
```

### 3.5 删除文件

删除工作区的文件

```git
rm -rf test.txt
```

将删除版本库的文件

方式1:

```git
rm -rf test.txt #删除工作区的文件

# 现在可以恢复删除的文件到工作区：git checkout -- test.txt

git add test.txt #相当于将删除指令放入暂存区

# 现在可以恢复删除的文件到暂存区：git reset HEAD test.txt

git commit ..... #提交版本库
```

```git
git rm -rf test.txt #相当于删除工作区的文件，并且执行了git add

# 现在可以恢复删除的文件到暂存区：git reset HEAD test.txt

git commit ..... #提交版本库
```

## 4. 远程仓库

创建SSH Key ：

```shell
ssh-keygen -t rsa -C "youremail@example.com"
```

可以在用户主目录里找到.ssh目录，里面有id_rsa和id_rsa.pub两个文件，这两个就是SSH Key的秘钥对，id_rsa是私钥，不能泄露出去，id_rsa.pub是公钥，可以放心地告诉任何人。

### 4.1 添加远程仓库

添加后，远程库的名字就是origin，这是Git默认的叫法

```git
git remote add origin git@github.com:your.git
```

由于远程库是空的，我们第一次推送master分支时，加上了-u参数，Git不但会把本地的master分支内容推送的远程新的master分支，还会把本地的master分支和远程的master分支关联起来，在以后的推送或者拉取时就可以简化命令。

```git
git push -u origin master
```

此后，每次本地提交后，只要有必要，就可以使用命令git push origin master推送最新修改；

`git remote -v` 查看远程库信息：

```git
git remote -v
```

`git remote rm <name>` 删除远程库：

```git
git remote rm origin
```

此处的“删除”其实是解除了本地和远程的绑定关系，并不是物理上删除了远程库。远程库本身并没有任何改动。要真正删除远程库，需要登录到GitHub，在后台页面找到删除按钮再删除。

### 4.2 远程克隆

git clone [远程仓库地址]

```git
git clone origin.git
```

## 5. 分支管理

### 5.1 创建与合并分支

在版本回退里，你已经知道，每次提交，Git都把它们串成一条时间线，这条时间线就是一个分支。截止到目前，只有一条时间线，在Git里，这个分支叫主分支，即master分支。HEAD严格来说不是指向提交，而是指向master，master才是指向提交的，所以，HEAD指向的就是当前分支。

一开始的时候，master分支是一条线，Git用master指向最新的提交，再用HEAD指向master，就能确定当前分支，以及当前分支的提交点；

每次提交，master分支都会向前移动一步，这样，随着你不断提交，master分支的线也越来越长。

当我们创建新的分支，例如dev时，Git新建了一个指针叫dev，指向master相同的提交，再把HEAD指向dev，就表示当前分支在dev上；

Git创建一个分支很快，因为除了增加一个dev指针，改改HEAD的指向，工作区的文件都没有任何变化！

不过，从现在开始，对工作区的修改和提交就是针对dev分支了，比如新提交一次后，dev指针往前移动一步，而master指针不变；

假如我们在dev上的工作完成了，就可以把dev合并到master上。Git怎么合并呢？最简单的方法，就是直接把master指向dev的当前提交，就完成了合并；

所以Git合并分支也很快！就改改指针，工作区内容也不变！

合并完分支后，甚至可以删除dev分支。删除dev分支就是把dev指针给删掉，删掉后，我们就剩下了一条master分支；

首先，我们创建dev分支，然后切换到dev分支：

```git
git checkout -b dev
```

git checkout命令加上-b参数表示创建并切换，相当于以下两条命令：

```git
git branch dev
git checkout dev
```

然后，用git branch命令查看当前分支：

```git
git branch
```

git branch命令会列出所有分支，当前分支前面会标一个*号。

在dev分支上我们修改test.txt文件：Hello World!!!qqqq

提交之后，再切换为master分支

```git
git checkout master
```

切换回master分支后，再查看一个test.txt文件，dev分支的修改内容不见了！因为那个提交是在dev分支上，而master分支此刻的提交点并没有变：

`git merge`*命令用于合并指定分支到当前分支*。现在，我们把dev分支的工作成果合并到master分支上：

```git
$ git merge dev
Updating 728a081..a28a0c4
Fast-forward
 test.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

注意到上面的`Fast-forward`信息，Git告诉我们，这次合并是“快进模式”，也就是直接把master指向dev的当前提交，所以合并速度非常快。

合并完成后，就可以放心地删除dev分支了：

```git
git branch -d dev
```

> 因为创建、合并和删除分支非常快，所以Git鼓励你使用分支完成某个任务，合并后再删掉分支，这和直接在master分支上工作效果是一样的，但过程更安全。

switch切换分支

创建并切换到新的dev分支，可以使用：

```git
git switch -c dev
```

直接切换到已有的master分支，可以使用：

```git
git switch master
```

### 5.2 解决冲突

准备新的feature1分支：

```git
git switch -c feature1
```

修改test.txt文件的内容并在feature1分支上提交：Hello World!!!feature1

切换到master分支：`git switch master`

修改test.txt文件的内容并在master分支上提交：Hello World!!!master

现在，master分支和feature1分支各自都分别有新的提交，这种情况下，Git无法执行“快速合并”，只能试图把各自的修改合并起来，但这种合并就可能会有冲突：

```git
$ git merge feature1
Auto-merging test.txt
CONFLICT (content): Merge conflict in test.txt
Automatic merge failed; fix conflicts and then commit the result.
```

Git告诉我们，test.txt文件存在冲突，必须手动解决冲突后再提交。git status也可以告诉我们冲突的文件：

```git
$ git status
On branch master
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   test.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

我们可以直接查看readme.txt的内容：

```txt
<<<<<<< HEAD
Hello World!!!master
=======
Hello World!!!feature1
>>>>>>> feature1
```

Git用<<<<<<<，=======，>>>>>>>标记出不同分支的内容，我们修改如下后保存：Hello World!!!master and feature1

再添加提交：

```git
git add test.txt
git commit -m "master and feature1"
```

用带参数的git log也可以看到分支的合并情况：

```git
$ git log --graph --pretty=oneline --abbrev-commit
*   3a2834f (HEAD -> master) master and feature1
|\
| * 63a8de3 (feature1) feature1
* | a0e7929 master
|/
* a28a0c4 four commit
* 728a081 commit 4
* eb2f88b three commit
* 6507263 second commit
* 5a14f64 first commit
```

合并成功，最后，删除feature1分支：`git branch -d feature1`

小结：

* 当Git无法自动合并分支时，就必须首先解决冲突。解决冲突后，再提交，合并完成。
* 解决冲突就是把Git合并失败的文件手动编辑为我们希望的内容，再提交。
* 用`git log --graph`命令可以看到分支合并图。

### 5.3 分支管理策略

通常，合并分支时，如果可能，Git会用Fast forward模式，但这种模式下，删除分支后，会丢掉分支信息。

如果要强制禁用Fast forward模式，Git就会在merge时生成一个新的commit，这样，从分支历史上就可以看出分支信息。

下面我们实战一下--no-ff方式的git merge：

这里的--no--ff 模式其实就是相当于master指针new了一个跟dev指针一样的空间并且放了相同的内容然后指向这个空间。而原来的快速模式，就是简单将master指针指向dev指针指向的内容而已，并没有自己创造空间。

首先，仍然创建并切换dev分支：`git switch -c dev`
修改readme.txt文件，并提交一个新的commit，test.txt：Hello World!!!dev111

切换回master：git switch master

准备合并dev分支，请注意--no-ff参数，表示禁用Fast forward：

```git
$ git merge --no-ff -m "merge dev with no-ff" dev
Merge made by the 'recursive' strategy.
 test.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

因为本次合并要创建一个新的commit，所以加上-m参数，把commit描述写进去。

合并后，我们用git log看看分支历史：

```git
$ git log --graph --pretty=oneline --abbrev-commit
*   6cc7985 (HEAD -> master) merge dev with no-ff
|\
| * f38baab (dev) dev
|/
*   3a2834f master and feature1
|\
| * 63a8de3 feature1
* | a0e7929 master
|/
* a28a0c4 four commit
* 728a081 commit 4
* eb2f88b three commit
* 6507263 second commit
* 5a14f64 first commit
```

分支策略
在实际开发中，我们应该按照几个基本原则进行分支管理：

首先，master分支应该是非常稳定的，也就是仅用来发布新版本，平时不能在上面干活；

那在哪干活呢？干活都在dev分支上，也就是说，dev分支是不稳定的，到某个时候，比如1.0版本发布时，再把dev分支合并到master上，在master分支发布1.0版本；

每个人都在dev分支上干活，每个人都有自己的分支，时不时地往dev分支上合并就可以了。

小结：
> 合并分支时，加上--no-ff参数就可以用普通模式合并，合并后的历史有分支，能看出来曾经做过合并，而fast forward合并就看不出来曾经做过合并。

### 5.4 Bug分支

每个bug都可以通过一个新的临时分支来修复，修复后，合并分支，然后将临时分支删除；

当你接到一个修复一个代号101的bug的任务时，当前正在dev上进行的工作还没有提交：

```git
$ git status
On branch dev
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   test.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

dev工作只进行到一半，还没法提交，但是，必须先修复这个bug；当前的dev分支的test.txt：Hello World!!! dev doing

Git还提供了一个stash功能，可以把当前工作现场“储藏”起来，等以后恢复现场后继续工作：

```git
git stash
```

现在，用git status查看工作区，就是干净的（除非有没有被Git管理的文件），因此可以放心地创建分支来修复bug。

```git
$ git status
On branch dev
nothing to commit, working tree clean
```

首先确定要在哪个分支上修复bug，假定需要在master分支上修复，就从master创建临时分支(bug-101)：

```git
git checkout master
git checkout -b bug-101

#修改test.txt：Hello World!!!  he bug has been fixed!!!

git add test.txt
git commit -m "fixed bug-101"
```

修复完成后，切换到master分支，并完成合并，最后删除bug-101分支：

```git
git switch master

git merge --no-ff -m "merged bug fix 101" bug-101
```

现在回到dev分支继续工作：

```git
git switch dev
```

`git stash list`查看工作现场

```git
$ git stash list
stash@{0}: WIP on dev: f38baab dev
```

工作现场还在，Git把stash内容存在某个地方了，但是需要恢复一下，有两个办法：

一是用git stash apply恢复，但是恢复后，stash内容并不删除，你需要用git stash drop来删除；

另一种方式是用git stash pop，恢复的同时把stash内容也删了：

```git
git stash pop
``

查看工作现场

```git
$ git stash list
stash@{0}: WIP on dev: 731abfd fixed bug-101
stash@{1}: WIP on dev: 731abfd fixed bug-101
```

恢复

```git
#默认栈顶
git stash apply

#栈顶
git stash apply stash@{0}
``
为了方便操作，Git专门提供了一个cherry-pick命令，让我们能复制一个特定的提交到当前分支：

```git
$ git cherry-pick 731abfd197
[master f54cc87] fixed bug-101
 Date: Wed Sep 28 17:02:43 2022 +0800
 1 file changed, 1 insertion(+), 1 deletion(-)
```

小结

* 修复bug时，我们会通过创建新的bug分支进行修复，然后合并，最后删除；
* 当手头工作没有完成时，先把工作现场git stash一下，然后去修复bug，修复后，再git stash pop，回到工作现场；
* 在master分支上修复的bug，想要合并到当前dev分支，可以用`git cherry-pick <commit>`命令，把bug提交的修改“复制”到当前分支，避免重复劳动。

### 5.5 Feature分支

删除一个已提交还未合并的分支。

首先创建一个分支，并提交修改

```git
git switch -c feature
# test.txt：Hello World!!!  feature  
git add test.txt  
git commit -m "feature"
```

切回dev，准备合并：`git switch dev`，现在突然要删除这个feature分支

```git
$ git branch -d feature
error: The branch 'feature' is not fully merged.
If you are sure you want to delete it, run 'git branch -D feature'.
```

销毁失败。Git友情提醒，feature-vulcan分支还没有被合并，如果删除，将丢失掉修改，如果要强行删除，需要使用大写的-D参数。。

现在我们强行删除：

```git
$ git branch -D feature
Deleted branch feature (was 246cd76).
```

小结：

* 开发一个新feature，最好新建一个分支；
* 如果要丢弃一个没有被合并过的分支，可以通过`git branch -D <name>`强行删除。

### 5.6 多人协作

当你从远程仓库克隆时，实际上Git自动把本地的master分支和远程的master分支对应起来了，并且，远程仓库的默认名称是origin。

要查看远程库的信息，用git remote：

```git
$ git remote
origin
```

或者，用git remote -v显示更详细的信息：

```git
$ git remote -v
origin  git@github.com:vstk771/notes.git (fetch)
origin  git@github.com:vstk771/notes.git (push)
```

*上面显示了可以抓取和推送的origin的地址。如果没有推送权限，就看不到push的地址。*

推送分支，就是把该分支上的所有本地提交推送到远程库。推送时，要指定本地分支，这样，Git就会把该分支推送到远程库对应的远程分支上：`git push origin master`

如果要推送其他分支，比如dev，就改成：`git push origin dev`

但是，并不是一定要把本地分支往远程推送，那么，哪些分支需要推送，哪些不需要呢？

* master分支是主分支，因此要时刻与远程同步；
* dev分支是开发分支，团队所有成员都需要在上面工作，所以也需要与远程同步；
* bug分支只用于在本地修复bug，就没必要推到远程了，除非老板要看看你每周到底修复了几个bug；
* feature分支是否推到远程，取决于你是否和你的小伙伴合作在上面开发。

*总之，就是在Git中，分支完全可以在本地自己藏着玩，是否推送，视你的心情而定！*

当你的小伙伴从远程库clone时，默认情况下，你的小伙伴只能看到本地的master分支。可以用git branch命令看看：

```git
$ git branch
* master
```

在dev分支上开发，就必须创建远程origin的dev分支到本地，即：远程仓库存在dev分支，用这个命令创建本地dev分支(可自由切换)：`git checkout -b dev origin/dev`

```git
git switch -c dev

$ git checkout -b dev origin/dev
Switched to a new branch 'dev'
Branch 'dev' set up to track remote branch 'dev' from 'origin'.

//在dev分支开发，修改test.txt：Hello  dev

git add test.txt
git commit -m "first commit dev"
git push origin dev
```

也可以在本地创建分支dev2,然后做一些工作再提交远程仓库：

```git
git switch -c dev2
git add dev2_test.txt
git commit -m "first commit dev2"

$ git push origin dev2
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 6 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 295 bytes | 295.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
remote:
remote: Create a pull request for 'dev2' on GitHub by visiting:
remote:      https://github.com/vstk771/gitTest/pull/new/dev2
remote:
To github.com:vstk771/gitTest.git
 * [new branch]      dev2 -> dev2
```

你的小伙伴已经向origin/dev分支推送了他的提交，而碰巧你也对同样的文件作了修改，并试图推送：

推送失败，因为你的小伙伴的最新提交和你试图推送的提交有冲突，解决办法也很简单，Git已经提示我们，先用git pull把最新的提交从origin/dev抓下来，然后，在本地合并，解决冲突，再推送：`git pull`

git pull也失败了，原因是没有指定本地dev分支与远程origin/dev分支的链接，根据提示，设置dev和origin/dev的链接：

```git
git branch --set-upstream-to=origin/dev dev
```

这回git pull成功，但是合并有冲突，需要手动解决，解决的方法和分支管理中的解决冲突完全一样。解决后，提交，再push：

```git
git commit -m "fix and merge"

git push origin dev
```

因此，多人协作的工作模式通常是这样：

1. 首先，可以试图用`git push origin <branch-name>`推送自己的修改；
2. 如果推送失败，则因为远程分支比你的本地更新，需要先用git pull试图合并；
3. 如果合并有冲突，则解决冲突，并在本地提交；
4. 没有冲突或者解决掉冲突后，再用`git push origin <branch-name>`推送就能成功！
5. 如果git pull提示no tracking information，则说明本地分支和远程分支的链接关系没有创建，用命令`git branch --set-upstream-to <branch-name> origin/<branch-name>`。

小结：

* 查看远程库信息，使用git remote -v；
* 本地新建的分支如果不推送到远程，对其他人就是不可见的；
* 从本地推送分支，使用git push origin branch-name，如果推送失败，先用git pull抓取远程的新提交；
* 在本地创建和远程分支对应的分支，使用git checkout -b branch-name origin/branch-name，本地和远程分支的名称最好一致；
* 建立本地分支和远程分支的关联，使用git branch --set-upstream branch-name origin/branch-name；
* 从远程抓取分支，使用git pull，如果有冲突，要先处理冲突。

### 5.7 Rebase

`git rebase` ：把分叉的提交历史“整理”成一条直线，看上去更直观

## 6. 标签管理

## 7. 自定义Git

* 忽略某些文件时，需要编写.gitignore；
* .gitignore文件本身要放到版本库里，并且可以对.gitignore做版本管理！

.gitignore文件：

```git
# 排除所有.开头的隐藏文件:
.*

# 排除所有.xlsx文件
*.xlsx

#排除xxx/这个文件夹
xxx/

# 不排除.gitignore
!.gitignore
```


---

> Author: cjt  
> URL: https://cui-jiang-tao.github.io/posts/git/  

