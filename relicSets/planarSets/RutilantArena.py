from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class RutilantArena(RelicSet):
  def __init__(self,
               graphic:str='',
               shortname:str='Rutilant Arena',
               uptime:float=1.0,
               **config):
    self.graphic = graphic
    self.shortname = shortname
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    char.CR += 0.08
    char.DmgType['basic'] += 0.20 * self.uptime
    char.DmgType['skill'] += 0.20 * self.uptime