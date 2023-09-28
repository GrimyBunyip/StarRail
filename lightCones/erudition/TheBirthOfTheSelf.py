from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class TheBirthOfTheSelf(BaseLightCone):
    def __init__(self,
                uptime:float=0.5,
                **config):
        self.loadConeStats('The Birth of the Self')
        self.setSuperposition(config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('DMG',description=self.name,
                                    amount=0.24 + 0.06 * self.superposition,
                                    type='followup')
            char.addStat('DMG',description=self.name,
                                    amount=0.24 + 0.06 * self.superposition,
                                    type='followup',
                                    uptime=self.uptime)

if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    TheBirthOfTheSelf(**Configuration).print()