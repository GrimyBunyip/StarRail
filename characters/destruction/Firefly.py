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
                attackForTalent:float=2900,
                breakEffectMV:float=3.6,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Firefly')
        self.attackForTalent=attackForTalent
        self.breakEffectMV=breakEffectMV
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['enhancedBasic'] = [BaseMV(area='single', stat='atk', value=2.0, eidolonThreshold=3, eidolonBonus=0.2)]

        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=2.0, eidolonThreshold=3, eidolonBonus=0.20)]
        self.motionValueDict['enhancedSkill'] = [BaseMV(area='single', stat='atk', value=2.0+0.2*self.breakEffectMV, eidolonThreshold=3, eidolonBonus=0.2),
                                                BaseMV(area='adjacent', stat='atk', value=2.0+0.1*self.breakEffectMV, eidolonThreshold=3, eidolonBonus=0.16)]

        self.motionValueDict['ultimate'] = [BaseMV(area='single', stat='atk', value=3.2, eidolonThreshold=5, eidolonBonus=0.256),
                                            BaseMV(area='adjacent', stat='atk', value=1.6, eidolonThreshold=5, eidolonBonus=0.128)]
        
        # Talents
        self.addStat('BreakEffect',description='Firefly Talent',amount=(attackForTalent-1600)*0.1/100)
        
        # Eidolons

        # Gear
        self.equipGear()
        
    def applyUltVulnerability(self,team:list,uptime=None):
        uptime = self.weaknessBrokenUptime if uptime is None else uptime
        for character in team:
            character.addStat('Vulnerability',description='Firefly Ult',
                         amount=0.225 if self.eidolon >= 5 else 0.20833,
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
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
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
        retval.energy = ( 144.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
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
                
    def useSuperBreak(self):
        retval = BaseEffect()
        type = ['break','superBreak']

        totalBreakEffect = self.getTotalStat('BreakEffect')
        superBreakDamage = self.breakLevelMultiplier
        superBreakDamage *= 0.5 if totalBreakEffect >= 3.6 else (0.35 if totalBreakEffect >= 2.0 else 0.0)
        # superBreakDamage *= BREAK_MULTIPLIERS[self.element] # does not seem to scale off type
        superBreakDamage *= self.getBreakEffect(type)
        superBreakDamage *= self.getVulnerability(type)
        superBreakDamage = self.applyDamageMultipliers(superBreakDamage,type)

        retval.damage = superBreakDamage
        self.addDebugInfo(retval,type,f'Super Break Damage {self.name}')
        
        # factor in uptime
        retval *= self.weaknessBrokenUptime
        return retval
    
    def extraTurn(self,advanceType=['skill','enhancedSkill'],setSpeed=None):
        retval = BaseEffect()
        type = ['Firefly Advance Forward']
        retval.actionvalue = -(1.0 + self.getAdvanceForward(advanceType))
        self.addDebugInfo(retval,type,'Firefly Advance Forward 100%')
        return retval