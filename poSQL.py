import os
import psycopg2

class SQLiter:
  def __init__(self):
    self.DATABASE_URL = os.environ['DATABASE_URL']
    #self.con = psycopg2.connect(DATABASE_URL, sslmode='require')
    self.con = psycopg2.connect(dbname='d48m04bohdscjt',
                                user='sdhjmwjlisovxf', 
                                password='75577485b50664f0cba60bc31547470761803b7f7da7d21995817401eba29767', 
                                host='ec2-54-228-250-82.eu-west-1.compute.amazonaws.com')
    self.cur = self.con.cursor()
    
  def select_users(self):
    with self.con:
      self.cur.execute('SELECT * FROM "User"')
      result = self.cur.fetchall()
      return result
    
  def select_user_po_id(self, id):
    self.cur.execute("""SELECT * FROM "User" WHERE id=?""", (id,))
    result = self.cur.fetchall()
    return result
    
  def add_user(self, name, password):
    with self.con:
      return self.cur.execute("""INSERT INTO "User"(name, password, admin) VALUES (?, ?, False)""", (name, password))
    
  def check_user(self, name, password):
    self.cur.execute("""SELECT name, password, admin FROM "User" WHERE name=? and password=?""", (name, password))
    result = self.cur.fetchall()
    return result
  
  def check_user_only_name(self, name):
    self.cur.execute("""SELECT admin FROM "User" WHERE name=?""", (name,))
    result = self.cur.fetchall()
    return result
    
  def select_messages(self):
    with self.con:
      self.cur.execute("""SELECT * FROM "Message";""")
      result = self.cur.fetchall()
      return result
    
  def close(self):
    return self.con.close()