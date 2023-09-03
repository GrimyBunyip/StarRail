from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class MessengerTraversingHackerspace2pc(RelicSet):
  def __init__(self,
               graphic:str='',
               shortname:str='Messenger 2pc',
               **config):
    self.graphic = graphic
    self.shortname = shortname

  def equipTo(self, char:BaseCharacter):
    char.percSpd += 0.06
    
class MessengerTraversingHackerspace4pc(RelicSet):
  def __init__(self,
               graphic:str='',
               shortname:str='Messenger 4pc',
               uptime = 0.25,
               **config):
    self.graphic = graphic
    self.shortname = shortname
    self.uptime = uptime

  def equipTo(self, char:BaseCharacter):
    char.percSpd += 0.12 * self.uptime