from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from baseClasses.BaseMV import BaseMV

class Arlan(BaseCharacter):

    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                percentHP:float=0.5,
                hpUptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Arlan')
        self.percentHP = percentHP
        self.hpUptime = hpUptime
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=2.4, eidolonThreshold=3, eidolonBonus=0.24)]
        self.motionValueDict['ultimate'] = [BaseMV(area='single', stat='atk', value=3.2, eidolonThreshold=5, eidolonBonus=0.256),
                                            BaseMV(area='adjacent', stat='atk', value=1.6, eidolonThreshold=5, eidolonBonus=0.128)]
        self.motionValueDict['ultimateE6'] = [BaseMV(area='single', stat='atk', value=3.2, eidolonThreshold=5, eidolonBonus=0.256),
                                            BaseMV(area='adjacent', stat='atk', value=3.2, eidolonThreshold=5, eidolonBonus=0.256)]
        
        # Talents
        self.addStat('DMG',description='trace',
                     amount=min(1.0, (0.792 if self.eidolon >= 5 else 0.72) * self.percentHP))
        
        # Eidolons
        if self.eidolon >= 1.0:
            self.addStat('DMG',description='e1',type=['skill'],amount=0.10,uptime=self.hpUptime)
        if self.eidolon >= 6.0:
            self.addStat('DMG',description='e6',type=['ultimate'],amount=0.20,uptime=self.hpUptime)

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
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimateE6',type) if self.eidolon >= 6 else self.getTotalMotionValue('ultimate',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * min(3, self.numEnemies) * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        self.addDebugInfo(retval,type)
        return retval