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
        
        def applyTeamBuff(team):
            for char in team:
                char.addStat('ATK.percent',description=self.shortname,
                             amount=0.08)
                
        self.applyTeamBuff = applyTeamBuff

    def equipTo(self, char:BaseCharacter):
        char.teamBuffList.append(self.applyTeamBuff)
        char.addStat('HP.percent',description=self.shortname,
                     amount=0.12)