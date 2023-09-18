from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Kafka(BaseCharacter):
  def __init__(self,
               relicstats:RelicStats,
               lightcone:BaseLightCone=None,
               relicsetone:RelicSet=None,
               relicsettwo:RelicSet=None,
               planarset:RelicSet=None,
               **config):
    super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
    self.loadCharacterStats('Kafka')
    
    # Motion Values should be set before talents or gear
    self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
    self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=1.6, eidolonThreshold=3, eidolonBonus=0.16),
                                     BaseMV(type='skill',area='adjacent', stat='atk', value=0.6, eidolonThreshold=3, eidolonBonus=0.06)]
    self.motionValueDict['dot'] = [BaseMV(type=['dot','ultimate'],area='single', stat='atk', value=2.90, eidolonThreshold=5, eidolonBonus=0.2828)]
    self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='all', stat='atk', value=0.8, eidolonThreshold=5, eidolonBonus=0.064)]
    self.motionValueDict['talent'] = [BaseMV(type=['talent','followup'],area='single', stat='atk', value=1.4, eidolonThreshold=5, eidolonBonus=0.196)]
    
    # Talents
    
    # Eidolons
    self.DmgType['dot'] += 0.25 if self.eidolon >= 2 else 0.0
    self.DmgType['dot'] += 0.30 / self.numEnemies if self.eidolon >= 1 else 0.0
    
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
    num_adjacents = min( self.numEnemies - 1, 2 )
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('skill')
    retval.damage *= self.getTotalCrit('skill')
    retval.damage *= self.getTotalDmg('skill')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * (1.0 + self.breakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergyAttack['skill'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
    retval.skillpoints = -1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
    
    dotExplosion = self.useDot() + self.useBreakDot()
    dotExplosion *= 0.78 if self.eidolon >= 3 else 0.75
    
    retval += dotExplosion
    return retval

  def useUltimate(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('ultimate')
    retval.damage *= self.getTotalCrit('ultimate')
    retval.damage *= self.getTotalDmg('ultimate')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * self.numEnemies * (1.0 + self.breakEfficiency)
    retval.energy = ( 5.0 + self.bonusEnergyAttack['ultimate'] ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['ultimate'])
    
    # assume breakDot single target, usualDot AOE
    dotExplosion = self.useDot() * self.numEnemies + self.useBreakDot()
    dotExplosion *= 1.0 if self.eidolon >= 5 else 1.04
    
    retval += dotExplosion
    return retval

  def useTalent(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('talent')
    retval.damage *= self.getTotalCrit('talent')
    retval.damage *= self.getTotalDmg('talent')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 10.0 + self.bonusEnergyAttack['talent'] ) * ( 1.0 + self.ER )
    retval.skillpoints = 0.0
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['talent'])
    return retval

  def useDot(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('dot')
    # no crits on dots
    retval.damage *= self.getTotalDmg('dot') + (1.56 if self.eidolon >= 6 else 0.0)
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.energy = ( 0.0 + self.bonusEnergyAttack['dot'] + (2.0 if self.eidolon >= 4 else 0.0) ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['dot'])
    return retval