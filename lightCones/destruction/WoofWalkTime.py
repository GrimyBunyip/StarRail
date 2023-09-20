from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class WoofWalkTime(BaseLightCone):
  def __init__(self,
               uptime:float = 1.0,
               **config):
    self.loadConeStats('Woof! Walk Time!')
    self.setSuperposition(config)
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == self.path:
      char.percAtk += 0.075 + 0.025 * self.superposition
      char.Dmg += ( 0.12 + 0.04 * self.superposition ) * self.uptime
    
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  WoofWalkTime(**Configuration).print()