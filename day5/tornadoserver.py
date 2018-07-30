from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, parse_config_file, options


from day5.app.myapp import *


define('duankou', type=int, default=8888)
parse_config_file('../config/config')


app = MyApplication(hs=[('/', IndexHandler),
                        ('/login', LoginHandler),
                        ('/blog', BlogHandler),
                        ('/regist', RegistHandler),
                        ('/check', CheckHandler),
                        ('/imageperson', ImagePerHandler)],
                    tp='mytemplate',
                    sp='mystatics', \
                    um={'loginmodule': LoginModule, 'blogmodule': BlogModule, 'registmodule': RegistModule})
server = HTTPServer(app)
server.listen(options.duankou)
IOLoop.current().start()
