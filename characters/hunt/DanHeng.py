from copy import copy
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class DanHeng(BaseCharacter):
  def __init__(self,
               lightcone:BaseLightCone,
               relicsetone:RelicSet,
               relicsettwo:RelicSet,
               planarset:RelicSet,
               relicstats:RelicStats,
               talentUptime:float = 0.25,
               slowUptime:float = 1.0,
               fasterThanLightUptime:float = 1.0,
               hiddenDragonUptime:float = 0.0,
               e1Uptime:float = 0.5,
               **config):
    super().__init__(lightcone, relicsetone, relicsettwo, planarset, relicstats, config)
    self.loadCharacterStats('Dan Heng')
    
    self.talentUptime = talentUptime
    self.slowUptime = slowUptime
    self.e1Uptime = e1Uptime
    self.fasterThanLightUptime = fasterThanLightUptime
    self.hiddenDragonUptime = hiddenDragonUptime

    self.longName = 'Dan Heng E{} {} S{}\n{} + {} + {}\nTalent Uptime: {}\nSlow Uptime: {}\n20% Spd Uptime: {}'.format(self.eidolon, self.lightcone.name, self.lightcone.superposition,
                                                                                          relicsetone.shortname, relicsettwo.shortname, planarset.shortname,
                                                                                          self.talentUptime,
                                                                                          self.slowUptime,
                                                                                          self.fasterThanLightUptime)

    # Talents

    self.percSpd += 0.20 * self.fasterThanLightUptime # Faster Than Light
    self.basicDmg += 0.40 * self.slowUptime # High Gale

    self.ultDmg += (1.296 if self.eidolon >= 5 else 1.2) * self.slowUptime # Ultimate

    self.CR += 0.12 * self.e1Uptime # The Higher You Fly, the Harder You Fall
    
    self.taunt *= 1.0 - 0.5 * self.hiddenDragonUptime # A2 ascension

    self.resPen += ( 0.396 if self.eidolon >= 5 else 0.36 ) * talentUptime * (0.5 if self.eidolon < 2 else 1.0)

    self.equipGear()
    self.balanceCrit()

  def useBasic(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk() + self.baseAtk * self.basicPercAtk
    retval.damage *= 1.1 if self.eidolon >= 3 else 1.0
    retval.damage *= 1.0 + min(self.CR + self.basicCR, 1.0) * (self.CD + self.basicCD)
    retval.damage *= 1.0 + self.Dmg + self.windDmg + self.basicDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.BreakEfficiency)
    retval.energy = ( 20.0 + self.bonusEnergyBasic ) * (1.0 + self.ER)
    retval.skillpoints = 1.0
    return retval

  def useSkill(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk() + self.baseAtk * self.skillPercAtk
    retval.damage *= 2.86 if self.eidolon >= 3 else 2.6
    retval.damage *= 1.0 + min(self.CR + self.skillCR, 1.0) * (self.CD + self.skillCD)
    retval.damage *= 1.0 + self.Dmg + self.windDmg + self.skillDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * (1.0 + self.BreakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergySkill ) * (1.0 + self.ER)
    retval.skillpoints = -1.0
    return retval

  def useUltimate(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk() + self.baseAtk * self.ultPercAtk
    retval.damage *= 4.32 if self.eidolon >= 5 else 4.0
    retval.damage *= 1.0 + min(self.CR + self.ultimateCR, 1.0) * (self.CD + self.ultimateCD)
    retval.damage *= 1.0 + self.Dmg + self.windDmg + self.ultDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 90.0 * (1.0 + self.BreakEfficiency)
    retval.energy = ( 5.0 + self.bonusEnergyUltimate ) * (1.0 + self.ER)
    retval.skillpoints = 0.0
    return retval
  
def DanHengEstimationV1(character:BaseCharacter, Configuration:dict, CharacterDict:dict, EffectDict:dict):
  
  playerTurns = ( Configuration['numRounds'] + 0.5 )  * character.getTotalSpd() / 100
  enemyTurns = ( Configuration['numRounds'] + 0.5 ) * Configuration['enemySpeed'] / 100
  enemyAttacks = enemyTurns * Configuration['numberEnemyAttacksPerTurn'] * character.taunt / 100.0

  #I'm just gonna ballpark 4 procs of EagleOfTwilightLine 4 pc here
  playerTurns += 0.25 * 4

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
  
  print("Dan Heng Effects:")
  totalEffect.print()

  CharacterDict[character.name] = copy(character)
  EffectDict[character.name] = copy(totalEffect)