from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class CruisingInTheStellarSea(BaseLightCone):
  baseAtk = 529.2
  baseDef = 463.05
  baseHP = 953

  def __init__(self,
               graphic:str = 'https://static.wikia.nocookie.net/houkai-star-rail/images/2/2a/Light_Cone_Cruising_in_the_Stellar_Sea.png',
               shortname:str = 'Cruising',
               passiveUptime:float = 0.5,
               **config):
    self.graphic = graphic
    self.shortname = shortname
    self.passiveUptime = passiveUptime
    self.superposition = config['hertaSuperpositions']

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    char.CR += 0.06 + 0.02 * self.superposition
    char.CR += (0.06 + 0.02 * self.superposition) * self.passiveUptime