import tornado.ioloop
import tornado.web
import tornado
import tornado.httpserver

import re
import os
from poSQL import *

s = SQLiter()

class MainHandler(tornado.web.RequestHandler):
  s = SQLiter()
  def get(self):
    if self.current_user:
      self.current_user = self.current_user
    else:
      self.current_user = None
  
  def get_current_user(self):
    return self.get_secure_cookie("user")
    
class Chat(MainHandler):
  def get(self):
    messages = s.select_messages()
    for m in messages:
      index = messages.index(m)
      m = list(m)
      user_name = s.select_user_po_id(int(m[1]))[0][0]
      m.append(user_name)
      messages[index] = m
    self.render('templates/chat.html', messages=messages)
    
class ImportRegister(MainHandler):
  def get(self):
    self.render('templates/register.html')
    
class Register(MainHandler):
  def post(self):
    username = self.get_argument("username", '')
    password1 = self.get_argument("password1", '')
    password2 = self.get_argument("password2", '')
    if password1 == password2:
      s.add_user(username, password1)
      self.redirect('/log')
    else:
      self.write('<strong>Error(((</strong>')
    
class ImportLogin(MainHandler):
  def get(self):
    self.render('templates/login.html')
    
class Login(MainHandler):  
  @tornado.gen.coroutine
  def post(self):
    username = self.get_argument("username", '')
    password = self.get_argument("password", '')
    print(username, password)
    users = s.select_users()
    print(users)
    if s.check_user(username, password):
      print(s.check_user_only_name(username))
      self.set_secure_cookie("user",  self.get_argument("username"), expires_days=2)
        
    self.current_user = self.current_user
    self.redirect("/")
    
  get = post
  
class Logout(MainHandler):
  def get(self):
    self.clear_cookie("user")
    self.redirect("/")
    
def make_app():
  return tornado.web.Application([
    (r"/", Chat),
    (r"/reg", ImportRegister),
    (r"/register", Register),
    (r"/log", ImportLogin),
    (r"/login", Login),
    (r"/logout", Logout),
  ], cookie_secret="2332ddyffdy89sd69ds6666y6668")

if __name__ == "__main__":
  app = make_app()
  port = int(os.environ.get("PORT", 5000))
  app.listen(port)
  tornado.ioloop.IOLoop.current().start()