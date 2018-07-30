import pymysql


class DBUtil:
    def __init__(self, **kwargs):
        # 获取数据里连接参数
        # 建立与数据库的连接
        host = kwargs.get('host', '127.0.0.1')
        port = kwargs.get('port', 3306)
        user = kwargs.get('user', 'root')
        password = kwargs.get('password', '123456')
        database = kwargs.get('database', 'blog_db')
        charset = kwargs.get('charset', 'utf8')
        print('123')
        connection = pymysql.connect(user=user,
                                     password=password,
                                     host=host,
                                     port=port,
                                     database=database,
                                     charset=charset,
                                     )
        if connection:
            self.cursor = connection.cursor()
            print('连接陈宫个')
        else:
            print('连接失败')
            raise Exception('数据库连接参数有误！')

    def isloginsuccess(self, username, password):
        # 根据输入的用户名和密码
        # 判定用户登录是否成功
        sql = "select  count(*) from td_user where user_name = %s and user_password = %s "
        params = (username, password)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchone()
        if result[0]:
            return True
        else:
            return False

    def saveuser(self, username, pwd, img, city):
        # 根据用户输入的信息完成用户注册
        sql = "insert into td_user(user_name, user_password, user_avatar, user_city)values (%s,%s,%s,%s)"
        params = (username, pwd, img, city)
        print('我来了')
        try:

            print(sql,params)
            self.cursor.execute(sql, params)
            self.cursor.connection.commit()
        except Exception as e:
            err = str(e)
            r = 'dberror'
            code = err.split(',')[0].split('(')[1]
            if code == '1062':
                r = 'duplicate'
            raise Exception(r)

    def getblogs(self):
        # 取出数据路中与博客相关的内容，
        sql = ''' select user_name,user_avatar,blog_title,blog_content,tc,c
from (
        select comment_blog_id,count(*)c 
        from td_comment
        group by comment_blog_id
     )t3
right join (    
       select user_name,user_avatar,blog_id,blog_title,blog_content,tc
from td_user
join (
     select blog_id,blog_title,blog_content,tc,blog_user_id
     from td_blog
     left join (
       select rel_blog_id, group_concat(tag_content)tc
       from td_tag
       join (
           select rel_blog_id,rel_tag_id
           from td_blog_tag
          )t
       on tag_id = rel_tag_id
       group by rel_blog_id
         )t1
     on blog_id = rel_blog_id

     )t2
on user_id = blog_user_id
     )t4
on comment_blog_id = blog_id '''
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        blogs=[]
        for b in result:
            blog={}
            blog['author'] = b[0]
            blog['title'] = b[2]
            blog['content'] = b[3]
            blog['img'] = b[1]
            blog['tags'] = b[4]
            blog['count'] = b[5]

            blogs.append(blog)
        return blogs

    def isexists(self, username):
        sql = 'select  count(*) from td_user where user_name = %s'
        params = (username,)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchone()
        if result[0]:
            return True
        else:
            return False

    def getpresonImage(self,username):
        sql = 'select  user_avatar from td_user where user_name=%s '
        params = (username,)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchone()
        print('result',result)
        if result:
            if result[0]:
                return result[0]
            else:
                return ''
        else:
            return ''