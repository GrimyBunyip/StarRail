import os
import pandas as pd
from baseClasses.BaseCharacter import BaseCharacter

STATS_FILEPATH = 'settings\ConeStats.csv'
if os.name == 'posix':
  STATS_FILEPATH = STATS_FILEPATH.replace('\\','/')

class BaseLightCone(object):
  baseAtk:float
  baseDef:float
  baseHP:float
  superposition:int
  rarity:int
  herta:bool
  name:str
    
  def loadConeStats(self, name:str):
    df = pd.read_csv(STATS_FILEPATH)
    rows = df.iloc[:, 0]
    for column in df.columns:
        data = df.loc[rows[rows == name].index,column].values[0]
        self.__dict__[column] = data
        
  def setSuperposition(self, config:dict):
    if self.rarity == 3:
      self.superposition = config['threestarSuperpositions']
    elif self.rarity == 4:
      self.superposition = config['fourstarSuperpositions']
    elif self.rarity == 5:
      if self.herta:
        self.superposition = config['hertaSuperpositions']
      else:
        self.superposition = config['fivestarSuperpositions']
        
  def addBaseStats(self, char:BaseCharacter):
    char.baseAtk += self.baseAtk
    char.baseDef += self.baseDef
    char.baseHP += self.baseHP
    char.lightcone = self

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    
  def print(self):
    for key, value in self.__dict__.items():
      print(key, value)