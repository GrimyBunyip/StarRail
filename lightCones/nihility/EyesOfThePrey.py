from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class EyesOfThePrey(BaseLightCone):
  def __init__(self,
               **config):
    self.loadConeStats('Eyes of the Prey')
    self.setSuperposition(config)

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'nihility':
      char.EHR += 0.15 + 0.05 * self.superposition
      char.dotDmg += 0.18 + 0.06 * self.superposition
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  EyesOfThePrey(**Configuration).print()