from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class BeforeTheTutorialMissionStarts(BaseLightCone):
    def __init__(self,
                uptime:float = 1.0,
                superposition:int=None,
                **config):
        self.loadConeStats('Before the Tutorial Mission Starts')
        self.setSuperposition(superposition,config)
        self.uptime=uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('EHR',description=self.name,
                                    amount=0.15 + 0.05 * self.superposition)
            char.addStat('BonusEnergyAttack',description=self.name,
                                                    amount=3.0+ 1.0 * self.superposition,
                                                    uptime=self.uptime)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    BeforeTheTutorialMissionStarts(**Configuration).print()