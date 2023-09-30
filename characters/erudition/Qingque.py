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
        self.averageAutarky = 0.0
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type=['basic'],area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['enhancedBasic'] = [BaseMV(type=['basic'],area='single', stat='atk', value=2.4, eidolonThreshold=5, eidolonBonus=0.24),
                                                BaseMV(type=['basic'],area='adjacent', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['ultimate'] = [BaseMV(type=['ultimate'],area='all', stat='atk', value=2.0, eidolonThreshold=3, eidolonBonus=0.16)]
        
        # Talents
        self.addStat('SPD.percent',description='trace',amount=0.1,uptime=self.winningHandUptime)
        self.addStat('ATK.percent',description='talent',
                     amount=0.792 if self.eidolon >= 3 else 0.72,
                     type=['enhancedBasic'])
        
        # Eidolons
        if self.eidolon >= 1:
            self.addStat('DMG',description='e1',amount=0.1,type=['ultimate'])
        
        # Gear
        self.equipGear()

    def useBasic(self):
        retval = BaseEffect()
        type = ['basic']
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
        self.addDebugInfo(retval, type)
        return retval

    def useEnhancedBasic(self):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        type = ['basic','enhancedBasic']
        retval.damage = self.getTotalMotionValue('enhancedBasic')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        
        retval *= 1.0 + self.averageAutarky
        
        retval.skillpoints = 1.0 if self.eidolon >= 6 else 0.0
        retval.actionvalue = 1.0 - self.getAdvanceForward(type)
        retval.energy += 1.0 if self.eidolon >= 2 else 0.0
        retval += self.endTurn()
        self.addDebugInfo(retval, type)
        return retval
    
    def endTurn(self):
        self.averageAutarky = 0.0
        return super().endTurn()

    def useSkill(self):
        retval = BaseEffect()
        retval.skillpoints = -1.0
        
        damageBoost = 0.308 if self.eidolon > 5 else 0.28

        stacks = self.getTempBuffStacks('skill')
        if stacks is None:
            self.addTempStat('DMG',description='skill',amount=damageBoost,stacks=1,duration=1)
        else:
            stacks = min(4, stacks+1)
            self.setTempBuffStacks('skill',stacks)
        
        if self.eidolon >= 4:
            self.averageAutarky += ( 1.0 - self.averageAutarky ) * 0.76
            
        retval.energy += 1.0 if self.eidolon >= 2 else 0.0
        
        self.addDebugInfo(retval, type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval, type)
        return retval