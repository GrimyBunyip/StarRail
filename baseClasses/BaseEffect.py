from copy import deepcopy

class BaseEffect:
    damage:float
    gauge:float
    energy:float
    skillpoints:float
    actionvalue:float
    debugInfo:list
    debugCount:list

    def __init__(self, damage:float=0.0, gauge:float=0.0, energy:float=0.0, skillpoints:float=0.0, actionvalue:float=0.0, debugInfo:list=[], debugCount:list=[]):
        self.damage = damage
        self.gauge = gauge
        self.energy = energy
        self.skillpoints = skillpoints
        self.actionvalue = actionvalue
        self.debugInfo = deepcopy(debugInfo)
        self.debugCount = deepcopy(debugCount)

    def print(self):
        print(self.__dict__)

    # some code so we can do arithmetic with this object

    def __add__(self, value:'BaseEffect'):
        damage = self.damage + value.damage
        gauge = self.gauge + value.gauge
        energy = self.energy + value.energy
        skillpoints = self.skillpoints + value.skillpoints
        actionvalue = self.actionvalue + value.actionvalue
        debugInfo = self.debugInfo + value.debugInfo
        debugCount = self.debugCount + value.debugCount

        return BaseEffect(damage, gauge, energy, skillpoints, actionvalue, debugInfo, debugCount)

    def __sub__(self, value:'BaseEffect'):
        damage = self.damage - value.damage
        gauge = self.gauge - value.gauge
        energy = self.energy - value.energy
        skillpoints = self.skillpoints - value.skillpoints
        actionvalue = self.actionvalue - value.actionvalue
        debugInfo = self.debugInfo + value.debugInfo # not really properly defined here
        debugCount = self.debugCount + value.debugCount

        return BaseEffect(damage, gauge, energy, skillpoints, actionvalue, debugInfo, debugCount)

    def __mul__(self, value:float):
        damage = self.damage * value
        gauge = self.gauge * value
        energy = self.energy * value
        skillpoints = self.skillpoints * value
        actionvalue = self.actionvalue * value
        debugInfo = self.debugInfo
        debugCount = [x * value for x in self.debugCount]

        return BaseEffect(damage, gauge, energy, skillpoints, actionvalue, debugInfo, debugCount)
    
    def __truediv__(self, value:float):
        damage = self.damage / value
        gauge = self.gauge / value
        energy = self.energy / value
        skillpoints = self.skillpoints / value
        actionvalue = self.actionvalue / value
        debugInfo = self.debugInfo
        debugCount = [x / value for x in self.debugCount]

        return BaseEffect(damage, gauge, energy, skillpoints, actionvalue, debugInfo, debugCount)

    def __radd__(self, value:float):
        return self.__add__(value)

    def __iadd__(self, value:float):
        return self.__add__(value)

    def __isub__(self, value:float):
        return self.__sub__(value)

    def __rmul__(self, value:float):
        return self.__mul__(value)

    def __imul__(self, value:float):
        return self.__mul__(value)

    def __itruediv__(self, value:float):
        return self.__truediv__(value)
    
def sumEffects(effectList:list):
    totalEffects = BaseEffect()
    for effect in effectList:
        totalEffects += effect
    return totalEffects