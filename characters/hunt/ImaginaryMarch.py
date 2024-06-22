from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class ImaginaryMarch(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                master:BaseCharacter,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                e1Uptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Imaginary March 7th')
        self.e1Uptime = e1Uptime
        self.master=master
        
        skillMV = 0.0
        if self.master.path == 'hunt' in ['erudition', 'destruction', 'hunt']:
            skillMV = 0.22 if self.eidolon >= 3 else 0.2
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0 + skillMV, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['enhancedBasic'] = [BaseMV(area='single', stat='atk', value=1.0 + skillMV, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['followup'] = [BaseMV(area='single', stat='atk', value=0.6 + skillMV)]

        self.motionValueDict['ultimate'] = [BaseMV(area='single', stat='atk', value=2.4, eidolonThreshold=5, eidolonBonus=0.192)]
        

        # Talents
        self.addStat('DMG',description='March 7th Talent',
                     amount=0.88 if self.eidolon >= 5 else 0.8,
                     type=['enhancedBasic'])
        self.addStat('SPD.percent',description='March 7th Talent',amount=0.1)
        
        # Eidolons
        if self.eidolon >= 1:
            self.addStat('CD',description='March 7th E1',
                         amount=0.36,
                         uptime=self.e1Uptime,
                         type=['enhancedBasic'])
            
        if self.eidolon >= 4:
            self.addStat('BonusEnergyAttack',description='March 7th E4',amount=5.0,type=['basic','skill','enhancedBasic'])
        
        # Gear
        self.equipGear()
        
    def applySkillBuff(self,target:BaseCharacter):
        target.addStat('SPD.percent',description='March 7th Skill Buff',amount=0.1)
        
    def applyE6Buff(self,target:BaseCharacter,uptime:float=1.0):
        if self.eidolon >= 6:
            target.addStat('CD',description='March 7th e6 buff',amount=0.6,uptime=uptime)
            target.addStat('BreakEffect',description='March 7th e6 buff',amount=0.36,uptime=uptime)
        
    def useBasic(self):
        skillGauge = 1.0
        if self.master.path == 'hunt' in ['harmony', 'nihility', 'preservation', 'abundance']:
            skillGauge = 2.0
            
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type) * skillGauge
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useEnhancedBasic(self, actionValue:float=1.0, numHits:float=1.0, chance:float=0.6):
        skillGauge = 1.0
        if self.master.path == 'hunt' in ['harmony', 'nihility', 'preservation', 'abundance']:
            skillGauge = 2.0
            
        retval = BaseEffect()
        type = ['enhancedBasic']
        
        extraHits = chance * (1.0 - chance) + 2 * (1.0 - chance) * chance ** 2 + 3 * chance ** 3
        
        retval.damage = self.getTotalMotionValue('enhancedBasic',type) * (numHits + extraHits)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 15.0 * self.getBreakEfficiency(type) * numHits * skillGauge
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 0.0
        retval.actionvalue = actionValue - self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 90.0 * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useFollowup(self):
        skillGauge = 1.0
        if self.master.path == 'hunt' in ['harmony', 'nihility', 'preservation', 'abundance']:
            skillGauge = 2.0
            
        retval = BaseEffect()
        type = ['followup']
        retval.damage = self.getTotalMotionValue('followup',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 15.0 * self.getBreakEfficiency(type) * skillGauge
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = 0.0 - self.getAdvanceForward(type)    
        self.addDebugInfo(retval,type)    
        return retval