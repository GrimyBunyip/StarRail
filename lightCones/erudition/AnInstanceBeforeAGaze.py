from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class AnInstanceBeforeAGaze(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('An Instance Before A Gaze')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CD',description=self.name, amount=0.30 + 0.06 * self. superposition)
            char.addStat('DMG',description=self.name, 
                         amount=(0.0030 + 0.0006 * self. superposition) * min(180.0,char.maxEnergy),
                         type=['ultimate'])
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    AnInstanceBeforeAGaze(**Configuration).print()