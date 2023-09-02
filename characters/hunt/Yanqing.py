from copy import copy
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
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

    self.longName = 'Yanqing E{} {} S{}\n{} + {} + {}\nSoulsteel Uptime: {}\nUltimate Uptime: {}'.format(self.eidolon, self.lightcone.shortname, self.lightcone.superposition,
                                                                                          relicsetone.shortname, relicsettwo.shortname, planarset.shortname,
                                                                                          self.soulsteelUptime,
                                                                                          self.rainingBlissUptime)

    # Talents

    self.ER += 0.10 * self.soulsteelUptime if self.eidolon >= 2 else 0.0
    self.resPen += 0.12 * self.e4Uptime if self.eidolon >= 4 else 0.0

    #soulsteel
    self.CR += self.soulsteelUptime * ( 0.22 if self.eidolon >= 5 else 0.20 )
    self.CD += self.soulsteelUptime * ( 0.33 if self.eidolon >= 5 else 0.30 )
    self.blissCR = 0.6
    self.blissCD = 0.54 if self.eidolon >= 5 else 0.5
    self.taunt *= 0.4

    self.equipGear()
    #self.balanceCrit() do not balance crit on yanqing

  def useBasic(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk()
    retval.damage *= ( 1.1 if self.eidolon >= 3 else 1.0 ) + ( 0.6 if self.eidolon >= 1 else 0.0 )
    retval.damage *= 1.0 + min(self.CR + self.basicCR + self.blissCR * self.rainingBlissUptime, 1.0) * (self.CD + self.basicCD + self.blissCD * self.rainingBlissUptime)
    retval.damage *= 1.0 + self.Dmg + self.iceDmg + self.basicDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.BreakEfficiency)
    retval.energy = ( 20.0 + self.bonusEnergyBasic ) * (1.0 + self.ER)
    retval.skillpoints = 1.0
    return retval

  def useSkill(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk()
    retval.damage *= ( 2.42 if self.eidolon >= 3 else 2.2 ) + ( 0.6 if self.eidolon >= 1 else 0.0 )
    retval.damage *= 1.0 + min(self.CR + self.skillCR + self.blissCR * self.rainingBlissUptime, 1.0) * (self.CD + self.skillCD + self.blissCD * self.rainingBlissUptime)
    retval.damage *= 1.0 + self.Dmg + self.iceDmg + self.skillDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * (1.0 + self.BreakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergySkill ) * (1.0 + self.ER)
    retval.skillpoints = -1.0
    return retval

  def useUltimate(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk()
    retval.damage *= ( 3.78 if self.eidolon >= 5 else 3.5 ) + ( 0.6 if self.eidolon >= 1 else 0.0 )
    retval.damage *= 1.0 + min(self.CR + self.ultimateCR + self.blissCR, 1.0) * (self.CD + self.ultimateCD + self.blissCD)
    retval.damage *= 1.0 + self.Dmg + self.iceDmg + self.ultDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 90.0 * (1.0 + self.BreakEfficiency)
    retval.energy = ( 5.0 + self.bonusEnergyUlt ) * (1.0 + self.ER)
    retval.skillpoints = 0.0
    return retval

  def useTalent(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk()
    retval.damage *= 0.55 if self.eidolon >= 5 else 0.5
    retval.damage *= 1.0 + min(self.CR + self.blissCR * self.rainingBlissUptime, 1.0) * (self.CD + self.blissCD * self.rainingBlissUptime)
    retval.damage *= 1.0 + self.Dmg + self.iceDmg + self.followupDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.BreakEfficiency)
    retval.energy = ( 10.0 + self.bonusEnergyTalent ) * (1.0 + self.ER)
    retval.skillpoints = 0.0
    
    retval *= 0.62 if self.eidolon >= 5 else 0.6
    return retval
  
def YanqingEstimationV1(character:BaseCharacter, Configuration:dict, CharacterDict:dict, EffectDict:dict):

  playerTurns = ( Configuration['numRounds'] + 0.5 )  * character.getTotalSpd() / 100
  enemyTurns = ( Configuration['numRounds'] + 0.5 ) * Configuration['enemySpeed'] / 100
  enemyAttacks = enemyTurns * Configuration['numberEnemyAttacksPerTurn'] * character.taunt / 100.0

  totalEffect = BaseEffect()
  
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