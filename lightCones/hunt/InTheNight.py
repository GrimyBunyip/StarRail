from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
import math

class InTheNight(BaseLightCone):
  def __init__(self,
               **config):
    self.loadConeStats('In the Night')
    self.setSuperposition(config)

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'hunt':
      char.CR += 0.15 + 0.03 * self.superposition
      num_stacks = math.floor( ( char.getTotalSpd() - 100.0 ) / 10.0 )
      num_stacks = min(num_stacks, 6)
      char.basicDmg += 0.05 + 0.01 * self.superposition
      char.ultimateCD += 0.10 + 0.02 * self.superposition
      
    
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  InTheNight(**Configuration).print()