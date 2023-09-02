from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class OnTheFallOfAnAeon(BaseLightCone):
  def __init__(self,
               uptime:float = 0.5,
               stacks:float = 4.0,
               **config):
    self.loadConeStats('On the Fall of an Aeon')
    self.setSuperposition(config)
    self.uptime = uptime
    self.stacks = stacks

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'destruction':
      char.percAtk += ( 0.06 + 0.02 * self.superposition ) * self.stacks
      char.Dmg += ( 0.09 + 0.03 * self.superposition ) * self.uptime
    
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  OnTheFallOfAnAeon(**Configuration).print()