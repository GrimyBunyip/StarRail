from copy import copy
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseEffect import BaseEffect


def DefaultEstimator(rotationName:str, rotation:list, char:BaseCharacter, config:dict, CharacterDict:dict, EffectDict:dict,
                     breakDotMode:str = 'limited', dotMode:str = 'alwaysSingle'):
  
  totalEffect:BaseEffect = BaseEffect()
  
  for entry in rotation:
      totalEffect += entry
  
  # We estimate break damage proportional to the amount of break gauge applied
  num_breaks = totalEffect.gauge / config['enemyToughness']
  totalEffect += char.useBreak() * num_breaks
  if breakDotMode == 'limited': # limited means we are not able to maintain 100% break dot uptime
    totalEffect += char.useBreakDot() * num_breaks
    if char.element in ['physical', 'fire', 'lightning', 'wind']:
      totalEffect += char.useBreakDot() * num_breaks # these four elements tick twice
  
  # apply a number of dot ticks proportional to enemy speed, this does not count kafka procs
  num_enemy_turns = totalEffect.actionvalue * char.enemySpeed / char.getTotalSpd()
  if dotMode == 'alwaysSingle':
    totalEffect += char.useDot() * num_enemy_turns
  elif dotMode == 'alwaysBlast':
    totalEffect += char.useDot() * num_enemy_turns * min(3, char.numEnemies)
  elif dotMode == 'alwaysAll':
    totalEffect += char.useDot() * num_enemy_turns * char.numEnemies  
  
  if breakDotMode == 'alwaysSingle':
    totalEffect += char.useBreakDot() * num_enemy_turns
  elif breakDotMode == 'alwaysBlast':
    totalEffect += char.useBreakDot() * num_enemy_turns * min(3, char.numEnemies)
  elif breakDotMode == 'alwaysAll':
    totalEffect += char.useBreakDot() * num_enemy_turns * char.numEnemies

  CharacterDict[rotationName] = copy(char)
  EffectDict[rotationName] = copy(totalEffect)