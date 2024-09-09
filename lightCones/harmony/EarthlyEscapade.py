from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class EarthlyEscapade(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                uptime:float=1.0,
                **config):
        self.loadConeStats('Earthly Escapade')
        self.setSuperposition(superposition,config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CD',description=self.name,amount=0.25 + 0.07 * self.superposition)
            
            def applyTeamBuff(team):
                for targetChar in team:
                    targetChar.addStat('CR',
                                description=f'{self.shortname} from {char.name}',
                                amount=0.09 + 0.01 * self.superposition,
                                uptime=self.uptime,)
                    targetChar.addStat('CD',
                                description=f'{self.shortname} from {char.name}',
                                amount=0.21 + 0.07 * self.superposition,
                                uptime=self.uptime,)
                    
            char.teamBuffList.append(applyTeamBuff)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    EarthlyEscapade(**Configuration).print()