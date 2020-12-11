import tornado.ioloop
import tornado.web
import tornado
import tornado.httpserver
import yaml

import os
import re
import typing

import owm
from poSQL import *
import adminka as adm
#from hesirka import Heshirka
#from dop_data import Data

he = Heshirka()
po = poSQL()
we = owm.Weather()
#dd = Data()

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
  async def get(self):
    if self.current_user:
      user = self.current_user.decode()
      user_info = po.select_user_po_name(user)[0]
      print(user_info)
      rubrics = po.select_rubrics_plus_op_rubric(user_info[4])[::-1]
      fixing_rubrics = po.select_fixing_rubrics(user_info[4])[::-1]
    else:
      rubrics = po.select_rubrics_plus_op_rubric(0)[::-1]
      fixing_rubrics = po.select_fixing_rubrics(0)[::-1]
    self.render('templates/chat.html', temp=self.temp, rubrics=rubrics, fixing_rubrics=fixing_rubrics)
    
class Rubric(Chat):
  async def get(self):
    url = str(self.request.path)
    rubric_id = re.search(r"rubric-[0-9]*", str(url), flags=0)
    rubric_id = re.search(r"c-[0-9]*", str(rubric_id))
    rubric_id = rubric_id.group(0)[2:]
    rubric = po.select_rubric_only_id(rubric_id)[0]
    if rubric[4] != -10:
      if self.current_user:
        user_info = po.select_user_po_name(self.current_user.decode())[0]
        if rubric[4] <= user_info[4]:
          messages = po.select_rubric_messages(rubric_id)
          for m in messages:
            index = messages.index(m)
            m = list(m)
            user = po.select_user_po_id(int(m[2]))[0]
            user_id = user[0]
            user_name = user[1]
            m.append(user)
            user_ava = user[6]
            user_ava = self.static_url(f'avatar/{user_ava}')
            #decode_msg = b'%b' % m[1]
            #m[1] = decode_msg
            m.append(user_ava)
            messages[index] = m
          self.render('templates/rubric.html', messages=messages, rubric=rubric, rubric_id=rubric_id, temp=self.temp)
        else:
          self.redirect('/')
      else:
        messages = po.select_rubric_messages(rubric_id)
        for m in messages:
          index = messages.index(m)
          m = list(m)
          user = po.select_user_po_id(int(m[2]))[0]
          user_id = user[0]
          user_name = user[1]
          m.append(user)
          user_ava = user[6]
          user_ava = self.static_url(f'avatar/{user_ava}')
          #decode_msg = b'%b' % m[1]
          #m[1] = decode_msg
          m.append(user_ava)
          messages[index] = m
        self.render('templates/rubric.html', messages=messages, rubric=rubric, rubric_id=rubric_id, temp=self.temp)
    else:
      messages = po.select_rubric_messages(rubric_id)
      for m in messages:
        index = messages.index(m)
        m = list(m)
        user = po.select_user_po_id(int(m[2]))[0]
        user_id = user[0]
        user_name = user[1]
        m.append(user)
        user_ava = user[6]
        user_ava = self.static_url(f'avatar/{user_ava}')
        #decode_msg = b'%b' % m[1]
        #m[1] = decode_msg
        m.append(user_ava)
        messages[index] = m
      self.render('templates/rubric.html', messages=messages, rubric=rubric, rubric_id=rubric_id, temp=self.temp)
          
  @tornado.gen.coroutine
  def post(self):
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
    if rubric[4] != -10:
      if self.current_user:
        user_info = po.select_user_po_name(self.current_user.decode())[0]
        if rubric[4] <= user_info[4]:
          messages = po.select_rubric_messages(rubric_id)
          for m in messages:
            index = messages.index(m)
            m = list(m)
            user = po.select_user_po_id(int(m[2]))[0]
            user_id = user[0]
            user_name = user[1]
            m.append(user)
            user_ava = user[6]
            user_ava = self.static_url(f'avatar/{user_ava}')
            m.append(user_ava)
            #decode_msg = b'%b' % m[1]
            #m[1] = decode_msg
            messages[index] = m
          self.render('templates/rubric.html', messages=messages, rubric=rubric, rubric_id=rubric_id, temp=self.temp)
        else:
          self.redirect('/')
      else:
        self.redirect('/')
    else:
      messages = po.select_rubric_messages(rubric_id)
      for m in messages:
        index = messages.index(m)
        m = list(m)
        user = po.select_user_po_id(int(m[2]))[0]
        user_id = user[0]
        user_name = user[1]
        m.append(user)
        user_ava = user[6]
        user_ava = self.static_url(f'avatar/{user_ava}')
        print(m[1])
        m.append(user_ava)
        print('--', m[1])
        #decode_msg = b'%b' % m[1]
        #m[1] = decode_msg
        messages[index] = m
      self.render('templates/rubric.html', messages=messages, rubric=rubric, rubric_id=rubric_id, temp=self.temp)
    
