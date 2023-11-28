import os
from copy import deepcopy
import pandas as pd
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BuffEffect import BuffEffect

EMPTY_STATS = {  # character stats
                'ATK':[], 'DEF':[], 'HP':[],
                'DMG':[], 'CR':[], 'CD':[],
                # defensive stats
                'DmgReduction':[], 'AllRes':[],'RES':[],
                'Shield':[], 'Heal':[],
                'Taunt':[],
                # offensive stats
                'Vulnerability':[],
                'DefShred':[],
                'ResPen':[],
                # energy stats
                'ER':[], 'BonusEnergyAttack':[], 'BonusEnergyTurn': [],
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
    tempStats:dict

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
    enemyMaxHP:float
    enemyToughness:float
    breakLevelMultiplier:float
    enemyRes:float
    weaknessBrokenUptime:float

    def __init__(self, relicstats={}, lightcone=None, relicsetone=None, relicsettwo=None, planarset=None, **config):
        self.__dict__.update(config)
        self.stats = deepcopy(EMPTY_STATS)
        self.tempStats = deepcopy(EMPTY_STATS)
        
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
                if not data == 0.0: # don't bother loading empty stats
                    self.addStat(column,'Character Stats',data)
            else:
                self.__dict__[column] = data
                
        self.initialEnergy = self.maxEnergy * 0.5
        self.eidolon = self.fourstarEidolons if self.rarity == 4 else self.fivestarEidolons
        
        self.longName = f'{self.name} E{self.eidolon} {self.lightcone.name} S{self.lightcone.superposition} {self.lightcone.nameAffix}'

    def parseName(self, name:str, type:list=None, mathType:str='base'):
        splitname = name.split('.')
        if len(splitname) > 1:
            name = splitname[0]
            if splitname[1] in ['base','percent','flat']:
                mathType = splitname[1]
            else:
                type = [splitname[1]]
        return name, type, mathType

    def addStat(self, name:str, description:str, amount:float, type:list=None, stacks:float=1.0, uptime:float=1.0, mathType:str='base'):
        name, type, mathType = self.parseName(name,type,mathType)
        self.stats[name].append(BuffEffect(name=name, description=description, amount=amount, type=type, stacks=stacks, uptime=uptime, mathType=mathType))

    def addTempStat(self, name:str, description:str, amount:float, type:list=None, stacks:float=1.0, uptime:float=1.0, mathType:str='base', duration:int=None):
        name, type, mathType = self.parseName(name,type,mathType)
        self.tempStats[name].append(BuffEffect(name=name, description=description, amount=amount, type=type, stacks=stacks, uptime=uptime, mathType=mathType, duration=duration))
        
    def getTempBuffDuration(self, description:str):
        for _, values in self.tempStats.items():
            for value in values:
                value:BuffEffect
                if value.description == description:
                    return value.duration
        return None
    
    def getTempBuffStacks(self, description:str):
        for _, values in self.tempStats.items():
            for value in values:
                value:BuffEffect
                if value.description == description:
                    return value.stacks
        return None
            
    def setTempBuffDuration(self, description:str, duration:int):
        for _, values in self.tempStats.items():
            for value in values:
                value:BuffEffect
                if value.description == description:
                    value.duration = duration
                
    def setTempBuffStacks(self, description:str, stacks:int):
        for _, values in self.tempStats.items():
            for value in values:
                value:BuffEffect
                if value.description == description:
                    value.stacks = stacks
        
    def clearTempBuffs(self):
        self.tempStats = deepcopy(EMPTY_STATS)
        
    def endTurn(self):
        for _, value in self.tempStats.items():
            value:list
            for tempStat in value:
                tempStat:BuffEffect
                if tempStat.duration is not None:
                    tempStat.duration -= 1
                if tempStat.duration <= 0:
                    value.remove(tempStat)
        return BaseEffect()

    def equipGear(self):
        if self.relicstats is not None: self.relicstats.equipTo(self)
        if self.lightcone is not None: self.lightcone.equipTo(self)
        if self.relicsetone is not None: self.relicsetone.equipTo(self)
        if self.relicsettwo is not None: self.relicsettwo.equipTo(self)
        if self.planarset is not None: self.planarset.equipTo(self)
    
    def getTotalStat(self, stat:str, type:list=[], element:str=None):
        typeTotal = {'base': 0.0,
                     'percent':0.0,
                     'flat':0.0,}
        if element is None and self.element not in type:
            type.append(self.element)
        
        for entry in self.stats[stat]:
            entry:BuffEffect
            if entry.type is None or any(x in entry.type for x in type):
                typeTotal[entry.mathType] += entry.amount * entry.stacks * entry.uptime
                
        for entry in self.tempStats[stat]:
            entry:BuffEffect
            if entry.type is None or any(x in entry.type for x in type):
                typeTotal[entry.mathType] += entry.amount * entry.stacks * entry.uptime
            
        return typeTotal['base'] * (1.0 + typeTotal['percent']) + typeTotal['flat']
    
    def getTotalCrit(self, type:list=[], element:str=None):
        totalCR = self.getTotalStat('CR',type,element)
        totalCD = self.getTotalStat('CD',type,element)
        return 1.0 + min(1.0, totalCR) * totalCD
    
    def getDmg(self,type:list=[], element:str=None):
        return 1.0 + self.getTotalStat('DMG',type,element)
    
    def getVulnerability(self,type:list=[], element:str=None):
        return 1.0 + self.getTotalStat('Vulnerability',type,element)
    
    def getBreakEffect(self,type:list=[], element:str=None):
        return 1.0 + self.getTotalStat('BreakEffect',type,element)
    
    def getBreakEfficiency(self,type:list=[], element:str=None):
        return 1.0 + self.getTotalStat('BreakEfficiency',type,element)
    
    def getER(self,type:list=[], element:str=None):
        return 1.0 + self.getTotalStat('ER',type,element)
    
    def getAdvanceForward(self,type:list=[], element:str=None):
        return 0.0 - min(1.0,self.getTotalStat('AdvanceForward',type,element))
    
    def getBonusEnergyAttack(self,type:list=[], element:str=None):
        return self.getTotalStat('BonusEnergyAttack',type,element)
    
    def getBonusEnergyTurn(self,type:list=[], element:str=None):
        return self.getTotalStat('BonusEnergyTurn',type,element)
    
    def getDefShred(self,type:list=[], element:str=None):
        return min(1.0,self.getTotalStat('DefShred',type,element))
    
    def getResPen(self,type:list=[], element:str=None):
        return self.getTotalStat('ResPen',type,element)
    
    def getTotalMotionValue(self, mvKey:str, type:list):
        total = 0.0
        for key, value in self.motionValueDict.items():
            if key == mvKey:
                if isinstance(value, list):
                    total += sum(x.calculate(self, type) for x in value)
                else:
                    total += value.calculate(self, type)
        return total

    def useBasic(self):
        retval = BaseEffect()
        type = ['basic']
        retval.energy = 20.0 * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.energy = 30.0 * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.energy = 5.0 * self.getER(type)
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useTalent(self):
        return BaseEffect()

    def useEnhancedBasic(self):
        return BaseEffect()

    def useDot(self):
        return BaseEffect()

    def useBreak(self):
        retval = BaseEffect()
        type = ['break']

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
        baseDotDamage *= self.getBreakEffect(type)
        baseDotDamage *= self.getVulnerability(type)
        baseDotDamage = self.applyDamageMultipliers(baseDotDamage,type)

        retval.damage = baseDotDamage
        self.addDebugInfo(retval,type,'Break Damage')
        return retval

    def useBreakDot(self):
        retval = BaseEffect()
        type = ['break','dot']
        baseDotDamage = 0.0

        if self.element == 'physical':
            baseDotDamage = 2.0 * self.breakLevelMultiplier
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

        baseDotDamage *= self.getBreakEffect(type)
        baseDotDamage *= self.getVulnerability(type)
        baseDotDamage = self.applyDamageMultipliers(baseDotDamage,type)

        retval.damage = baseDotDamage
        self.addDebugInfo(retval,type,'Break Dot')
        return retval

    def applyDamageMultipliers(self, baseDamage:float, type:list=[], element:str=None) -> float:
        damage = baseDamage
        damage *= (80 + 20 ) / ( ( self.enemyLevel + 20 ) * ( 1 - self.getDefShred(type,element) ) + 80 + 20 )
        damage *= max(min(1 - self.enemyRes + self.getResPen(type,element), 2.0), 0.1)
        damage *= 0.9 + 0.1 * self.weaknessBrokenUptime
        return damage

    def addDebugInfo(self, effect:BaseEffect, type:list, name:str=None):
        # clean out elements from name
        [type.remove(x) for x in ['fire','ice','wind','lightning','physical','quantum','imaginary'] if x in type]
        
        debugEntry = []
        if name is None:
            name = self.name
            for typeinfo in type:
                name += ' ' + typeinfo
            debugEntry.append(name)
        else:
            debugEntry.append(name)
        debugEntry.append(effect.damage)
        debugEntry.append(effect.energy)
        debugEntry.append(effect.skillpoints)
        debugEntry.append(effect.gauge)
        debugEntry.append(effect.actionvalue)
        for stat in ['SPD', 'ATK', 'HP', 'DEF', 'DMG', 'CR', 'CD', 'Vulnerability', 'ResPen', 'DefShred'] :
            debugEntry.append([self.getTotalStat(stat,type),getStatComments(self,stat,type)])
        effect.debugInfo.append(debugEntry)
        effect.debugCount.append(1)
        
    def print(self):
        print(f'##### Name: {self.name} #####')
        print('SPD: {:.2f} - CR: {:.3f} - CD: {:.3f}'.format(self.getTotalStat('SPD'),
                                                             self.getTotalStat('CR'),
                                                             self.getTotalStat('CD'),))
        print('ATK: {:.1f} - HP: {:.1f} - DEF: {:.1f} - EHR: {:.3f}'.format(self.getTotalStat('ATK'),
                                                                            self.getTotalStat('HP'),
                                                                            self.getTotalStat('DEF'),
                                                                            self.getTotalStat('EHR'),))
        print('RES: {:.3f} - EHR: {:.3f} - DMG: {:.2f} - BreakEffect {:.3f}'.format(self.getTotalStat('RES'),
                                                 self.getTotalStat('EHR'),
                                                 self.getTotalStat('DMG',type=[self.element]),
                                                 self.getTotalStat('BreakEffect')))
        
def getStatComments(character:BaseCharacter,stat:str,type:list=[]):
    retval = ''
    commentList = character.stats[stat] + character.tempStats[stat]
    commentList.sort(key=lambda x: x.mathType)
    for entry in commentList:
        if entry.uptime <= 0.0:
            continue
        if entry.type is None or any(x in entry.type for x in type):
            entry:BuffEffect
            retval += entry.description + ':    '
            retval += str(round(entry.amount,2))
            if entry.mathType == 'flat':
                retval += ' ' + entry.mathType
            if entry.stacks is not None and entry.stacks != 1.0:
                retval += ', ' + str(round(entry.stacks,2)) + ' stacks'
            if entry.uptime is not None and entry.uptime < 1.0 and entry.uptime != 0.0:
                retval += ', ' + str(round(entry.uptime,2)) + ' uptime'
            if entry.duration is not None and entry.duration > 0.0:
                retval += ', ' + str(round(entry.duration,1)) + ' duration'
            retval += '\n'
            
    return retval