import os
import datetime
from datetime import datetime, date, time, timedelta, timezone
import calendar
import psycopg2
# import numba
# from numba import int16, int32

# spec = [
#   ('self.con', numba.uint8)
# ]

class poSQL:
  def __init__(self):
    #self.DATABASE_URL = os.environ['DATABASE_URL']
    #self.con = psycopg2.connect(DATABASE_URL, sslmode='require')
    self.con = psycopg2.connect(dbname='d48m04bohdscjt',
                                user='sdhjmwjlisovxf', 
                                password='75577485b50664f0cba60bc31547470761803b7f7da7d21995817401eba29767', 
                                host='ec2-54-228-250-82.eu-west-1.compute.amazonaws.com')
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
  
  def add_message(self, text, rubric_id, user_id):
    with self.con:
      return self.cur.execute("""INSERT INTO "Message"(text, pub_date, rubric_id, user_id) VALUES (%s, %s, %s, %s);""", (text, datetime.today(), rubric_id, user_id))
  
  def select_rubric_messages(self, rubric_id):
    with self.con:
      self.cur.execute("""SELECT * FROM "Message" WHERE rubric_id=%s;""", (rubric_id,))
      result = self.cur.fetchall()
      return result
    
  def select_fixing_rubrics(self, op):
    with self.con:
      self.cur.execute("""SELECT * FROM "Rubric" WHERE min_op<=%s and fixing=true;""", (op,))
      result = self.cur.fetchall()
      return result
  
  def select_rubric_only_id(self, id):
    with self.con:
      self.cur.execute("""SELECT * FROM "Rubric" WHERE id=%s;""", (id,))
      result = self.cur.fetchall()
      return result
  
  def select_rubric_only_title(self, rubric_title):
    with self.con:
      self.cur.execute("""SELECT * FROM "Rubric" WHERE title=%s;""", (rubric_title,))
      result = self.cur.fetchall()
      return result
  
  def select_rubrics(self):
    with self.con:
      self.cur.execute("""SELECT * FROM "Rubric";""")
      result = self.cur.fetchall()
      return result
    
  def select_rubrics_plus_op_rubric(self, op):
    with self.con:
      self.cur.execute("""SELECT * FROM "Rubric" WHERE min_op<=%s and fixing=false;""", (op,))
      result = self.cur.fetchall()
      return result
    
  def add_rubric(self, title, mini_dop, min_op, only_red, user_id=None):
    with self.con:
      return self.cur.execute("""INSERT INTO "Rubric"(title, date, mini_dop, min_op, only_red, create_user_id) VALUES (%s, %s, %s, %s, %s, %s);""", (title, datetime.today(), mini_dop, min_op, only_red, user_id))
    
  def add_op(self, user_name, op):
    with self.con:
      return self.cur.execute("""UPDATE "User" SET op=op+%s WHERE name=%s""", (int(op), user_name))
    
  def close(self):
    return self.con.close()
