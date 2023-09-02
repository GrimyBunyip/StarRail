from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class CruisingInTheStellarSea(BaseLightCone):
  def __init__(self,
               uptime:float = 0.5,
               **config):
    self.loadConeStats('Cruising in the Stellar Sea')
    self.setSuperposition(config)
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'hunt':
      char.CR += 0.06 + 0.02 * self.superposition
      char.CR += (0.06 + 0.02 * self.superposition) * self.uptime
    
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  CruisingInTheStellarSea(**Configuration).print()