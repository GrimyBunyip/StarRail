from copy import copy
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseEffect import BaseEffect


def DefaultEstimator(rotationName:str, rotation:list, char:BaseCharacter, config:dict, CharacterDict:dict, EffectDict:dict):
  
  totalEffect = BaseEffect()
  
  for entry in rotation:
      totalEffect += entry
  
  # assume we apply break a number of times proportional to our gauge output and enemy toughness
  num_breaks = totalEffect.gauge / config['enemyToughness']
  totalEffect += char.useBreak() * num_breaks

  # apply a number of break dots proportional to the amount of breaks we applied, up to the number of enemy turns
  num_dots = min(config['numEnemies'], num_breaks * 2)
  totalEffect += char.useBreakDot() * num_dots

  CharacterDict[rotationName] = copy(char)
  EffectDict[rotationName] = copy(totalEffect)