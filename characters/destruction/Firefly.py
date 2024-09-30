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
                eidolon:int=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Firefly')
        self.eidolon = self.eidolon if eidolon is None else eidolon
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['enhancedBasic'] = [BaseMV(area='single', stat='atk', value=2.0, eidolonThreshold=3, eidolonBonus=0.2)]

        # Talents
        self.addStat('BreakEfficiency',description='Firefly Ultimate BreakEfficiency', amount=0.5, type=['enhancedBasic','enhancedSkill'])
        
        # Eidolons
        if self.eidolon >= 1:
            self.addStat('DefShred',description='Firefly E1', amount=0.15, type=['enhancedSkill'])

        # Gear
        self.equipGear()
        
        # Team Buffs
        def addBreakEffectTalent(team:list=[]):
            self.addStat('BreakEffect',description='Firefly Talent',amount=(self.getTotalStat('ATK')-1800)*0.008/10)
            breakEffectMV = self.getBreakEffect()

            self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=2.0, eidolonThreshold=3, eidolonBonus=0.20)]
            self.motionValueDict['enhancedSkill'] = [BaseMV(area='single', stat='atk', value=2.0+0.2*breakEffectMV, eidolonThreshold=3, eidolonBonus=0.2),
                                                    BaseMV(area='adjacent', stat='atk', value=1.0+0.1*breakEffectMV, eidolonThreshold=3, eidolonBonus=0.1)]
                    
        self.teamBuffList.append(addBreakEffectTalent)

        
    def applyUltVulnerability(self):
        self.addStat('Vulnerability',description='Firefly Ult Vulnerability',
                        amount=0.22 if self.eidolon >= 5 else 0.20,
                        type=['break'])

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
        retval.energy = ( 240.0 * (0.55 if self.eidolon >= 3 else 0.5) + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useEnhancedSkill(self):
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
        retval.skillpoints = 0.0 if self.eidolon >= 1 else -1.0
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
                
    def useSuperBreak(self,extraTypes:list=[]):
        retval = BaseEffect()
        type = ['break','superBreak'] + extraTypes

        totalBreakEffect = self.getTotalStat('BreakEffect')
        superBreakDamage = self.breakLevelMultiplier
        superBreakDamage *= 0.5 if totalBreakEffect >= 3.6 else (0.35 if totalBreakEffect >= 2.0 else 0.0)
        # superBreakDamage *= BREAK_MULTIPLIERS[self.element] # does not seem to scale off type
        superBreakDamage *= self.getBreakEffect(type)
        superBreakDamage *= self.getVulnerability(type)
        superBreakDamage = self.applyDamageMultipliers(superBreakDamage,type)

        retval.damage = superBreakDamage
        # factor in uptime
        retval *= self.weaknessBrokenUptime
        self.addDebugInfo(retval,type,f'Super Break Damage {self.name}')
        
        return retval
    
    def extraTurn(self,advanceType=['skill','enhancedSkill'],setSpeed=None):
        retval = BaseEffect()
        type = ['Firefly Advance Forward']
        retval.actionvalue = -(1.0 + self.getAdvanceForward(advanceType))
        self.addDebugInfo(retval,type,'Firefly Advance Forward 100%')
        return retval