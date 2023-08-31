from copy import copy
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from lightCones.ASecretVow import ASecretVow
from lightCones.CruisingInTheStellarSea import CruisingInTheStellarSea
from relicSets.InertSalsotto import InertSalsotto
from relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc

# Lazy, haven't implemented E1 or E4 or E6

class Blade(BaseCharacter):

  def __init__(self,
               lightcone:BaseLightCone,
               relicsetone:RelicSet,
               relicsettwo:RelicSet,
               planarset:RelicSet,
               relicstats:RelicStats,
               name:str='Blade',
               hpLossTally:float = 0.9,
               hellscapeUptime:float = 1.0,
               graphic:str = 'https://static.wikia.nocookie.net/houkai-star-rail/images/9/90/Character_Blade_Icon.png',
               **config):
    super().__init__()
    self.lightcone = lightcone
    self.relicsetone = relicsetone
    self.relicsettwo = relicsettwo
    self.planarset = planarset
    self.relicstats = relicstats
    
    self.hpLossTally = hpLossTally
    self.hellscapeUptime = hellscapeUptime

    self.name = name
    self.graphic = graphic
    self.config = config
    self.eidolon = config['fivestarEidolons']

    self.element = 'wind'

    # Base Stats

    self.baseAtk = 543.31
    self.baseDef = 485.1
    self.baseHP = 1358
    self.baseSpd = 97
    self.maxEnergy = 130

    # Talents

    self.CR += 0.027 + 0.04 + 0.053 # Ascensions
    self.percHP += 0.04 + 0.06 + 0.06 + 0.08 + 0.04 # Ascensions
    self.Res += 0.04 + 0.06 # Ascensions
    self.followupDmg += 0.20 # Ascensions
    
    self.CR += 0.15 * self.hellscapeUptime if self.eidolon >= 2 else 0.0

    self.equipGear()
    self.balanceCrit()

  def useBasic(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk()
    retval.damage *= 1.1 if self.eidolon >= 3 else 1.0
    retval.damage *= 1.0 + min(self.CR, 1.0) * self.CD
    retval.damage *= 1.0 + self.windDmg + self.basicDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.BreakEff)
    retval.energy = 20.0 * (1.0 + self.ER)
    retval.skillpoints = 1.0
    return retval

  def useEnhancedBasic(self):
    num_adjacents = min( self.config['numEnemies'] - 1, 2 )
    retval = BaseEffect()
    retval.damage = self.getTotalAtk() * ( 0.44 if self.eidolon >= 3 else 0.4 )
    retval.damage += self.getTotalHP() * ( 1.10 if self.eidolon >= 3 else 1.0 )
    retval.damage += self.getTotalAtk() * ( 0.176 if self.eidolon >= 3 else 0.16 ) * num_adjacents
    retval.damage += self.getTotalHP() * ( 0.440 if self.eidolon >= 3 else 0.40 ) * num_adjacents
    retval.damage *= 1.0 + min(self.CR, 1.0) * self.CD
    retval.damage *= 1.0 + self.windDmg + self.basicDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * (1.0 + self.BreakEff)
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
    num_adjacents = min( self.config['numEnemies'] - 1, 2 )
    retval = BaseEffect()
    retval.damage = self.getTotalAtk() * ( 0.432 if self.eidolon >= 5 else 0.4 )
    retval.damage += self.getTotalHP() * ( 1.08 if self.eidolon >= 5 else 1.0 )
    retval.damage += self.getTotalAtk() * ( 0.1728 if self.eidolon >= 5 else 0.16 ) * num_adjacents
    retval.damage += self.getTotalHP() * ( 0.432 if self.eidolon >= 5 else 0.40 ) * num_adjacents
    retval.damage += self.getTotalHP() * ( 1.08 * self.hpLossTally if self.eidolon >= 3 else 1.0 * self.hpLossTally )
    retval.damage += self.getTotalHP() * ( 0.432 * self.hpLossTally if self.eidolon >= 3 else 0.40 * self.hpLossTally ) * num_adjacents
    retval.damage *= 1.0 + min(self.CR, 1.0) * self.CD
    retval.damage *= 1.0 + self.windDmg + self.ultDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 60.0 + 60.0 * num_adjacents ) * (1.0 + self.BreakEff)
    retval.energy = 5.0 * (1.0 + self.ER)
    retval.skillpoints = 0
    return retval

  def useTalent(self):
    retval = BaseEffect()
    retval.damage = self.getTotalAtk() * ( 0.484 if self.eidolon >= 5 else 0.44 ) * self.config['numEnemies']
    retval.damage += self.getTotalHP() * ( 1.21 if self.eidolon >= 5 else 1.1 ) * self.config['numEnemies']
    retval.damage *= 1.0 + min(self.CR, 1.0) * self.CD
    retval.damage *= 1.0 + self.windDmg + self.followupDmg
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = ( 30.0 * self.config['numEnemies'] ) * (1.0 + self.BreakEff)
    retval.energy = 10.0 * (1.0 + self.ER)
    retval.skillpoints = 0
    return retval
  
def BladeV1(Configuration:dict, CharacterDict:dict, EffectDict:dict):
    relic1 = LongevousDisciple2pc()
    relic2 = LongevousDisciple4pc()
    relic3 = InertSalsotto()
    relicstats = RelicStats(mainstats = ['percHP', 'flatSpd', 'CR', 'windDmg'],
                            substats = {'CR': 7, 'CD': 7, 'flatSpd': 6})
    Cone = ASecretVow(passiveUptime = 0.5, **Configuration)
    character = Blade(Cone,
                relic1,
                relic2,
                relic3,
                relicstats,
                'Blade E0 Secret Vow S5\n7 CR, 7 CD, 6 Spd Substats\n50% health loss tally\nBlade takes 1 hit per enemy turn\n50% Secret Vow Uptime',
                hpLossTally=0.5,
                **Configuration)

    playerTurns = ( Configuration['numRounds'] + 0.5 )  * character.getTotalSpd() / 100
    enemyTurns = ( Configuration['numRounds'] + 0.5 ) * Configuration['enemySpeed'] / 100

    totalEffect = BaseEffect()
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
    # Assume blade takes 1 hit per enemy turn. 1 hit per Ult, 1.333 hits per his turn
    num_hits = enemyTurns + playerTurns * (4/3) + num_ults
    totalEffect += character.useTalent() * ( num_hits / 5.0 ) 
    print("Blade Effects:")
    totalEffect.print()

    CharacterDict[character.name] = copy(character)
    EffectDict[character.name] = copy(totalEffect)