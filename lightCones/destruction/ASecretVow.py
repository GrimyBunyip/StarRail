from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class ASecretVow(BaseLightCone):
    def __init__(self,
                uptime:float = 0.5,
                **config):
        self.loadConeStats('A Secret Vow')
        self.setSuperposition(config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('DMG', description=self.name,
                        amount=0.15 + 0.05 * self.superposition)
            char.addStat('DMG', description=self.name,
                        amount=0.15 + 0.05 * self.superposition,
                        uptime=self.uptime)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    ASecretVow(**Configuration).print()