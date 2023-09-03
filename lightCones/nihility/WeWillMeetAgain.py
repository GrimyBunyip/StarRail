from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseMV import BaseMV

class WeWillMeetAgain(BaseLightCone):
  def __init__(self,
               **config):
    self.loadConeStats('We Will Meet Again')
    self.setSuperposition(config)
    
  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'nihility':
      char.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=0.36+0.12*self.superposition)] + char.motionValueDict['basic'] if 'basic' in char.motionValueDict else []
      char.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=0.36+0.12*self.superposition)] + char.motionValueDict['skill'] if 'skill' in char.motionValueDict else []
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  WeWillMeetAgain(**Configuration).print()