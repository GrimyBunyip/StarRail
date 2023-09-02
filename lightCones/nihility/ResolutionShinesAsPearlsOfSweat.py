from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class ResolutionShinesAsPearlsOfSweat(BaseLightCone):
  def __init__(self,
               uptime:float=1.0,
               **config):
    self.loadConeStats('Resolution Shines As Pearls of Sweat')
    self.setSuperposition(config)
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'nihility':
      char.defShred += ( 0.11 + 0.01 * self.superposition ) * self.uptime
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  ResolutionShinesAsPearlsOfSweat(**Configuration).print()