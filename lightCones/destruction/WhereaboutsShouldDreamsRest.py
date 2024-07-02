from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class WhereaboutsShouldDreamsRest(BaseLightCone):
    def __init__(self,
                uptime:float = 1.0,
                superposition:int=None,
                **config):
        self.loadConeStats('Whereabouts Should Dreams Rest', shortname='Whereabouts')
        self.setSuperposition(superposition,config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('Vulnerability', description=self.name,
                        amount=0.2 + 0.04 * self.superposition,
                        uptime=self.uptime,
                        type=['break'])
            char.addStat('BreakEffect', description=self.name,
                        amount=0.50 + 0.10 * self.superposition)