from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Welt(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                ultUptime:float=1.0,
                slowUptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Welt')
        self.ultUptime = ultUptime
        self.slowUptime = slowUptime
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=0.72, eidolonThreshold=3, eidolonBonus=0.072)]
        self.motionValueDict['ultimate'] = [BaseMV(area='all', stat='atk', value=1.5, eidolonThreshold=5, eidolonBonus=0.12)]
        self.motionValueDict['talent'] = [BaseMV(area='single', stat='atk', value=0.6, eidolonThreshold=5, eidolonBonus=0.06)]
        
        # Talents
        self.addStat('Vulnerability',description='ultimate',amount=0.12,uptime=self.ultUptime)
        self.addStat('BonusEnergyAttack',description='trace',amount=10.0,type=['ultimate'])
        self.addStat('DMG',description='trace',amount=0.20,uptime=config['weaknessBrokenUptime'])
        
        # Eidolons
        if self.eidolon >= 2:
            self.addStat('BonusEnergyAttack',description='e2',amount=3.0,type=['talent'])
        
        # Gear
        self.equipGear()

    def useBasic(self):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic',type) + (0.50 if self.eidolon >= 1 else 0.0)
        retval.damage *= 1.5 if self.eidolon >= 6 else 1.0
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        
        retval += self.useTalent(type) * self.slowUptime
        return retval

    def useSkill(self):
        num_hits = 4.0 if self.eidolon >= 6 else 3.0
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill',type) * (num_hits + (0.8 if self.eidolon >= 1 else 0.0) ) # e1 does not proc extra talent
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * num_hits * self.getBreakEfficiency(type)
        retval.energy = ( 10.0 * num_hits + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        
        retval += self.useTalent(type) * num_hits * self.slowUptime
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
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type) # unclear if this bonus energy is affected by ER
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        
        retval += self.useTalent(type) * self.numEnemies * self.slowUptime
        return retval

    def useTalent(self, type:list):
        retval = BaseEffect()
        type = type + ['talent']
        retval.damage = self.getTotalMotionValue('talent',type)
        retval.damage *= self.getTotalCrit(type) # hmm, is this additive MV? fix this later
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.energy = self.getBonusEnergyAttack(type) * self.getER(type) # unclear if this bhonus energy is affected by ER
        self.addDebugInfo(retval,type)
        return retval