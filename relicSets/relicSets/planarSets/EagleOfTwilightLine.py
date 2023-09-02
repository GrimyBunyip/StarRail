from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class EagleOfTwilightLine2pc(RelicSet):
  def __init__(self,
               graphic:str='https://static.wikia.nocookie.net/houkai-star-rail/images/3/3f/Item_Eagle_of_Twilight_Line.png',
               shortname:str='Eagle 2pc',
               **config):
    self.graphic = graphic
    self.shortname = shortname

  def equipTo(self, char:BaseCharacter):
    char.windDmg += 0.10

class EagleOfTwilightLine4pc(RelicSet):
  def __init__(self,
               graphic:str='https://static.wikia.nocookie.net/houkai-star-rail/images/3/3f/Item_Eagle_of_Twilight_Line.png',
               shortname:str='Eagle 4pc',
               **config):
    self.graphic = graphic
    self.shortname = shortname

  def equipTo(self, char:BaseCharacter):
    pass # not auto-implementing this for now