from copy import copy
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

# Lazy, haven't implemented E1 or E4 or E6

class Blade(BaseCharacter):

  def __init__(self,
               lightcone:BaseLightCone,
               relicsetone:RelicSet,
               relicsettwo:RelicSet,
               planarset:RelicSet,
               relicstats:RelicStats,
               hpLossTally:float = 0.9,
               hellscapeUptime:float = 1.0,
               **config):
    super().__init__(lightcone, relicsetone, relicsettwo, planarset, relicstats, config)
    self.loadCharacterStats('Blade')
    
    self.hpLossTally = hpLossTally
    self.hellscapeUptime = hellscapeUptime

    self.longName = 'Blade E{} {} S{}\n{} + {} + {}\nhpLossTally Uptime: {}\nHellscape Uptime: {}'.format(self.eidolon, self.lightcone.shortname, self.lightcone.superposition,
                                                                                          relicsetone.shortname, relicsettwo.shortname, planarset.shortname,
                                                                                          self.hpLossTally,
                                                                                          self.hellscapeUptime)

    # Talents

    self.followupDmg += 0.20 # Ascensions
    
    self.CR += 0.15 * self.hellscapeUptime if self.eidolon >= 2 else 0.0

    self.equipGear()
    self.balanceCrit()

  def useBasic(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk()
    retval.damage *= 1.1 if self.eidolon >= 3 else 1.0
    retval.damage *= 1.0 + min(self.CR, 1.0) * self.CD
    retval.damage *= 1.0 + self.Dmg + self.windDmg + self.basicDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.BreakEfficiency)
    retval.energy = 20.0 * (1.0 + self.ER)
    retval.skillpoints = 1.0
    return retval

  def useEnhancedBasic(self):
    num_adjacents = min( self.numEnemies - 1, 2 )
    retval = BaseEffect()
    retval.damage = self.getTotalAtk() * ( 0.44 if self.eidolon >= 3 else 0.4 )
    retval.damage += self.getTotalHP() * ( 1.10 if self.eidolon >= 3 else 1.0 )
    retval.damage += self.getTotalAtk() * ( 0.176 if self.eidolon >= 3 else 0.16 ) * num_adjacents
    retval.damage += self.getTotalHP() * ( 0.440 if self.eidolon >= 3 else 0.40 ) * num_adjacents
    retval.damage *= 1.0 + min(self.CR, 1.0) * self.CD
    retval.damage *= 1.0 + self.Dmg + self.windDmg + self.basicDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * (1.0 + self.BreakEfficiency)
    retval.energy = 30.0 * (1.0 + self.ER)
    retval.skillpoints = - 1.0 / 3 # just gonna estimate it by tweaking this here
    return retval

  def useSkill(self):
    retval = BaseEffect()
    retval.damage = 0.0
    retval.gauge = 0.0
    retval.energy = 0.0
    retval.skillpoints = -1.0
    return retval

  def useUltimate(self):
    num_adjacents = min( self.numEnemies - 1, 2 )
    retval = BaseEffect()
    retval.damage = self.getTotalAtk() * ( 0.432 if self.eidolon >= 5 else 0.4 )
    retval.damage += self.getTotalHP() * ( 1.08 if self.eidolon >= 5 else 1.0 )
    retval.damage += self.getTotalAtk() * ( 0.1728 if self.eidolon >= 5 else 0.16 ) * num_adjacents
    retval.damage += self.getTotalHP() * ( 0.432 if self.eidolon >= 5 else 0.40 ) * num_adjacents
    retval.damage += self.getTotalHP() * ( 1.08 * self.hpLossTally if self.eidolon >= 3 else 1.0 * self.hpLossTally )
    retval.damage += self.getTotalHP() * ( 0.432 * self.hpLossTally if self.eidolon >= 3 else 0.40 * self.hpLossTally ) * num_adjacents
    retval.damage *= 1.0 + min(self.CR, 1.0) * self.CD
    retval.damage *= 1.0 + self.Dmg + self.windDmg + self.ultDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 60.0 + 60.0 * num_adjacents ) * (1.0 + self.BreakEfficiency)
    retval.energy = 5.0 * (1.0 + self.ER)
    retval.skillpoints = 0
    return retval

  def useTalent(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk() * ( 0.484 if self.eidolon >= 5 else 0.44 ) * self.numEnemies
    retval.damage += self.getTotalHP() * ( 1.21 if self.eidolon >= 5 else 1.1 ) * self.numEnemies
    retval.damage *= 1.0 + min(self.CR, 1.0) * self.CD
    retval.damage *= 1.0 + self.Dmg + self.windDmg + self.followupDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 30.0 * self.numEnemies ) * (1.0 + self.BreakEfficiency)
    retval.energy = 10.0 * (1.0 + self.ER)
    retval.skillpoints = 0
    return retval
  
def BladeEstimationsV1(character:BaseCharacter, Configuration:dict, CharacterDict:dict, EffectDict:dict):

  playerTurns = ( Configuration['numRounds'] + 0.5 )  * character.getTotalSpd() / 100
  enemyTurns = ( Configuration['numRounds'] + 0.5 ) * Configuration['enemySpeed'] / 100
  enemyAttacks = enemyTurns * Configuration['numberEnemyAttacksPerTurn'] * character.taunt / 100.0

  totalEffect = BaseEffect()
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