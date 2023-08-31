from baseClasses.BaseEffect import BaseEffect
import pandas as pd

STATS_FILEPATH = 'characterStats\characterStats.csv'

class BaseCharacter(object):
  baseAtk:float
  baseDef:float
  baseHP:float
  baseSpd:float
  taunt:float
  maxEnergy:float

  # define information we would pull from the configuration dictionary and might use
  # helps with autocomplete in vs code
  numEnemies:int
  numRounds:float
  enemyLevel:int
  enemySpeed:float
  enemyType:str  
  bonusEnergyFlat:float
  bonusEnergyPerEnemyAttack:float
  numberEnemyAttacksPerTurn:float
  enemyMaxHP:float
  enemyToughness:float
  breakLevelMultiplier:float
  enemyRes:float
  brokenMultiplier:float
  
  def __init__(self, lightcone, relicsetone, relicsettwo, planarset, relicstats, config:dict):
    self.__dict__.update(config)
    
    self.eidolon = self.fourstarEidolons if self.rarity == 4 else self.fivestarEidolons
    
    self.lightcone = lightcone
    self.relicsetone = relicsetone
    self.relicsettwo = relicsettwo
    self.planarset = planarset
    self.relicstats = relicstats

    self.percAtk = 0.0
    self.percDef = 0.0
    self.percHP = 0.0
    self.percSpd = 0.0
    self.flatAtk = 0.0
    self.flatDef = 0.0
    self.flatHP = 0.0
    self.flatSpd = 0.0

    self.ER = 0.0
    self.BreakEffect = 0.0
    self.BreakEfficiency = 0.0

    self.EHR = 0.0
    self.Res = 0.0
    self.Break = 0.0
    self.Heal = 0.0

    self.Dmg = 0.0
    self.windDmg = 0.0
    self.fireDmg = 0.0
    self.iceDmg = 0.0
    self.lighDmg = 0.0
    self.physDmg = 0.0
    self.quanDmg = 0.0
    self.imagDmg = 0.0

    self.basicDmg = 0.0
    self.skillDmg = 0.0
    self.ultDmg = 0.0
    self.dotDmg = 0.0
    self.followupDmg = 0.0

    self.defShred = 0.0
    self.resPen = 0.0
    
  def loadCharacterStats(self, name:str):
    df = pd.read_csv(STATS_FILEPATH)
    rows = df.iloc[:, 0]
    for column in df.columns:
        data = df.loc[rows[rows == name].index,column].values[0]
        self.__dict__[column] = data

  def equipGear(self):
    self.lightcone.equipTo(self)
    self.relicsetone.equipTo(self)
    self.relicsettwo.equipTo(self)
    self.planarset.equipTo(self)
    self.relicstats.equipTo(self)

  def balanceCrit(self):
    totalCV = self.CR * 2 + self.CD
    self.CR = totalCV / 4.0
    self.CD = totalCV / 2.0

  def getTotalAtk(self):
    return self.baseAtk * ( 1 + self.percAtk ) + self.flatAtk

  def getTotalDef(self):
    return self.baseDef * ( 1 + self.percDef ) + self.flatDef

  def getTotalHP(self):
    return self.baseHP * ( 1 + self.percHP ) + self.flatHP

  def getTotalSpd(self):
    return self.baseSpd * ( 1 + self.percSpd ) + self.flatSpd

  def useBasic(self):
    retval = BaseEffect()
    retval.gauge = 30.0 * (1.0 + self.BreakEfficiency)
    retval.energy = 20.0 * (1.0 + self.ER)
    retval.skillpoints = 1.0
    return retval

  def useSkill(self):
    retval = BaseEffect()
    retval.gauge = 60.0 * (1.0 + self.BreakEfficiency)
    retval.energy = 30.0 * (1.0 + self.ER)
    retval.skillpoints = -1.0
    return retval

  def useUltimate(self):
    retval = BaseEffect()
    retval.energy = 5.0 * (1.0 + self.ER)
    return retval

  def useTalent(self):
    return BaseEffect()

  def useEnhancedBasic(self):
    return BaseEffect()

  def useDot(self):
    return BaseEffect()

  def useBreak(self):
    retval = BaseEffect()

    breakMultipliers = {
        'wind': 2.0,
        'fire': 2.0,
        'ice': 1.0,
        'lightning': 1.0,
        'wind': 1.5,
        'quantum': 0.5,
        'imaginary': 0.5,
    }

    baseDotDamage = self.breakLevelMultiplier
    baseDotDamage *= 0.5 + self.enemyToughness / 120
    baseDotDamage *= breakMultipliers[self.element]
    baseDotDamage *= 1.0 + self.Break
    baseDotDamage = self.applyDamageMultipliers(baseDotDamage)

    retval.damage = baseDotDamage
    return retval

  def useBreakDot(self):
    retval = BaseEffect()
    baseDotDamage = 0.0

    if self.element == 'physical':
      baseDotDamage = 2.0 *self.breakLevelMultiplier
      baseDotDamage *= 0.5 + self.enemyToughness / 120
      if self.enemyType == 'elite':
        bleedDamage = 0.07 * self.enemyMaxHP
      else:
        bleedDamage = 0.16 * self.enemyMaxHP
      baseDotDamage = min(baseDotDamage, bleedDamage)
    elif self.element == 'fire':
      baseDotDamage = self.breakLevelMultiplier
    elif self.element == 'ice':
      baseDotDamage = self.breakLevelMultiplier
    elif self.element == 'lightning':
      baseDotDamage = 2.0 * self.breakLevelMultiplier
    elif self.element == 'wind': #assume 3 stacks
      baseDotDamage = 3.0 * self.breakLevelMultiplier
    elif self.element == 'quantum': #assume 3 stacks
      baseDotDamage = 0.6 * 3 * self.breakLevelMultiplier
      baseDotDamage *= 0.5 + self.enemyToughness / 120

    baseDotDamage *= 1.0 + self.Break
    baseDotDamage = self.applyDamageMultipliers(baseDotDamage)

    retval.damage = baseDotDamage
    return retval

  def applyDamageMultipliers(self, baseDamage:float) -> float:
    damage = baseDamage
    damage *= (80 + 20 ) / ( ( self.enemyLevel + 20 ) * ( 1 - self.defShred ) + 80 + 20 )
    damage *= max(min(1 - self.enemyRes + self.resPen, 2.0), 0.1)
    damage *= self.brokenMultiplier
    return damage
