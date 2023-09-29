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
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Yanqing')

        self.soulsteelUptime = soulsteelUptime
        self.e4Uptime = e4Uptime
        self.freezeChance = freezeChance
        self.bliss=False
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['icing'] = [BaseMV(type='basic',area='single', stat='atk', value=0.3)]
        self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1),
                                        BaseMV(type='basic',area='single', stat='atk', value=0.0, eidolonThreshold=1, eidolonBonus=0.6)]
        self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=2.2, eidolonThreshold=3, eidolonBonus=0.22),
                                        BaseMV(type='skill',area='single', stat='atk', value=0.0, eidolonThreshold=1, eidolonBonus=0.6)]
        self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=3.5, eidolonThreshold=5, eidolonBonus=0.28),
                                            BaseMV(type='ultimate',area='single', stat='atk', value=0.0, eidolonThreshold=1, eidolonBonus=0.6)]
        self.motionValueDict['talent'] = [BaseMV(type=['talent','followup'],area='single', stat='atk', value=0.5, eidolonThreshold=5, eidolonBonus=0.05)]
        self.motionValueDict['freezeDot'] = [BaseMV(type=['talent','dot'],area='single', stat='atk', value=0.5, eidolonThreshold=5, eidolonBonus=0.05)]
        
        # Talents
        self.getTotalStat('ER') += 0.10 * self.soulsteelUptime if self.eidolon >= 2 else 0.0
        self.resPen += 0.12 * self.e4Uptime if self.eidolon >= 4 else 0.0

        # Soulsteel
        self.CR += self.soulsteelUptime * ( 0.22 if self.eidolon >= 5 else 0.20 )
        self.CD += self.soulsteelUptime * ( 0.33 if self.eidolon >= 5 else 0.30 )
        
        # Bliss is always up for Ult
        self.percTaunt -= 0.6 * self.soulsteelUptime

        # Eidolons
        
        # Gear
        self.equipGear()

    def useBasic(self, icing=True):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('basic') + self.getTotalMotionValue('icing') if icing else 0.0
        retval.damage *= self.getTotalCrit(['basic'])
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useSkill(self, icing=True):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('skill') + self.getTotalMotionValue('icing') if icing else 0.0
        retval.damage *= self.getTotalCrit(['skill'])
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useUltimate(self, icing=True):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('ultimate') + self.getTotalMotionValue('icing') if icing else 0.0
        retval.damage *= self.getTotalCrit(['ultimate'])
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 90.0 * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        return retval

    def useTalent(self, icing=True):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('talent') + self.getTotalMotionValue('icing') if icing else 0.0
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 10.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = 0.0 - self.getAdvanceForward(type)
        
        procrate = 0.62 if self.eidolon >= 5 else 0.6
        retval *= procrate
        
        retval += self.useFreezeDot()
        return retval
    
    def useFreezeDot(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('dot')
        retval.damage *= self.getTotalCrit(['dot','talent'])
        retval.damage *= self.getTotalDmg(['dot','talent'])
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        
        procrate = 0.62 if self.eidolon >= 5 else 0.6
        retval *= procrate * self.freezeChance
        return retval
    
    def useBliss(self):
        retval = BaseEffect()
        self.bliss=True
        self.CR += 0.6
        self.CD += 0.54 if self.eidolon >= 5 else 0.5
        return retval
        
    def endTurn(self):
        retval = BaseEffect()
        if self.bliss==True:
            self.CR -= 0.6
            self.CD -= 0.54 if self.eidolon >= 5 else 0.5
            self.bliss = False
        return retval
        