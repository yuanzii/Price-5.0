# Price-5.0

-改变方案 ---> 计算开销/成本比
-vue client port ---> 8050
-server api port ---> 2050
-use new database ---> price_5

-自定义前端端口
 -所在目录：node_modules\@vue\cli-service\lib\commands
 -需要修改的文件：serve.js

-配置全局访问接口API地址 
 -api variable ("http://ip:port")
 -所在目录：src\interface\index.js
 -全局 ---> main.js
 -引用 无需import ---> this.$api

-更改数据库
 -backend\server\db\psql_psycopg2.py
 -backend\server\db\psql_sqlalchemy.py
 
-同一服务器内的 PostgreSQL 复制数据库

 -CREATE DATABASE dvdrental_test WITH TEMPLATE dvdrental;
 根据源数据库的大小，完成复制可能需要一段时间。

 如果dvdrental数据库有活动连接，您将收到以下错误：
 -ERROR:  source database "dvdrental" is being accessed by other users
  DETAIL:  There is 1 other session using the database.

 以下查询返回活动连接：
 -SELECT pid, usename, client_addr FROM pg_stat_activity WHERE datname ='dvdrental';
 
 要终止与dvdrental数据库的活动连接，请使用以下查询：
 -SELECT pg_terminate_backend (pid) FROM pg_stat_activity WHERE datname = 'dvdrental';

 之后，再次执行第一个语句将 dvdrental 数据库复制到 dvdrental_test 数据库。

