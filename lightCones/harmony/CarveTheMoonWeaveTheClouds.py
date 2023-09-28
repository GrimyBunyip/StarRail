from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class CarveTheMoonWeaveTheClouds(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Carve the Moon, Weave the Clouds')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            pass #harmony cones not yet implemented fully
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    CarveTheMoonWeaveTheClouds(**Configuration).print()