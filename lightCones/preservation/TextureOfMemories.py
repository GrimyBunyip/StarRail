from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class TextureOfMemories(BaseLightCone):
  def __init__(self,
               uptime:float,
               **config):
    self.loadConeStats('TextureOfMemories')
    self.setSuperposition(config)
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'preservation':
      char.Res += 0.06 + 0.02 * self.superposition
      char.dmgReduction += ( 0.09 + 0.03 * self.superposition ) * self.uptime
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  TextureOfMemories(**Configuration).print()