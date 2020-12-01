import pyowm
from pyowm.utils import config
from pyowm.utils import timestamps
import yaml

class Weather:
  def __init__(self):
    f = open('config.yaml')
    config = yaml.safe_load(f)
    projectConfig = config['project']
    
    self.owm = pyowm.OWM(projectConfig['owm'])
    self.mgr = self.owm.weather_manager()
    self.observation = self.mgr.weather_at_place('Petropavlovsk-Kamchatskiy, RU')
    self.w = self.observation.weather
    
  def temp_in_PK(self):
    return int(self.w.temperature('celsius')['temp'])
  
  def weather_in_PK(self):
    return self.w.detailed_status