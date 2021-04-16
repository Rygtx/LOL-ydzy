[Forked from zzzzzzhang/LOL-ydzy](https://github.com/zzzzzzhang/LOL-ydzy "复刻自zzzzzzhang/LOL-ydzy")

# 云顶之弈助手
---
基于遗传算法,根据现有英雄自动推荐比较好的阵容

由于我也玩得比较少，各个种族羁绊不大了解,所以权重默认当一样的


出现新的羁绊的话,需要在程序里修改（目前适应云顶S5版本）

---
首先需要下载data文件夹到程序目录下（版本更新新英雄需要更新文件，提供了爬虫程序，也可以自己修改文件中内容）

如果是ide用户,在最后main()函数里改变参数就可以

同时为了不熟悉python的小伙伴做了一个cmd版本，输入你想要确定使用的英雄,用空格隔开

遗传参数可以在 YD-GA_cmd.py 里改

最后别忘记安装依赖  ``pip install pandas``

---
大概5s之内运行完,不会耽误游戏时间
---
### 2019/9/29 适配9.19版本
增加铲子凑羁绊功能

### 2019/10/21 适配9.20版本

### 2021/04/16 适配云顶S5版本

优化结果如下(S5)
cmd：
![ori](https://raw.githubusercontent.com/rygtx/LOL-ydzy/master/figure/figure_cmd_s5.png)
ide（jupyter notebook）：
![ori](https://raw.githubusercontent.com/zzzzzzhang/LOL-ydzy/master/figure/figure_ide.png)
