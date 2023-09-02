from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class TheMolesWelcomeYou(BaseLightCone):
  def __init__(self,
               stacks:int = 3, # you gain 1 stack for each type of basic, skill, ultimate.
               **config):
    self.loadConeStats('The Moles Welcome You')
    self.setSuperposition(config)
    self.stacks = stacks

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'destruction':
      char.percAtk += ( 0.09 + 0.03 * self.superposition ) * self.stacks
    
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  TheMolesWelcomeYou(**Configuration).print()