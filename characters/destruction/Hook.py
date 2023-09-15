from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from baseClasses.BaseMV import BaseMV

class Hook(BaseCharacter):

  def __init__(self,
               relicstats:RelicStats,
               lightcone:BaseLightCone=None,
               relicsetone:RelicSet=None,
               relicsettwo:RelicSet=None,
               planarset:RelicSet=None,
               burnedUptime:float=1.0,
               **config):
    super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
    self.loadCharacterStats('Hook')
    self.burnedUptime = burnedUptime
    
    # Motion Values should be set before talents or gear
    self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
    
    self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=2.4, eidolonThreshold=3, eidolonBonus=0.24)]
    self.motionValueDict['dot'] = [BaseMV(type=['skill','dot'],area='single', stat='atk', value=0.65, eidolonThreshold=3, eidolonBonus=0.065)]

    self.motionValueDict['enhancedSkill'] = [BaseMV(type='skill',area='single', stat='atk', value=2.8, eidolonThreshold=3, eidolonBonus=0.28),
                                             BaseMV(type='skill',area='adjacent', stat='atk', value=0.8, eidolonThreshold=3, eidolonBonus=0.08)]
        
    self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=4.0, eidolonThreshold=5, eidolonBonus=0.32)]
    self.motionValueDict['talent'] = [BaseMV(type='talent',area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
    
    # Talents
    self.advanceForwardType['ultimate'] += 0.20 # ascension
    self.bonusEnergyType['ultimate'] += 5.0
    self.bonusEnergyType['basic'] += 5.0 * self.burnedUptime
    self.bonusEnergyType['skill'] += 5.0 * self.burnedUptime
    self.bonusEnergyType['ultimate'] += 5.0 * self.burnedUptime
    
    # Eidolons
    self.DmgType['enhancedSkill'] += 0.20 if self.eidolon >= 1 else 0.0
    self.Dmg += (0.20 * self.burnedUptime) if self.eidolon >= 6 else 0.0

    # Gear
    self.equipGear()
    #self.balanceCrit()

  def useBasic(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('basic') + self.getTotalMotionValue('talent') * self.burnedUptime
    retval.damage *= self.getTotalCrit('basic')
    retval.damage *= self.getTotalDmg('basic')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 20.0 + self.bonusEnergyType['basic'] ) * ( 1.0 + self.ER )
    retval.skillpoints = 1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['basic'])
    return retval

  def useSkill(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('skill') + self.getTotalMotionValue('talent') * self.burnedUptime
    retval.damage *= self.getTotalCrit('skill')
    retval.damage *= self.getTotalDmg('skill')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergyType['skill'] ) * ( 1.0 + self.ER )
    retval.skillpoints = -1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
    return retval

  def useEnhancedSkill(self):
    num_adjacents = min( self.numEnemies - 1, 2 )
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('enhancedSkill') + self.getTotalMotionValue('talent') * self.burnedUptime
    retval.damage *= self.getTotalCrit(['skill','enhancedSkill'])
    retval.damage *= self.getTotalDmg(['skill','enhancedSkill'])
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * (1.0 + self.breakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergyType['skill'] ) * ( 1.0 + self.ER )
    retval.skillpoints = -1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
    return retval

  def useUltimate(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('ultimate') + self.getTotalMotionValue('talent') * self.burnedUptime
    retval.damage *= self.getTotalCrit('ultimate')
    retval.damage *= self.getTotalDmg('ultimate')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 90.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 5.0 + self.bonusEnergyType['ultimate'] ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['ultimate'])
    return retval
  
  def useDot(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('dot')
    # no crits on dots
    retval.damage *= self.getTotalDmg('dot')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    return retval