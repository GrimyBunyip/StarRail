from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class CarveTheMoonWeaveTheClouds(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('Carve the Moon, Weave the Clouds')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            def applyTeamBuff(team):
                for targetChar in team:
                    targetChar.addStat('ATK.percent',
                                description=f'{self.shortname} from {char.name}',
                                amount=0.075 + 0.025 * self.superposition,
                                uptime=1.0/3.0)
                    targetChar.addStat('CD',
                                description=f'{self.shortname} from {char.name}',
                                amount=0.09 + 0.03 * self.superposition,
                                uptime=1.0/3.0)
                    targetChar.addStat('ER',
                                description=f'{self.shortname} from {char.name}',
                                amount=0.045 + 0.015 * self.superposition,
                                uptime=1.0/3.0)
                    
            char.teamBuffList.append(applyTeamBuff)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    CarveTheMoonWeaveTheClouds(**Configuration).print()