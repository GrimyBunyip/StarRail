from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Acheron(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                num_other_nihility:int = 2,
                thunder_core_uptime:float = 1.0,
                thunder_core_stacks:float = 3.0,
                e1Uptime:float = 1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Acheron')
        self.num_other_nihility = num_other_nihility
        self.thunder_core_uptime = thunder_core_uptime
        self.thunder_core_stacks = thunder_core_stacks
        self.e1Uptime = e1Uptime
        
        mv_mult = 1.6 if self.num_other_nihility >= 2 else (1.15 if self.num_other_nihility == 1 else 1.0 )
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0 * mv_mult, eidolonThreshold=5, eidolonBonus=0.1 * mv_mult)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=1.6 * mv_mult, eidolonThreshold=3, eidolonBonus=0.16 * mv_mult),
                                        BaseMV(area='adjacent', stat='atk', value=0.6 * mv_mult, eidolonThreshold=3, eidolonBonus=0.06 * mv_mult),]
        self.motionValueDict['ultimate_st'] = [BaseMV(area='single', stat='atk', value=0.24 * mv_mult, eidolonThreshold=5, eidolonBonus=0.0192 * mv_mult)]
        self.motionValueDict['ultimate_aoe'] = [BaseMV(area='all', stat='atk', value=0.15 * mv_mult, eidolonThreshold=5, eidolonBonus=0.012 * mv_mult)]
        self.motionValueDict['ultimate_end'] = [BaseMV(area='all', stat='atk', value=1.2 * mv_mult, eidolonThreshold=5, eidolonBonus=0.096 * mv_mult),
                                                BaseMV(area='single', stat='atk', value=6 * 0.25 * mv_mult)]
        
        # Talents
        self.addStat('DMG',description='Acheron Trace',amount=0.30,uptime=self.thunder_core_uptime,stacks=self.thunder_core_stacks)
        self.addStat('ResPen',description='Acheron Talent',amount=0.20,type=['ultimate'])
        
        # Eidolons
        if self.eidolon >= 1:
            self.addStat('CR',description='Acheron e1',amount=0.18,uptime=self.e1Uptime)
        
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
        #retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useSkill(self):
        num_adjacent = min(2.0, self.numEnemies - 1.0)
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 60.0 + 30.0 * num_adjacent ) * self.getBreakEfficiency(type)
        #retval.energy = ( 10.0 * num_hits + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate_st(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate_st',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 15.0 * self.numEnemies * self.getBreakEfficiency(type)
        #retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type) # unclear if this bonus energy is affected by ER
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate_aoe(self, num_stacks:float = 3.0):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate_aoe',type) * (1.0 + num_stacks)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 15.0 * self.numEnemies * self.getBreakEfficiency(type)
        #retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type) # unclear if this bonus energy is affected by ER
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate_end(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate_end',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 15.0 * self.numEnemies * self.getBreakEfficiency(type) # must be at least 15
        #retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type) # unclear if this bonus energy is affected by ER
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval