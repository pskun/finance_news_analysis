# 注意事项
1. 修改PYTHONPATH

把项目所在目录添加到PYTHONPATH中。
方法：
通过PYTHONPATH 中的任何 .pth 文件来添加pythonpath。
比如我想添加/home/aa这个路径到pythonpath里，可以这样做：
	1、新建一个文件，名字随便，但后缀名须是.pth，比如aa.pth；

	2、内容直接输入“/home/aa”(没有引号)，如果有多个路径可以多行输入，但每行保 证只有一个路径；

	3、然后文件保存到sys.path列表中的任一文件夹下，一般来说我们保存到/usr/local/lib/python*/dist- packages，需要特别指出的是在不同版本中dist-packages可能被改成site-packages，反正sys.path里显示的是什么 就照着这个来；最后重启python就可以了。