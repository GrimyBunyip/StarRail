from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Yukong(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                bowstringUptime:float=2.0/3.0,
                ultUptime:float=1.0/3.0,
                majestaProcs:float=2.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Yukong')
        
        self.bowstringUptime = bowstringUptime
        self.ultUptime = ultUptime
        self.majestaprocs = majestaProcs

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['enhancedBasic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1),
                                                BaseMV(area='single', stat='atk', value=0.8, eidolonThreshold=5, eidolonBonus=0.08)]
        self.motionValueDict['ultimate'] = [BaseMV(area='single', stat='atk', value=3.8, eidolonThreshold=5, eidolonBonus=0.304)]

        # Talents
        self.addStat('CR',description='ultimate',
                     amount=0.294 if self.eidolon >= 5 else 0.28,
                     type=['ultimate'])
        self.addStat('CD',description='ultimate',
                     amount=0.702 if self.eidolon >= 5 else 0.65,
                     type=['ultimate'])
        self.addStat('DMG',description='Yukong Trace',amount=0.12,type=['imaginary'])
        self.addStat('BonusEnergyTurn',description='Yukong Trace',amount=2.0,type=['skill'],stacks=self.majestaprocs)

        # Eidolons
        if self.eidolon >= 2:
            self.addStat('BonusEnergyAttack',description='e2',amount=5.0,stacks=3.0,type='ultimate')
        if self.eidolon >= 4:
            self.addStat('DMG',description='e4',amount=0.3,uptime=self.bowstringUptime)
        
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
        return retval
        
    def useEnhancedBasic(self):
        retval = BaseEffect()
        type = ['enhancedBasic','basic']
        retval.damage = self.getTotalMotionValue('enhancedBasic',type)
        retval.damage *= self.getTotalCrit(['enhancedBasic','basic'])
        retval.damage *= self.getDmg(['enhancedBasic','basic'])
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.energy = (30.0 + self.getBonusEnergyTurn(type)) * self.getER(type) # 4 bonus energy from ascension 6, but it could be more
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
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
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        return retval