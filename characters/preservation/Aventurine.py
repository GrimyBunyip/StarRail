from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Aventurine(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                leverage_cr:float = 0.48,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Aventurine')
        self.leverage_cr = leverage_cr

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='def', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['ultimate'] = [BaseMV(area='single', stat='def', value=2.7, eidolonThreshold=5, eidolonBonus=0.216)]
        self.motionValueDict['talent'] = [BaseMV(area='single', stat='def', value=0.25, eidolonThreshold=5, eidolonBonus=0.025)]

        # Talents
        self.addStat('CR',description='Aventurine Trace',amount=self.leverage_cr)

        # Eidolons
        
        # Gear
        self.equipGear()
        
    def applyUltDebuff(self,team:list, rotationDuration:float=4.0,targetingUptime:float=None):
        ultUptime = (3.0 / rotationDuration) * self.getTotalStat('SPD') / self.enemySpeed
        if targetingUptime is None:
            ultUptime /= self.numEnemies
        ultUptime = min(1.0, ultUptime)
        for character in team:
            character.addStat('CD',description='Aventurine Ultimate',
                            amount=(0.15 if self.eidolon >= 5 else 0.03),
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
        retval.energy = ( 30.0 + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
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
        retval.gauge = 90.0 * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval
        
    def useTalent(self):
        retval = BaseEffect()
        type = ['talent','followup']
        retval.damage = self.getTotalMotionValue('talent',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 10.0 * self.getBreakEfficiency(type)
        retval.energy = -1.0 + ( 0.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval