from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class SheAlreadyShutHerEyes(BaseLightCone):
    def __init__(self,
                uptime:float=1.0,
                **config):
        self.loadConeStats('She Already Shut Her Eyes')
        self.setSuperposition(config)
        self.uptime=uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.stats['HP'].append(BuffEffect(description=self.name,
                                    amount=0.2 + 0.04 * self.superposition,
                                    mathType='percent'))
            char.stats['ER'].append(BuffEffect(description=self.name,
                                    amount=0.1 + 0.02 * self.superposition))
            char.stats['DMG'].append(BuffEffect(description=self.name,
                                    amount=0.075 + 0.015 * self.superposition,
                                    uptime=self.uptime))
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    SheAlreadyShutHerEyes(**Configuration).print()