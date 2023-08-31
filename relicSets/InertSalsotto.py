from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class InertSalsotto(RelicSet):
  def __init__(self,
               graphic:str='',
               shortname:str='Inert Salsotto',
               passiveUptime:float = 1.0,
               **config):
    self.graphic = graphic
    self.shortname = shortname
    self.passiveUptime = passiveUptime

  def equipTo(self, char:BaseCharacter):
    char.CR += 0.08
    char.ultDmg += 0.15 * self.passiveUptime
    char.followupDmg += 0.15 * self.passiveUptime