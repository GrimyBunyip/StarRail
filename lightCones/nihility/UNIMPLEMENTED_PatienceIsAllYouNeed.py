from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class PatienceIsAllYouNeed(BaseLightCone):
  def __init__(self,
               stacks:float=3.0,
               **config):
    self.loadConeStats('Patience is All You Need')
    self.setSuperposition(config)
    self.stacks = stacks

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'nihility':
      char.Dmg += 0.20 + 0.04 * self.superposition
      char.percSpd += ( 0.04 + 0.008 * self.superposition ) * self.stacks
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  PatienceIsAllYouNeed(**Configuration).print()