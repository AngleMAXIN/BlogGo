# Blog Go 项目 #

----------
## 第一次提交 ##

- 添加了config.py以及manage.py
- 完成了数据模型的编写以及数据迁移
- 完成了静态文件以及前端首页模板的部分工作
-                       时间：2018/3/25 22:07

----------

## 第二次提交 ##

- 添加了首页的附加功能，完善了首页旁边的列表。及作者风云榜，热门文章，标签等
- 在数据模型中添加了tag标签
-                       时间：2018/3/29 17:17

----------
## 第三次提交 ##

- 完善了主页及其详情页右边菜单的功能，把他们添加了进了全局变量中（第一次，贼他妈难）
- 完善了关于我的详情页
-						时间 : 2018/4/2/ 23:09
						
----------
## 第四次提交 ##

- 增加了注册、登录功能，登录里还有一些bug，时间太晚，明天解决
- 重构了数据库
-                       时间 ： 2018/4/3 22:36

----------
## 第五次提交 ##
- 对用户注册时的信息进行合法性检测，添加了专门的模块
- 完善了上一次留下的bug
-                      时间 ： 2018/4/4 23:08
                      
---------
## 第六次提交 ##
- 对用户注册时的密码进行了加密处理
- 对登录、注册、发表文章的页面代码进行了改进
- 测试了发表文章的功能，正常
-                     时间 ： 2018/4/6 11:03
                    
----------
## 第七次提交 ##
- 添加了全文搜索的功能
-                      时间： 2018/4/9 21:44
	
----------
## 第八次提交 ##
- 对项目结构进行了大调整，使用了蓝图
    	
		#app/main/__init__.py
		
    	from flask import Blueprint
    	main = Blueprint('main', __name__,template_folder='templates')
    	from . import views

		---------------------

		#app/__init__.py
		
		from flask import Flask
		from flask_sqlalchemy import SQLAlchemy
		from config import config
		import pymysql
		
		pymysql.install_as_MySQLdb()
		
		db = SQLAlchemy()
		
		def create_app(config_name):
	    app = Flask(__name__)
	    app.config.from_object(config[config_name])
	    config[config_name].init_app(app)
	    db.init_app(app)
	
	    from .main import main as main_bluprint
	    app.register_blueprint(main_bluprint)
	
	    return app