from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Himeko(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                magmaUptime:float=1.0,
                benchmarkUptime:float=1.0,
                e1Uptime:float=1.0,
                e2Uptime:float=0.5,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Himeko')
        self.magmaUptime = magmaUptime
        self.benchmarkUptime = benchmarkUptime
        self.e1Uptime = e1Uptime
        self.e2Uptime = e2Uptime
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]

        self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=2.0, eidolonThreshold=5, eidolonBonus=0.2),
                                        BaseMV(type='skill',area='adjacent', stat='atk', value=0.8, eidolonThreshold=5, eidolonBonus=0.08)]

        self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='all', stat='atk', value=2.3, eidolonThreshold=3, eidolonBonus=0.184)]

        self.motionValueDict['talent'] = [BaseMV(type=['talent','followup'],area='all', stat='atk', value=1.4, eidolonThreshold=5, eidolonBonus=0.14)]
        self.motionValueDict['dot'] = [BaseMV(type=['dot'],area='all', stat='atk', value=0.3)]

        # Talents
        self.addStat('DMG',description='trace',amount=0.2,uptime=self.magmaUptime)
        self.addStat('CR',description='trace',amount=0.15,uptime=self.benchmarkUptime)
        
        # Eidolons
        if self.eidolon >= 1:
            self.addStat('SPD.percent',description='e1',amount=0.2,uptime=self.e1Uptime)
        if self.eidolon >= 2:
            self.addStat('DMG',description='e2',amount=0.15,uptime=e2Uptime)
        
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
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return 

    def useSkill(self):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('skill')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate') * ((1.8 * retval.damage / self.numEnemies) if self.eidolon >= 6 else 1.0)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        return retval

    def useTalent(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('talent')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 30.0 * self.numEnemies ) * self.getBreakEfficiency(type)
        retval.energy = ( 10.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = 0.0 - self.getAdvanceForward(type)
        return retval
    
    def useDot(self):
        retval = BaseEffect()
        type = ['dot']
        retval.damage = self.getTotalMotionValue('dot')
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        return retval