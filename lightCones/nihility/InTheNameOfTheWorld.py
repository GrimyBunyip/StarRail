from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class InTheNameOfTheWorld(BaseLightCone):
  def __init__(self,
               uptime:float = 1.0,
               **config):
    self.loadConeStats('In the Name of the World')
    self.setSuperposition(config)
    self.uptime=uptime

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'nihility':
      char.Dmg += ( 0.20 + 0.04 * self.superposition ) * self.uptime
      char.skillPercAtk += 0.20 + 0.04 * self.superposition
      # also boosts skill EHR, but not implementing that atm
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  InTheNameOfTheWorld(**Configuration).print()