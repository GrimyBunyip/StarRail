from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class EagleOfTwilightLine2pc(RelicSet):
    def __init__(self,
                graphic:str='https://static.wikia.nocookie.net/houkai-star-rail/images/3/3f/Item_Eagle_of_Twilight_Line.png',
                shortname:str='Eagle 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('DMG',description=self.shortname,
                                amount=0.10,
                                type='wind')

class EagleOfTwilightLine4pc(RelicSet):
    def __init__(self,
                graphic:str='https://static.wikia.nocookie.net/houkai-star-rail/images/3/3f/Item_Eagle_of_Twilight_Line.png',
                shortname:str='Eagle 4pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('AdvanceForward',description=self.shortname,
                                amount=0.25,
                                type='ultimate')