from PIL import Image
import numba
from numba import int16, int32
import typing

spec = [('x', numba.int64)]

#@numba.jitclass(spec)
class Tests(object): 
  def __init__(self):
    self.x = 2
  
  consol = lambda self, x: str(x + 1)
  
  def open_def_fiel(self):
    f = open('chat-tornado/static/avatar/default_ava.jpg', 'r')
    assert f.read() == ''
    print(f.read())
    
  def arrayTest(self, n):
    print('start')
    array = []
    for i in range(0, n):
      array.append(i)
      
    print('end')
    
  def test_int(self, str: str) -> int:
    a: int = str
    a: int = a*2
    list = [a]
    print(list)
    
  
if __name__ == '__main__':
  T = Tests()
  #Tests().arrayTest(1000000000000000)
  T.test_int('2')
  