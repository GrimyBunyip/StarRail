from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class BeforeDawn(BaseLightCone):
  def __init__(self,
               uptime:float=1.0,
               **config):
    self.loadConeStats('Before Dawn')
    self.setSuperposition(config)
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'erudition':
      char.CD += 0.30 + 0.06 * self.superposition
      char.skillDmg += 0.15 + 0.03 * self.superposition
      char.ultDmg += 0.15 + 0.03 * self.superposition
      char.followupDmg += ( 0.40 + 0.08 * self. superposition ) * self.uptime
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  BeforeDawn(**Configuration).print()