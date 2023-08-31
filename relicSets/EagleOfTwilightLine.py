from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class EagleOfTwilightLine2pc(RelicSet):
  def __init__(self,
               graphic:str='https://static.wikia.nocookie.net/houkai-star-rail/images/3/3f/Item_Eagle_of_Twilight_Line.png',
               **config):
    self.graphic = graphic

  def equipTo(self, char:BaseCharacter):
    char.windDmg += 0.10

class EagleOfTwilightLine4pc(RelicSet):
  def __init__(self,
               graphic:str='https://static.wikia.nocookie.net/houkai-star-rail/images/3/3f/Item_Eagle_of_Twilight_Line.png',
               **config):
    self.graphic = graphic

  def equipTo(self, char:BaseCharacter):
    pass # not auto-implementing this for now