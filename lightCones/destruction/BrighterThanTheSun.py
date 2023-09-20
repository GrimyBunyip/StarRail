from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class BrighterThanTheSun(BaseLightCone):
  def __init__(self,
               uptime:float = 1.0,
               stacks:float = 2.0,
               **config):
    self.loadConeStats('Brighter Than the Sun')
    self.setSuperposition(config)
    self.uptime = uptime
    self.stacks = stacks

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == self.path:
      char.CR += 0.15 + 0.03 * self.superposition
      char.percAtk += ( 0.15 + 0.03 * self.superposition ) * self.stacks * self.uptime
      char.ER += ( 0.05 + 0.01 * self.superposition ) * self.stacks * self.uptime
    
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  BrighterThanTheSun(**Configuration).print()