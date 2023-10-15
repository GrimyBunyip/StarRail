from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class IShallBeMyOwnSword(BaseLightCone):
    def __init__(self,
                atkStacks = 3.0,
                defShredUptime:float = 1.0,
                **config):
        self.loadConeStats('I Shall Be My Own Sword')
        self.setSuperposition(config)
        self.atkStacks = atkStacks
        self.defShredUptime = defShredUptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CD',description=self.name,
                                    amount=0.17 + 0.03 * self.superposition)
            char.addStat('DMG',description=self.name,
                                    amount=0.115 + 0.025 * self.superposition,
                                    stacks=self.atkStacks)
            char.addStat('DefShred',description=self.name,
                                    amount=0.1 + 0.02 * self.superposition,
                                    uptime=self.defShredUptime)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    IShallBeMyOwnSword(**Configuration).print()