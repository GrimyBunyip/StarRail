from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class SolitaryHealing(BaseLightCone):
  def __init__(self,
               uptime:float=1.0,
               **config):
    self.loadConeStats('Solitary Healing')
    self.setSuperposition(config)
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'nihility':
      char.breakEffect += 0.15 + 0.05 * self.superposition
      char.DmgType['dot'] += ( 0.18 + 0.06 * self.superposition ) * self.uptime
      # on kill energy not factored in
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  SolitaryHealing(**Configuration).print()