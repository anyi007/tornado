from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, parse_config_file, options
from tornado.web import Application, RequestHandler


define('duankou', type=int, default=8888)
parse_config_file('../config/config')


class PythonHandler(RequestHandler):
    def get(self, *arg, **kwargs):
        self.write('Hello Python')
        # 获取用户的请求参数
        d = self.get_query_argument('day', None)
        s = self.get_argument('subject', None)
        ds = self.get_query_arguments('day')
        ss = self.get_query_arguments('subject')
        print(d, s)
        print(ds, ss)

    def post(self, *arg, **kwargs):
        self.write('nihao ')
        d = self.get_body_argument('day', None)
        s = self.get_body_argument('subject', None)
        ds = self.get_body_arguments('day')
        ss = self.get_body_arguments('subject')
        print(d, s)
        print(ds, ss)
        arg_d = self.get_argument('day', None)  # =get_body_argument+get_query_argument
        arg_ds = self.get_arguments('day')
        print(arg_d, arg_ds)


class IndexHandler(RequestHandler):
    def get(self, *arg, **kwargs):
        self.write('<a href=/java> try try java<a><br>')
        self.write('<a href=/python> try try python<a>')

    def post(self, *arg, **kwargs):
        pass


class JavaHandler(RequestHandler):
    def get(self, p1=None, p2=None, *arg, **kwargs):
        self.write('Hello Java<br>')
        if p1:
            self.write('今天是' + p1+'<br>')
        if p2:
            self.write('学习的课程是' + p2)

    def post(self, *arg, **kwargs):
        pass


app = Application(handlers=[('/', IndexHandler),
                            ('/java', JavaHandler),
                            ('/java/(day[0-9]+)', JavaHandler),
                            ('/java/(day[0-9]+)/([a-z0-9]+)', JavaHandler),
                            ('/python', PythonHandler)])
server = HTTPServer(app)
server.listen(options.duankou)
IOLoop.current().start()
