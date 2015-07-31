###pytoolBox

#### 语法结构
- command = macro + pipe expr + io indirect
- expr = variable | data | function call | partial function | block
- data = str | list | dict
- block = python expression | command
- function = python buildin function | udf function | mapped function | composite function

命令(command)是支持io重定向和宏
表达式可以是一个变量，数据(比如list)，函数调用，构造偏函数，或者block
数据支持：字符串，表，字典
函数包含：python内置函数，用户自定义函数，复合函数，mapped函数(= map(func,..) )


####文件模块说明
- shell 包含整个语法解释器
- util 常用的功能组件
- iotool 与stdout和io有关的函数
- oscmd 操作系统有关的一些函数；一部分unix命令
- pytool 复杂的命令；一般一个命令可以独自完成一个工作
- funcManager 管理除xshell以外的功能函数模块
- pipe 和util类似；来自pipe库: https://github.com/JulienPalard/Pipe


