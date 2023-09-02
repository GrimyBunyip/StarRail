from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class WeWillMeetAgain(BaseLightCone):
  def __init__(self,
               **config):
    self.loadConeStats('We Will Meet Again')
    self.setSuperposition(config)
    
  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'nihility':
      #UNIMPLEMENTED
      pass
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  WeWillMeetAgain(**Configuration).print()