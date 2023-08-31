from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class HunterOfGlacialForest2pc(RelicSet):
  def __init__(self,
               graphic:str='',
               **config):
    self.graphic = graphic

  def equipTo(self, char:BaseCharacter):
    char.iceDmg += 0.10
    
class HunterOfGlacialForest4pc(RelicSet):
  def __init__(self,
               graphic:str='',
               passiveUptime = 1.0,
               **config):
    self.graphic = graphic
    self.passiveUptime = passiveUptime

  def equipTo(self, char:BaseCharacter):
    char.CD += 0.25 * self.passiveUptime