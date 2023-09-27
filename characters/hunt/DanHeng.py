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
        self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=2.6, eidolonThreshold=3, eidolonBonus=0.26)]
        self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=4.0, eidolonThreshold=5, eidolonBonus=0.32)]
        self.motionValueDict['ultimateSlowed'] = [BaseMV(type='ultimate',area='single', stat='atk', value=4.0+1.2, eidolonThreshold=5, eidolonBonus=0.32+0.096)]

        # Talents
        self.percSpd += 0.20 * self.fasterThanLightUptime # Faster Than Light
        self.CR += 0.12 * self.e1Uptime # The Higher You Fly, the Harder You Fall
        self.percTaunt -= 0.5 * self.hiddenDragonUptime # A2 ascension
        self.resPen += ( 0.396 if self.eidolon >= 5 else 0.36 ) * talentUptime * (0.5 if self.eidolon < 2 else 1.0)

        # Eidolons
        
        # Gear
        self.equipGear()
        
    def useBasic(self, slowed = True):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('basic')
        retval.damage *= self.getTotalCrit('basic')
        retval.damage *= self.getTotalDmg('basic') + ( 0.40 if slowed else 0.0 ) #    High Gale
        retval.damage = self.applyDamageMultipliers(retval.damage)
        retval.gauge = 30.0 * (1.0 + self.breakEfficiency)
        retval.energy = ( 20.0 + self.bonusEnergyAttack['basic'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['basic'])
        return retval

    def useSkill(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('skill')
        retval.damage *= self.getTotalCrit('skill')
        retval.damage *= self.getTotalDmg('skill')
        retval.damage = self.applyDamageMultipliers(retval.damage)
        retval.gauge = 60.0 * (1.0 + self.breakEfficiency)
        retval.energy = ( 30.0 + self.bonusEnergyAttack['skill'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
        return retval

    def useUltimate(self, slowed = True):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('ultimateSlowed') if slowed else self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit('ultimate')
        retval.damage *= self.getTotalDmg('ultimate')
        retval.damage = self.applyDamageMultipliers(retval.damage)
        retval.gauge = 90.0 * (1.0 + self.breakEfficiency)
        retval.energy = ( 5.0 + self.bonusEnergyAttack['ultimate'] ) * ( 1.0 + self.ER )
        retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['ultimate'])
        return retval
