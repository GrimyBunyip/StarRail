from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Pela(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                bashUptime:float=1.0,
                e2Uptime:float=0.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Pela')
        self.bashUptime = bashUptime
        self.e2Uptime = e2Uptime
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=2.1, eidolonThreshold=3, eidolonBonus=0.21)]
        self.motionValueDict['ultimate'] = [BaseMV(area='all', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.08)]
        self.motionValueDict['e6'] = [BaseMV(area='single', stat='atk', value=0.4)]
        
        # Talents
        self.addStat('BonusEnergyAttack',description='talent',amount=11.0 if self.eidolon >= 5 else 10.0)
        self.addStat('DMG',description='trace',amount=0.2,uptime=self.bashUptime)
        self.addStat('EHR',description='talent',amount=0.1)
        
        # Eidolons
        if self.eidolon >= 2:
            self.addStat('SPD.percent',description='e2',amount=0.10,uptime=self.e2Uptime)
        
        # Gear
        self.equipGear()
        
    def applyUltDebuff(self,team:list, rotation_turns:float=3.0):
        pelaUltUptime = (2.0 / rotation_turns) * self.getTotalStat('SPD') / self.enemySpeed
        pelaUltUptime = min(1.0, pelaUltUptime)
        for character in team:
            character.addStat('DefShred',description='Pela Ultimate',
                            amount=0.42 if self.eidolon >= 5 else 0.40,
                            uptime=pelaUltUptime)

    def useBasic(self):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic',type) + (self.getTotalMotionValue('e6',type) if self.eidolon >= 6 else 0.0)
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
        retval.damage = self.getTotalMotionValue('skill',type) + (self.getTotalMotionValue('e6',type) if self.eidolon >= 6 else 0.0)
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
        retval.damage = self.getTotalMotionValue('ultimate',type) + (self.getTotalMotionValue('e6',type) * self.numEnemies if self.eidolon >= 6 else 0.0)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type) # unclear if this bonus energy is affected by ER
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval