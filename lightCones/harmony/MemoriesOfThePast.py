from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class MemoriesOfThePast(BaseLightCone):
  def __init__(self,
               **config):
    self.loadConeStats('Memories of the Past')
    self.setSuperposition(config)

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'harmony':
      pass #harmony cones not yet implemented fully
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  MemoriesOfThePast(**Configuration).print()