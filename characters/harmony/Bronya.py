from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Bronya(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Bronya')

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['followup'] = [BaseMV(type='followup',area='single', stat='atk', value=0.8)]

        # Talents
        self.advanceForwardType['basic'] = 0.33 if self.eidolon >= 3 else 0.3
        self.CRType['basic'] =+ 1.0 # Ascension 2
        self.Dmg += 0.10 # Ascension 6

        # Eidolons
        
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
        retval.energy = ( 30.0 + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
        retval.skillpoints = -1.0 + (0.5 if self.eidolon >= 1 else 0.0)
        retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
        return retval

    def useUltimate(self, targetCharacter:BaseCharacter = None):
        retval = BaseEffect()
        retval.energy = 5.0 * ( 1.0 + self.ER )
        retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['ultimate'])
        return retval
        
    def useFollowup(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('basic') * 0.8
        retval.damage *= self.getTotalCrit('basic')
        retval.damage *= self.getTotalDmg('basic')
        retval.damage = self.applyDamageMultipliers(retval.damage)
        retval.gauge = 30.0 * (1.0 + self.breakEfficiency)
        retval.energy = ( 5.0 + self.bonusEnergyAttack['followup'] ) * ( 1.0 + self.ER )
        return retval
    
    def useAdvanceForward(self, advanceAmount:float=1.0):
        retval = BaseEffect()
        retval.actionvalue = max(-1.0,-advanceAmount)
        return retval