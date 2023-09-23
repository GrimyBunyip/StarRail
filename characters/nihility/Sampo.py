from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Sampo(BaseCharacter):
  def __init__(self,
               relicstats:RelicStats,
               lightcone:BaseLightCone=None,
               relicsetone:RelicSet=None,
               relicsettwo:RelicSet=None,
               planarset:RelicSet=None,
               ultUptime:float=2.0/3.0,
               windshearUptime:float=1.0,
               windshearStacks:float=5.0,
               **config):
    super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
    self.loadCharacterStats('Sampo')
    self.ultUptime = ultUptime
    self.windshearUptime = windshearUptime
    self.windshearStacks = windshearStacks
    
    # Motion Values should be set before talents or gear
    self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
    self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=0.56, eidolonThreshold=3, eidolonBonus=0.056)]
    self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='all', stat='atk', value=1.6, eidolonThreshold=5, eidolonBonus=0.128)]
    self.motionValueDict['dot'] = [BaseMV(type=['talent','dot'],area='single', stat='atk', value=0.52, eidolonThreshold=5, eidolonBonus=0.052)]
    self.motionValueDict['dote6'] = [BaseMV(type=['talent','dot'],area='single', stat='atk', value=0.52+0.15, eidolonThreshold=5, eidolonBonus=0.052)]
    
    # Talents
    self.VulnerabilityType['dot'] += (0.32 if self.eidolon >= 5 else 0.3) * self.ultUptime
    self.bonusEnergyAttack['ultimate'] += 10.0
    
    # Eidolons
    
    # Gear
    self.equipGear()

  def useBasic(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('basic')
    retval.damage *= self.getTotalCrit('basic')
    retval.damage *= self.getTotalDmg('basic')
    retval.damage *= self.getVulnerabilityType('basic')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 20.0 + self.bonusEnergyAttack['basic'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
    retval.skillpoints = 1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['basic'])
    return retval

  def useSkill(self):
    num_hits = 6.0 if self.eidolon else 5.0
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('skill') * num_hits
    retval.damage *= self.getTotalCrit('skill')
    retval.damage *= self.getTotalDmg('skill')
    retval.damage *= self.getVulnerabilityType('skill')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 15.0 + 15.0 * num_hits ) * (1.0 + self.breakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergyAttack['skill'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
    retval.skillpoints = -1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
    
    # assume we hit up to 3 enemies
    dotExplosion = self.useDot() * num_hits
    dotExplosion.damage *= 0.08 if self.eidolon >= 4 else 0.0
    retval += dotExplosion
    return retval

  def useUltimate(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('ultimate')
    retval.damage *= self.getTotalCrit('ultimate')
    retval.damage *= self.getTotalDmg('ultimate')
    retval.damage *= self.getVulnerabilityType('ultimate')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * self.numEnemies * (1.0 + self.breakEfficiency)
    retval.energy = ( 5.0 + self.bonusEnergyAttack['ultimate'] ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['ultimate'])
    return retval

  def useDot(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('dote6') if self.eidolon >= 6 else self.getTotalMotionValue('dot')
    # no crits on dots
    retval.damage *= self.windshearStacks * self.windshearUptime
    retval.damage *= self.getTotalDmg('dot')
    retval.damage *= self.getVulnerabilityType('dot')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.energy = ( 0.0 + self.bonusEnergyAttack['dot'] ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['dot'])
    return retval