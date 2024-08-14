from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Feixiao(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                eidolon:int=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Feixiao')
        self.eidolon = self.eidolon if eidolon is None else eidolon

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=2.0, eidolonThreshold=5, eidolonBonus=0.20)]
        self.motionValueDict['talent'] = [BaseMV(area='single', stat='atk', value=1.1, eidolonThreshold=5, eidolonBonus=0.11)]
        self.motionValueDict['ultimateGun'] = [BaseMV(area='single', stat='atk', value=0.60 + 0.3, eidolonThreshold=3, eidolonBonus=0.048 + 0.03)]
        self.motionValueDict['ultimateAxe'] = [BaseMV(area='single', stat='atk', value=0.60 + 0.3, eidolonThreshold=3, eidolonBonus=0.048 + 0.03)]
        self.motionValueDict['ultimateFinal'] = [BaseMV(area='single', stat='atk', value=1.6, eidolonThreshold=3, eidolonBonus=0.128)]
        
        # Talents
        self.addStat('BreakEfficiency',description='Ultimate Weakness Break Efficiency',amount=1.0,type=['ultimate'])
        self.addStat('ATK.percent',description='Feixiao Talent',amount=0.48)
        self.addStat('CD',description='Feixiao Talent',amount=0.36,type=['ultimate'])

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
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate','followup']
        retval.damage = self.getTotalMotionValue('ultimateGun',type) * self.weaknessBrokenUptime * 6 * ( 1.25 if self.eidolon >= 1 else 1.0 )
        retval.damage += self.getTotalMotionValue('ultimateAxe',type) * (1.0 - self.weaknessBrokenUptime) * 6 * ( 1.25 if self.eidolon >= 1 else 1.0 )
        retval.damage += self.getTotalMotionValue('ultimateFinal',type) * ( 1.5 if self.eidolon >= 1 else 1.0 )
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 15.0 * 7.0 * self.getBreakEfficiency(type)
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
        retval.gauge = 15.0 * self.getBreakEfficiency(type)
        self.addDebugInfo(retval,type)
        return retval
