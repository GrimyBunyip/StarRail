from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class JingYuan(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                battaliaCrushUptime:float=1.0,
                warMarshalUptime:float=1.0,
                e6uptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Jing Yuan')
        self.battaliaCrushUptime = battaliaCrushUptime
        self.warMarshalUptime = warMarshalUptime
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(type='skill',area='all', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='all', stat='atk', value=2.0, eidolonThreshold=3, eidolonBonus=0.16)]
        self.motionValueDict['talent'] = [BaseMV(type=['talent','followup'],area='single', stat='atk', value=0.66, eidolonThreshold=5, eidolonBonus=0.066)]
        
        # Talents
        self.CR += 0.1 * self.warMarshalUptime
        self.CRType['talent'] = 0.0
        self.CDType['talent'] = self.battaliaCrushUptime * 0.25
        
        # Eidolons
        self.DmgType['basic'] += 0.2 if self.eidolon >= 2 else 0.0
        self.DmgType['skill'] += 0.2 if self.eidolon >= 2 else 0.0
        self.DmgType['ultimate'] += 0.2 if self.eidolon >= 2 else 0.0
        self.Dmg += ( 0.36 * self.e6uptime ) if self.eidolon >= 6 else 0.0
        
        # Gear
        self.equipGear()

    def useBasic(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('basic')
        retval.damage *= self.getTotalCrit('basic')
        retval.damage *= self.getTotalDmg('basic')
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
        retval.gauge = ( 30.0 * self.numEnemies ) * (1.0 + self.breakEfficiency)
        retval.energy = ( 30.0 + self.bonusEnergyAttack['skill'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit('ultimate')
        retval.damage *= self.getTotalDmg('ultimate')
        retval.damage = self.applyDamageMultipliers(retval.damage)
        retval.gauge = 60.0 * self.numEnemies * (1.0 + self.breakEfficiency)
        retval.energy = ( 5.0 + self.bonusEnergyAttack['ultimate'] ) * ( 1.0 + self.ER )
        retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['ultimate'])
        return retval

    def useTalent(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('talent')
        retval.damage *= self.getTotalCrit(['talent','followup'])
        retval.damage *= self.getTotalDmg(['talent','followup'])
        retval.damage = self.applyDamageMultipliers(retval.damage)
        retval.gauge = 15.0 * (1.0 + self.breakEfficiency)
        retval.energy = ( 2.0 * ( 1.0 + self.ER ) ) if self.eidolon >= 4 else 0.0
        retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['talent'])
        
        multiplier = 1.0
        if self.numEnemies >= 2:
            multiplier += 0.5 if self.eidolon >= 1 else 0.25
        if self.numEnemies >= 3:
            multiplier += ( 0.5 if self.eidolon >= 1 else 0.25 ) * ( self.numEnemies - 2 ) / self.numEnemies
            
        retval.damage *= multiplier
        return retval