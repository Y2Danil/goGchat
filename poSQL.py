import os
import datetime
from datetime import datetime, date, time, timedelta, timezone
import calendar
import psycopg2

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
    self.cur.execute("""SELECT * FROM "User" WHERE id=%s""", (id,))
    result = self.cur.fetchall()
    return result
  
  def select_user_po_name(self, name):
    self.cur.execute("""SELECT * FROM "User" WHERE name=%s""", (name,))
    result = self.cur.fetchall()
    return result
    
  def add_user(self, name, password):
    with self.con:
      return self.cur.execute("""INSERT INTO "User"(name, password, admin) VALUES (%s, %s, False)""", (name, password))
    
  def check_user(self, name, password):
    self.cur.execute("""SELECT name, password, admin FROM "User" WHERE name=%s and password=%s""", (name, password))
    result = self.cur.fetchall()
    return result
  
  def check_user_only_name(self, name):
    self.cur.execute("""SELECT admin FROM "User" WHERE name=%s""", (name,))
    result = self.cur.fetchall()
    return result
    
  def select_messages(self):
    self.cur.execute("""SELECT * FROM "Message";""")
    result = self.cur.fetchall()
    return result
  
  def add_message(self, text, rubric_id, user_id):
    with self.con:
      return self.cur.execute("""INSERT INTO "Message"(text, pub_date, rubric_id, user_id) VALUES (%s, %s, %s, %s);""", (text, datetime.today(), rubric_id, user_id))
  
  def select_rubric_messages(self, rubric_id):
    self.cur.execute("""SELECT * FROM "Message" WHERE rubric_id=%s;""", (rubric_id,))
    result = self.cur.fetchall()
    return result
  
  def select_rubric_only_id(self, id):
    self.cur.execute("""SELECT * FROM "Rubric" WHERE id=%s;""", (id,))
    result = self.cur.fetchall()
    return result
  
  def select_rubric_only_title(self, rubric_title):
    self.cur.execute("""SELECT * FROM "Rubric" WHERE title=%s;""", (rubric_title,))
    result = self.cur.fetchall()
    return result
  
  def select_rubrics(self):
    self.cur.execute("""SELECT * FROM "Rubric";""")
    result = self.cur.fetchall()
    return result
    
  def close(self):
    return self.con.close()