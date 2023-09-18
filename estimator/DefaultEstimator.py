from copy import copy
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseEffect import BaseEffect

def DefaultEstimator(rotationName:str, rotation:list, char:BaseCharacter, config:dict, VisualizationDict:dict,
                     breakDotMode:str = 'limited', dotMode:str = 'alwaysSingle'):
  
  totalEffect:BaseEffect = BaseEffect()
  breakEffect:BaseEffect = BaseEffect()
  dotEffect:BaseEffect = BaseEffect()
  
  for entry in rotation:
      totalEffect += entry
  
  # We estimate break damage proportional to the amount of break gauge applied
  num_breaks = totalEffect.gauge * config['weaknessBrokenUptime'] / config['enemyToughness']
  breakEffect += char.useBreak() * num_breaks
  if breakDotMode == 'limited': # limited means we are not able to maintain 100% break dot uptime
    breakEffect += char.useBreakDot() * num_breaks
    if char.element in ['physical', 'fire', 'lightning', 'wind']:
      breakEffect += char.useBreakDot() * num_breaks # these four elements tick twice
  
  # apply a number of dot ticks proportional to enemy speed, this does not count kafka procs
  num_enemy_turns = totalEffect.actionvalue * char.enemySpeed / char.getTotalSpd()
  if dotMode == 'alwaysSingle':
    dotEffect += char.useDot() * num_enemy_turns
  elif dotMode == 'alwaysBlast':
    dotEffect += char.useDot() * num_enemy_turns * min(3, char.numEnemies)
  elif dotMode == 'alwaysAll':
    dotEffect += char.useDot() * num_enemy_turns * char.numEnemies  
  
  if breakDotMode == 'alwaysSingle':
    breakEffect += char.useBreakDot() * num_enemy_turns
  elif breakDotMode == 'alwaysBlast':
    breakEffect += char.useBreakDot() * num_enemy_turns * min(3, char.numEnemies)
  elif breakDotMode == 'alwaysAll':
    breakEffect += char.useBreakDot() * num_enemy_turns * char.numEnemies

  VisualizationDict['CharacterDict'][rotationName] = copy(char)
  VisualizationDict['EffectDict'][rotationName] = copy(totalEffect)
  VisualizationDict['BreakDict'][rotationName] = copy(breakEffect)
  VisualizationDict['DotDict'][rotationName] = copy(dotEffect)