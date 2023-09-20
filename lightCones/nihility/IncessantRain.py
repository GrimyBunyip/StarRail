from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class IncessantRain(BaseLightCone):
  def __init__(self,
               uptime:float=1.0,
               uptimeAether:float=1.0,
               **config):
    self.loadConeStats('Incessant Rain')
    self.setSuperposition(config)
    self.uptime = uptime
    self.uptimeAether = uptimeAether

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == self.path:
      char.EHR += 0.20 + 0.04 * self.superposition
      char.CR += ( 0.10 + 0.02 * self.superposition ) * self.uptime
      char.Dmg += ( 0.10 + 0.02 * self.superposition ) * self.uptimeAether
      char.Vulnerability += 0.1 + 0.02 * self.superposition
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  IncessantRain(**Configuration).print()