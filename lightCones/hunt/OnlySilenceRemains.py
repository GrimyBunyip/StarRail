from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class OnlySilenceRemains(BaseLightCone):
  def __init__(self, 
               **config):
    self.loadConeStats('Only Silence Remains')
    self.setSuperposition(config)

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == self.path:
      char.percAtk += 0.12 + 0.04 * self.superposition
      char.CR += ( 0.09 + 0.03 * self.superposition ) if char.numEnemies <= 2 else 0.0
    
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  OnlySilenceRemains(**Configuration).print()