from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Tingyun(BaseCharacter):
  def __init__(self,
               relicstats:RelicStats,
               lightcone:BaseLightCone=None,
               relicsetone:RelicSet=None,
               relicsettwo:RelicSet=None,
               planarset:RelicSet=None,
               allyAttack:float=2500.0,
               speedUptime:float=1.0/3.0,
               **config):
    super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
    self.loadCharacterStats('Tingyun')
    
    self.allyAttack = allyAttack
    self.speedUptime = speedUptime

    # Motion Values should be set before talents or gear
    self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]

    # Talents
    self.percSpd += 0.20 * self.speedUptime
    self.DmgType['basic'] += 0.40
    self.bonusEnergyAttack['turn'] += 5.0 if self.eidolon >= 2 else 0.0

    # Eidolons
    
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
    
    retval += self.useTalent()
    return retval

  def useSkill(self):
    retval = BaseEffect()
    retval.energy = ( 30.0 + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
    retval.skillpoints = -1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
    return retval

  def useUltimate(self):
    retval = BaseEffect()
    retval.energy = 5.0 * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['ultimate'])
    return retval
  
  def useTalent(self):
    retval = BaseEffect()
    retval.damage = 0.66 if self.eidolon >= 5 else 0.6
    retval.damage *= self.allyAttack
    return retval