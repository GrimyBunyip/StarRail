from baseClasses.BaseCharacter import BaseCharacter
from settings.RelicRolls import RELIC_ATK_MAINSTAT, RELIC_HP_MAINSTAT, RELIC_MAINSTATS, RELIC_SUBSTATS, average

class RelicStats(object):
  def __init__(self, mainstats:list, substats:dict):
    self.mainstats = mainstats
    self.substats = substats

  def equipTo(self, char:BaseCharacter):
    char.flatAtk += RELIC_ATK_MAINSTAT
    char.flatHP += RELIC_HP_MAINSTAT

    for mainstat in self.mainstats:
      char.__dict__[mainstat] += RELIC_MAINSTATS[mainstat]

    for substat, num in self.substats.items():
      char.__dict__[substat] += average(RELIC_SUBSTATS[substat]) * num