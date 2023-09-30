from copy import copy
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseEffect import BaseEffect

class VisualizationInfo():
    name:str
    character:BaseCharacter
    effect:BaseEffect
    breakEffect:BaseEffect
    dotEffect:BaseEffect
    extraImage:str
    
def DotEstimator(rotation:list, char:BaseCharacter, config:dict, dotMode:str = 'alwaysSingle'):
    # apply a number of dot ticks proportional to enemy speed, this does not count kafka procs
    num_enemy_turns = sum([x.actionvalue for x in rotation]) * char.enemySpeed / char.getTotalStat('SPD')
    if dotMode == 'alwaysSingle':
        return num_enemy_turns
    elif dotMode == 'alwaysBlast':
        return num_enemy_turns * min(3, char.numEnemies)
    elif dotMode == 'alwaysAll':
        return num_enemy_turns * char.numEnemies
    return 0.0

def DefaultEstimator(rotationName:str, rotation:list, char:BaseCharacter, config:dict, breakDotMode:str = 'limited', numDot:float=0.0, extraImage:str=None):
    
    totalEffect:BaseEffect = BaseEffect()
    breakEffect:BaseEffect = BaseEffect()
    dotEffect:BaseEffect = BaseEffect()
    
    for entry in rotation:
        entry:BaseEffect
        totalEffect += entry
    
    # We estimate break damage proportional to the amount of break gauge applied
    num_breaks = totalEffect.gauge * config['weaknessBrokenUptime'] / config['enemyToughness']
    breakEffect += char.useBreak() * num_breaks
    if breakDotMode == 'limited': # limited means we are not able to maintain 100% break dot uptime
        if char.element in ['physical', 'fire', 'lightning', 'wind']:
            breakEffect += char.useBreakDot() * num_breaks * 2 # these four elements tick twice
        else:
            breakEffect += char.useBreakDot() * num_breaks
            
    newDot = char.useDot()
    char.addDebugInfo(newDot,['dot'],'Dot Ticks')
    dotEffect += newDot * numDot
    
    num_enemy_turns = totalEffect.actionvalue * char.enemySpeed / char.getTotalStat('SPD')
    if breakDotMode == 'alwaysSingle':
        breakEffect += char.useBreakDot() * num_enemy_turns
    elif breakDotMode == 'alwaysBlast':
        breakEffect += char.useBreakDot() * num_enemy_turns * min(3, char.numEnemies)
    elif breakDotMode == 'alwaysAll':
        breakEffect += char.useBreakDot() * num_enemy_turns * char.numEnemies

    retval = VisualizationInfo()
    retval.name = rotationName
    retval.character = copy(char)
    retval.effect = copy(totalEffect)
    retval.breakEffect = copy(breakEffect)
    retval.dotEffect = copy(dotEffect)
    retval.extraImage = extraImage
    
    return retval