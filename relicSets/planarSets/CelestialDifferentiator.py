from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class CelestialDifferentiator(RelicSet):
  def __init__(self,
               graphic:str='',
               shortname:str='Celestial Differentiator',
               uptime:float = 0.0,
               **config):
    self.graphic = graphic
    self.shortname = shortname
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    char.CD += 0.16
    char.CR += 0.6 * self.uptime