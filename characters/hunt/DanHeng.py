from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class DanHeng(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                talentUptime:float = 0.0,
                fasterThanLightUptime:float = 1.0,
                hiddenDragonUptime:float = 0.0,
                e1Uptime:float = 0.5,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Dan Heng')
        
        self.talentUptime = talentUptime
        self.e1Uptime = e1Uptime
        self.fasterThanLightUptime = fasterThanLightUptime
        self.hiddenDragonUptime = hiddenDragonUptime

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type=['basic'],area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(type=['skill'],area='single', stat='atk', value=2.6, eidolonThreshold=3, eidolonBonus=0.26)]
        self.motionValueDict['ultimate'] = [BaseMV(type=['ultimate'],area='single', stat='atk', value=4.0, eidolonThreshold=5, eidolonBonus=0.32)]
        self.motionValueDict['ultimateSlowed'] = [BaseMV(type=['ultimate'],area='single', stat='atk', value=4.0+1.2, eidolonThreshold=5, eidolonBonus=0.32+0.096)]

        # Talents
        self.addStat('SPD.percent',description='trace',amount=0.20,uptime=self.fasterThanLightUptime)
        self.addStat('Taunt',description='trace',amount=-0.5,uptime=self.hiddenDragonUptime)
        self.addStat('ResPen',description='talent',
                    amount=0.396 if self.eidolon >= 5 else 0.36,
                    uptime=self.talentUptime)

        # Eidolons
        if self.eidolon >= 1:
            self.addStat('CR',description='e1',amount=0.12,uptime=self.e1Uptime)
        
        # Gear
        self.equipGear()
        
    def useBasic(self, slowed = True):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type) + ( 0.40 if slowed else 0.0 ) #    High Gale
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval, type)
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval, type)
        return retval

    def useUltimate(self, slowed = True):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimateSlowed') if slowed else self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 90.0 * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval, type)
        return retval
