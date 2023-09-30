from baseClasses.BaseCharacter import BaseCharacter
from settings.RelicRolls import RELIC_ATK_MAINSTAT, RELIC_HP_MAINSTAT, RELIC_MAINSTATS, RELIC_SUBSTATS, average

class RelicStats(object):
    def __init__(self, mainstats:list, substats:dict):
        self.mainstats = mainstats
        self.substats = substats

    def equipTo(self, char:BaseCharacter):
        # always add flat ATK and HP, we don't ask the user to input these manually
        char.addStat('ATK.flat',description='Relic Mainstat',amount=RELIC_ATK_MAINSTAT)
        char.addStat('HP.flat',description='Relic Mainstat',amount=RELIC_HP_MAINSTAT)

        for mainstat in self.mainstats:
            char.addStat(mainstat,description='Relic Mainstat',amount=RELIC_MAINSTATS[mainstat])

        for substat, num in self.substats.items():
            char.addStat(substat,description='Relic Substat',amount=average(RELIC_SUBSTATS[substat]),stacks=num)