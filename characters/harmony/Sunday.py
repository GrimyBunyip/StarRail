from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Sunday(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Sunday')

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]

        # Talents

        # Eidolons
        
        # Gear
        self.equipGear()
        
    def applyTraceBuff(self,team:list):
        for character in team:
            character:BaseCharacter
            character.addStat('DMG',description='Sunday Trace',amount=0.1)
             
    def applyUltBuff(self,character:BaseCharacter,uptime:float):
        character.addStat('CD',description='Sunday Ult',
                            amount=((0.28 * self.getTotalStat('CD') + 0.0832) if self.eidolon >= 3 else (0.25 * self.getTotalStat('CD') + 0.08)),
                            uptime=uptime)
        
    def applySkillBuff(self,character:BaseCharacter,uptime:float,type:list=None,hasSummon:bool=False):
        character.addStat('DMG',description='Sunday Skill',
                            amount=(0.4 if self.eidolon >= 5 else 0.44) * (2.0 if hasSummon else 1.0),
                            uptime=uptime, type=type)
        character.addStat('CR',description='Sunday Talent',
                            amount=0.22 if self.eidolon >= 5 else 0.2,
                            uptime=uptime, type=type)
        
    def useBasic(self):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.energy = ( 30.0 + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -0.5
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.energy = 5.0 * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval
    
    def useAdvanceForward(self, advanceAmount:float=1.0):
        retval = BaseEffect()
        retval.actionvalue = max(-1.0,-advanceAmount)
        self.addDebugInfo(retval,['Advance Forward'],'Sunday Advance Forward')
        return retval
    
    def giveUltEnergy(self,target:BaseCharacter):
        retval = BaseEffect()
        retval.energy = 0.2 * target.maxEnergy
        self.addDebugInfo(retval,['Huohuo Energy'],'Huohuo Ult Energy')
        return retval