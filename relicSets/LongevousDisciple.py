from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class LongevousDisciple2pc(RelicSet):
  def __init__(self,
               graphic:str='',
               **config):
    self.graphic = graphic

  def equipTo(self, char:BaseCharacter):
    char.percHP += 0.12
    
class LongevousDisciple4pc(RelicSet):
  def __init__(self,
               graphic:str='',
               passiveUptime = 1.0,
               **config):
    self.graphic = graphic
    self.passiveUptime = passiveUptime

  def equipTo(self, char:BaseCharacter):
    char.CR += 0.16 * self.passiveUptime