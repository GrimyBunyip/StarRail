from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Sushang(BaseCharacter):

  def __init__(self,
               relicstats:RelicStats,
               lightcone:BaseLightCone=None,
               relicsetone:RelicSet=None,
               relicsettwo:RelicSet=None,
               planarset:RelicSet=None,
               weaknessBrokenUptime:float = 0.5,
               weaknessBrokenStacks:float=2.0,
               ripostedStacks:float=10.0,
               **config):
    super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
    self.loadCharacterStats('Sushang')
    
    self.weaknessBrokenUptime = weaknessBrokenUptime
    self.weaknessBrokenStacks = weaknessBrokenStacks
    self.riposteStacks = ripostedStacks
    self.ultBuffCooldown = 0
    
    # Motion Values should be set before talents or gear
    self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
    self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=2.1, eidolonThreshold=3, eidolonBonus=0.21)]
    self.motionValueDict['swordStance'] = [BaseMV(type=['skill','swordStance'],area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
    self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=3.2, eidolonThreshold=5, eidolonBonus=0.256)]
    
    # Talents
    self.percAtkType['swordStance'] = 0.0 # need this to suppress an error message
    self.percSpd += (0.21 if self.eidolon >= 5 else 0.2) * self.weaknessBrokenUptime * (weaknessBrokenStacks if self.eidolon >= 6 else 1.0)
    self.DmgType['swordStance'] = 0.0249999996740371 * self.riposteStacks # number from datamine?
    self.advanceForwardType['basic'] += 0.15 * self.weaknessBrokenUptime
    self.advanceForwardType['skill'] += 0.15 * self.weaknessBrokenUptime
    self.advanceForwardType['ultimate'] += 1.0
    
    # Bliss is always up for Ult

    # Eidolons
    self.dmgReduction += 0.20 if self.eidolon >= 2 else 0.0
    self.breakEffect += 0.40 if self.eidolon >= 4 else 0.0
    
    # Gear
    self.equipGear()

  def useBasic(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('basic')
    retval.damage *= self.getTotalCrit(['basic'])
    retval.damage *= self.getTotalDmg('basic')
    retval.damage *= self.getVulnerabilityType('basic')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 20.0 + self.bonusEnergyAttack['basic'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
    retval.skillpoints = 1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['basic'])
    self.endTurn()
    return retval

  def useSkill(self):
    stanceChance = self.weaknessBrokenUptime + (1.0 - self.weaknessBrokenUptime) * 0.33
    if self.ultBuffCooldown > 0.0:
      stanceChance *= 2 # 2 more chances at half damage, is essentially 1 more full chance
    
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('skill') + stanceChance * self.getTotalMotionValue('swordStance')
    retval.damage *= self.getTotalCrit(['skill'])
    retval.damage *= self.getTotalDmg('skill')
    retval.damage *= self.getVulnerabilityType('skill')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergyAttack['skill'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
    retval.skillpoints = -1.0 + (self.weaknessBrokenUptime if self.eidolon >= 1 else 0.0)
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
    self.endTurn()
    return retval

  def useSwordStance(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('swordStance')
    retval.damage *= self.getTotalCrit('skill')
    retval.damage *= self.getTotalDmg(['skill','swordStance'])
    retval.damage *= self.getVulnerabilityType('skill')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    return retval

  def useUltimate(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('ultimate')
    retval.damage *= self.getTotalCrit(['ultimate'])
    retval.damage *= self.getTotalDmg('ultimate')
    retval.damage *= self.getVulnerabilityType('ultimate')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 90.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 5.0 + self.bonusEnergyAttack['ultimate'] ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['ultimate'])
    self.ultBuffCooldown = 2
    self.percAtk += (0.324 if self.eidolon >= 5 else 0.3)
    return retval

  def useTalent(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('talent')
    retval.damage *= self.getTotalCrit(['followup','talent'])
    retval.damage *= self.getTotalDmg(['followup','talent'])
    retval.damage *= self.getVulnerabilityType(['followup','talent'])
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 10.0 + self.bonusEnergyAttack['talent'] + self.bonusEnergyAttack['followup'] ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['talent'] - self.advanceForwardType['followup'])
    return retval
  
  def endTurn(self):
    self.ultBuffCooldown -= 1
    if self.ultBuffCooldown == 0:
      self.percAtk -= (0.324 if self.eidolon >= 5 else 0.3)
    