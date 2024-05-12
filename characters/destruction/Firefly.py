from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from baseClasses.BaseMV import BaseMV

class Firefly(BaseCharacter):

    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                breakEffectMV:float=3.6,
                breakEffectTalent:float=0.6,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Firefly')
        self.breakEffectMV = min(3.6,breakEffectMV)
        self.breakEffectTalent = min(0.6,breakEffectTalent)
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['enhancedBasic'] = [BaseMV(area='single', stat='atk', value=2.5, eidolonThreshold=3, eidolonBonus=0.2)]

        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=2.5, eidolonThreshold=3, eidolonBonus=0.25)]
        self.motionValueDict['enhancedSkill'] = [BaseMV(area='single', stat='atk', value=4.0+0.5*self.breakEffectMV, eidolonThreshold=3, eidolonBonus=0.32),
                                                BaseMV(area='adjacent', stat='atk', value=2.0+0.25*self.breakEffectMV, eidolonThreshold=3, eidolonBonus=0.16)]

        self.motionValueDict['ultimate'] = [BaseMV(area='single', stat='atk', value=3.2, eidolonThreshold=5, eidolonBonus=0.256),
                                            BaseMV(area='adjacent', stat='atk', value=1.6, eidolonThreshold=5, eidolonBonus=0.128)]
        
        # Talents
        self.addStat('DefShred',description='Firefly Talent',
                     amount=0.40 if self.breakEffectMV >= 3.6 else 0.30 if self.breakEffectMV >= 2.5 else 0.0,
                     type=['enhancedSkill','enhancedBasic'])
        self.addStat('BreakEffect',description='Firefly Talent', amount=breakEffectTalent)
        
        # Eidolons

        # Gear
        self.equipGear()
        
    def applyUltVulnerability(self,team:list,uptime=None):
        uptime = self.weaknessBrokenUptime if uptime is None else uptime
        for character in team:
            self.addStat('Vulnerability',description='Firefly Ult',
                         amount=0.1296 if self.eidolon >= 5 else 0.12,
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

    def useEnhancedBasic(self):
        retval = BaseEffect()
        type = ['basic','enhancedBasic']
        retval.damage = self.getTotalMotionValue('enhancedBasic',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 45.0 * self.getBreakEfficiency(type)
        retval.energy = ( 0.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = (1.0 + self.getAdvanceForward(type)) * self.getModifiedAV()
        self.addDebugInfo(retval,type)
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 120.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useEnhancedSkill(self, setSpeed=None):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        type = ['skill','enhancedSkill']
        retval.damage = self.getTotalMotionValue('enhancedSkill',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 90.0 + 45.0 * num_adjacents ) * self.getBreakEfficiency(type)
        retval.energy = ( 0.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = (1.0 + self.getAdvanceForward(type)) * self.getModifiedAV(setSpeed=setSpeed)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.energy = 5.0 * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval
    
    def getModifiedAV(self, setSpeed=None):
        # returns the approximate Action Value cost of an enhanced skill or basic
        # apply this to extra turn as well for simplicity
        speed = self.getTotalStat('SPD')
        newSpeed = (speed +(55.0 if self.eidolon >= 5 else 50.0)) if setSpeed is None else setSpeed
        actionValue = speed / newSpeed
        return actionValue
    
    def extraTurn(self,advanceType=['skill','enhancedSkill'],setSpeed=None):
        retval = BaseEffect()
        type = ['Firefly Advance Forward']
        retval.actionvalue = -(1.0 + self.getAdvanceForward(advanceType)) * self.getModifiedAV(setSpeed=setSpeed)
        self.addDebugInfo(retval,type,'Firefly Advance Forward 100%')
        return retval        