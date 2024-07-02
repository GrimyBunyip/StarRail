from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class ForTomorrowsJourney(BaseLightCone):
    def __init__(self,
                 uptime=1.0/3.0,
                superposition:int=None,
                **config):
        self.loadConeStats('For Tomorrow\'s Journey')
        self.setSuperposition(superposition,config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('ATK.percent',description=self.name,amount=0.12 + 0.04 * self.superposition)
            char.addStat('DMG',description=self.name,amount=0.15 + 0.03 * self.superposition,uptime=self.uptime)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    ForTomorrowsJourney(**Configuration).print()