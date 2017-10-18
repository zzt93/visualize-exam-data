# 使用Anaconda安装mysql驱动 

1. 列出anaconda里的环境：

   > conda info --envs

2. 根据刚刚列出来的环境，激活使用的python版本

   > activate py36

3. 安装驱动

   > conda install mysql-connector-python

# 使用Anaconda安装peewee

1. 列出anaconda里的环境：

      > conda info --envs

2. 根据刚刚列出来的环境，激活使用的python版本

      > activate py36

3. 安装驱动

      > pip install peewee

# 材料来源
[peewee官方文档](http://peewee.readthedocs.io/en/latest/index.html) 

# 发现程序运行报错了
1. 新建一个MySQL数据库，表名为"visualize_exam", 字符集为"utf8mb4"
2. 打开database.model.py，运行该文件的create_tables()函数

   ​