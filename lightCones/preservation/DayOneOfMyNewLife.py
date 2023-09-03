from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class DayOneOfMyNewLife(BaseLightCone):
  def __init__(self,
               **config):
    self.loadConeStats('Day One of My New Life')
    self.setSuperposition(config)

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'preservation':
      char.percDef += 0.14 + 0.02 * self.superposition
      char.allRes += 0.07 + 0.01 * self.superposition
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  DayOneOfMyNewLife(**Configuration).print()