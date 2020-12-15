import tornado.ioloop
import tornado.wsgi
import tornado.web
import tornado
import tornado.httpserver
import yaml

import os
import re
import typing
from ftplib import FTP

import owm
from poSQL import *
import adminka as adm
from hesirka import Heshirka
#from dop_data import Data

he = Heshirka(0)
po = poSQL()
we = owm.Weather()
#dd = Data()

class MainHandler(tornado.web.RequestHandler):
  po = poSQL()
  # int_temp = we.temp_in_PK()
  # str_temp = str(we.temp_in_PK())
  temp = we.temp_in_PK()
    
  def get(self):
    print('a')
    if self.current_user:
      self.current_user = self.current_user
    else:
      self.current_user = None
      
    if not self.get_secure_cookie('key'):
      self.set_secure_cookie('key', None)
      print('a')
      self.key = None
    else:
      self.set_secure_cookie('key', self.key)
      self.key = self.get_secure_cookie('key')
      
  def get_current_user(self):
    return self.get_secure_cookie("user")
  
  def key(self):
    return self.get_secure_cookie("key")
    
class Chat(MainHandler):
  # async def get(self):
  #   if self.current_user:
    #   user = self.current_user.decode()
    #   user_info = po.select_user_po_name(user)[0]
    #   print(user_info)
    #   rubrics = po.select_themes_plus_op_theme(user_info[4])[::-1]
    #   fixing_rubrics = po.select_fixing_themes(user_info[4])[::-1]
    # else:
    #   rubrics = po.select_themes_plus_op_theme(0)[::-1]
    #   fixing_rubrics = po.select_fixing_themes(0)[::-1]
    # self.render('templates/chat.html', temp=self.temp, rubrics=rubrics, fixing_rubrics=fixing_rubrics)
    
  @tornado.gen.coroutine
  def get(self):
    if self.current_user:
      user = self.current_user.decode()
      user_info = po.select_user_po_name(user)[0]
      print(user_info)
      types = po.select_types()
      rubrics = []
      self.render('templates/chat.html', temp=self.temp, types=types, user_info=user_info)
      # for type in types:
      #   rubric = po.select_themes_plus_op_theme(user_info[4], type[0])
      #   rubrics
      # rubrics = po.select_themes_plus_op_theme(user_info[4])[::-1]
      # fixing_rubrics = po.select_fixing_themes(user_info[4], 1)[::-1]
    else:
      types = po.select_types()
      # rubrics = po.select_themes_plus_op_theme(0)[::-1]
      # fixing_rubrics = po.select_fixing_themes(0)[::-1]
      self.render('templates/chat.html', temp=self.temp, types=types)
    
class Type(Chat):
  @tornado.gen.coroutine
  def get(self):
    url = self.request.path;
    type_id = url[6:];
    if self.current_user:
      user_info = po.select_user_po_name(self.current_user.decode('utf-8'))[0];
      type = po.select_type_po_id(int(type_id), user_info[4])[0]
      themes = po.select_themes_po_type(int(type_id), user_info[4])
      
      self.render('templates/type.html', type=type, themes=themes)
    else:
      type = po.select_type_po_id(int(type_id), 0)[0]
      themes = po.select_themes_po_type(int(type_id), 0)
      
      self.render('templates/type.html', type=type, themes=themes)
    
