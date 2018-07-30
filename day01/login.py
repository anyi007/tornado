from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, parse_config_file,options
from tornado.web import Application, RequestHandler

define('duankou', type=int, default=8888)
parse_config_file('../config/config')


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        html = ''
        tishi = self.get_query_argument('tishi', None)
        if tishi:
            html = tishi

        html += "<form action=/login method=post enctype=multipart/form-data>" \
             "<span>用户名：</span><input type=text name=username><br>" \
             "<span>密&nbsp;&nbsp;&nbsp;&nbsp;码：</span><input type=password name=password><br>" \
            "<span>文件：</span><input type=file  name=avatar ><br>" \
            "<span>文件：</span><input type=file  name=avatar><br>" \
            "<input type=submit value=登录><input type=reset value=重置>" \
             "</form>"
        self.write(html)


class LoginHandler(RequestHandler):
    def post(self, *args, **kwargs):
        username = self.get_body_argument('username', None)
        password = self.get_body_argument('password', None)
        avatar = self.get_body_argument('avatar', None)
        if username == 'abc' and password == '123':
            #  self.write('登录成功')
            self.redirect('/blog?username='+username)
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

            self.redirect('/?tishi='+'用户名或密码错误')


class BlogHandler(RequestHandler):
    def set_default_headers(self):
        print('set_default_handlers方法被调用')

    def initialize(self):
        print('initialize被调用')

    def on_finish(self):
        print('on_finish被调用')

    def get(self, *args, **kwargs):
        print('get被调用')
        username = self.get_query_argument('username', None)
        html = "<form action=/login method=post>" \
               "<h1><span>欢迎"+username+"来到博客首页：</span></h1> "\
               "</form>"
        self.write(html)

    def post(self, *args, **kwargs):
        pass


app = Application(handlers=[('/', IndexHandler),
                            ('/login', LoginHandler),
                            ('/blog', BlogHandler)])
server = HTTPServer(app)
server.listen(options.duankou)
IOLoop.current().start()
