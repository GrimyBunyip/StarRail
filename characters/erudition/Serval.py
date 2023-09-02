from copy import copy
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Serval(BaseCharacter):
  def __init__(self,
               lightcone:BaseLightCone,
               relicsetone:RelicSet,
               relicsettwo:RelicSet,
               planarset:RelicSet,
               relicstats:RelicStats,
               **config):
    super().__init__(lightcone, relicsetone, relicsettwo, planarset, relicstats, config)
    self.loadCharacterStats('Serval')
    
    self.longName = 'Serval E{} {} S{}\n{} + {} + {}'.format(self.eidolon, self.lightcone.name, self.lightcone.superposition,
                                                                                          relicsetone.shortname, relicsettwo.shortname, planarset.shortname,)

    # Talents

    self.equipGear()
    self.balanceCrit()

  def useBasic(self, addTalent = True):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk() + self.baseAtk * self.basicPercAtk
    talentBase = 1.1 if self.eidolon >= 3 else 1.0
    talentBase += ( self.numEnemies * ( 0.792 if self.eidolon >= 5 else 0.72 ) ) if addTalent else 0.0
    retval.damage *= talentBase
    retval.damage *= 1.1 if self.eidolon >= 3 else 1.0
    retval.damage *= 1.0 + min(self.CR + self.basicCR, 1.0) * (self.CD + self.basicCD)
    retval.damage *= 1.0 + self.Dmg + self.lighDmg + self.basicDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 30.0 * self.numEnemies if addTalent else 30.0 ) * (1.0 + self.BreakEfficiency)
    retval.energy = ( 20.0 + self.bonusEnergyBasic ) * (1.0 + self.ER)
    retval.skillpoints = 1.0
    return retval

  def useSkill(self, addTalent = True):
    num_adjacents = min( self.numEnemies - 1, 2 )
    retval = BaseEffect()
    retval.damage = self.getTotalAtk() + self.baseAtk * self.skillPercAtk
    talentBase = ( 1.4 if self.eidolon >= 3 else 1.54 ) + num_adjacents * ( 0.6 if self.eidolon >= 3 else 0.66 )
    talentBase += ( ( 0.792 if self.eidolon >= 5 else 0.72 ) * ( 1 + num_adjacents ) )  if addTalent else 0.0
    retval.damage *= talentBase
    retval.damage *= 1.0 + min(self.CR + self.skillCR, 1.0) * (self.CD + self.skillCD)
    retval.damage *= 1.0 + self.Dmg + self.lighDmg + self.skillDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * (1.0 + self.BreakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergySkill ) * (1.0 + self.ER)
    retval.skillpoints = -1.0
    return retval

  def useUltimate(self, addTalent = True):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk() + self.baseAtk * self.ultPercAtk
    talentBase = 1.8 if self.eidolon >= 5 else 1.944
    talentBase += ( 0.792 if self.eidolon >= 5 else 0.72 ) if addTalent else 0.0
    retval.damage *= self.numEnemies * talentBase
    retval.damage *= 1.0 + min(self.CR + self.ultimateCR, 1.0) * (self.CD + self.ultimateCD)
    retval.damage *= 1.0 + self.Dmg + self.lighDmg + self.ultDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * self.numEnemies * (1.0 + self.BreakEfficiency)
    retval.energy = ( 5.0 + self.bonusEnergyUlt ) * (1.0 + self.ER)
    retval.skillpoints = 0.0
    return retval

  def useDot(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk() + self.baseAtk * self.dotPercAtk
    retval.damage *= 1.04 if self.eidolon >= 5 else 114.4
    #no crits on dots
    retval.damage *= 1.0 + self.Dmg + self.lighDmg + self.dotDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 0.0
    retval.energy = 0.0
    retval.skillpoints = 0.0
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