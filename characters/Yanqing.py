from copy import copy
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from lightCones.CruisingInTheStellarSea import CruisingInTheStellarSea
from relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc, HunterOfGlacialForest4pc
from relicSets.SpaceSealingStation import SpaceSealingStation

class Yanqing(BaseCharacter):

  def __init__(self,
               lightcone:BaseLightCone,
               relicsetone:RelicSet,
               relicsettwo:RelicSet,
               planarset:RelicSet,
               relicstats:RelicStats,
               name:str='Yanqing',
               graphic:str = 'https://static.wikia.nocookie.net/houkai-star-rail/images/5/57/Character_Yanqing_Icon.png',
               soulsteelUptime = 1.0,
               searingStingUptime = 1.0,
               rainingBlissUptime = 0.25,
               **config):
    super().__init__()
    self.lightcone = lightcone
    self.relicsetone = relicsetone
    self.relicsettwo = relicsettwo
    self.planarset = planarset
    self.relicstats = relicstats

    self.soulsteelUptime = soulsteelUptime
    self.searingStingUptime = searingStingUptime
    self.rainingBlissUptime = rainingBlissUptime

    self.name = name
    self.graphic = graphic
    self.config = config
    self.eidolon = config['fivestarEidolons']

    self.element = 'ice'

    # Base Stats

    self.baseAtk = 679.14
    self.baseDef = 412.34
    self.baseHP = 893.00
    self.baseSpd = 109
    self.maxEnergy = 140

    # Talents

    self.percAtk += 0.04 + 0.06 + 0.08 + 0.04 + 0.06 # Ascensions
    self.iceDmg += 0.032 + 0.048 + 0.064 # Ascensions
    self.percHP += 0.06 + 0.04 # Ascensions

    self.ER += 0.10 * self.soulsteelUptime if self.eidolon >= 2 else 0.0
    self.resPen += 0.12 * self.searingStingUptime if self.eidolon >= 4 else 0.0

    #soulsteel
    self.CR += self.soulsteelUptime * ( 0.22 if self.eidolon >= 5 else 0.20 )
    self.CD += self.soulsteelUptime * ( 0.33 if self.eidolon >= 5 else 0.30 )
    self.bliss_cr = 0.6
    self.bliss_cd = 0.54 if self.eidolon >= 5 else 0.5

    self.equipGear()
    #self.balanceCrit() do not balance crit on yanqing

  def useBasic(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk()
    retval.damage *= ( 1.1 if self.eidolon >= 3 else 1.0 ) + ( 0.6 if self.eidolon >= 1 else 0.0 )
    retval.damage *= 1.0 + min(self.CR + self.bliss_cr * self.rainingBlissUptime, 1.0) * (self.CD + self.bliss_cd * self.rainingBlissUptime)
    retval.damage *= 1.0 + self.iceDmg + self.basicDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.BreakEff)
    retval.energy = 20.0 * (1.0 + self.ER)
    retval.skillpoints = 1.0
    return retval

  def useSkill(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk()
    retval.damage *= ( 2.42 if self.eidolon >= 3 else 2.2 ) + ( 0.6 if self.eidolon >= 1 else 0.0 )
    retval.damage *= 1.0 + min(self.CR + self.bliss_cr * self.rainingBlissUptime, 1.0) * (self.CD + self.bliss_cd * self.rainingBlissUptime)
    retval.damage *= 1.0 + self.iceDmg + self.skillDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * (1.0 + self.BreakEff)
    retval.energy = 30.0 * (1.0 + self.ER)
    retval.skillpoints = -1.0
    return retval

  def useUltimate(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk()
    retval.damage *= ( 3.78 if self.eidolon >= 5 else 3.5 ) + ( 0.6 if self.eidolon >= 1 else 0.0 )
    retval.damage *= 1.0 + min(self.CR + self.bliss_cr, 1.0) * (self.CD + self.bliss_cd)
    retval.damage *= 1.0 + self.iceDmg + self.ultDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 90.0 * (1.0 + self.BreakEff)
    retval.energy = 5.0 * (1.0 + self.ER)
    retval.skillpoints = 0.0
    return retval


  def useTalent(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk()
    retval.damage *= 0.55 if self.eidolon >= 5 else 0.5
    retval.damage *= 1.0 + min(self.CR + self.bliss_cr * self.rainingBlissUptime, 1.0) * (self.CD + self.bliss_cd * self.rainingBlissUptime)
    retval.damage *= 1.0 + self.iceDmg + self.followupDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.BreakEff)
    retval.energy = 10.0 * (1.0 + self.ER)
    retval.skillpoints = 0.0
    
    retval *= 0.62 if self.eidolon >= 5 else 0.6
    return retval
  
def YanqingV1(Configuration:dict, CharacterDict:dict, EffectDict:dict):
  relic1 = HunterOfGlacialForest2pc()
  relic2 = HunterOfGlacialForest4pc()
  relic3 = SpaceSealingStation()
  relicstats = RelicStats(mainstats = ['percAtk', 'flatSpd', 'CD', 'iceDmg'],
                          substats = {'percAtk': 8, 'CD': 12})
  Cone = CruisingInTheStellarSea(passiveUptime = 0.5, **Configuration)
  character = Yanqing(Cone,
                relic1,
                relic2,
                relic3,
                relicstats,
                'Yanqing E0 Cruising S5\n8 ATK% subs, 12 CD subs\n100% soulsteel uptime',
                soulsteelUptime = 1.0,
                searingStingUptime = 1.0,
                rainingBlissUptime = 0.25,
                **Configuration)

  playerTurns = ( Configuration['numRounds'] + 0.5 )  * character.getTotalSpd() / 100
  enemyTurns = ( Configuration['numRounds'] + 0.5 ) * Configuration['enemySpeed'] / 100

  totalEffect = BaseEffect()
  # assume we spam skill every single turn
  totalEffect += playerTurns * character.useSkill()
  totalEffect += playerTurns * character.useTalent() # apply soul sync as well
  # assume we apply break a number of times proportional to our gauge output and enemy toughness
  num_breaks = totalEffect.gauge / Configuration['enemyToughness']
  totalEffect += character.useBreak() * num_breaks
  # apply a number of break dots proportional to the amount of breaks we applied, up to the number of enemy turns
  num_dots = min(enemyTurns * Configuration['numEnemies'], num_breaks)
  totalEffect += character.useBreakDot() * num_dots
  # assume we use an ult proportional to the amount of energy we gained. Ignoring rounding errors and energy from enemy attacks
  num_ults = totalEffect.energy / character.maxEnergy
  totalEffect += character.useUltimate() * num_ults
  totalEffect += character.useTalent() * num_ults # apply soul sync as well
  print(character.CR, character.CD)
  print("Yanqing Effects:")
  totalEffect.print()

  CharacterDict[character.name] = copy(character)
  EffectDict[character.name] = copy(totalEffect)