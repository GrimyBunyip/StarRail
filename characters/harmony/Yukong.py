from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Yukong(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                bowstringUptime:float=2.0/3.0,
                ultUptime:float=1.0/3.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Yukong')
        
        self.bowstringUptime = bowstringUptime
        self.ultUptime = ultUptime

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['enhancedBasic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1),
                                                BaseMV(type=['enhancedBasic','basic'],area='single', stat='atk', value=0.8, eidolonThreshold=5, eidolonBonus=0.08)]
        self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=3.8, eidolonThreshold=5, eidolonBonus=0.304)]

        # Talents
        self.CRType['ultimate'] += 0.294 if self.eidolon >= 5 else 0.28
        self.CDType['ultimate'] += 0.702 if self.eidolon >= 5 else 0.65
        self.Dmg += 0.12 # Ascension 4
        self.bonusEnergyAttack['ultimate'] += 2.0 # 2 bonus energy from ascension 6, but it could be more

        # Eidolons
        self.bonusEnergyAttack['ultimate'] += 15.0 if self.eidolon >= 2 else 0.0
        self.Dmg += 0.3 * self.bowstringUptime
        
        # Gear
        self.equipGear()
        
    def useBasic(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('basic')
        retval.damage *= self.getTotalCrit('basic')
        retval.damage *= self.getTotalDmg('basic')
        retval.damage = self.applyDamageMultipliers(retval.damage)
        retval.gauge = 30.0 * (1.0 + self.breakEfficiency)
        retval.energy = ( 20.0 + self.bonusEnergyAttack['basic'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['basic'])
        return retval
        
    def useEnhancedBasic(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('enhancedBasic')
        retval.damage *= self.getTotalCrit(['enhancedBasic','basic'])
        retval.damage *= self.getTotalDmg(['enhancedBasic','basic'])
        retval.damage = self.applyDamageMultipliers(retval.damage)
        retval.gauge = 60.0 * (1.0 + self.breakEfficiency)
        retval.energy = ( 20.0 + self.bonusEnergyAttack['basic'] + self.bonusEnergyAttack['enhancedBasic'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['basic']) - min(1.0,self.advanceForwardType['enhancedBasic'])
        return retval

    def useSkill(self):
        retval = BaseEffect()
        retval.energy = (30.0 + 4.0) * ( 1.0 + self.ER ) # 4 bonus energy from ascension 6, but it could be more
        retval.skillpoints = -1.0 + (0.5 if self.eidolon >= 1 else 0.0)
        retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit('ultimate')
        retval.damage *= self.getTotalDmg('ultimate')
        retval.damage = self.applyDamageMultipliers(retval.damage)
        retval.gauge = 90.0 * (1.0 + self.breakEfficiency)
        retval.energy = ( 5.0 + self.bonusEnergyAttack['ultimate'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
        retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['ultimate'])
        return retval