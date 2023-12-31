from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class TodayIsAnotherPeacefulDay(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Today Is Another Peaceful Day')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('DMG',description=self.name,
                                    amount=(0.0015 + 0.0005 * self.superposition) * min(160.0, char.maxEnergy))
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    TodayIsAnotherPeacefulDay(**Configuration).print()