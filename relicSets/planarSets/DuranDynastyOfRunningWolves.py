from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class DuranDynastyOfRunningWolves(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Duran',
                stacks:float = 6.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        char.addStat('DMG',description=self.shortname,
                                amount=0.04,
                                stacks=self.stacks,
                                type=['followup'])
        if self.stacks >= 6:
            char.addStat('CD',description=self.shortname,
                                amount=0.24)
        # party wide buffs not yet implemented