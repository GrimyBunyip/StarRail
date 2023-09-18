from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class MeshingCogs(BaseLightCone):
  def __init__(self,
               **config):
    self.loadConeStats('Meshing Cogs')
    self.setSuperposition(config)

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'harmony':
      pass #harmony cones not yet implemented fully
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  MeshingCogs(**Configuration).print()