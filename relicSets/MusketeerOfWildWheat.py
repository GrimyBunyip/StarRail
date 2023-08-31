from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class MusketeerOfWildWheat2pc(RelicSet):
  def __init__(self,
               graphic:str='',
               **config):
    self.graphic = graphic

  def equipTo(self, char:BaseCharacter):
    char.percAtk += 0.12

class MusketeerOfWildWheat4pc(RelicSet):
  def __init__(self,
               graphic:str='',
               **config):
    self.graphic = graphic

  def equipTo(self, char:BaseCharacter):
    char.percSpd += 0.06
    char.basicDmg += 0.10