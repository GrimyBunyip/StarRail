from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class TheBirthOfTheSelf(BaseLightCone):
  def __init__(self,
               uptime:float=0.5,
               **config):
    self.loadConeStats('The Birth of the Self')
    self.setSuperposition(config)
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == self.path:
      char.DmgType['followup'] += 0.24 + 0.06 * self.superposition
      char.DmgType['followup'] += ( 0.24 + 0.06 * self.superposition ) * self.uptime
    
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  TheBirthOfTheSelf(**Configuration).print()