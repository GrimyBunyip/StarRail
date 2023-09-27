from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class ASecretVow(BaseLightCone):
    def __init__(self,
                uptime:float = 0.5,
                **config):
        self.loadConeStats('A Secret Vow')
        self.setSuperposition(config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addBaseStats(char)
        if char.path == self.path:
            char.Dmg += 0.15 + 0.05 * self.superposition
            char.Dmg += ( 0.15 + 0.05 * self.superposition ) * self.uptime
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    ASecretVow(**Configuration).print()