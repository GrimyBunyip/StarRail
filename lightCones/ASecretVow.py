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
    char.basicDmg += 0.40
    char.skillDmg += 0.40
    char.ultDmg += 0.40
    char.followupDmg += 0.40
    char.dotDmg += 0.40
    char.basicDmg += 0.40 * self.passiveUptime
    char.skillDmg += 0.40 * self.passiveUptime
    char.ultDmg += 0.40 * self.passiveUptime
    char.followupDmg += 0.40 * self.passiveUptime
    char.dotDmg += 0.40 * self.passiveUptime