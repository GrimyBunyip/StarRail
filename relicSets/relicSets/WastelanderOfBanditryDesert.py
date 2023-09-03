from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class WastelanderOfBanditryDesert2pc(RelicSet):
  def __init__(self,
               graphic:str='',
               shortname:str = 'Wastelander 2pc',
               **config):
    self.graphic = graphic
    self.shortname = shortname

  def equipTo(self, char:BaseCharacter):
    char.imagDmg += 0.16
    
class WastelanderOfBanditryDesert4pc(RelicSet):
  def __init__(self,
               graphic:str='',
               shortname:str = 'Wastelander 4pc',
               uptimeCR:float = 1.0,
               uptimeCD:float = 0.25,
               **config):
    self.graphic = graphic
    self.shortname = shortname
    self.uptimeCR = uptimeCR
    self.uptimeCD = uptimeCD

  def equipTo(self, char:BaseCharacter):
    char.CR += 0.10 * self.uptimeCR
    char.CD += 0.20 * self.uptimeCD