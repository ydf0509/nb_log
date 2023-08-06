
import nb_log
import tornado.ioloop
import tornado.web

nb_log.get_logger(None)

# nb_log.get_logger('tornado')
#
# access_log = nb_log.get_logger("tornado.access")
# print(access_log)
# app_log = nb_log.get_logger("tornado.application")
# gen_log = nb_log.get_logger("tornado.general")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print('hw')
        self.write("Hello world")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
        ]
        tornado.web.Application.__init__(self, handlers)

if __name__=="__main__":
    app = Application()
    app.listen(8001)
    print("Tornado Started in port 8001，http://127.0.0.1:8000")
    tornado.ioloop.IOLoop.current().start()