class Rubric(Chat):
  async def get(self):
    url = str(self.request.path)
    rubric_id = re.search(r"(rubric-[0-9]*)\/\w+", str(url), flags=0)
    rubric_id = re.search(r"c-[0-9]*", str(rubric_id))
    rubric_id = rubric_id.group(0)[2:]
    rubric = po.select_theme_only_id(rubric_id)[0]
    
    col_msg = re.search(r"rubric-[0-9]*\/\w+", str(url), flags=0)
    col_msg = re.search(r"(\/\d+)", col_msg.group(0))
    col_stranich = []
    
    if self.key():
      key = self.key()
    else:
      key = None
    if rubric[4] != -10:
      if self.current_user:
        user_info = po.select_user_po_name(self.current_user.decode())[0]
        if rubric[4] <= user_info[4]:
          messages = po.select_theme_messages(rubric_id)
          
          len_msgs = len(messages)
          copy_len_msgs = len_msgs
          
          if len_msgs > 15:
            srez = {'start': 0, 'end': 0}
            msg_col = 0
            for i in range(0, len_msgs):
              if len_msgs > 14:
                col_stranich.append(i+1)
                len_msgs -= 15
              else:
                if len_msgs > 0:
                  col_stranich.append(i+1)
                  break
                else: 
                  break
                
            len_msgs = copy_len_msgs
            
            for i in range(0, int(col_msg.group(0)[1:])):
              print(i)
              if len_msgs > 14:
                if i != 0:
                  srez['start'] += 15
                srez['end'] += 15
                len_msgs -= 15
              else:
                if len_msgs > 0 and len_msgs < 15:
                  srez['start'] += len_msgs
                  srez['end'] += len_msgs
                  break
                else:
                  break
    
            messages = messages[srez['start']:srez['end']]
            
          for m in messages:
            index = messages.index(m)
            m = list(m)
            user = po.select_user_po_id(int(m[2]))[0]
            user_id = user[0]
            user_name = user[1]
            m.append(user)
            user_ava = user[6]
            user_ava = self.static_url(f'avatar/{user_ava}')
            try:
              m[1] = he.deshifr(m[1], self.key()).decode('utf-8')
            except UnicodeDecodeError:
              pass
            m.append(user_ava)
            messages[index] = m
          self.render('templates/rubric.html', messages=messages, rubric=rubric, rubric_id=rubric_id, temp=self.temp, key=key, col_stranich=col_stranich, col_msg=col_msg.group(0)[1:], len_msgs=copy_len_msgs)
        else:
          self.redirect('/')
      else:
        messages = po.select_theme_messages(rubric_id)
        len_msgs = len(messages)
        copy_len_msgs = len_msgs
          
        if len_msgs > 15:
          srez = {'start': 0, 'end': 0}
          msg_col = 0
          for i in range(0, len_msgs):
            if len_msgs > 14:
              col_stranich.append(i+1)
              len_msgs -= 15
            else:
              if len_msgs > 0:
                col_stranich.append(i+1)
                break
              else: 
                break
                
          len_msgs = copy_len_msgs
          
          for i in range(0, int(col_msg.group(0)[1:])):
            print(i)
            if len_msgs > 14:
              if i != 0:
                srez['start'] += 15
              srez['end'] += 15
              len_msgs -= 15
              
            else:
              if len_msgs > 0 and len_msgs < 15:
                srez['start'] += len_msgs
                srez['end'] += len_msgs
                break
              else:
                break
    
          messages = messages[srez['start']:srez['end']]
          
        for m in messages:
          index = messages.index(m)
          m = list(m)
          user = po.select_user_po_id(int(m[2]))[0]
          user_id = user[0]
          user_name = user[1]
          m.append(user)
          user_ava = user[6]
          user_ava = self.static_url(f'avatar/{user_ava}')
          try:
              m[1] = he.deshifr(m[1], self.key()).decode('utf-8')
          except UnicodeDecodeError:
            pass
          m.append(user_ava)
          messages[index] = m
        self.render('templates/rubric.html', messages=messages, rubric=rubric, rubric_id=rubric_id, temp=self.temp, key=key, col_stranich=col_stranich, col_msg=col_msg.group(0)[1:], len_msgs=copy_len_msgs)
    else:
      messages = po.select_theme_messages(rubric_id)
      len_msgs = len(messages)
      copy_len_msgs = len_msgs
          
      if len_msgs > 15:
        srez = {'start': 0, 'end': 0}
        msg_col = 0
        for i in range(0, len_msgs):
          if len_msgs > 14:
            col_stranich.append(i+1)
            len_msgs -= 15
          else:
            if len_msgs > 0:
              col_stranich.append(i+1)
              break
            else: 
              break
                
        len_msgs = copy_len_msgs
          
        for i in range(0, int(col_msg.group(0)[1:])):
          print(i)
          if len_msgs > 14:
            if i != 0:
              srez['start'] += 15
            srez['end'] += 15
            len_msgs -= 15
          else:
            if len_msgs > 0 and len_msgs < 15:
              srez['start'] += len_msgs
              srez['end'] += len_msgs
              break
            else:
              break
    
        messages = messages[srez['start']:srez['end']]
      for m in messages:
        index = messages.index(m)
        m = list(m)
        user = po.select_user_po_id(int(m[2]))[0]
        user_id = user[0]
        user_name = user[1]
        m.append(user)
        user_ava = user[6]
        user_ava = self.static_url(f'avatar/{user_ava}')
        try:
          m[1] = he.deshifr(m[1], self.key()).decode('utf-8')
        except UnicodeDecodeError:
          pass
        m.append(user_ava)
        messages[index] = m
      self.render('templates/rubric.html', messages=messages, rubric=rubric, rubric_id=rubric_id, temp=self.temp, key=key, col_stranich=col_stranich, col_msg=col_msg.group(0)[1:], len_msgs=copy_len_msgs)

class AddRubric(MainHandler):
  async def get(self):
    if self.current_user:
      user_info = po.select_user_po_name(self.current_user.decode())[0];
      print(user_info);
      types = po.select_types_op(user_info[4]);
      self.render('templates/rubricAdd.html', temp=self.temp, user_info=user_info, types=types);
    else:
      self.redirect('/');
  
  @tornado.gen.coroutine
  def post(self):
    if self.current_user:
      rubric_name: str = self.get_argument("rubric_name", '')
      mini_dop: str = self.get_argument("mini_dop", '')
      min_op: int = int(self.get_argument("min_op", ''))
      type_theme: int = self.get_argument('type_theme', '');
      only_read = self.get_argument("only_read", '');
      themes = po.select_themes()
      for t in themes:
        if t[1] == rubric_name:
          self.redirect('/addTheme')
          return False
      
      if only_read == 'true':
        only_read: bool = True
        post: str = self.get_argument('text_in_only_read', '')
        user = self.current_user.decode()
        user_info = po.select_user_po_name(user)[0]
        user_id = user_info[0]
        print(only_read)
        print(user_info)
        po.add_theme(rubric_name, mini_dop, min_op, only_read, user_id)
        rubric = po.select_themes()[-1]
        rubric_id: int = rubric[0]
        po.add_message(post, rubric_id, user_id)
        self.redirect('/')
      else:
        only_read: bool = False
        user = self.current_user.decode()
        user_info = po.select_user_po_name(user)[0]
        user_id = user_info[0]
        print(only_read)
        print(user_info)
        po.add_theme(rubric_name, mini_dop, min_op, only_read, user_id, type_theme)
        self.redirect('/')
    else:
      self.redirect('/log')
    
