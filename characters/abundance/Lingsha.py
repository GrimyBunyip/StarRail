from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Lingsha(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                eidolon:int=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Lingsha')
        self.eidolon = self.eidolon if eidolon is None else eidolon

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(area='all', stat='atk', value=0.8, eidolonThreshold=5, eidolonBonus=0.08)]
        self.motionValueDict['talent'] = [BaseMV(area='single', stat='atk', value=0.75, eidolonThreshold=3, eidolonBonus=0.075),
                                          BaseMV(area='all', stat='atk', value=0.75, eidolonThreshold=3, eidolonBonus=0.075)]
        self.motionValueDict['ultimate'] = [BaseMV(area='all', stat='atk', value=1.5, eidolonThreshold=3, eidolonBonus=0.15)]

        # Talents
        self.addStat('BonusEnergyAttack',description='Lingsha Talent',amount=10,type=['basic'])

        # Eidolons
        if self.eidolon >= 1:
            self.addStat('BreakEfficiency',description='E1',amount=0.5)
            self.addStat('DefShred',description='E1',amount=0.2,type=['Break'])
        
        # Gear
        self.equipGear()
        

    def addAttackForTalent(self):
        self.addStat('ATK.percent',description='Lingsha Break Talent',amount=min(0.50,0.25 * self.getBreakEffect()))
        self.addStat('Heal',description='Lingsha Break Talent',amount=min(0.20,0.10 * self.getBreakEffect()))
        
    def applyUltDebuff(self,team:list, rotationDuration:float=3.0):
        ultUptime = (2.0 / rotationDuration) * self.getTotalStat('SPD') / self.enemySpeed
        ultUptime = min(1.0, ultUptime)
        for character in team:
            character.addStat('CD',description='Lingsha Ultimate',
                            amount=(0.27 if self.eidolon >= 3 else 0.25),
                            uptime=ultUptime)
        
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
        retval.gauge = 30.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useTalent(self):
        retval = BaseEffect()
        type = ['followup']
        retval.damage = self.getTotalMotionValue('talent',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = (30.0 + 30.0 * self.numEnemies) * self.getBreakEfficiency(type)
        retval.energy = ( 0.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval