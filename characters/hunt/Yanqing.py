from copy import copy
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Yanqing(BaseCharacter):

  def __init__(self,
               lightcone:BaseLightCone,
               relicsetone:RelicSet,
               relicsettwo:RelicSet,
               planarset:RelicSet,
               relicstats:RelicStats,
               soulsteelUptime = 1.0,
               e4Uptime = 1.0,
               rainingBlissUptime = 0.25,
               **config):
    super().__init__(lightcone, relicsetone, relicsettwo, planarset, relicstats, config)
    self.loadCharacterStats('Yanqing')

    self.soulsteelUptime = soulsteelUptime
    self.e4Uptime = e4Uptime
    self.rainingBlissUptime = rainingBlissUptime

    self.longName = 'Yanqing E{} {} S{}\n{} + {} + {}\nSoulsteel Uptime: {}\nUltimate Uptime: {}'.format(self.eidolon, self.lightcone.name, self.lightcone.superposition,
                                                                                          relicsetone.shortname, relicsettwo.shortname, planarset.shortname,
                                                                                          self.soulsteelUptime,
                                                                                          self.rainingBlissUptime)

    # Motion Values should be set before talents or gear
    self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1),
                                     BaseMV(type='basic',area='single', stat='atk', value=0.0, eidolonThreshold=1, eidolonBonus=0.6)]
    self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=2.2, eidolonThreshold=3, eidolonBonus=0.22),
                                     BaseMV(type='skill',area='single', stat='atk', value=0.0, eidolonThreshold=1, eidolonBonus=0.6)]
    self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=3.5, eidolonThreshold=5, eidolonBonus=0.28),
                                        BaseMV(type='ultimate',area='single', stat='atk', value=0.0, eidolonThreshold=1, eidolonBonus=0.6)]
    self.motionValueDict['talent'] = [BaseMV(type=['talent','followup'],area='single', stat='atk', value=0.5, eidolonThreshold=5, eidolonBonus=0.05)]
    
    # Talents
    self.ER += 0.10 * self.soulsteelUptime if self.eidolon >= 2 else 0.0
    self.resPen += 0.12 * self.e4Uptime if self.eidolon >= 4 else 0.0

    # Soulsteel
    self.CR += self.soulsteelUptime * ( 0.22 if self.eidolon >= 5 else 0.20 )
    self.CD += self.soulsteelUptime * ( 0.33 if self.eidolon >= 5 else 0.30 )
    self.CRType['bliss'] = 0.6 * self.rainingBlissUptime
    self.CDType['bliss'] = ( 0.54 if self.eidolon >= 5 else 0.5 ) * self.rainingBlissUptime
    
    # Bliss is always up for Ult
    self.CRType['blissUlt'] = 0.6
    self.CDType['blissUlt'] = 0.54 if self.eidolon >= 5 else 0.5
    self.percTaunt -= 0.6 * self.soulsteelUptime

    # Eidolons
    
    # Gear
    self.equipGear()
    #self.balanceCrit() do not balance crit on yanqing

  def useBasic(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('basic')
    retval.damage *= self.getTotalCrit(['basic','bliss'])
    retval.damage *= self.getTotalDmg('basic')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.BreakEfficiency)
    retval.energy = ( 20.0 + self.bonusEnergyType['basic'] ) * ( 1.0 + self.ER )
    retval.skillpoints = 1.0
    return retval

  def useSkill(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('skill')
    retval.damage *= self.getTotalCrit(['skill','bliss'])
    retval.damage *= self.getTotalDmg('skill')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * (1.0 + self.BreakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergyType['skill'] ) * ( 1.0 + self.ER )
    retval.skillpoints = -1.0
    return retval

  def useUltimate(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('ultimate')
    retval.damage *= self.getTotalCrit(['ultimate','blissUlt'])
    retval.damage *= self.getTotalDmg('ultimate')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 90.0 * (1.0 + self.BreakEfficiency)
    retval.energy = ( 5.0 + self.bonusEnergyType['ultimate'] ) * ( 1.0 + self.ER )
    return retval

  def useTalent(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('talent')
    retval.damage *= self.getTotalCrit(['followup','talent','bliss'])
    retval.damage *= self.getTotalDmg(['followup','talent'])
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.BreakEfficiency)
    retval.energy = ( 10.0 + self.bonusEnergyType['talent'] + self.bonusEnergyType['followup'] ) * ( 1.0 + self.ER )
    
    procrate = 0.62 if self.eidolon >= 5 else 0.6
    retval *= procrate
    return retval
  
def YanqingEstimationV1(character:BaseCharacter, Configuration:dict, CharacterDict:dict, EffectDict:dict):

  playerTurns = ( Configuration['numRounds'] + 0.5 )  * character.getTotalSpd() / 100
  enemyTurns = ( Configuration['numRounds'] + 0.5 ) * Configuration['enemySpeed'] / 100
  enemyAttacks = enemyTurns * Configuration['numberEnemyAttacksPerTurn'] * character.taunt / 100.0

  totalEffect:BaseEffect = BaseEffect()
  
  # bonus energy from kills and getting hit
  totalEffect.energy += Configuration['bonusEnergyFlat']
  totalEffect.energy += Configuration['bonusEnergyPerEnemyAttack'] * enemyAttacks
  
  # assume we spam skill every single turn
  totalEffect += playerTurns * character.useSkill()
  totalEffect += playerTurns * character.useTalent()
  
  # assume we apply break a number of times proportional to our gauge output and enemy toughness
  num_breaks = totalEffect.gauge / Configuration['enemyToughness']
  totalEffect += character.useBreak() * num_breaks
  
  # apply a number of break dots proportional to the amount of breaks we applied, up to the number of enemy turns
  num_dots = min(enemyTurns * Configuration['numEnemies'], num_breaks)
  totalEffect += character.useBreakDot() * num_dots
  
  # assume we use an ult proportional to the amount of energy we gained. Ignoring rounding errors and energy from enemy attacks
  num_ults = ( totalEffect.energy - (5 + 10 * (0.62 if character.eidolon >= 5 else 0.6) ) * (1 + character.ER) ) / character.maxEnergy
  
  totalEffect += num_ults * character.useUltimate()
  totalEffect += num_ults * character.useTalent() # apply soul sync as well
  
  print("Yanqing Effects:")
  totalEffect.print()

  CharacterDict[character.name] = copy(character)
  EffectDict[character.name] = copy(totalEffect)