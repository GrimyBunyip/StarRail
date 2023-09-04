from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from baseClasses.BaseMV import BaseMV

class Clara(BaseCharacter):

  def __init__(self,
               relicstats:RelicStats,
               lightcone:BaseLightCone=None,
               relicsetone:RelicSet=None,
               relicsettwo:RelicSet=None,
               planarset:RelicSet=None,
               aTightEmbraceUptime:float=1.0,
               **config):
    super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
    self.loadCharacterStats('Clara')
    
    self.aTightEmbraceUptime = aTightEmbraceUptime

    # Motion Values should be set before talents or gear
    self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
    self.motionValueDict['skill'] = [BaseMV(type='skill',area='all', stat='atk', value=1.2, eidolonThreshold=3, eidolonBonus=0.12)]
    
    self.motionValueDict['markOfSvarog'] = [BaseMV(type='skill',area='single', stat='atk', value=1.2, eidolonThreshold=3, eidolonBonus=0.12)]
    
    self.motionValueDict['talent'] = [BaseMV(type=['talent','followup'],area='single', stat='atk', value=1.6, eidolonThreshold=5, eidolonBonus=0.16)]
    self.motionValueDict['enhancedTalent'] = [BaseMV(type=['talent','followup'],area='single', stat='atk', value=1.6, eidolonThreshold=5, eidolonBonus=0.16),
                                              BaseMV(type=['talent','followup'],area='adjacent', stat='atk', value=0.8, eidolonThreshold=5, eidolonBonus=0.08),]
    # technically I just halved the MV's, could be weird if something buffs Clara's MVs
    
    # Talents
    self.DmgType['followup'] += 0.30 # Revenge Talent
    
    # Eidolons
    # handle handle e1 manually, by using the argument in the useSkill call
    self.percAtk += ( 0.30 * self.aTightEmbraceUptime ) if self.eidolon >= 2 else 0.0
    # better to handle e6 manually

    # Gear
    self.equipGear()
    self.balanceCrit()

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

  def useSkill(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('skill')
    retval.damage *= self.getTotalCrit('skill')
    retval.damage *= self.getTotalDmg('skill')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * self.numEnemies * (1.0 + self.breakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergyType['skill'] ) * ( 1.0 + self.ER )
    retval.skillpoints = -1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
    return retval

  def useMarkOfSvarog(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('markOfSvarog')
    retval.damage *= self.getTotalCrit('skill')
    retval.damage *= self.getTotalDmg('skill')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    return retval

  def useUltimate(self):
    retval = BaseEffect()
    retval.energy = ( 5.0 + self.bonusEnergyType['ultimate'] ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['ultimate'])
    return retval

  def useTalent(self, enhanced=False):
    retval = BaseEffect()
    if enhanced:
      retval.damage = self.getTotalMotionValue('enhancedTalent')
    else:
      retval.damage = self.getTotalMotionValue('talent')
      
    retval.damage *= self.getTotalCrit(['followup','talent'])
    retval.damage *= self.getTotalDmg(['followup','talent']) + ( (1.728 if self.eidolon >= 5 else 1.6) if enhanced else 0.0)
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( ( 30.0 * min(3,self.numEnemies) ) if enhanced else 30.0 ) * (1.0 + self.breakEfficiency)
    retval.energy = ( 5.0 + self.bonusEnergyType['followup'] + self.bonusEnergyType['talent'] ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['talent'] - self.advanceForwardType['followup'])
    return retval