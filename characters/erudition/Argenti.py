from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Argenti(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                talentStacks=12.0,
                courageUptime=0.5,
                e2Uptime=0.25,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Argenti')
        self.talentStacks = min(talentStacks,12.0 if self.eidolon >= 4 else 10.0)
        self.courageUptime = courageUptime
        self.e2Uptime = e2Uptime
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]

        self.motionValueDict['skill'] = [BaseMV(area='all', stat='atk', value=1.2, eidolonThreshold=3, eidolonBonus=0.12)]

        self.motionValueDict['ultimate'] = [BaseMV(area='all', stat='atk', value=1.6, eidolonThreshold=5, eidolonBonus=0.128)]
        self.motionValueDict['enhancedUltimate'] = [BaseMV(area='all', stat='atk', value=2.8, eidolonThreshold=5, eidolonBonus=0.224),
                                                    BaseMV(area='single', stat='atk', value=0.95*6, eidolonThreshold=5, eidolonBonus=0.076*6)]

        # Talents
        self.addStat('CR',description='talent',
                     amount=0.028 if self.eidolon>=3 else 0.025,
                     uptime=self.talentStacks)
        self.addStat('BonusEnergyAttack',description='talent',
                     amount=3, type=['basic'])
        self.addStat('BonusEnergyAttack',description='talent',
                     amount=3, stacks=self.numEnemies, type=['skill'])
        self.addStat('BonusEnergyAttack',description='talent',
                     amount=3, stacks=self.numEnemies, type=['ultimate'])
        self.addStat('DMG',description='trace',amount=0.15,uptime=self.courageUptime)
        
        # Eidolons
        if self.eidolon >= 1:
            self.addStat('CD',description='e1',amount=0.04,
                        uptime=self.talentStacks)
        if self.eidolon >= 2 and self.numEnemies >= 3:
            self.addStat('ATK.percent',description='e2',amount=0.40,
                        type=['ultimate','enhancedUltimate'])
            self.addStat('ATK.percent',description='e2',amount=0.40,
                        type=['basic','skill'],
                        uptime=self.e2Uptime)
        if self.eidolon >= 6:
            self.addStat('DefShred',description='e6',amount=0.30,type=['ultimate','enhancedUltimate'])
        
        # Gear
        self.equipGear()

    def useBasic(self):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return 

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
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
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useEnhancedUltimate(self):
        retval = BaseEffect()
        type = ['ultimate','enhancedUltimate']
        retval.damage = self.getTotalMotionValue('enhancedUltimate',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 60.0 * self.numEnemies + 15.0 * 6 ) * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval