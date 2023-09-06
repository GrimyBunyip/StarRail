from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from baseClasses.BaseMV import BaseMV

class Blade(BaseCharacter):

  def __init__(self,
               relicstats:RelicStats,
               lightcone:BaseLightCone=None,
               relicsetone:RelicSet=None,
               relicsettwo:RelicSet=None,
               planarset:RelicSet=None,
               hpLossTally:float = 0.9,
               hellscapeUptime:float = 1.0,
               rejectedByDeathUptime:float = 1.0,
               **config):
    super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
    self.loadCharacterStats('Blade')
    
    self.hpLossTally = min(0.9,hpLossTally)
    self.hellscapeUptime = hellscapeUptime
    self.rejectedByDeathUptime = rejectedByDeathUptime

    # Motion Values should be set before talents or gear
    self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]

    self.motionValueDict['enhancedBasic'] = [BaseMV(type='basic',area='single', stat='atk', value=0.4, eidolonThreshold=5, eidolonBonus=0.04),
                                             BaseMV(type='basic',area='single', stat='hp', value=1.0, eidolonThreshold=5, eidolonBonus=0.1),
                                             BaseMV(type='basic',area='adjacent', stat='atk', value=0.16, eidolonThreshold=5, eidolonBonus=0.016),
                                             BaseMV(type='basic',area='adjacent', stat='hp', value=0.4, eidolonThreshold=5, eidolonBonus=0.04)]

    self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=0.4, eidolonThreshold=3, eidolonBonus=0.032),
                                        BaseMV(type='ultimate',area='adjacent', stat='atk', value=0.16, eidolonThreshold=3, eidolonBonus=0.0128),
                                        BaseMV(type='ultimate',area='single', stat='hp', value=1.0, eidolonThreshold=3, eidolonBonus=0.08),
                                        BaseMV(type='ultimate',area='adjacent', stat='hp', value=0.40, eidolonThreshold=3, eidolonBonus=0.032),
                                        BaseMV(type='ultimate',area='single', stat='hp', value=1.0*self.hpLossTally, eidolonThreshold=3, eidolonBonus=0.08*self.hpLossTally),
                                        BaseMV(type='ultimate',area='adjacent', stat='hp', value=0.40*self.hpLossTally, eidolonThreshold=3, eidolonBonus=0.032*self.hpLossTally)]
    
    self.motionValueDict['talent'] = [BaseMV(type=['talent','followup'],area='all', stat='atk', value=0.44, eidolonThreshold=3, eidolonBonus=0.044),
                                      BaseMV(type=['talent','followup'],area='all', stat='hp', value=1.1, eidolonThreshold=3, eidolonBonus=0.11)]
    
    # Talents
    self.DmgType['followup'] += 0.20
    self.Dmg += 0.456 if self.eidolon >= 3 else 0.40
    
    # Eidolons
    self.CR += ( 0.15 * self.hellscapeUptime ) if self.eidolon >= 2 else 0.0
    self.percHP += ( 0.40 * self.rejectedByDeathUptime ) if self.eidolon >= 4 else 0.0
    if self.eidolon >= 1:
      self.motionValueDict['ultimate'][4].value = 1.5*self.hpLossTally

    # Gear
    self.equipGear()
    

  def useBasic(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('basic')
    retval.damage *= self.getTotalCrit('basic')
    retval.damage *= self.getTotalDmg('basic')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 20.0 + self.bonusEnergyType['basic'] ) * ( 1.0 + self.ER )
    retval.skillpoints = 1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['basic'])
    return retval

  def useEnhancedBasic(self):
    num_adjacents = min( self.numEnemies - 1, 2 )
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('enhancedBasic')
    retval.damage *= self.getTotalCrit('basic')
    retval.damage *= self.getTotalDmg('basic')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * (1.0 + self.breakEfficiency)
    retval.energy = ( 30.0 + 10.0 + self.bonusEnergyType['basic'] ) * ( 1.0 + self.ER ) # + 10.0 energy from Shuhu's Gift
    retval.skillpoints = 0.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['basic'])
    return retval

  def useSkill(self):
    retval = BaseEffect()
    retval.energy = 10.0 * ( 1.0 + self.ER) # + 10.0 energy from Shuhu's Gift
    retval.skillpoints = -1.0
    return retval
  
  def takeDamage(self):
    retval = BaseEffect()
    retval.energy = 10.0 * ( 1.0 + self.ER) # + 10.0 energy from Shuhu's Gift
    return retval

  def useUltimate(self):
    num_adjacents = min( self.numEnemies - 1, 2 )
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('ultimate')
    retval.damage *= self.getTotalCrit('ultimate')
    retval.damage *= self.getTotalDmg('ultimate')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 60.0 + 60.0 * num_adjacents ) * (1.0 + self.breakEfficiency)
    retval.energy = ( 5.0 + 10.0 + self.bonusEnergyType['ultimate'] ) * ( 1.0 + self.ER ) # + 10.0 energy from Shuhu's Gift
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['ultimate'])
    return retval

  def useTalent(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('talent')
    retval.damage *= self.getTotalCrit(['followup','talent'])
    retval.damage *= self.getTotalDmg(['followup','talent'])
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 30.0 * self.numEnemies ) * (1.0 + self.breakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergyType['followup'] + self.bonusEnergyType['talent'] ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['talent'] - self.advanceForwardType['followup'])
    return retval