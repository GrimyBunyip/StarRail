from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class BrokenKeel(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Broken Keel',
                uptime:float = 1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.addStat('RES',description=self.shortname,
                                amount=0.10)
        
        def applyTeamBuff(team):
            for char in team:
                char.addStat('CD',description=f'{self.shortname} from {char.name}',
                             amount=0.10,
                             uptime=self.uptime)
                
        char.teamBuffList.append(applyTeamBuff)