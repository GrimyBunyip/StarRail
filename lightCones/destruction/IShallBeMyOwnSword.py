from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class IShallBeMyOwnSword(BaseLightCone):
  def __init__(self,
               uptime:float = 1.0,
               **config):
    self.loadConeStats('I Shall Be My Own Sword')
    self.setSuperposition(config)
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'destruction':
      char.skillDmg += 0.25 + 0.05 * self.superposition
      char.CD += 0.3 + 0.06 * self.superposition
      char.bonusEnergyUlt += 10.0 + 2.0 * self.superposition
    
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  IShallBeMyOwnSword(**Configuration).print()