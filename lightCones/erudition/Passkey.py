from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class Passkey(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('Passkey')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('BonusEnergyAttack',description=self.name,
                         amount=7.0 + 1.0 * self.superposition,
                         type=['skill'])
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    Passkey(**Configuration).print()