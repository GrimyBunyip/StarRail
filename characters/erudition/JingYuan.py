from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class JingYuan(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                battaliaCrushUptime:float=1.0,
                warMarshalUptime:float=1.0,
                e2Uptime:float=0.5,
                e6Uptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Jing Yuan')
        self.battaliaCrushUptime = battaliaCrushUptime
        self.warMarshalUptime = warMarshalUptime
        self.e2Uptime = e2Uptime
        self.e6Uptime = e6Uptime
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type=['basic'],area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(type=['skill'],area='all', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['ultimate'] = [BaseMV(type=['ultimate'],area='all', stat='atk', value=2.0, eidolonThreshold=3, eidolonBonus=0.16)]
        self.motionValueDict['talent'] = [BaseMV(type=['talent','followup'],area='single', stat='atk', value=0.66, eidolonThreshold=5, eidolonBonus=0.066)]
        
        # Talents
        self.addStat('CR',description='trace',amount=0.1,uptime=self.warMarshalUptime)
        self.addStat('CD',description='trace',amount=0.25,type=['talent'],uptime=self.battaliaCrushUptime)
        
        # Eidolons
        if self.eidolon >= 2:
            self.addStat('DMG',description='e2',amount=0.2,type=['basic'],uptime=self.e2Uptime)
            self.addStat('DMG',description='e2',amount=0.2,type=['skill'],uptime=self.e2Uptime)
            self.addStat('DMG',description='e2',amount=0.2,type=['ultimate'],uptime=self.e2Uptime)
        if self.eidolon >= 6:
            self.addStat('DMG',description='e6',amount=0.36,uptime=self.e6Uptime)
        
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
        self.addDebugInfo(retval,type)
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 30.0 * self.numEnemies ) * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
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
        self.addDebugInfo(retval,type)
        return retval

    def useTalent(self):
        retval = BaseEffect()
        type = ['talent','followup']
        retval.damage = self.getTotalMotionValue('talent')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 15.0 * self.getBreakEfficiency(type)
        retval.energy = ( 2.0 * self.getER(type) ) if self.eidolon >= 4 else 0.0
        retval.actionvalue = self.getAdvanceForward(type)
        
        multiplier = 1.0
        if self.numEnemies >= 2:
            multiplier += 0.5 if self.eidolon >= 1 else 0.25
        if self.numEnemies >= 3:
            multiplier += ( 0.5 if self.eidolon >= 1 else 0.25 ) * ( self.numEnemies - 2 ) / self.numEnemies
            
        retval *= multiplier
        self.addDebugInfo(retval,type)
        return retval