class AddRubric(MainHandler):
  async def get(self):
    if self.current_user:
      user_info = po.select_user_po_name(self.current_user.decode())[0];
      print(user_info)
      self.render('templates/rubricAdd.html', temp=self.temp, user_info=user_info);
    else:
      self.redirect('/')
  
  @tornado.gen.coroutine
  def post(self):
    if self.current_user:
      rubric_name: str = self.get_argument("rubric_name", '')
      mini_dop: str = self.get_argument("mini_dop", '')
      min_op: int = int(self.get_argument("min_op", ''))
      only_read = self.get_argument("only_read")
      if only_read == 'true':
        only_read: bool = True
        post: str = self.get_argument('text_in_only_read', '')
        user = self.current_user.decode()
        user_info = po.select_user_po_name(user)[0]
        user_id = user_info[0]
        print(only_read)
        print(user_info)
        po.add_rubric(rubric_name, mini_dop, min_op, only_read, user_id)
        rubric = po.select_rubrics()[-1]
        rubric_id: int = rubric[0]
        po.add_message(post, rubric_id, user_id)
        self.redirect('/')
      else:
        only_read: bool = False
        user = self.current_user.decode()
        user_info = po.select_user_po_id(user)[0]
        user_id = user_info[0]
        print(only_read)
        print(user_info)
        po.add_rubric(rubric_name, mini_dop, min_op, only_read, user_id)
        self.redirect('/')
    else:
      self.redirect('/log')
    
class AddMessage(Rubric):
  @tornado.gen.coroutine
  def post(self):
    if self.current_user:
      rubric_name = self.get_argument("rubric_name", '')
      rubric = po.select_rubric_only_title(rubric_name)[0]
      rubric_id = rubric[0]
      message_text = self.get_argument("message_textarea", '')
      print(self.current_user.decode())
      user = po.select_user_po_name(self.current_user.decode())
      print(user)
      #message_text = he.shifr(message_text.encode('utf-8'), b'abcdefgh')
      #print(message_text)
      po.add_message(message_text, rubric_id, user[0][0])
      print(f'/rubric-{rubric_id}')
      self.redirect(f'/rubric-{rubric_id}')
    else:
      self.redirect('/')
      
class UserAcc(MainHandler):
  @tornado.gen.coroutine
  def get(self):
    url = self.request.path
    print(url)
    redic = int(url[9:])
    print(redic)
    user = po.select_user_po_name(self.current_user.decode())[0]
    if user[-1] in [True, 1, 'true', 'True'] or user[3] in [True, 1, 'true', 'True'] or self.current_user.decode() == redic:
      user_info = po.select_user_po_id(redic)[0]
      if user_info[1] == self.current_user.decode():
        youIsUser = True
      else: 
        youIsUser = False
      ava = user_info[6]
      ava = self.static_url(f"avatar/{ava}")
      print(user_info)
      print(self.current_user)
      self.render('templates/moder_user.html', temp=self.temp, user_info=user_info, ava=ava, youIsUser=youIsUser, current_user=self.current_user.decode())
    else:
      self.render('/')
      
