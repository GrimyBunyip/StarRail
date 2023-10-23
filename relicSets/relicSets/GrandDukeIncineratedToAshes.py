from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class GrandDuke2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Grand Duke 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('DMG',description=self.shortname,
                                amount=0.18,type=['followup'])
        
class GrandDuke4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Grand Duke 4pc',
                followupStacks = 4.0,
                stacks = 7.0,
                uptime = 0.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.followupStacks = min(7.0,followupStacks)
        self.stacks = min(7.0,stacks)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        # buff applied to followup attacks
        char.addStat('ATK.percent',description=self.shortname,
                                amount=0.06,stacks=self.followupStacks,type=['followup'])
        # may need to tweak this for characters that aren't jing yuan or similar
        char.addStat('ATK.percent',description=self.shortname,
                     amount=0.06,stacks=self.stacks,uptime=self.uptime,type=['basic'])
        char.addStat('ATK.percent',description=self.shortname,
                     amount=0.06,stacks=self.stacks,uptime=self.uptime,type=['skill'])
        char.addStat('ATK.percent',description=self.shortname,
                     amount=0.06,stacks=self.stacks,uptime=self.uptime,type=['ultimate'])