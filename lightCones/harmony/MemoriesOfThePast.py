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
      char.bonusEnergyAttack['basic'] += 3.0 + 1.0 * self.superposition
      char.bonusEnergyAttack['skill'] += 3.0 + 1.0 * self.superposition
      char.bonusEnergyAttack['ultimate'] += 3.0 + 1.0 * self.superposition
      char.bonusEnergyAttack['talent'] += 3.0 + 1.0 * self.superposition
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  MemoriesOfThePast(**Configuration).print()