from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class PanCosmicCommercialEnterprise(RelicSet):
  def __init__(self,
               graphic:str='',
               shortname:str='Pan-Cosmic Commercial Enterprise',
               **config):
    self.graphic = graphic
    self.shortname = shortname

  def equipTo(self, char:BaseCharacter):
    char.EHR += 0.1
    char.percAtk += min(0.25, char.EHR * 0.25) # be wary of sequencing issues, equipping gear is usually done last fortunately