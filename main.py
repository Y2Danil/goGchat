import tornado.ioloop
import tornado.web
import tornado
import tornado.httpserver

import json
import re
import os

import owm
from poSQL import *

po = poSQL()
we = owm.Weather()

class MainHandler(tornado.web.RequestHandler):
  po = poSQL()
  # int_temp = we.temp_in_PK()
  # str_temp = str(we.temp_in_PK())
  temp = we.temp_in_PK()
    
  def get(self):
    if self.current_user:
      self.current_user = self.current_user
    else:
      self.current_user = None
  
  def get_current_user(self):
    return self.get_secure_cookie("user")
    
class Chat(MainHandler):
  def get(self):
    rubrics = po.select_rubrics()
    self.render('templates/chat.html', temp=self.temp, rubrics=rubrics)
    
class Rubric(Chat):
  def get(self):
    if self.get_argument("rubric_name", ''):
      rubric_name = self.get_argument("rubric_name", '')
      rubric = po.select_rubric_only_title(rubric_name)[0]
      rubric_id = rubric[0]
      rubric = po.select_rubric_only_title(rubric_name)[0]
    elif self.get_argument("rubric_input", ''):
      rubric_name = self.get_argument("rubric_input", '')
      rubric = po.select_rubric_only_title(rubric_name)[0]
      rubric_id = rubric[0]
      rubric = po.select_rubric_only_title(rubric_name)[0]
    else:
      url = str(self.request.path)
      print(url)
      rubric_id = re.search(r"rubric-[0-9]*", str(url), flags=0)
      rubric_id = re.search(r"c-[0-9]*", str(rubric_id))
      rubric_id = rubric_id.group(0)[2:]
      rubric = po.select_rubric_only_id(rubric_id)[0]
    messages = po.select_rubric_messages(rubric_id)
    for m in messages:
      index = messages.index(m)
      m = list(m)
      user = po.select_user_po_id(int(m[2]))[0]
      user_name = user[1]
      m.append(user)
      messages[index] = m
    self.render('templates/rubric.html', messages=messages, rubric=rubric, rubric_id=rubric_id, temp=self.temp)
    
class AddMessage(Rubric):
  @tornado.gen.coroutine
  def post(self):
    if self.current_user:
      self.current_user = self.current_user.decode()
      rubric_name = self.get_argument("rubric_name", '')
      rubric = po.select_rubric_only_title(rubric_name)
      rubric = rubric[0]
      rubric_id = rubric[0]
      message_text = self.get_argument("message_textarea", '')
      user = po.select_user_po_name(self.current_user)
      user = user[0]
      po.add_message(message_text, rubric_id, user[0])
      self.redirect(f'/rubric-{rubric_id}')
    else:
      self.redirect('/')
      
class UserAcc(MainHandler):
  def get(self):
    url = self.request.path
    print(url)
    redic = url[9:]
    print(redic)
    user = po.select_user_po_name(self.current_user.decode())[0]
    if user[-1] in [True, 1, 'true', 'True'] or user[3] in [True, 1, 'true', 'True']:
      user_info = po.select_user_po_name(redic)[0]
      print(user_info)
      self.render('templates/moder_user.html', temp=self.temp, user_info=user_info)
    else:
      self.render('/')
      
class AddOP(MainHandler):
  @tornado.gen.coroutine
  def post(self):
    redic = self.get_argument('url_in_user', '')
    if self.current_user:
      user = po.select_user_po_name(self.current_user.decode())[0]
      if user[-1] in [True, 1, 'true', 'True'] or user[3] in [True, 1, 'true', 'True']:
        userName = self.get_argument('addOP_username', '')
        op = self.get_argument('OP', '')
        po.add_op(userName, int(op))
    self.redirect(redic)
    
class ImportRegister(MainHandler):
  def get(self):
    self.render('templates/register.html', temp=self.temp)
    
class Register(MainHandler):
  def post(self):
    username = self.get_argument("username", '')
    password1 = self.get_argument("password1", '')
    password2 = self.get_argument("password2", '')
    if password1 == password2:
      po.add_user(username, password1)
      self.redirect('/log')
    else:
      self.write('<strong>Error(((</strong>')
    
class ImportLogin(MainHandler):
  def get(self):
    self.render('templates/login.html', temp=self.temp)
    
class Login(MainHandler):  
  @tornado.gen.coroutine
  def post(self):
    username = self.get_argument("username", '')
    password = self.get_argument("password", '')
    users = po.select_users()
    if po.check_user(username, password):
      print(po.check_user_only_name(username))
      self.set_secure_cookie("user",  self.get_argument("username"), expires_days=3)
        
    self.current_user = self.current_user
    self.redirect("/")
    
  get = post
  
class Logout(MainHandler):
  def get(self):
    self.clear_cookie("user")
    self.redirect("/")
    
    
class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
    (r"/", Chat),
    (r"/rubric-\d*", Rubric),
    (r'/add-message-in-rubric-\d*\w*\s*', AddMessage),
    (r"/userAcc-.\d*\w*\s*", UserAcc),
    (r'/addOP\d*\w*\s*', AddOP),
    (r"/reg", ImportRegister),
    (r"/register", Register),
    (r"/log", ImportLogin),
    (r"/login", Login),
    (r"/logout", Logout),
    ]
    settings = dict(
      cookie_secret="2332ddyffdy89sd69ds6666y6668",
      static_path = os.path.join(os.path.dirname(__file__), "static"),
      templates_path = os.path.join(os.path.dirname(__file__), "templates"),
      #xsrf_cookies=True,
    )
    super(Application, self).__init__(handlers, **settings)
  
    
"""def make_app():
  return tornado.web.Application([
    (r"/", Chat),
    (r"/reg", ImportRegister),
    (r"/register", Register),
    (r"/log", ImportLogin),
    (r"/login", Login),
    (r"/logout", Logout),
  ], cookie_secret="2332ddyffdy89sd69ds6666y6668")"""

if __name__ == "__main__":
  app = Application()
  port = int(os.environ.get("PORT", 5000))
  app.listen(port)
  #app.listen(8080)
  #fff
  tornado.ioloop.IOLoop.current().start()