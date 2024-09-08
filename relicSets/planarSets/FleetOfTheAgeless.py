from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class FleetOfTheAgeless(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Fleet',
                uptime:float = 1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.addStat('HP.percent',description=self.shortname,
                     amount=0.12)
        
        def applyTeamBuff(team):
            for char in team:
                char.addStat('ATK.percent',description=f'{self.shortname} from {char.name}',
                             amount=0.08)
                
        char.teamBuffList.append(applyTeamBuff)