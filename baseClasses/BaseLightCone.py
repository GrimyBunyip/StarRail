import os
from copy import deepcopy
import pandas as pd
from baseClasses.BaseCharacter import BaseCharacter, EMPTY_STATS
from baseClasses.BuffEffect import BuffEffect

STATS_FILEPATH = 'settings\ConeStats.csv'
if os.name == 'posix':
    STATS_FILEPATH = STATS_FILEPATH.replace('\\','/')

class BaseLightCone(object):
    stats:dict
    
    superposition:int
    rarity:str
    name:str
    shortname:str
    path:str
    nameAffix:str
        
    def loadConeStats(self, name:str, nameAffix:str='', shortname=None):
        self.name = name
        self.shortname = name if shortname is None else shortname
        self.nameAffix = nameAffix
        self.stats = deepcopy(EMPTY_STATS)
        df = pd.read_csv(STATS_FILEPATH)
        rows = df.iloc[:, 0]
        for column in df.columns:
            split_column = column.split('.')
            data = df.loc[rows[rows == name].index,column].values[0]
            if len(split_column) > 1:
                column_key = split_column[0]
                if not data == 0.0: # don't bother loading empty stats
                    effect = BuffEffect(column,'Light Cone Stats',data)
                    self.stats[column_key].append(effect)
            else:
                self.__dict__[column] = data
                
    def setSuperposition(self, superposition, config:dict):
        if superposition is not None:
            self.superposition = superposition
        elif self.rarity == '3':
            self.superposition = config['threestarSuperpositions']
        elif self.rarity == '4':
            self.superposition = config['fourstarSuperpositions']
        elif self.rarity == '5':
            self.superposition = config['fivestarSuperpositions']
        elif self.rarity == 'Event':
            self.superposition = config['eventSuperpositions']
        elif self.rarity == 'Herta':
            self.superposition = config['hertaSuperpositions']
        elif self.rarity == 'Forgottenhall':
            self.superposition = config['forgottenHallSuperpositions']
        elif self.rarity == 'Battlepass':
            self.superposition = config['battlePassSuperpositions']
                
    def addStats(self, char:BaseCharacter):
        for key, values in self.stats.items():
            for value in values:
                char.stats[key].append(value)
        char.lightcone = self

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        
    def print(self):
        for key, value in self.__dict__.items():
            if key == 'stats':
                for statkey, statvalue in value.items():
                    for buff in statvalue:
                        buff:BuffEffect
                        buff.print()
            else:
                print(key, value)