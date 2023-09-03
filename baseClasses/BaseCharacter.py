import pandas as pd
from baseClasses.BaseEffect import BaseEffect

STATS_FILEPATH = 'stats\CharacterStats.csv'

class BaseCharacter(object):
  baseAtk:float
  baseDef:float
  baseHP:float
  baseSpd:float

  CR:float
  CD:float

  taunt:float
  initialEnergy:float
  maxEnergy:float
  path:str
  element:str
  name:str

  percAtk:float
  percDef:float
  percHP:float
  EHR:float
  Res:float
  windDmg:float
  fireDmg:float
  iceDmg:float
  lighDmg:float
  physDmg:float
  quanDmg:float
  imagDmg:float

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

  def __init__(self, relicstats, lightcone=None, relicsetone=None, relicsettwo=None, planarset=None, **config):
    self.__dict__.update(config)
    
    self.lightcone = lightcone
    self.relicsetone = relicsetone
    self.relicsettwo = relicsettwo
    self.planarset = planarset
    self.relicstats = relicstats

    self.percSpd = 0.0
    self.flatAtk = 0.0
    self.flatDef = 0.0
    self.flatHP = 0.0
    self.flatSpd = 0.0

    self.ER = 0.0
    self.breakEffect = 0.0
    self.breakEfficiency = 0.0
    self.Heal = 0.0
    
    self.allRes = 0.0
    self.dmgReduction = 0.0
    self.percTaunt = 0.0
    self.percShield = 0.0
    
    self.Dmg = 0.0
    self.DmgType = {
      'basic':0.0,
      'skill':0.0,
      'ultimate':0.0,
      'talent':0.0,
      'followup':0.0,
      'dot':0.0,
    }
    
    self.CRType = {
      'basic':0.0,
      'skill':0.0,
      'ultimate':0.0,
      'talent':0.0,
      'followup':0.0,
      'dot':0.0,
    }
    
    self.CDType = {
      'basic':0.0,
      'skill':0.0,
      'ultimate':0.0,
      'talent':0.0,
      'followup':0.0,
      'dot':0.0,
    }

    self.percAtkType = {
      'basic':0.0,
      'skill':0.0,
      'ultimate':0.0,
      'talent':0.0,
      'followup':0.0,
      'dot':0.0,
    }

    self.percDefType = {
      'basic':0.0,
      'skill':0.0,
      'ultimate':0.0,
      'talent':0.0,
      'followup':0.0,
      'dot':0.0,
    }

    self.percHPType = {
      'basic':0.0,
      'skill':0.0,
      'ultimate':0.0,
      'talent':0.0,
      'followup':0.0,
      'dot':0.0,
    }
    
    self.bonusEnergyType = {
      'basic':0.0,
      'skill':0.0,
      'ultimate':0.0,
      'talent':0.0,
      'followup':0.0,
      'dot':0.0,
    }
    
    self.advanceForwardType = {
      'basic':0.0,
      'skill':0.0,
      'ultimate':0.0,
      'talent':0.0,
      'followup':0.0,
      'dot':0.0,
    }

    self.defShred = 0.0
    self.resPen = 0.0
    
    self.motionValueDict = {}
    
  def loadCharacterStats(self, name:str):
    df = pd.read_csv(STATS_FILEPATH)
    rows = df.iloc[:, 0]
    for column in df.columns:
        data = df.loc[rows[rows == name].index,column].values[0]
        self.__dict__[column] = data
        
    self.initialEnergy = self.maxEnergy * 0.5
    self.eidolon = self.fourstarEidolons if self.rarity == 4 else self.fivestarEidolons
    
    self.longName = '{} E{} {} S{}\n{}{}{}'.format(self.name, self.eidolon, self.lightcone.name, self.lightcone.superposition,
                                                          "" if self.relicsetone is None else self.relicsetone.shortname, 
                                                          "" if self.relicsettwo is None else (" + " + self.relicsettwo.shortname), 
                                                          "" if self.planarset is None else (" + " + self.planarset.shortname))

  def equipGear(self):
    if self.lightcone is not None: self.lightcone.equipTo(self)
    if self.relicsetone is not None: self.relicsetone.equipTo(self)
    if self.relicsettwo is not None: self.relicsettwo.equipTo(self)
    if self.planarset is not None: self.planarset.equipTo(self)
    if self.relicstats is not None: self.relicstats.equipTo(self)

  def balanceCrit(self):
    totalCV = self.CR * 2 + self.CD
    self.CR = totalCV / 4.0
    self.CD = totalCV / 2.0
    
  def getTotalTaunt(self):
    return self.taunt * (1 + self.percTaunt)

  def getTotalAtk(self, type='None'):
    if isinstance(type, list):
      bonuses = sum([self.percAtkType[x] for x in type])
      return self.baseAtk * ( 1 + self.percAtk + bonuses ) + self.flatAtk
    else:
      return self.baseAtk * ( 1 + self.percAtk + self.percAtkType[type] ) + self.flatAtk

  def getTotalDef(self, type='None'):
    if isinstance(type, list):
      bonuses = sum([self.percDefType[x] for x in type])
      return self.baseDef * ( 1 + self.percDef + bonuses ) + self.flatDef
    else:
      return self.baseDef * ( 1 + self.percDef + self.percDefType[type] ) + self.flatDef

  def getTotalHP(self, type='None'):
    if isinstance(type, list):
      bonuses = sum([self.percHPType[x] for x in type])
      return self.baseHP * ( 1 + self.percHP + bonuses ) + self.flatHP
    else:
      return self.baseHP * ( 1 + self.percHP + self.percHPType[type] ) + self.flatHP
  
  def getTotalCrit(self, type='None'):
    if isinstance(type, list):
      crBonuses = sum([self.CRType[x] for x in type])
      cdBonuses = sum([self.CDType[x] for x in type])
      return 1.0 + min(1.0, self.CR + crBonuses) * (self.CD + cdBonuses)
    else:
      return 1.0 + min(1.0, self.CR + self.CRType[type]) * (self.CD + self.CDType[type])
    
  def getTotalDmg(self, type='None'):
    elementDmg = {
      'wind': self.windDmg,
      'ice': self.iceDmg,
      'fire': self.fireDmg,
      'lightning': self.lighDmg,
      'physical': self.physDmg,
      'quantum': self.quanDmg,
      'imaginary': self.imagDmg,
    }
    
    if isinstance(type, list):
      bonuses = sum([self.DmgType[x] for x in type])
      return 1.0 + self.Dmg + elementDmg[self.element] + bonuses
    else:
      return 1.0 + self.Dmg + elementDmg[self.element] + self.DmgType[type]

  def getTotalSpd(self):
    return self.baseSpd * ( 1 + self.percSpd ) + self.flatSpd
  
  def getTotalMotionValue(self, type:str):
    total = 0.0
    for key, value in self.motionValueDict.items():
      if key == type:
        if isinstance(value, list):
          total += sum(x.calculate(self) for x in value)
        else:
          total += value.calculate(self)
    return total

  def useBasic(self):
    retval = BaseEffect()
    retval.gauge = 30.0 * (1.0 + self.breakEfficiency)
    retval.energy = 20.0 * (1.0 + self.ER)
    retval.skillpoints = 1.0
    return retval

  def useSkill(self):
    retval = BaseEffect()
    retval.gauge = 60.0 * (1.0 + self.breakEfficiency)
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
    baseDotDamage *= 1.0 + self.breakEffect
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

    baseDotDamage *= 1.0 + self.breakEffect
    baseDotDamage = self.applyDamageMultipliers(baseDotDamage)

    retval.damage = baseDotDamage
    return retval

  def applyDamageMultipliers(self, baseDamage:float) -> float:
    damage = baseDamage
    damage *= (80 + 20 ) / ( ( self.enemyLevel + 20 ) * ( 1 - self.defShred ) + 80 + 20 )
    damage *= max(min(1 - self.enemyRes + self.resPen, 2.0), 0.1)
    damage *= self.brokenMultiplier
    return damage
