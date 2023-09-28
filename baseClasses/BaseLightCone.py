import os
from copy import copy
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
    path:str
        
    def loadConeStats(self, name:str):
        self.name = name
        self.stats = copy(EMPTY_STATS)
        df = pd.read_csv(STATS_FILEPATH)
        rows = df.iloc[:, 0]
        for column in df.columns:
            split_column = column.split('.')
            data = df.loc[rows[rows == name].index,column].values[0]
            if len(split_column) > 1:
                column_key, column_type = split_column[0], split_column[1]
                if column_type in ['base','percent','flat']:
                    effect = BuffEffect(column_key,'Light Cone Stats',data,mathType=column_type)
                else:
                    effect = BuffEffect(column_key,'Light Cone  Stats',data,type=column_type)
                self.stats[column_key].append(effect)
            else:
                self.__dict__[column] = data
                
    def setSuperposition(self, config:dict):
        if self.rarity == '3':
            self.superposition = config['threestarSuperpositions']
        elif self.rarity == '4':
            self.superposition = config['fourstarSuperpositions']
        elif self.rarity == '5':
            self.superposition = config['fivestarSuperpositions']
        elif self.rarity == 'Herta':
            self.superposition = config['hertaSuperpositions']
        elif self.rarity == 'Forgottenhall':
            self.superposition = config['forgottenHallSuperpositions']
        elif self.rarity == 'Battlepass':
            self.superposition = config['battlePassSuperpositions']
                
    def addStats(self, char:BaseCharacter):
        for key, value in self.stats.items():
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