def MyAcc(MainHandler):
  @tornado.gen.coroutine
  def get(self):
    if self.current_user:
      user_info = po.select_user_po_name(self.current_user.decode())
      self.render('templates/moder_user.html', temp=self.temp, user_info=user_info)
      
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
    
class AddAva(UserAcc):
  @tornado.gen.coroutine
  def post(self):
    try:
      newAva = self.request.files['add_ava'][0];
      redic = self.get_argument('url', '');
      original_fname = newAva['filename'];
      redic = self.get_argument('url', '');
      user = self.get_argument('user', '');
      user = self.current_user;
      user_info = po.select_user_po_name(user.decode())[0];
      f = open('static/avatar/{0}'.format(user_info[6]), 'wb');
      f.write(newAva['body']);
      po.update_ava(self.current_user.decode(), user_info[6]);
      f.close();
      self.redirect(redic)
    except:
      pass

    
class ImportRegister(MainHandler):
  get = lambda self: self.render('templates/register.html', temp=self.temp)
    
class Register(MainHandler):
  @tornado.gen.coroutine
  def post(self):
    username = self.get_argument("username", '');
    password1 = self.get_argument("password1", '');
    password2 = self.get_argument("password2", '');
    if password1 == password2:
      po.add_user(username, password1);
      self.redirect('/log');
      user_info = po.select_user_po_name(username)[0];
      with open(f'static/avatar/ava_{username}_id={user_info[0]}.jpg', 'wb') as f:
        with open('static/avatar/default_ava.jpg', 'rb') as f2:
          ava = f2.read();
          f.write(ava);
          po.update_ava(f'static/avatar/ava_{username}_id={user_info[0]}.jpg', username);
    else:
      self.write('<strong>Error(((</strong>')
    
class ImportLogin(MainHandler):
  get = lambda self: self.render('templates/login.html', temp=self.temp)
    
class Login(MainHandler):  
  @tornado.gen.coroutine
  def post(self):
    username = self.get_argument("username", '')
    password = self.get_argument("password", '')
    users = po.select_users()
    if po.check_user(username, password):
      self.set_secure_cookie("user",  self.get_argument("username"), expires_days=3)
      self.current_user = self.current_user
      self.redirect("/")
    else:
      self.clear_cookie("user")
      self.redirect('/log')
  
class Logout(MainHandler):
  async def get(self):
    self.clear_cookie("user")
    self.redirect("/")
    
class Application(tornado.web.Application):
  def __init__(self):
    f = open('config.yaml')
    config = yaml.safe_load(f)
    projectConfig = config['project']
    
    handlers = [
      (r"/", Chat),
      (r"/rubric-\w+", Rubric),
      (r'/addRubric', AddRubric),
      (r'/add-message-in-rubric-\w*\d*\s*', AddMessage),
      (r"/userAcc-.\d*\w*\s*", UserAcc),
      (r'/addOP\d*\w*\s*', AddOP),
      (r'/add_ava', AddAva),
      (r"/reg", ImportRegister),
      (r"/register", Register),
      (r"/log", ImportLogin),
      (r"/login", Login),
      (r"/logout", Logout),
      (r"/admin", adm.MainAdmin),
    ]
    
    settings: typing.Dict = dict(
      cookie_secret=projectConfig['cookie_secret'],
      static_path = os.path.join(os.path.dirname(__file__), "static"),
      templates_path = os.path.join(os.path.dirname(__file__), "templates"),
      xsrf_cookies=True,
    )
    super(Application, self).__init__(handlers, **settings)

if __name__ == "__main__":
  app = Application()
  #port = int(os.environ.get("PORT", 5000))
  #app.listen(port)
  app.listen(8888)
  tornado.ioloop.IOLoop.current().start()