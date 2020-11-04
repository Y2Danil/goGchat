import sqlite3

class SQLiter:
  def __init__(self):
    self.con = sqlite3.connect('chat_db.sqlite')
    self.cur = self.con.cursor()
    
  def select_users(self):
    with self.con:
      self.cur.execute("SELECT * FROM user")
      result = self.cur.fetchall()
      return result
    
  def select_user_po_id(self, id):
    self.cur.execute("SELECT * FROM user WHERE id=?", (id,))
    result = self.cur.fetchall()
    return result
    
  def add_user(self, name, password):
    with self.con:
      return self.cur.execute("INSERT INTO user(name, password, admin) VALUES (?, ?, False)", (name, password))
    
  def check_user(self, name, password):
    self.cur.execute("SELECT name, password, admin FROM user WHERE name=? and password=?", (name, password))
    result = self.cur.fetchall()
    return result
  
  def check_user_only_name(self, name):
    self.cur.execute("SELECT admin FROM user WHERE name=?", (name,))
    result = self.cur.fetchall()
    return result
    
  def select_messages(self):
    with self.con:
      self.cur.execute("SELECT * FROM message")
      result = self.cur.fetchall()
      return result
    
  def close(self):
    return self.con.close()