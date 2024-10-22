from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class LongRoadLeadsHome(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('Long Road Leads Home', shortname='Long Road')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        char.addStat('BreakEffect', description=self.name, amount=0.50 + 0.10 * self.superposition)
        if char.path == self.path:
            def applyTeamBuff(team):
                for char in team:
                    char.addStat('Vulnerability',
                                description=f'{self.shortname} from {char.name}',
                                amount=0.175 + 0.025 * self.superposition,
                                type=['Break'])
                    
            char.teamBuffList.append(applyTeamBuff)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    LongRoadLeadsHome(**Configuration).print()