from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class ASecretVow(BaseLightCone):
  baseAtk = 529.2
  baseDef = 463.05
  baseHP = 953

  def __init__(self,
               graphic:str = '',
               shortname:str = 'Secret Vow',
               passiveUptime:float = 0.5,
               **config):
    self.graphic = graphic
    self.shortname = shortname
    self.passiveUptime = passiveUptime
    self.superposition = config['hertaSuperpositions']

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    char.Dmg += 0.15 + 0.05 * self.superposition
    char.Dmg += ( 0.15 + 0.05 * self.superposition ) * self.passiveUptime