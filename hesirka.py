import hashlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP, DES
from Crypto.Random import get_random_bytes
 
class Heshirka:
  def __init__(self):
    super().__init__()
    
  def pad(self, text):
    while len(text) % 8 != 0:
        text += b' '
    return text
  
  def gener_key(self, code=None):
    key = RSA.generate(2048)
    
    encrypted_key = key.exportKey(
        passphrase=code, 
        pkcs=8, 
        protection="scryptAndAES128-CBC"
    )
    
    return key.publickey().exportKey()
  
  def dekey(self):
    pass
    
  def shifr(self, text: bytes, key: bytes):
    des = DES.new(key, DES.MODE_ECB)
    text_dehash = text
    padded_text = self.pad(text_dehash)
    encrypted_text = des.encrypt(padded_text)
    data = des.decrypt(encrypted_text)
    
    return data
      
  def hesh_lite(self, str):
    res = hashlib.sha256(str.encode('utf-8'))
    return res.hexdigest()
  
  
if __name__ == "__main__":
  he = Heshirka()
  key = he.gener_key('nooneknows')
  #print(key)
  t = b"Hello!!!"
  msg = he.shifr(t, key)
  print(msg)