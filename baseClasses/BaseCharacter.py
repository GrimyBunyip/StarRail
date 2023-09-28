import os
from copy import copy
import pandas as pd
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BuffEffect import BuffEffect

EMPTY_STATS = {  # character stats
                'ATK':[], 'DEF':[], 'HP':[],
                'DMG':[], 'CR':[], 'CD':[],
                # defensive stats
                'DmgReduction':[], 'AllRes':[],
                'Shield':[], 'Heal':[],
                'Taunt':[],
                # offensive stats
                'Vulnerability':[],
                'DefShred':[],
                'ResPen':[],
                # energy stats
                'ER':[], 'BonusEnergyAttack':[],
                # action stats
                'SPD':[], 'AdvanceForward':[],
                # effect stats
                'EHR':[], 'BreakEffect':[], 'BreakEfficiency':[],
                }

STATS_FILEPATH = 'settings\CharacterStats.csv'
if os.name == 'posix':
    STATS_FILEPATH = STATS_FILEPATH.replace('\\','/')

class BaseCharacter(object):
    stats:dict

    graphic:str
    initialEnergy:float
    maxEnergy:float
    path:str
    element:str
    name:str

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
    weaknessBrokenUptime:float

    def __init__(self, relicstats, lightcone=None, relicsetone=None, relicsettwo=None, planarset=None, **config):
        self.__dict__.update(config)
        self.stats = EMPTY_STATS
        
        self.lightcone = lightcone
        self.relicsetone = relicsetone
        self.relicsettwo = relicsettwo
        self.planarset = planarset
        self.relicstats = relicstats
        
        self.motionValueDict = {}
        
    def loadCharacterStats(self, name:str):
        df = pd.read_csv(STATS_FILEPATH)
        rows = df.iloc[:, 0]
        for column in df.columns:
            split_column = column.split('.')
            data = df.loc[rows[rows == name].index,column].values[0]
            if len(split_column) > 1:
                column_key, column_type = split_column[0], split_column[1]
                if column_type in ['base','percent','flat']:
                    effect = BuffEffect(column_key,'Character Stats',data,mathType=column_type)
                else:
                    effect = BuffEffect(column_key,'Character Stats',data,type=column_type)
                self.stats[column_key].append(effect)
            else:
                self.__dict__[column] = data
                
        self.initialEnergy = self.maxEnergy * 0.5
        self.eidolon = self.fourstarEidolons if self.rarity == 4 else self.fivestarEidolons
        
        self.longName = '{} E{} {} S{}\n{}{}{}'.format(self.name, self.eidolon, self.lightcone.name, self.lightcone.superposition,
                                                        "" if self.relicsetone is None else self.relicsetone.shortname, 
                                                        "" if self.relicsettwo is None else (" + " + self.relicsettwo.shortname), 
                                                        "" if self.planarset is None else (" + " + self.planarset.shortname))

    def equipGear(self):
        if self.relicstats is not None: self.relicstats.equipTo(self)
        if self.lightcone is not None: self.lightcone.equipTo(self)
        if self.relicsetone is not None: self.relicsetone.equipTo(self)
        if self.relicsettwo is not None: self.relicsettwo.equipTo(self)
        if self.planarset is not None: self.planarset.equipTo(self)

    def balanceCrit(self):
        totalCV = self.CR * 2 + self.CD
        self.CD = max(0.5, totalCV / 2.0)
        self.CR = (totalCV - self.CD) / 2.0
        
    def getTotalTaunt(self):
        return self.taunt * (1 + self.percTaunt)

    def getTotalAtk(self, type=None):
        if isinstance(type, list):
            bonuses = sum([(self.percAtkType[x] if x in self.percAtkType else 0.0) for x in type])
            return self.baseAtk * ( 1 + self.percAtk + bonuses ) + self.flatAtk
        elif type is None or type not in self.percAtkType:
            return self.baseAtk * ( 1 + self.percAtk ) + self.flatAtk
        else:
            return self.baseAtk * ( 1 + self.percAtk + self.percAtkType[type] ) + self.flatAtk

    def getTotalDef(self, type=None):
        if isinstance(type, list):
            bonuses = sum([(self.percDefType[x] if x in self.percDefType else 0.0) for x in type])
            return self.baseDef * ( 1 + self.percDef + bonuses ) + self.flatDef
        elif type is None or type not in self.percDefType:
            return self.baseDef * ( 1 + self.percDef ) + self.flatDef
        else:
            return self.baseDef * ( 1 + self.percDef + self.percDefType[type] ) + self.flatDef

    def getTotalHP(self, type=None):
        if isinstance(type, list):
            bonuses = sum([(self.percHPType[x] if x in self.percHPType else 0.0) for x in type])
            return self.baseHP * ( 1 + self.percHP + bonuses ) + self.flatHP
        elif type is None or type not in self.percHPType:
            return self.baseHP * ( 1 + self.percHP ) + self.flatHP
        else:
            return self.baseHP * ( 1 + self.percHP + self.percHPType[type] ) + self.flatHP
    
    def getTotalCrit(self, type=None):
        if isinstance(type, list):
            crBonuses = sum([(self.CRType[x] if x in self.CRType else 0.0) for x in type])
            cdBonuses = sum([(self.CDType[x] if x in self.CDType else 0.0) for x in type])
            return 1.0 + min(1.0, self.CR + crBonuses) * (self.CD + cdBonuses)
        elif type is None:
            return 1.0 + min(1.0, self.CR) * self.CD
        else:
            return 1.0 + min(1.0, self.CR + self.CRType[type]) * (self.CD + self.CDType[type])
        
    def getTotalDmg(self, type=None, element=None):
        elementDmg = {
            'wind': self.windDmg,
            'ice': self.iceDmg,
            'fire': self.fireDmg,
            'lightning': self.lighDmg,
            'physical': self.physDmg,
            'quantum': self.quanDmg,
            'imaginary': self.imagDmg,
        }
        
        myElement = self.element if element is None else element
        
        if isinstance(type, list):
            bonuses = sum([(self.DmgType[x] if x in self.DmgType else 0.0) for x in type])
            return 1.0 + self.Dmg + elementDmg[myElement] + bonuses
        elif type is None or type not in self.DmgType:
            return 1.0 + self.Dmg + elementDmg[myElement]
        else:
            return 1.0 + self.Dmg + elementDmg[myElement] + self.DmgType[type]

    def getVulnerabilityType(self, type=None):
        if isinstance(type, list):
            bonuses = sum([(self.VulnerabilityType[x] if x in self.VulnerabilityType else 0.0) for x in type])
            return 1.0 + self.Vulnerability + bonuses
        elif type is None or type not in self.VulnerabilityType:
            return 1.0 + self.Vulnerability
        else:
            return 1.0 + self.Vulnerability + self.VulnerabilityType[type]

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
            'physical': 2.0,
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
        baseDotDamage *= self.getVulnerabilityType()
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
        elif self.element == 'wind': #assume 3 stacks to elites, 1 stack otherwise
            baseDotDamage = (3.0 if self.enemyType == 'elite' else 1.0) * self.breakLevelMultiplier
        elif self.element == 'quantum': #assume 3 stacks
            baseDotDamage = 0.6 * 3 * self.breakLevelMultiplier
            baseDotDamage *= 0.5 + self.enemyToughness / 120

        baseDotDamage *= 1.0 + self.breakEffect
        baseDotDamage *= self.getVulnerabilityType('dot')
        baseDotDamage = self.applyDamageMultipliers(baseDotDamage)

        retval.damage = baseDotDamage
        return retval

    def applyDamageMultipliers(self, baseDamage:float) -> float:
        damage = baseDamage
        damage *= (80 + 20 ) / ( ( self.enemyLevel + 20 ) * ( 1 - self.defShred ) + 80 + 20 )
        damage *= max(min(1 - self.enemyRes + self.resPen, 2.0), 0.1)
        damage *= 0.9 + 0.1 * self.weaknessBrokenUptime
        return damage
