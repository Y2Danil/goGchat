import os
import datetime
from datetime import datetime, date, time, timedelta, timezone
import calendar
import psycopg2
import yaml
# import numba
# from numba import int16, int32

# spec = [
#   ('self.con', numba.uint8)
# ]

class poSQL:
  def __init__(self):
    with open('config.yaml') as f:
      config = yaml.safe_load(f)
      db_config = config['postgres']
        
      self.con = psycopg2.connect(dbname=db_config['database'],
                                user=db_config['user'], 
                                password=db_config['password'], 
                                host=db_config['host'],
                                port=db_config['port'])
      self.cur = self.con.cursor()
    
  def select_users(self):
    with self.con:
      self.cur.execute("""SELECT * FROM "User";""")
      result = self.cur.fetchall()
      return result
    
  def select_user_po_id(self, id):
    with self.con:
      self.cur.execute("""SELECT * FROM "User" WHERE id=%s""", (id,))
      result = self.cur.fetchall()
      return result
  
  def select_user_po_name(self, name):
    with self.con:
      self.cur.execute("""SELECT * FROM "User" WHERE name=%s""", (name,))
      result = self.cur.fetchall()
      return result
    
  def add_user(self, name, password):
    with self.con:
      return self.cur.execute("""INSERT INTO "User"(name, password, admin) VALUES (%s, %s, False)""", (name, password))
    
  def update_ava(self, name, new_ava):
    with self.con:
      return self.cur.execute("""UPDATE "User" SET ava=%s WHERE name=%s""", (new_ava, name))
    
  def update_status_by_id(self, id, status):
    with self.con:
      return self.cur.execute("""UPDATE "User" SET status=%s WHERE id=%s""", (status, id))
    
  def check_user(self, name, password):
    with self.con:
      self.cur.execute("""SELECT name, password, admin FROM "User" WHERE name=%s and password=%s""", (name, password))
      result = self.cur.fetchall()
      return result
  
  def check_user_only_name(self, name):
    with self.con:
      self.cur.execute("""SELECT admin FROM "User" WHERE name=%s""", (name,))
      result = self.cur.fetchall()
      return result
    
  def select_messages(self):
    with self.con:
      self.cur.execute("""SELECT * FROM "Message";""")
      result = self.cur.fetchall()
      return result
    
  def select_message_po_id(self, id):
    with self.con:
      self.cur.execute("""SELECT * FROM "Message" WHERE id=%s;""", (id,))
      result = self.cur.fetchall()
      return result
  
  def add_message(self, text, rubric_id, user_id):
    with self.con:
      return self.cur.execute("""INSERT INTO "Message"(text, pub_date, rubric_id, user_id) VALUES (%s, %s, %s, %s);""", (text, datetime.today(), rubric_id, user_id))
  
  def update_msg(self, id, text):
    with self.con:
      return self.cur.execute("""UPDATE "Message" SET text=%s WHERE id=%s""", (text, id))
    
  def select_types(self):
    with self.con:
      self.cur.execute("""SELECT * FROM "Type";""")
      result = self.cur.fetchall()
      return result
    
  def select_types_op(self, op):
    with self.con:
      self.cur.execute("""SELECT * FROM "Type" WHERE min_op<=%s;""", (op,))
      result = self.cur.fetchall()
      return result
    
  def select_type_po_id(self, id, op):
    with self.con:
      self.cur.execute("""SELECT * FROM "Type" WHERE id=%s AND min_op<=%s;""", (id, op))
      result = self.cur.fetchall()
      return result
    
  def select_themes_po_type(self, type_id, op):
    with self.con:
      self.cur.execute("""SELECT * FROM "Theme" WHERE type_id=%s AND min_op<=%s;""", (type_id, op))
      result = self.cur.fetchall()
      return result
  
  def select_theme_messages(self, rubric_id):
    with self.con:
      self.cur.execute("""SELECT * FROM "Message" WHERE rubric_id=%s;""", (rubric_id,))
      result = self.cur.fetchall()
      return result
    
  def select_fixing_themes(self, op, type_id):
    with self.con:
      self.cur.execute("""SELECT * FROM "Theme" WHERE min_op<=%s AND fixing=true AND type_id=%s;""", (op, type_id))
      result = self.cur.fetchall()
      return result
  
  def select_theme_only_id(self, id):
    with self.con:
      self.cur.execute("""SELECT * FROM "Theme" WHERE id=%s;""", (id,))
      result = self.cur.fetchall()
      return result
  
  def select_themes_only_title(self, rubric_title):
    with self.con:
      self.cur.execute("""SELECT * FROM "Theme" WHERE title=%s;""", (rubric_title,))
      result = self.cur.fetchall()
      return result
  
  def select_themes(self):
    with self.con:
      self.cur.execute("""SELECT * FROM "Theme";""")
      result = self.cur.fetchall()
      return result
    
  def select_themes_plus_op_theme(self, op, type_id):
    with self.con:
      self.cur.execute("""SELECT * FROM "Theme" WHERE min_op<=%s and fixing=false and type_id=%s;""", (op, type_id))
      result = self.cur.fetchall()
      return result
    
  def select_like_msg(self, msg_id):
    with self.con:
      self.cur.execute("""SELECT * FROM "Like" WHERE msg_id=%s""", (msg_id,))
      result = self.cur.fetchall()
      return result
    
  def add_theme(self, title, mini_dop, min_op, only_red, user_id=None, type_id=None):
    with self.con:
      return self.cur.execute("""INSERT INTO "Theme"(title, date, mini_dop, min_op, only_red, create_user_id, type_id) VALUES (%s, %s, %s, %s, %s, %s, %s);""", (title, datetime.today(), mini_dop, min_op, only_red, user_id, type_id))
    
  def add_op(self, user_name, op):
    with self.con:
      return self.cur.execute("""UPDATE "User" SET op=op+%s WHERE name=%s""", (int(op), user_name))
    
  def close(self):
    return self.con.close()
