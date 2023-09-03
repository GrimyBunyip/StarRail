from copy import copy
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseEffect import BaseEffect


def DefaultEstimator(rotationName:str, rotation:list, char:BaseCharacter, config:dict, CharacterDict:dict, EffectDict:dict,
                     breakDotMode:str = 'limited'):
  
  totalEffect:BaseEffect = BaseEffect()
  
  for entry in rotation:
      totalEffect += entry
  
  # We estimate break damage proportional to the amount of break gauge applied
  num_breaks = totalEffect.gauge / config['enemyToughness']
  totalEffect += char.useBreak() * num_breaks
  if breakDotMode == 'limited':
    totalEffect += char.useBreakDot() * num_breaks
    if char.element in ['physical', 'fire', 'wind', 'imaginary']:
      totalEffect += char.useBreakDot() * num_breaks # these four elements tick twice
  
  # apply a number of dot ticks proportional to enemy speed, this does not count kafka procs
  num_enemy_turns = totalEffect.actionvalue * char.enemySpeed / char.getTotalSpd()
  totalEffect += char.useDot() * num_enemy_turns
  if breakDotMode == 'alwaysSingle':
    totalEffect += char.useBreakDot() * num_enemy_turns
  elif breakDotMode == 'alwaysBlast':
    totalEffect += char.useBreakDot() * num_enemy_turns * min(3, char.numEnemies)
  elif breakDotMode == 'alwaysAll':
    totalEffect += char.useBreakDot() * num_enemy_turns * char.numEnemies
    

  CharacterDict[rotationName] = copy(char)
  EffectDict[rotationName] = copy(totalEffect)