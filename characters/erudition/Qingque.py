from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Qingque(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                winningHandUptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Qingque')
        self.winningHandUptime = winningHandUptime
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['enhancedBasic'] = [BaseMV(type='basic',area='single', stat='atk', value=2.4, eidolonThreshold=5, eidolonBonus=0.24),
                                                BaseMV(type='basic',area='adjacent', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='all', stat='atk', value=2.0, eidolonThreshold=3, eidolonBonus=0.16)]
        
        # Talents
        self.percSpd += 0.1 * self.winningHandUptime
        self.DmgType['ultimate'] += 0.10 if self.eidolon >= 1 else 0.0
        self.DmgType['skillBuff'] = 0.0
        self.percAtkType['talent'] = 0.792 if self.eidolon >= 3 else 0.72
        self.averageAutarky = 0.0
        
        # Eidolons
        
        # Gear
        self.equipGear()

    def useBasic(self):
        retval = BaseEffect()
        type = 'basic'
        retval.damage = self.getTotalMotionValue('basic')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        
        retval *= 1.0 + self.averageAutarky
        
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        retval.energy += 1.0 if self.eidolon >= 2 else 0.0
        retval += self.endTurn()
        return retval

    def useEnhancedBasic(self):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('enhancedBasic')
        retval.damage *= self.getTotalCrit('enhancedBasic')
        retval.damage *= self.getTotalDmg('enhancedBasic')
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.bonusEnergyAttack['enhancedBasic'] + self.getBonusEnergyTurn(type) ) * self.getER(type)
        
        retval *= 1.0 + self.averageAutarky
        
        retval.skillpoints = 1.0 if self.eidolon >= 6 else 0.0
        retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['enhancedBasic'])
        retval.energy += 1.0 if self.eidolon >= 2 else 0.0
        retval += self.endTurn()
        return retval
    
    def endTurn(self):
        retval = BaseEffect()
        self.DmgType['skillBuff'] = 0.0
        self.averageAutarky = 0.0
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = 'skill'
        retval.skillpoints = -1.0
        
        damageBoost = 0.308 if self.eidolon > 5 else 0.28
        self.DmgType['skillBuff'] += damageBoost
        self.DmgType['skillBuff'] = min(4*damageBoost,self.DmgType['skillBuff'])
        
        if self.eidolon >= 4:
            self.averageAutarky += ( 1.0 - self.averageAutarky ) * 0.76
            
        retval.energy += 1.0 if self.eidolon >= 2 else 0.0
        
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = 'ultimate'
        retval.damage = self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        return retval