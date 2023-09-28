from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class ButTheBattleIsntOver(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('But the Battle Isn\'t Over')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.stats['ER'].append(BuffEffect(description=self.name,
                                    amount=0.08 + 0.02 * self.superposition))
            pass #harmony cones not yet implemented fully
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    ButTheBattleIsntOver(**Configuration).print()