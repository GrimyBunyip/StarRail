from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class WorrisomeBlissful(BaseLightCone):
  def __init__(self,
               stacks:float = 0.0,
               **config):
    self.loadConeStats('Worrisome, Blissful')
    self.setSuperposition(config)
    self.stacks = stacks

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'hunt':
      char.CR += 0.15 + 0.03 * self.superposition
      char.DmgType['followup'] += 0.25 + 0.05 * self.superposition
      char.CD += ( 0.10 + 0.02 * self.superposition ) * self.stacks
      
    
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  WorrisomeBlissful(**Configuration).print()