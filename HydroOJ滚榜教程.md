本教程基于Windows11，Resovler版本v2.6.1206
# 下载ICPC Resolver

[link](https://tools.icpc.global/resolver/)
推荐在Windows上使用，在linux上尝试没有成功，本人没有macOS设备也没有尝试...

# 解决中文乱码问题

[解决中文乱码](https://blog.csdn.net/xzx18822942899/article/details/128275137)

# 导出Ghost文件

在HydroOJ的“比赛成绩表”页面，选择“导出为Ghost”
# 使用脚本转为xml文件

使用仓库中的 `ghost_to_xml.py` 脚本将ghost文件转为xml文件，格式参考：

```
 python .\ghost_to_xml.py .\input.ghost '2025-05-24 13:30:00' output.xml
```

这里的时间为比赛开始的时间。

# 修改xml文件

xml文件示例如下：

```
<contest>
<info>
  <length>4:00:00</length>
  <penalty>20</penalty>
  <started>False</started>
  <starttime>1747544400.0</starttime>
  <title>中国科学院大学本科部第四届程序设计大赛（提高组）</title>
  <short-title>中国科学院大学本科部第四届程序设计大赛（提高组）</short-title>
  <scoreboard-freeze-length>1:00:00</scoreboard-freeze-length>
  <contest-id>default--3</contest-id>
</info>
```

1. 一般来说封榜时间需要修改，在 `scoreboard-freeze-length` 块内修改
2. 如要对参赛选手进行修改，需要在 `team` 块中修改：
	- 删除选手则直接把team块删除
	- 修改选手名字则在team块中修改
# 使用脚本生成ndjson文件

打开resolver工具包中的 `awards.bat` ，生成 `event.ndjson` 文件

在此过程中，若需要修改金银铜奖人数，使用 `Medal...` ；若需要配置首A奖，使用 `First to solve...`

最后使用 Save event feed` 导出为ndjson文件。

![[屏幕截图 2025-06-06 081544.png]]
# 运行滚榜

使用 `resolver.bat` 启动滚榜，格式参考：

```
.\resolver.bat .\event.ndjson --singleStep 30
```
上面命令指运行单步滚榜，从前30名开始（如果人数不够30就是全部滚榜），直接点击空格就可以进行单步滚榜。

还有一些其他命令可以进行自动滚榜等，具体可以查阅文档或者其他博客。

