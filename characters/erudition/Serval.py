from copy import copy
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
    self.motionValueDict['dot'] = [BaseMV(type=['dot','skill'],area='all', stat='atk', value=1.04, eidolonThreshold=3, eidolonBonus=1.144)]
    self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=1.8, eidolonThreshold=5, eidolonBonus=0.144)]
    self.motionValueDict['shockedBasic'] = [BaseMV(type='basic',area='all', stat='atk', value=0.72, eidolonThreshold=5, eidolonBonus=0.072)]
    self.motionValueDict['shockedSkill'] = [BaseMV(type='skill',area='all', stat='atk', value=0.72, eidolonThreshold=5, eidolonBonus=0.072)]
    self.motionValueDict['shockedUltimate'] = [BaseMV(type='ultimate',area='all', stat='atk', value=0.72, eidolonThreshold=5, eidolonBonus=0.072)]
    
    # Talents
    
    # Eidolons
    
    # Gear
    self.equipGear()
    self.balanceCrit()

  def useBasic(self, shocked = True):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('basic')
    retval.damage += self.getTotalMotionValue('shockedBasic') if shocked else 0.0
    retval.damage *= self.getTotalCrit('basic')
    retval.damage *= self.getTotalDmg('basic')
    
    retval.damage *= 1.1 if self.eidolon >= 3 else 1.0
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 30.0 * self.numEnemies if shocked else 30.0 ) * (1.0 + self.BreakEfficiency)
    retval.energy = ( 20.0 + self.bonusEnergyType['basic'] ) * ( 1.0 + self.ER )
    retval.skillpoints = 1.0
    return retval

  def useSkill(self, shocked = True):
    num_adjacents = min( self.numEnemies - 1, 2 )
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('skill')
    retval.damage += self.getTotalMotionValue('shockedSkill') if shocked else 0.0
    retval.damage *= self.getTotalCrit('skill')
    retval.damage *= self.getTotalDmg('skill')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * (1.0 + self.BreakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergyType['skill'] ) * ( 1.0 + self.ER )
    retval.skillpoints = -1.0
    return retval

  def useUltimate(self, shocked = True):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('ultimate')
    retval.damage += self.getTotalMotionValue('shockedUltimate') if shocked else 0.0
    retval.damage *= self.getTotalCrit('ultimate')
    retval.damage *= self.getTotalDmg('ultimate')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * self.numEnemies * (1.0 + self.BreakEfficiency)
    retval.energy = ( 5.0 + self.bonusEnergyType['ultimate'] ) * ( 1.0 + self.ER )
    return retval

  def useDot(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('dot')
    # no crits on dots
    retval.damage *= self.getTotalDmg('ultimate')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.energy = ( 0.0 + self.bonusEnergyType['dot'] ) * ( 1.0 + self.ER )
    return retval
  
def ServalEstimationV1(character:BaseCharacter, Configuration:dict, CharacterDict:dict, EffectDict:dict):
  
  playerTurns = ( Configuration['numRounds'] + 0.5 )  * character.getTotalSpd() / 100
  enemyTurns = ( Configuration['numRounds'] + 0.5 ) * Configuration['enemySpeed'] / 100
  enemyAttacks = enemyTurns * Configuration['numberEnemyAttacksPerTurn'] * character.taunt / 100.0

  totalEffect = BaseEffect()
  totalEffect.energy += Configuration['bonusEnergyFlat']
  totalEffect.energy += Configuration['bonusEnergyPerEnemyAttack'] * enemyAttacks
  
  # assume we spam skill every single turn
  totalEffect += playerTurns * character.useSkill()
  
  # assume we apply break a number of times proportional to our gauge output and enemy toughness
  num_breaks = totalEffect.gauge / Configuration['enemyToughness']
  totalEffect += character.useBreak() * num_breaks
  
  # apply a number of break dots proportional to the amount of breaks we applied, up to the number of enemy turns
  num_dots = min(enemyTurns * Configuration['numEnemies'], num_breaks * 2)
  totalEffect += character.useBreakDot() * num_dots
  
  # assume we use an ult proportional to the amount of energy we gained. Ignoring rounding errors and energy from enemy attacks
  num_ults = ( totalEffect.energy - 5 * (1 + character.ER) ) / character.maxEnergy
  totalEffect += num_ults * character.useUltimate()
  
  print("Serval Effects:")
  totalEffect.print()

  CharacterDict[character.name] = copy(character)
  EffectDict[character.name] = copy(totalEffect)