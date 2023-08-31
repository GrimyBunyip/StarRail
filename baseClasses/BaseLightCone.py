from baseClasses.BaseCharacter import BaseCharacter

class BaseLightCone(object):
  graphic = ''

  baseAtk = 0.0
  baseDef = 0.0
  baseHp = 0.0

  def addBaseStats(self, char:BaseCharacter):
    char.baseAtk += self.baseAtk
    char.baseDef += self.baseDef
    char.baseHP += self.baseHP
    char.lightcone = self

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)