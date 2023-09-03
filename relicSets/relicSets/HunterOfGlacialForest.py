from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class HunterOfGlacialForest2pc(RelicSet):
  def __init__(self,
               graphic:str='',
               shortname:str = 'Glacial 2pc',
               **config):
    self.graphic = graphic
    self.shortname = shortname

  def equipTo(self, char:BaseCharacter):
    char.iceDmg += 0.10
    
class HunterOfGlacialForest4pc(RelicSet):
  def __init__(self,
               graphic:str='',
               shortname:str = 'Glacial 4pc',
               uptime = 1.0,
               **config):
    self.graphic = graphic
    self.shortname = shortname
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    char.CD += 0.25 * self.uptime