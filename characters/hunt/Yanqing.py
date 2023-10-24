from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Yanqing(BaseCharacter):

    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                soulsteelUptime:float = 1.0,
                e4Uptime:float = 1.0,
                freezeChance:float = 0.5,
                gentleBladeUptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Yanqing')

        self.soulsteelUptime = soulsteelUptime
        self.e4Uptime = e4Uptime
        self.freezeChance = freezeChance
        self.gentleBladeUptime = gentleBladeUptime
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['icing'] = [BaseMV(area='single', stat='atk', value=0.3)]
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1),
                                        BaseMV(area='single', stat='atk', value=0.0, eidolonThreshold=1, eidolonBonus=0.6)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=2.2, eidolonThreshold=3, eidolonBonus=0.22),
                                        BaseMV(area='single', stat='atk', value=0.0, eidolonThreshold=1, eidolonBonus=0.6)]
        self.motionValueDict['ultimate'] = [BaseMV(area='single', stat='atk', value=3.5, eidolonThreshold=5, eidolonBonus=0.28),
                                            BaseMV(area='single', stat='atk', value=0.0, eidolonThreshold=1, eidolonBonus=0.6)]
        self.motionValueDict['talent'] = [BaseMV(area='single', stat='atk', value=0.5, eidolonThreshold=5, eidolonBonus=0.05)]
        self.motionValueDict['freezeDot'] = [BaseMV(area='single', stat='atk', value=0.5, eidolonThreshold=5, eidolonBonus=0.05)]
        
        # Talents
        self.addStat('SPD.percent',description='trace',amount=0.1,uptime=self.gentleBladeUptime) # Frost Favors the Brave
        self.addStat('RES',description='trace',amount=0.2,uptime=self.soulsteelUptime) # Frost Favors the Brave
        self.addStat('CR',description='soulsteel',
                     amount=0.22 if self.eidolon >= 5 else 0.20,
                     uptime=self.soulsteelUptime)
        self.addStat('CD',description='soulsteel',
                     amount=0.33 if self.eidolon >= 5 else 0.30,
                     uptime=self.soulsteelUptime)
        self.addStat('Taunt.percent',description='soulsteel',amount=-0.6,uptime=self.soulsteelUptime)

        # Eidolons
        if self.eidolon >= 2:
            self.addStat('ER',description='e2',amount=0.10,uptime=self.soulsteelUptime)
        if self.eidolon >= 4:
            self.addStat('ResPen',description='e4',amount=0.12,uptime=self.e4Uptime)
        
        # Gear
        self.equipGear()

    def useBasic(self, icing=True):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic',type) + self.getTotalMotionValue('icing',type) if icing else 0.0
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useSkill(self, icing=True):
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill',type) + self.getTotalMotionValue('icing',type) if icing else 0.0
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self, icing=True):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate',type) + self.getTotalMotionValue('icing',type) if icing else 0.0
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 90.0 * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useTalent(self, icing=True):
        retval = BaseEffect()
        type = ['talent','followup']
        retval.damage = self.getTotalMotionValue('talent',type) + self.getTotalMotionValue('icing',type) if icing else 0.0
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 10.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = 0.0 - self.getAdvanceForward(type)
        
        procrate = 0.62 if self.eidolon >= 5 else 0.6
        retval *= procrate
        self.addDebugInfo(retval,type)
        
        retval += self.useFreezeDot()
        return retval
    
    def useFreezeDot(self):
        retval = BaseEffect()
        type = ['dot','talent']
        retval.damage = self.getTotalMotionValue('freezeDot',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        
        procrate = 0.62 if self.eidolon >= 5 else 0.6
        retval *= procrate * self.freezeChance
        self.addDebugInfo(retval,type)
        return retval
    
    def useBliss(self):
        self.addTempStat('CR',description='ultimate',amount=0.6,duration=1)
        self.addTempStat('CD',description='ultimate',
                         amount=0.54 if self.eidolon >= 5 else 0.5,
                         duration=1)
        return BaseEffect()        