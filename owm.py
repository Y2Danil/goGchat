import pyowm
from pyowm.utils import config
from pyowm.utils import timestamps

class Weather:
  def __init__(self):
    self.owm = pyowm.OWM('cdf62a12d0f07be59ff578db64f3d8a2')
    self.mgr = self.owm.weather_manager()
    self.observation = self.mgr.weather_at_place('Petropavlovsk-Kamchatskiy, RU')
    self.w = self.observation.weather
    
  def temp_in_PK(self):
    return int(self.w.temperature('celsius')['temp'])
  
  def weather_in_PK(self):
    return self.w.detailed_status