from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Rappa(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                eidolon:int=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Rappa')
        self.eidolon = self.eidolon if eidolon is None else eidolon
        
        # Motion Values should be set before talents or gear
        # to do: check eidolons
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['enhancedBasic'] = [BaseMV(area='single', stat='atk', value=0.8*2, eidolonThreshold=5, eidolonBonus=0.08*2),
                                                 BaseMV(area='adjacent', stat='atk', value=0.4*2, eidolonThreshold=5, eidolonBonus=0.04*2),
                                                 BaseMV(area='all', stat='atk', value=0.8, eidolonThreshold=5, eidolonBonus=0.08),]

        self.motionValueDict['skill'] = [BaseMV(area='all', stat='atk', value=1.2, eidolonThreshold=3, eidolonBonus=0.12)]

        self.motionValueDict['ultimate'] = [BaseMV(area='all', stat='atk', value=1.6, eidolonThreshold=5, eidolonBonus=0.128)]
        self.motionValueDict['talent'] = [BaseMV(area='single', stat='atk', value=1.8, eidolonThreshold=3, eidolonBonus=0.18)]

        # Talents
        self.addStat('BreakEfficiency',description='Rappa Ult Buff',amount=0.5,type=['enhancedBasic'])
        self.addStat('BreakEffect',description='Rappa Ult Buff',amount=0.3,type=['enhancedBasic'])
        
        # Eidolons
        
        # Gear
        self.equipGear()

    def useTalent(self):
        retval = BaseEffect()
        type = ['talent']
        retval.damage = self.getTotalMotionValue('basic',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        self.addDebugInfo(retval,type)
        return retval

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
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        type = ['basic','enhancedBasic']
        retval.damage = self.getTotalMotionValue('enhancedBasic',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
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
        retval.gauge = 30.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.energy = 5.0 * self.getER(type)
        retval.actionvalue = -1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval
                
    def useSuperBreak(self,baseGauge:float,extraTypes:list=[]):
        retval = BaseEffect()
        type = ['break','superBreak'] + extraTypes

        superBreakDamage = self.breakLevelMultiplier
        superBreakDamage *= 0.6 # trace
        # superBreakDamage *= BREAK_MULTIPLIERS[self.element] # does not seem to scale off type
        superBreakDamage *= self.getBreakEffect(type)
        superBreakDamage *= self.getVulnerability(type)
        superBreakDamage = self.applyDamageMultipliers(superBreakDamage,type)

        retval.damage = superBreakDamage
        # factor in uptime
        retval *= self.weaknessBrokenUptime
        self.addDebugInfo(retval,type,f'Super Break Damage {self.name}')
        
        return retval