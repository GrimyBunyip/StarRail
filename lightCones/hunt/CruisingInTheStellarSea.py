from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class CruisingInTheStellarSea(BaseLightCone):
    def __init__(self,
                uptimeHP:float = 0.5,
                uptimeDefeat:float = 0.5,
                **config):
        self.loadConeStats('Cruising in the Stellar Sea')
        self.setSuperposition(config)
        self.uptimeHP = uptimeHP
        self.uptimeDefeat = uptimeDefeat

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.CR += 0.06 + 0.02 * self.superposition
            char.CR += (0.06 + 0.02 * self.superposition) * self.uptimeHP
            char.percAtk += (0.15 + 0.05 * self.superposition) * self.uptimeDefeat
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    CruisingInTheStellarSea(**Configuration).print()