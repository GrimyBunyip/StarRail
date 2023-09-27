from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class BeforeTheTutorialMissionStarts(BaseLightCone):
    def __init__(self,
                uptime:float = 1.0,
                **config):
        self.loadConeStats('Before the Tutorial Mission Starts')
        self.setSuperposition(config)
        self.uptime=uptime

    def equipTo(self, char:BaseCharacter):
        self.addBaseStats(char)
        if char.path == self.path:
            char.EHR += 0.15 + 0.05 * self.superposition
            # this implementation could be tricky if some of these skills are not attacks
            char.bonusEnergyAttack['basic'] += ( 3.0+ 1.0 * self.superposition ) * self.uptime
            char.bonusEnergyAttack['skill'] += ( 3.0+ 1.0 * self.superposition ) * self.uptime
            char.bonusEnergyAttack['ultimate'] += ( 3.0+ 1.0 * self.superposition ) * self.uptime
            char.bonusEnergyAttack['talent'] += ( 3.0+ 1.0 * self.superposition ) * self.uptime
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    BeforeTheTutorialMissionStarts(**Configuration).print()