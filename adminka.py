import tornado
import tornado.web
import tornado.httpserver

import main as m

class MainAdmin(m.MainHandler):
  @tornado.gen.coroutine
  def get(self):
    self.render('templates/main_adm.html', temp=self.temp)