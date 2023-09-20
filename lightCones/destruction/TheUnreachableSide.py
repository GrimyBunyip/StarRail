from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class TheUnreachableSide(BaseLightCone):
  def __init__(self,
               uptime:float = 1.0,
               **config):
    self.loadConeStats('The Unreachable Side')
    self.setSuperposition(config)
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == self.path:
      char.CR += 0.15 + 0.03 * self.superposition
      char.percHP += 0.15 + 0.03 * self.superposition
      char.Dmg += ( 0.20 + 0.04 * self.superposition ) * self.uptime
    
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  TheUnreachableSide(**Configuration).print()