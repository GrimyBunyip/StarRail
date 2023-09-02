from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class SomethingIrreplaceable(BaseLightCone):
  def __init__(self,
               uptime:float = 1.0,
               **config):
    self.loadConeStats('Something Irreplaceable')
    self.setSuperposition(config)
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'destruction':
      char.percAtk += 0.20 + 0.04 * self.superposition
      char.Dmg += ( 0.20 + 0.04 * self.superposition ) * self.uptime
    
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  SomethingIrreplaceable(**Configuration).print()