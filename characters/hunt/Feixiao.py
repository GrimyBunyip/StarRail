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
                ultUptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Feixiao')
        self.ultUptime = ultUptime

        # TO DO UPDATE EIDOLON BONUS THRESHOLDS
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=2.4, eidolonThreshold=3, eidolonBonus=0.24)]
        self.motionValueDict['talent'] = [BaseMV(area='single', stat='atk', value=2.0, eidolonThreshold=3, eidolonBonus=0.2)]
        self.motionValueDict['ultimateGun'] = [BaseMV(area='single', stat='atk', value=0.75 + 0.6 * self.ultUptime, eidolonThreshold=5, eidolonBonus=0.15)]
        self.motionValueDict['ultimateAxe'] = [BaseMV(area='single', stat='atk', value=0.75 + 0.6 * self.ultUptime, eidolonThreshold=5, eidolonBonus=0.15)]
        self.motionValueDict['ultimateFinal'] = [BaseMV(area='single', stat='atk', value=0.10 + 0.15 * self.ultUptime, eidolonThreshold=5, eidolonBonus=0.15)]
        
        # Talents
        self.addStat('AdvanceForward',description='Skill Advance',amount=0.10,type=['skill'])
        self.addStat('BreakEfficiency',description='Ultimate Weakness Break Efficiency',amount=1.0,type=['ultimate'])
        self.addStat('CD',description='Feixiao Talent',amount=0.60,type=['followup'])

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
        retval.damage = self.getTotalMotionValue('ultimateGun',type) * self.weaknessBrokenUptime
        retval.damage += self.getTotalMotionValue('ultimateAxe',type) * (1.0 - self.weaknessBrokenUptime)
        retval.damage += self.getTotalMotionValue('ultimateFinal',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 90.0 * self.getBreakEfficiency(type)
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
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        self.addDebugInfo(retval,type)
        return retval
