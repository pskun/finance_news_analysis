# 项目结构
.  
├── algorithm(算法模型框架)  
├── analyze(具体策略)   
├── crawler(scrapy爬虫)  
│   └── crawler  
│       └── spiders(爬虫具体抓取代码)  
├── database(数据库操作)  
├── preprocess(数据预处理)  
│   └── pre_data(预处理存放目录)  
├── strategy(回测接口)  
├── tonglian(通联数据获取接口)  
├── utils(通用处理类)  
└── data(存放数据的目录)

# Python库依赖
中文分词: [jieba](https://github.com/fxsjy/jieba)  
爬虫: [scrapy](http://scrapy.org/)  
Mysql连接: [MySQLdb](http://mysql-python.sourceforge.net/MySQLdb.html)  
ORM工具: [sqlalchemy](http://www.sqlalchemy.org/)  
AC自动机: [esmre](https://github.com/wharris/esmre)  
布隆过滤器: [pybloom](https://github.com/jaybaird/python-bloomfilter)  
机器学习: [scikit-learn](http://scikit-learn.org/)  
文本主题模型: [gensim](https://github.com/piskvorky/gensim)  
快速生成Python扩展模块: [Cython](http://cython.org/)

# 注意事项
1. 修改PYTHONPATH  
把项目所在目录添加到PYTHONPATH中。  
建议方法：  
通过PYTHONPATH 中的任何 .pth 文件来添加pythonpath。  
比如添加/home/aa这个路径到pythonpath里，可以这样做：  
    1、新建一个文件，名字随便，但后缀名须是.pth，比如aa.pth；  
	2、文件内容直接输入"/home/aa"(没有引号)，如果有多个路径可以多行输入，但每行保证只有一个路径；  
	3、然后文件保存到sys.path列表中的任一文件夹下，一般来说我们保存到/usr/local/lib/python*/dist-packages，需要特别指出的是在不同版本中dist-packages可能被改成site-packages，最后重启python就可以了。  