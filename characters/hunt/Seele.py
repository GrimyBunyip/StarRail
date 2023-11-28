from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Seele(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                sheathedBladeUptime:float=1.0,
                e1Uptime:float=0.8,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Seele')
        
        self.sheathedBladeUptime = sheathedBladeUptime
        self.e1Uptime = e1Uptime

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=2.2, eidolonThreshold=3, eidolonBonus=0.22)]
        self.motionValueDict['ultimate'] = [BaseMV(area='single', stat='atk', value=4.25, eidolonThreshold=5, eidolonBonus=0.34)]

        # Talents
        self.addStat('SPD.percent',description='Seele Trace',amount=0.25,uptime=self.sheathedBladeUptime)
        self.addStat('AdvanceForward',description='Seele Trace',amount=0.20,type=['basic'])

        # Eidolons
        if self.eidolon >= 1:
            self.addStat('CR',description='e1',amount=0.15,uptime=self.e1Uptime)
        if self.eidolon >= 2:
            self.addStat('SPD.percent',description='e2',amount=0.25,uptime=self.sheathedBladeUptime)
        # e6 not yet implemented
        
        # Gear
        self.equipGear()
        
    def useBasic(self):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
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
        retval.damage = self.getTotalMotionValue('skill',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 - self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type) + ( (0.88 if self.eidolon >= 3 else 0.8) if self.getTempBuffDuration('Resurgence') is None else 0.0 )
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 90.0 * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type) # too lazy to implement seele e6, who cares
        self.addDebugInfo(retval,type)
        return retval
    
    def useResurgence(self):
        retval = BaseEffect()
        type = ['talent']
        retval.actionvalue = -1.0
        retval.energy = ( 15.0 if self.eidolon >= 4 else 0.0 ) * self.getER(type)
        self.addTempStat('ResPen',description='Resurgence',amount=0.20,duration=1)
        self.addTempStat('DMG',description='Resurgence',amount=0.88 if self.eidolon >=3 else 0.8,duration=1)
        self.addDebugInfo(retval,['Resurgence'],'Seele Resurgence')
        return retval