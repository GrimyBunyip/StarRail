from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from baseClasses.BaseMV import BaseMV

class Blade(BaseCharacter):

    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                hpLossTally:float = 0.9,
                hellscapeUptime:float = 1.0,
                rejectedByDeathUptime:float = 1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Blade')
        
        self.hpLossTally = min(0.9,hpLossTally)
        self.hellscapeUptime = hellscapeUptime
        self.rejectedByDeathUptime = rejectedByDeathUptime

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type=['basic'],area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]

        self.motionValueDict['enhancedBasic'] = [BaseMV(type=['basic'],area='single', stat='atk', value=0.4, eidolonThreshold=5, eidolonBonus=0.04),
                                                BaseMV(type=['basic'],area='single', stat='hp', value=1.0, eidolonThreshold=5, eidolonBonus=0.1),
                                                BaseMV(type=['basic'],area='adjacent', stat='atk', value=0.16, eidolonThreshold=5, eidolonBonus=0.016),
                                                BaseMV(type=['basic'],area='adjacent', stat='hp', value=0.4, eidolonThreshold=5, eidolonBonus=0.04)]

        self.motionValueDict['ultimate'] = [BaseMV(type=['ultimate'],area='single', stat='atk', value=0.4, eidolonThreshold=3, eidolonBonus=0.032),
                                            BaseMV(type=['ultimate'],area='adjacent', stat='atk', value=0.16, eidolonThreshold=3, eidolonBonus=0.0128),
                                            BaseMV(type=['ultimate'],area='single', stat='hp', value=1.0, eidolonThreshold=3, eidolonBonus=0.08),
                                            BaseMV(type=['ultimate'],area='adjacent', stat='hp', value=0.40, eidolonThreshold=3, eidolonBonus=0.032),
                                            BaseMV(type=['ultimate'],area='single', stat='hp', value=1.0*self.hpLossTally, eidolonThreshold=3, eidolonBonus=0.08*self.hpLossTally),
                                            BaseMV(type=['ultimate'],area='adjacent', stat='hp', value=0.40*self.hpLossTally, eidolonThreshold=3, eidolonBonus=0.032*self.hpLossTally)]
        
        self.motionValueDict['talent'] = [BaseMV(type=['talent','followup'],area='all', stat='atk', value=0.44, eidolonThreshold=3, eidolonBonus=0.044),
                                        BaseMV(type=['talent','followup'],area='all', stat='hp', value=1.1, eidolonThreshold=3, eidolonBonus=0.11)]
        
        # Talents
        self.addStat('DMG',description='trace',type=['followup'],amount=0.2)
        self.addStat('DMG',description='hellscape',
                     amount=0.456 if self.eidolon >= 3 else 0.40,
                     uptime=self.hellscapeUptime)
        
        # Eidolons
        if self.eidolon >= 1:
            self.motionValueDict['ultimate'][4].value = 1.5*self.hpLossTally
        if self.eidolon >= 2:
            self.addStat('CR',description='e2',type=['followup'],amount=0.15,uptime=self.hellscapeUptime)
        if self.eidolon >= 4:
            self.addStat('HP.percent',description='e4',type=['followup'],amount=0.40,uptime=self.rejectedByDeathUptime)

        # Gear
        self.equipGear()

    def useBasic(self):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic')
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

    def useEnhancedBasic(self):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        type = ['basic','enhancedBasic']
        retval.damage = self.getTotalMotionValue('enhancedBasic')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 0.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type,'Blade Enhanced Basic')
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.skillpoints = -1.0
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 60.0 + 60.0 * num_adjacents ) * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useTalent(self):
        retval = BaseEffect()
        type = ['followup','talent']
        retval.damage = self.getTotalMotionValue('talent')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 30.0 * self.numEnemies ) * self.getBreakEfficiency(type)
        retval.energy = ( 10.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval