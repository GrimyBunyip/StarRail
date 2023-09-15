from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Himeko(BaseCharacter):
  def __init__(self,
               relicstats:RelicStats,
               lightcone:BaseLightCone=None,
               relicsetone:RelicSet=None,
               relicsettwo:RelicSet=None,
               planarset:RelicSet=None,
               magmaUptime:float=1.0,
               benchmarkUptime:float=1.0,
               e1Uptime:float=1.0,
               e2Uptime:float=0.5,
               **config):
    super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
    self.loadCharacterStats('Himeko')
    self.magmaUptime = magmaUptime
    self.benchmarkUptime = benchmarkUptime
    self.e1Uptime = e1Uptime
    self.e2Uptime = e2Uptime
    
    # Motion Values should be set before talents or gear
    self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]

    self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=2.0, eidolonThreshold=5, eidolonBonus=0.2),
                                     BaseMV(type='skill',area='adjacent', stat='atk', value=0.8, eidolonThreshold=5, eidolonBonus=0.08)]

    self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='all', stat='atk', value=2.3, eidolonThreshold=3, eidolonBonus=0.184)]

    self.motionValueDict['talent'] = [BaseMV(type=['talent','followup'],area='all', stat='atk', value=1.4, eidolonThreshold=5, eidolonBonus=0.14)]
    self.motionValueDict['dot'] = [BaseMV(type=['dot'],area='all', stat='atk', value=0.3)]

    # Talents
    self.Dmg += 0.2 * self.magmaUptime
    self.CR += 0.15 * self.benchmarkUptime
    
    # Eidolons
    self.percSpd += (0.2 * self.e1Uptime) if self.eidolon >= 1 else 0.0
    self.Dmg += (0.15 * self.e2Uptime) if self.eidolon >= 2 else 0.0
    
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
    return 

  def useSkill(self):
    num_adjacents = min( self.numEnemies - 1, 2 )
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('skill')
    retval.damage *= self.getTotalCrit('skill')
    retval.damage *= self.getTotalDmg('skill')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * (1.0 + self.breakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergyType['skill'] ) * ( 1.0 + self.ER )
    retval.skillpoints = -1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
    return retval

  def useUltimate(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('ultimate') * ((1.8 * retval.damage / self.numEnemies) if self.eidolon >= 6 else 1.0)
    retval.damage *= self.getTotalCrit('ultimate')
    retval.damage *= self.getTotalDmg('ultimate')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * self.numEnemies * (1.0 + self.breakEfficiency)
    retval.energy = ( 5.0 + self.bonusEnergyType['ultimate'] ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['ultimate'])
    return retval

  def useTalent(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('talent')
    retval.damage *= self.getTotalCrit(['followup','talent'])
    retval.damage *= self.getTotalDmg(['followup','talent'])
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 30.0 * self.numEnemies ) * (1.0 + self.breakEfficiency)
    retval.energy = ( 10.0 + self.bonusEnergyType['followup'] + self.bonusEnergyType['talent'] ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['talent'] - self.advanceForwardType['followup'])
    return retval
  
  def useDot(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('dot')
    retval.damage *= self.getTotalDmg('dot')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    return retval