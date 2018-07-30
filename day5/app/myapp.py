import time

from os import remove
from tornado.web import Application, RequestHandler, UIModule

from day5.util.dbutil import DBUtil
from day5.util.mysession import Session
from day5.util.myutil import mymd5


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        # 设置cookie
        # self.set_cookie('islogin', 'true')

        # 获取cookie
        # self.get_cookie('cookie')
        r = ''
        msg = self.get_query_argument('tishi', None)
        print(msg)
        if msg:
            r = '用户名或密码错误'
        s = Session(self)
        if s['islogin']:
            self.redirect('/blog')
        else:
            self.render('login.html', result=r)


class LoginHandler(RequestHandler):
    def post(self, *args, **kwargs):
        username = self.get_body_argument('username', None)
        password = self.get_body_argument('password', None)
        avatar = self.get_body_argument('avatar', None)

        pwd = mymd5(password)
        print('niao')
        dbutil = self.application.dbutil
        result = dbutil.isloginsuccess(username, pwd)
        if result:
            #  self.write('登录成功')
            s =Session(self)
            s['islogin'] = True
            self.redirect('/blog?username=' + username)
            print(self.request.files)
            if self.request.files:
                avs = self.request.files['avatar']
                for a in avs:
                    body = a['body']
                    # 上传的这一个个文件内容
                    # 保存到服务器的硬盘中
                    filename = a['filename']
                    writer = open('upload/{}'.format(filename), 'wb')
                    writer.write(body)
                    writer.close()
        else:
            #  self.write('用户名或密码错误')
            self.redirect('/?tishi=' + '用户名或密码错误')

            # result = '用户名或密码错误'
            # self.render('login.html')


class BlogHandler(RequestHandler):
    def set_default_headers(self):
        # 让继承者自定义相应头中的内容
        print('set_default_handlers方法被调用')

    def initialize(self):
        # 让继承者在执行get/post方法之前传入参数
        # 或者执行一些初始化操作
        print('initialize被调用')

    def on_finish(self):
        # 执行get/post方法执行完成后，释放资源
        print('on_finish被调用')

    def get(self, *args, **kwargs):
        print('get被调用')
        # 以json 字符串作为响应内容
        # {'key':value}
        # resp = {'key1': 'value1', 'key2': 'value2'}
        # # self.write(resp)
        # self.set_header('Content-Type', 'application/json;charset=UTF-8')
        # jsonstr = json.dumps(resp)  # 将字典转换成字符串
        # self.write(jsonstr)
        # blogs=[]
        # blogs.append({"author": '张三峰',
        #               "title": '太极',
        #               "content": "思量波前进",
        #               'tags': '一打四',
        #               'count': 4})
        # blogs.append({"author": '小思',
        #               "title": '世界杯',
        #               "content": "c罗输了",
        #               'tags': 'c罗',
        #               'count': 10000})
        # blogs.append({"author": '小思',
        #               "title": '世界杯',
        #               "content": "梅西输了",
        #               'tags': '梅西',
        #               'count': 60000})
        # dbutil = self.application.dbutil
        # b = dbutil.getblogs()
        c = self.get_cookie('cookie')
        s = Session(self)
        if s['islogin']:
            self.render('blog.html')
        else:
            self.redirect('/')

    def post(self, *args, **kwargs):
        pass

    def myfunc(self, a, b):
        return a + b


class LoginModule(UIModule):
    def render(self, *args, **kwargs):
        print(self.request)
        print(self.request.uri)  # 路径加参数
        print(self.request.path)  # uri路径
        print(self.request.query)  # 参数
        r = ''
        if self.request.query:
            r = '用户名密码错误'
        return self.render_string('mymodule/login_module.html', result=r)


class BlogModule(UIModule):
    def render(self, *args, **kwargs):
        dbutil = self.handler.application.dbutil
        b = dbutil.getblogs()
        return self.render_string('mymodule/blog_module.html', blogs=b)


class RegistHandler(RequestHandler):
    def get(self, *args, **kwargs):
        return self.render('register.html')

    def post(self, *args, **kwargs):
        username = self.get_body_argument('username', None)
        password = self.get_body_argument('password', None)

        # 将原始的possword 利用摘要算法（md）进行格式转化

        pwd = mymd5(password)
        img = self.get_body_argument('img', None)
        city = self.get_body_argument('city', None)
        if username and password and city:
            img = None
            if self.request.files:
                f = self.request.files['img'][0]
                body = f['body']
                filename = f['filename']
                flname = str(time.time()) + filename
                writer = open('mystatics/upload/{}'.format(flname), 'wb')
                writer.write(body)
                writer.close()
                img = flname
            dbutil = self.application.dbutil
            try:
                dbutil.saveuser(username, pwd, img, city)
            except Exception as e:
                if img:
                    remove('mystatics/upload/{}'.format(img))
                err = str(e)
                self.redirect('/regist?msg=' + err)

            else:
                self.redirect('/')
        else:
            self.redirect('/regist?msg=empty')


class RegistModule(UIModule):
    def render(self, *args, **kwargs):

        r = ''
        if self.request.query:
            err = self.request.query.split('=')[1]
            if err == 'empty':
                r = '请输入完整'
            if err == 'duplicate':
                r = '用户名重复'
            if err == 'dberror':
                r = '数据库错误'
        return self.render_string('mymodule/reigst_module.html', result=r)


class CheckHandler(RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        username = self.get_body_argument('username', None)
        # 将username取数据库查询
        print(username)
        # 根据查询生成响应内容
        if self.application.dbutil.isexists(username):
            re = {'msg': 'fail'}
            self.write(re)
        else:
            re = {'msg': 'ok'}
            self.write(re)


class ImagePerHandler(RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        username = self.get_body_argument('username', None)
        print(username)
        img = self.application.dbutil.getpresonImage(username)
        re = {'img': img}
        self.write(re)



class MyApplication(Application):
    def __init__(self, hs, tp, sp, um):
        super().__init__(handlers=hs, template_path=tp, static_path=sp, ui_modules=um)
        self.dbutil = DBUtil()
