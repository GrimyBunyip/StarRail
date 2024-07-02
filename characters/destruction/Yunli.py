from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from baseClasses.BaseMV import BaseMV

class Yunli(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                sunderUptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Yunli')
        self.sunderUptime = sunderUptime

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=1.2, eidolonThreshold=3, eidolonBonus=0.12),
                                         BaseMV(area='adjacent', stat='atk', value=0.6, eidolonThreshold=3, eidolonBonus=0.06),]
        
        self.motionValueDict['ultimate'] = [BaseMV(area='single', stat='atk', value=2.0, eidolonThreshold=5, eidolonBonus=0.16),
                                            BaseMV(area='adjacent', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.08),]
        
        self.motionValueDict['enhancedUltimate'] = [BaseMV(area='single', stat='atk', value=2.0, eidolonThreshold=5, eidolonBonus=0.16),
                                                    BaseMV(area='adjacent', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.08),
                                                    BaseMV(area='single', stat='atk', value=6*0.6, eidolonThreshold=5, eidolonBonus=6*0.048),]
        
        self.motionValueDict['talent'] = [BaseMV(area='single', stat='atk', value=1.2, eidolonThreshold=5, eidolonBonus=0.12),
                                         BaseMV(area='adjacent', stat='atk', value=0.6, eidolonThreshold=5, eidolonBonus=0.06),]     
        
        # Talents
        self.addStat('CD',description='Yunli Ultimate CD Buff',
                     amount=1.08 if self.eidolon >= 5 else 1.0, 
                     type=['ultimate'])
        
        self.addStat('ATK.percent',description='Yunli Sunder Talent',amount=0.3,uptime=self.sunderUptime)
        
        self.addStat('BonusEnergyAttack',description='Yunli Counter Energy',amount=15.0,type=['followup'])
        
        # Eidolons

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
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type)) * self.getER(type)
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

    def useUltimate(self):
        num_adjacent = min(2, self.numEnemies-1)
        retval = BaseEffect()
        type = ['followup', 'ultimate']
        retval.damage = self.getTotalMotionValue('ultimate',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 30.0 + 30.0 * num_adjacent ) * self.getBreakEfficiency(type)
        retval.energy = ( 10.0 + 5.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.actionvalue = 0.0 - self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useEnhancedUltimate(self):
        num_adjacent = min(2, self.numEnemies-1)
        retval = BaseEffect()
        type = ['followup', 'ultimate']
        retval.damage = self.getTotalMotionValue('enhancedUltimate',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 30.0 + 30.0 * num_adjacent + 15.0 * 6 ) * self.getBreakEfficiency(type)
        retval.energy = ( 10.0 + 5.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.actionvalue = 0.0 - self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useTalent(self):
        num_adjacent = min(2, self.numEnemies-1)
        retval = BaseEffect()
        type = ['followup','talent']
        retval.damage = self.getTotalMotionValue('talent',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 30.0 + 30.0 * num_adjacent ) * self.getBreakEfficiency(type)
        retval.energy = ( 10.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = 0.0 - self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval