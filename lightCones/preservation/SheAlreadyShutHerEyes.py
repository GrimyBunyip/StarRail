from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class SheAlreadyShutHerEyes(BaseLightCone):
    def __init__(self,
                uptime:float=1.0,
                **config):
        self.loadConeStats('She Already Shut Her Eyes')
        self.setSuperposition(config)
        self.uptime=uptime

    def equipTo(self, char:BaseCharacter):
        self.addBaseStats(char)
        if char.path == self.path:
            char.percHP += 0.2 + 0.04 * self.superposition
            char.ER += 0.1 + 0.02 * self.superposition
            char.Dmg += ( 0.075 + 0.015 * self.superposition ) * self.uptime
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    SheAlreadyShutHerEyes(**Configuration).print()