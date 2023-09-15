from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Serval(BaseCharacter):
  def __init__(self,
               relicstats:RelicStats,
               lightcone:BaseLightCone=None,
               relicsetone:RelicSet=None,
               relicsettwo:RelicSet=None,
               planarset:RelicSet=None,
               **config):
    super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
    self.loadCharacterStats('Serval')
    
    # Motion Values should be set before talents or gear
    self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
    self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=1.4, eidolonThreshold=3, eidolonBonus=0.14),
                                     BaseMV(type='skill',area='adjacent', stat='atk', value=0.6, eidolonThreshold=3, eidolonBonus=0.06)]
    self.motionValueDict['dot'] = [BaseMV(type=['dot','skill'],area='single', stat='atk', value=1.04, eidolonThreshold=3, eidolonBonus=0.104)]
    self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='all', stat='atk', value=1.8, eidolonThreshold=5, eidolonBonus=0.144)]
    self.motionValueDict['shockedBasic'] = [BaseMV(type='basic',area='all', stat='atk', value=0.72, eidolonThreshold=5, eidolonBonus=0.072)]
    self.motionValueDict['shockedSkill'] = [BaseMV(type='skill',area='all', stat='atk', value=0.72, eidolonThreshold=5, eidolonBonus=0.072)]
    self.motionValueDict['shockedUltimate'] = [BaseMV(type='ultimate',area='all', stat='atk', value=0.72, eidolonThreshold=5, eidolonBonus=0.072)]
    
    # Talents
    
    # Eidolons
    if self.eidolon >= 1 and self.numEnemies >= 2:
      self.motionValueDict['basic'].append(BaseMV(type='basic',area='single', stat='atk', value=0.6))
    
    # Gear
    self.equipGear()

  def useBasic(self, shocked = True):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('basic')
    retval.damage += self.getTotalMotionValue('shockedBasic') if shocked else 0.0
    retval.damage *= self.getTotalCrit('basic')
    retval.damage *= self.getTotalDmg('basic') + 0.3 if (shocked and self.eidolon >= 6) else 0.0
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 30.0 * self.numEnemies if shocked else 30.0 ) * (1.0 + self.breakEfficiency)
    retval.energy = ( 20.0 + self.bonusEnergyType['basic'] + 4.0 if (shocked and self.eidolon >= 2) else 0.0 ) * ( 1.0 + self.ER )
    retval.skillpoints = 1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['basic'])
    return retval

  def useSkill(self, shocked = True):
    num_adjacents = min( self.numEnemies - 1, 2 )
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('skill')
    retval.damage += self.getTotalMotionValue('shockedSkill') if shocked else 0.0
    retval.damage *= self.getTotalCrit('skill')
    retval.damage *= self.getTotalDmg('skill') + 0.3 if (shocked and self.eidolon >= 6) else 0.0
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * (1.0 + self.breakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergyType['skill'] + 4.0 if (shocked and self.eidolon >= 2) else 0.0 ) * ( 1.0 + self.ER )
    retval.skillpoints = -1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
    return retval

  def useUltimate(self, shocked = True):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('ultimate')
    retval.damage += self.getTotalMotionValue('shockedUltimate') if shocked else 0.0
    retval.damage *= self.getTotalCrit('ultimate')
    retval.damage *= self.getTotalDmg('ultimate') + 0.3 if (shocked and self.eidolon >= 6) else 0.0
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * self.numEnemies * (1.0 + self.breakEfficiency)
    retval.energy = ( 5.0 + self.bonusEnergyType['ultimate'] + 4.0 if (shocked and self.eidolon >= 2) else 0.0 ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['ultimate'])
    return retval

  def useDot(self, shocked = True):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('dot')
    # no crits on dots
    retval.damage *= self.getTotalDmg('dot') + ( 0.3 if (shocked and self.eidolon >= 6) else 0.0 )
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.energy = ( 0.0 + self.bonusEnergyType['dot'] ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['dot'])
    return retval