from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class FirmamentFrontlineGlamoth(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Firmament',
                stacks:int = 1,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        char.addStat('ATK.percent',description=self.shortname,
                                amount=0.12)
        if self.stacks == 1:
            char.addStat('DMG',description=self.shortname,
                                amount=0.12)
        elif self.stacks == 2:
            char.addStat('DMG',description=self.shortname,
                                amount=0.20)