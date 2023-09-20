from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class PlanetaryRendezvous(BaseLightCone):
  def __init__(self,
               **config):
    self.loadConeStats('Planetary Rendezvous')
    self.setSuperposition(config)

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == self.path:
      pass #harmony cones not yet implemented fully
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  PlanetaryRendezvous(**Configuration).print()