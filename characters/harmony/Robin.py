from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Robin(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                eidolon:int=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Robin')
        self.eidolon = self.eidolon if eidolon is None else eidolon
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['ultimate'] = [BaseMV(area='single', stat='atk', value=1.2, eidolonThreshold=3, eidolonBonus=0.096)]

        # Talents

        # Eidolons
        
        # Gear
        self.equipGear()
        
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
    
    def applyTalentBuff(self,team:list):
        for character in team:
            character.addStat('CD',description='Robin Talent Buff',
                                    amount=0.23 if self.eidolon >= 5 else 0.20)
            character.addStat('CD',description='Robin Trace Buff',
                                    amount=0.25,
                                    type=['followup'])
    
    def applySkillBuff(self,team:list,uptime:float=1.0):
        for character in team:
            character.addStat('DMG',description='Robin Skill Buff',
                                    amount=0.55 if self.eidolon >= 3 else 0.50,
                                    uptime=uptime)
        
    def applyUltBuff(self,team:list,uptime=0.5,type=None,ignoreSpeed=False):
        amount = self.getTotalStat('ATK')
        amount *= 0.2432 if self.eidolon >= 3 else 0.228
        amount += 230 if self.eidolon >= 3 else 200
        for character in team:
            character.addStat('ATK.flat',description='Robin Ultimate Buff',
                                amount=amount,
                                uptime=uptime,
                                type=type)
            
            if self.eidolon >= 1:
                character.addStat('ResPen',description='Robin E1',
                                amount=0.24,
                                uptime=uptime,
                                type=type)
                
            if self.eidolon >= 2 and not ignoreSpeed:
                character.addStat('SPD.percent', description='Robin E2',
                                amount=0.16,
                                uptime=uptime,
                                type=type)

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.energy = ( 35.0 + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.energy = 5.0 * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        retval.actionvalue += self.getTotalStat('SPD') / 90.0 - 1.0 # apply reverse advance for ultimate
        self.addDebugInfo(retval,type)
        return retval
    
    def useAdvanceTrace(self):
        retval = BaseEffect()
        type = ['trace']
        retval.actionvalue = 0.25
        self.addDebugInfo(retval,type)
        return retval
    
    def useTalent(self):
        retval = BaseEffect()
        type = ['talent']
        retval.energy = 3.0 if self.eidolon >= 2 else 2.0
        retval.energy *= self.getER(type)
        self.addDebugInfo(retval,type)
        return retval
    
    def useConcertoDamage(self, deprecatedType:list):
        retval = BaseEffect()
        type = ['additionalDamage']
        retval.damage = self.getTotalMotionValue('ultimate',type)
        retval.damage *= 1.0 + 1.0 * 1.5 # static crit 
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        self.addDebugInfo(retval,type)
        return retval
    
    def useAdvanceForward(self, advanceAmount:float=1.0):
        retval = BaseEffect()
        retval.actionvalue = max(-1.0,-advanceAmount)
        self.addDebugInfo(retval,['Advance Forward'],'Robin Advance Forward')
        return retval
