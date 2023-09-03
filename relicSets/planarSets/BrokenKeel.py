from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class BrokenKeel(RelicSet):
  def __init__(self,
               graphic:str='',
               shortname:str='Broken Keel',
               uptime:float = 1.0,
               **config):
    self.graphic = graphic
    self.shortname = shortname
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    char.Res += 0.10
    char.CD += 0.10
    # party wide buffs not yet implemented