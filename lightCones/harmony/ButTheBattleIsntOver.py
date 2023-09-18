from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class ButTheBattleIsntOver(BaseLightCone):
  def __init__(self,
               **config):
    self.loadConeStats('But the Battle Isn\'t Over')
    self.setSuperposition(config)

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'harmony':
      pass #harmony cones not yet implemented fully
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  ButTheBattleIsntOver(**Configuration).print()