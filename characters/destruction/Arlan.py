from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from baseClasses.BaseMV import BaseMV

class Arlan(BaseCharacter):

    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                percentHP:float=0.5,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Arlan')
        self.percentHP = percentHP
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=2.4, eidolonThreshold=3, eidolonBonus=0.24)]
        self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=3.2, eidolonThreshold=5, eidolonBonus=0.256),
                                                                            BaseMV(type='ultimate',area='adjacent', stat='atk', value=1.6, eidolonThreshold=5, eidolonBonus=0.128)]
        self.motionValueDict['ultimateE6'] = [BaseMV(type='ultimate',area='single', stat='atk', value=3.2, eidolonThreshold=5, eidolonBonus=0.256),
                                                                            BaseMV(type='ultimate',area='adjacent', stat='atk', value=3.2, eidolonThreshold=5, eidolonBonus=0.256)]
        
        # Talents
        self.Dmg += min(1.0, (0.792 if self.eidolon >= 5 else 0.72) * self.percentHP)
        
        # Eidolons
        self.DmgType['skill'] += 0.10 if self.percentHP <= 0.5 else 0.0
        self.DmgType['ultimate'] += 0.20 if self.percentHP <= 0.5 else 0.0

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

    def useSkill(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('skill')
        retval.damage *= self.getTotalCrit('skill')
        retval.damage *= self.getTotalDmg('skill')
        retval.damage = self.applyDamageMultipliers(retval.damage)
        retval.gauge = 60.0 * (1.0 + self.breakEfficiency)
        retval.energy = ( 30.0 + self.bonusEnergyAttack['skill'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('ultimateE6') if self.eidolon >= 6 else self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit('ultimate')
        retval.damage *= self.getTotalDmg('ultimate')
        retval.damage = self.applyDamageMultipliers(retval.damage)
        retval.gauge = 60.0 * min(3, self.numEnemies) * (1.0 + self.breakEfficiency)
        retval.energy = ( 5.0 + self.bonusEnergyAttack['ultimate'] ) * ( 1.0 + self.ER )
        return retval