from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Bronya(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Bronya')

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['followup'] = [BaseMV(area='single', stat='atk', value=0.8)]

        # Talents
        self.addStat('AdvanceForward',description='talent',
                     amount=0.33 if self.eidolon >= 3 else 0.3,
                     type=['basic'])
        self.addStat('CR',description='Bronya Trace',amount=1.0,type=['basic'])

        # Eidolons
        
        # Gear
        self.equipGear()
        
    def applyTraceBuff(self,team:list):
        for character in team:
            character:BaseCharacter
            character.addStat('DMG',description='Bronya Trace',amount=0.1)
             
    def applyUltBuff(self,character:BaseCharacter,uptime:float):
        character.addStat('ATK.percent',description='Bronya Ult',
                            amount=0.594 if self.eidolon >= 3 else 0.55,
                            uptime=uptime)
        character.addStat('CD',description='Bronya Ult',
                            amount=((0.168 * self.getTotalStat('CD') + 0.216) if self.eidolon >= 3 else (0.16 * self.getTotalStat('CD') + 0.2)),
                            uptime=uptime)
        
    def applySkillBuff(self,character:BaseCharacter,uptime:float):
        character.addStat('DMG',description='Bronya Skill',
                            amount=0.726 if self.eidolon >= 5 else 0.66,
                            uptime=uptime)
        
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
        retval.skillpoints = -1.0 + (0.5 if self.eidolon >= 1 else 0.0)
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self, targetCharacter:BaseCharacter = None):
        retval = BaseEffect()
        type = ['ultimate']
        retval.energy = 5.0 * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval
        
    def useFollowup(self):
        retval = BaseEffect()
        type = ['basic','followup']
        retval.damage = self.getTotalMotionValue('basic',type) * 0.8
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        self.addDebugInfo(retval,type,'Bronya Followup')
        return retval
    
    def useAdvanceForward(self, advanceAmount:float=1.0):
        retval = BaseEffect()
        retval.actionvalue = max(-1.0,-advanceAmount)
        self.addDebugInfo(retval,['Advance Forward'],'Bronya Advance Forward')
        return retval