from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class NowhereToRun(BaseLightCone):
  def __init__(self,
               **config):
    self.loadConeStats('Nowhere to Run')
    self.setSuperposition(config)

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == self.path:
      char.percAtk += 0.24 + 0.06 * self.superposition
    
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  NowhereToRun(**Configuration).print()