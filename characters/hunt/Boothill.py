from baseClasses.BaseCharacter import BREAK_MULTIPLIERS, BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Boothill(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                trickshotChance:float=0.5,
                standoffUptime:float=1.0,
                trickshotStacks:int=3,
                breakEffect:float=3.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Boothill')
        self.trickshotChance = trickshotChance
        self.standoffUptime = standoffUptime
        self.trickshotStacks = trickshotStacks

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['enhancedBasic'] = [BaseMV(area='single', stat='atk', value=2.2, eidolonThreshold=3, eidolonBonus=0.22)]
        self.motionValueDict['ultimate'] = [BaseMV(area='single', stat='atk', value=4.0, eidolonThreshold=3, eidolonBonus=0.32)]

        # Talents
        self.addStat('BreakEfficiency',description='Boothill Talent',amount=0.5,stacks=3.0)
        
        self.addStat('BonusEnergyAttack',description='Boothill Point Blank Talent Energy',
                     amount=10.0,
                     uptime=self.trickshotChance)
        self.addStat('Vulnerability',description='Boothill Standoff Vulnerability',
                     amount=0.33 if self.eidolon >= 5 else 0.3,
                     uptime=self.standoffUptime)
        
        self.addStat('CR',description='Ghost Load',amount=min(breakEffect * 0.1, 0.1))
        self.addStat('CD',description='Ghost Load',amount=min(breakEffect * 0.5, 1.5))

        # Eidolons
        
        # Gear
        self.equipGear()
        
    def useBasic(self, slowed = True):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type) + ( 0.40 if slowed else 0.0 ) #    High Gale
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
        retval.skillpoints = -1.0
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
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
    
        breakEffect = BaseEffect()
        breakType = ['break']

        baseDotDamage = self.breakLevelMultiplier
        baseDotDamage *= 1.7 if self.trickshotStacks >= 3 else 1.2 if self.trickshotStacks == 2 else 0.7
        baseDotDamage *= 0.5 + min(self.enemyToughness, 30.0*16) / 120
        baseDotDamage *= self.weaknessBrokenUptime
        baseDotDamage *= BREAK_MULTIPLIERS[self.element]
        baseDotDamage *= self.getBreakEffect(breakType)
        baseDotDamage *= self.getVulnerability(breakType)
        baseDotDamage = self.applyDamageMultipliers(baseDotDamage,breakType)

        retval.damage = baseDotDamage
        self.addDebugInfo(breakEffect,breakType,'Break Damage')
        retval += breakEffect
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
