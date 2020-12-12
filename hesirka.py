import hashlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP, DES
from Crypto.Random import get_random_bytes

#spec = [('run', int32)]
 
#@jitclass(spec)
class Heshirka:
  def __init__(self, run):
    self.run = run
    #super().__init__()
    
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
    if type(text) != bytes:
      text = text.encode('utf-8')
    else:
      pass
    des = DES.new(key, DES.MODE_ECB)
    padded_text = self.pad(text)
    encrypted_text = des.encrypt(padded_text)
    
    return encrypted_text
  
  def deshifr(self, data: bytes, key: bytes):
    des = DES.new(key, DES.MODE_ECB)
    data = des.decrypt(data)
    
    return data
      
  def hesh_lite(self, str):
    res = hashlib.sha256(str.encode('utf-8'))
    return res.hexdigest()
