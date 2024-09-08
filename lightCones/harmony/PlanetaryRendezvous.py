from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class PlanetaryRendezvous(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('Planetary Rendezvous')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            def applyTeamBuff(team):
                for char in team:
                    char.addStat(f'DMG.{char.element}',
                                description=f'{self.shortname} from {char.name}',
                                amount=0.09 + 0.03 * self.superposition,)
                    
            char.teamBuffList.append(applyTeamBuff)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    PlanetaryRendezvous(**Configuration).print()