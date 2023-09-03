from copy import copy
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from baseClasses.BaseMV import BaseMV

# Lazy, haven't implemented E1 or E4 or E6

class Blade(BaseCharacter):

  def __init__(self,
               relicstats:RelicStats,
               lightcone:BaseLightCone=None,
               relicsetone:RelicSet=None,
               relicsettwo:RelicSet=None,
               planarset:RelicSet=None,
               hpLossTally:float = 0.9,
               hellscapeUptime:float = 1.0,
               **config):
    super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
    self.loadCharacterStats('Blade')
    
    self.hpLossTally = hpLossTally
    self.hellscapeUptime = hellscapeUptime

    # Motion Values should be set before talents or gear
    self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]

    self.motionValueDict['enhancedBasic'] = [BaseMV(type='basic',area='single', stat='atk', value=0.4, eidolonThreshold=3, eidolonBonus=0.04),
                                             BaseMV(type='basic',area='single', stat='hp', value=1.0, eidolonThreshold=3, eidolonBonus=0.1),
                                             BaseMV(type='basic',area='adjacent', stat='atk', value=0.16, eidolonThreshold=3, eidolonBonus=0.016),
                                             BaseMV(type='basic',area='adjacent', stat='hp', value=0.4, eidolonThreshold=3, eidolonBonus=0.04)]

    self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=0.4, eidolonThreshold=5, eidolonBonus=0.032),
                                        BaseMV(type='ultimate',area='adjacent', stat='atk', value=0.16, eidolonThreshold=5, eidolonBonus=0.0128),
                                        BaseMV(type='ultimate',area='single', stat='hp', value=1.0, eidolonThreshold=5, eidolonBonus=0.08),
                                        BaseMV(type='ultimate',area='adjacent', stat='hp', value=0.40, eidolonThreshold=5, eidolonBonus=0.032),
                                        BaseMV(type='ultimate',area='single', stat='hp', value=1.0*self.hpLossTally, eidolonThreshold=5, eidolonBonus=0.08*self.hpLossTally),
                                        BaseMV(type='ultimate',area='adjacent', stat='hp', value=0.40*self.hpLossTally, eidolonThreshold=5, eidolonBonus=0.032*self.hpLossTally)]
    
    self.motionValueDict['talent'] = [BaseMV(type=['talent','followup'],area='all', stat='atk', value=0.44, eidolonThreshold=5, eidolonBonus=0.044),
                                      BaseMV(type=['talent','followup'],area='all', stat='hp', value=1.1, eidolonThreshold=5, eidolonBonus=0.11)]
    
    # Talents
    self.DmgType['followup'] += 0.20
    
    # Eidolons
    self.CR += 0.15 * self.hellscapeUptime if self.eidolon >= 2 else 0.0

    # Gear
    self.equipGear()
    self.balanceCrit()
    

  def useBasic(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('basic')
    retval.damage *= self.getTotalCrit('basic')
    retval.damage *= self.getTotalDmg('basic')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.BreakEfficiency)
    retval.energy = ( 20.0 + self.bonusEnergyType['basic'] ) * ( 1.0 + self.ER )
    retval.skillpoints = 1.0
    return retval

  def useEnhancedBasic(self):
    num_adjacents = min( self.numEnemies - 1, 2 )
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('enhancedBasic')
    retval.damage *= self.getTotalCrit('basic')
    retval.damage *= self.getTotalDmg('basic')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * (1.0 + self.BreakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergyType['basic'] ) * ( 1.0 + self.ER )
    retval.skillpoints = - 1.0 / 3 # just gonna estimate it by tweaking this here
    return retval

  def useSkill(self):
    retval = BaseEffect()
    retval.skillpoints = -1.0
    return retval

  def useUltimate(self):
    num_adjacents = min( self.numEnemies - 1, 2 )
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('ultimate')
    retval.damage *= self.getTotalCrit('ultimate')
    retval.damage *= self.getTotalDmg('ultimate')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 60.0 + 60.0 * num_adjacents ) * (1.0 + self.BreakEfficiency)
    retval.energy = ( 5.0 + self.bonusEnergyType['ultimate'] ) * ( 1.0 + self.ER )
    return retval

  def useTalent(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('talent')
    retval.damage *= self.getTotalCrit(['followup','talent'])
    retval.damage *= self.getTotalDmg(['followup','talent'])
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 30.0 * self.numEnemies ) * (1.0 + self.BreakEfficiency)
    retval.energy = ( 10.0 + self.bonusEnergyType['followup'] + self.bonusEnergyType['talent'] ) * ( 1.0 + self.ER )
    return retval
  
def BladeEstimationsV1(character:BaseCharacter, Configuration:dict, CharacterDict:dict, EffectDict:dict):

  playerTurns = ( Configuration['numRounds'] + 0.5 )  * character.getTotalSpd() / 100
  enemyTurns = ( Configuration['numRounds'] + 0.5 ) * Configuration['enemySpeed'] / 100
  enemyAttacks = enemyTurns * Configuration['numberEnemyAttacksPerTurn'] * character.taunt / 100.0

  totalEffect:BaseEffect = BaseEffect()
  totalEffect.energy += Configuration['bonusEnergyFlat']
  totalEffect.energy += Configuration['bonusEnergyPerEnemyAttack'] * enemyAttacks
  
  # assume we spam skill every single turn
  totalEffect += playerTurns * character.useEnhancedBasic()
  
  # assume we apply break a number of times proportional to our gauge output and enemy toughness
  num_breaks = totalEffect.gauge / Configuration['enemyToughness']
  totalEffect += character.useBreak() * num_breaks
  
  # apply a number of break dots proportional to the amount of breaks we applied, up to the number of enemy turns
  num_dots = min(enemyTurns * Configuration['numEnemies'], num_breaks * 2)
  totalEffect += character.useBreakDot() * num_dots
  
  # assume we use an ult proportional to the amount of energy we gained. Ignoring rounding errors and energy from enemy attacks
  num_ults = totalEffect.energy / character.maxEnergy
  totalEffect += character.useUltimate() * num_ults
  
  # Assume blade takes 1 hit per enemy attack. 1 hit per Ult, 1.333 hits per his turn
  num_hits = enemyAttacks + playerTurns * (4/3) + num_ults
  totalEffect += character.useTalent() * ( num_hits / 5.0 ) 
  
  print("Blade Effects:")
  totalEffect.print()

  CharacterDict[character.name] = copy(character)
  EffectDict[character.name] = copy(totalEffect)