class KeyRubric(MainHandler):
  @tornado.gen.coroutine
  def post(self):
    key = self.get_argument('key', '');
    redic: str = self.get_argument('redic', '');
    if self.current_user:
      if len(key) != 8:
        key = b'keyIdiot'
      else:
        pass
      self.set_secure_cookie('key', key);
      self.key = self.get_secure_cookie('key');
      print(self.key);
    
      self.redirect(redic);
    else:
      self.set_secure_cookie('key', key);
      self.key = self.get_secure_cookie('key');
      self.redirect(redic);
  
class AddMessage(Rubric):
  @tornado.gen.coroutine
  def post(self):
    if self.current_user:
      rubric_name = self.get_argument("rubric_name", '')
      redic = self.get_argument("redic", '')
      rubric = po.select_themes_only_title(rubric_name)[0]
      rubric_id = rubric[0]
      message_text = self.get_argument("message_textarea", '')
      print(self.current_user.decode())
      user = po.select_user_po_name(self.current_user.decode())
      print(user)
      message_text = he.shifr(message_text, self.key())
      print(message_text)
      po.add_message(message_text, rubric_id, user[0][0])
      # print(f'/rubric-{rubric_id}')
      messages = po.select_theme_messages(rubric_id)
      print('>>>', messages)
      srez = {'start': 0, 'end': 0}
          
      len_msgs = len(messages)
      print(len_msgs)
      index = 0
      for i in range(0, len_msgs):
        print(i)
        if i % 2 == 0:
          index += 1
        
        print('>>>', index)
          
      print(index)
      print(rubric_id)
      self.redirect(f'/rubric-{rubric_id}/{index}')
    else:
      self.redirect('/')
      
class UserAcc(MainHandler):
  @tornado.gen.coroutine
  def get(self):
    if self.current_user:
      url = self.request.path
      redic = int(url[9:])
      #user = po.select_user_po_name(self.current_user.decode())[0]
      user = po.select_user_po_id(redic)[0]
      cur_user = po.select_user_po_name(self.current_user.decode('utf-8'))[0]
      if True:
        #user_info = po.select_user_po_id(redic)[0]
        if user[1] == self.current_user.decode():
          youIsUser = True
        else: 
          youIsUser = False
        avatars = []
        os.chdir('static/avatar')
        for root, dirs, files in os.walk(".", topdown = False):
          for name in files:
            avatars.append(os.path.join(root, name)[2:])
        os.chdir('../../')
        avatars.remove('ava_Danil++_id=1.jpg')
        ava = user[6]
        ava = self.static_url(f"avatar/{ava}")
        self.render('templates/moder_user.html',
                    temp=self.temp, 
                    user_info=user,
                    ava=ava,
                    youIsUser=youIsUser,
                    avatars=avatars,
                    cur_user=cur_user)
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
      userName = self.get_argument('addOP_username', '')
      op = self.get_argument('OP', '')
      if int(op) <= 5:
        po.add_op(userName, int(op))
      else:
        if user[3]:
          po.add_op(userName, int(op))
        else:
          po.add_op(userName, 5)
    self.redirect(redic)
    
class AddAva(UserAcc):
  @tornado.gen.coroutine
  def post(self):
    try:
      #newAva = self.request.files['add_ava'][0];
      newAVA = self.get_argument('newAva', '');
      redic = self.get_argument('url', '');
      print(redic)
      if self.current_user:
        user = self.current_user.decode('utf-8');
        
        po.update_ava(user, newAVA);
      # f = open('static/avatar/{0}'.format(user_info[6]), 'wb');
      # f.write(newAva['body']);
      
      # f.close();
      self.redirect(redic);
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
      (r"/type-\w+", Type),
      (r"/rubric-\w+\/\w+", Rubric),
      (r'/post-key', KeyRubric),
      (r'/addTheme', AddRubric),
      (r'/add-message-in-rubric-\w*\d*\s*', AddMessage),
      (r"/userAcc-.\d*\w*\s*", UserAcc),
      (r'/addOP\d*\w*\s*', AddOP),
      (r'/addAva', AddAva),
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
  port = int(os.environ.get("PORT", 5000))
  app.listen(port)
  app.listen(8888)
  tornado.ioloop.IOLoop.current().start()