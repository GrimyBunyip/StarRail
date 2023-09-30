from baseClasses.BaseCharacter import BaseCharacter

class BaseMV:
    def __init__(self, area:str, stat:str, value:float, eidolonThreshold:int = 5, eidolonBonus:float = 0.0):
        if area not in ['single', 'adjacent', 'blast', 'all']:
            raise ValueError('invalid area selected for BaseMV')
        if stat not in ['atk','def','hp']:
            raise ValueError('invalid stat selected for BaseMV')
        
        #self.type = type
        self.area = area
        self.stat = stat
        self.value = value
        self.eidolonThreshold = eidolonThreshold
        self.eidolonBonus = eidolonBonus
        
    def calculate(self, char:BaseCharacter, type:list):
        mv = self.value +    ( self.eidolonBonus if char.eidolon > self.eidolonThreshold else 0.0 )

        if self.stat == 'atk':
            amount = mv * char.getTotalStat('ATK',type=type)
        elif self.stat == 'def':
            amount = mv * char.getTotalStat('DEF',type=type)
        elif self.stat == 'hp':
            amount = mv * char.getTotalStat('HP',type=type)
        else:
            raise ValueError('invalid stat selected for BaseMV')
                
        if self.area == 'single': # no need to modify amount here
            pass 
        elif self.area == 'adjacent': # adjacent can only affect up to 2 targets, and only if there are enough enemies
            amount *= min(2,char.numEnemies-1)
        elif self.area == 'blast':
            amount *= min(3,char.numEnemies)
        elif self.area == 'all':
            amount *= char.numEnemies
        else:
            raise ValueError('invalid area selected for BaseMV')
            
        return amount

if __name__ == '__main__':
    mv = BaseMV(area='single', stat='atk', value=1.0)
    