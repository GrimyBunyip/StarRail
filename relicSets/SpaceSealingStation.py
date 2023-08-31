from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class SpaceSealingStation(RelicSet):
  def __init__(self,
               graphic:str='https://static.wikia.nocookie.net/houkai-star-rail/images/7/78/Item_Space_Sealing_Station.png',
               passiveUptime:float = 1.0,
               **config):
    self.graphic = graphic
    self.passiveUptime = passiveUptime

  def equipTo(self, char:BaseCharacter):
    char.percAtk += 0.12
    char.percAtk += 0.12 * self.passiveUptime