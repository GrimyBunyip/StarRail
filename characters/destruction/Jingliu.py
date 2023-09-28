from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from baseClasses.BaseMV import BaseMV

class Jingliu(BaseCharacter):

    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                transmigrationPercAtk:float=1.8,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Jingliu')
        
        self.percAtkType['enhancedSkill'] = transmigrationPercAtk
        self.percAtkType['ultimate'] = transmigrationPercAtk

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        
        self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=2.0, eidolonThreshold=5, eidolonBonus=0.2)]
        
        self.motionValueDict['enhancedSkill'] = [BaseMV(type='skill',area='single', stat='atk', value=2.5, eidolonThreshold=5, eidolonBonus=0.25),
                                                BaseMV(type='skill',area='adjacent', stat='atk', value=1.25, eidolonThreshold=5, eidolonBonus=0.125)]
        
        self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=3.0, eidolonThreshold=3, eidolonBonus=0.24),
                                            BaseMV(type='ultimate',area='adjacent', stat='atk', value=1.5, eidolonThreshold=3, eidolonBonus=0.12)]
        
        # Talents
        self.CRType['transmigration'] = 0.50 # 
        self.CDType['transmigration'] = 0.0 # keep this empty
        self.DmgType['ultimate'] = 0.20 # Ascension
        # too lazy to implement e1, e2 and e4 and e6 for now
        
        # Eidolons
        # handle handle e1 manually, by using the argument in the useSkill call
        self.percAtk += ( 0.30 * self.aTightEmbraceUptime ) if self.eidolon >= 2 else 0.0
        # better to handle e6 manually

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
        retval.gauge = 60.0 * (1.0 + self.breakEfficiency)
        retval.energy = ( 20.0 + self.bonusEnergyAttack['skill'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill']) - 0.10 # advance forward from ascension
        return retval
    
    def extraTurn(self):
        retval = BaseEffect()
        retval.actionvalue = -1.0
        return retval        

    def useEnhancedSkill(self):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('enhancedSkill')
        retval.damage *= self.getTotalCrit(['skill','transmigration'])
        retval.damage *= self.getTotalDmg(['skill','transmigration'])
        retval.damage = self.applyDamageMultipliers(retval.damage)
        retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * (1.0 + self.breakEfficiency)
        retval.energy = ( 30.0 + self.bonusEnergyAttack['skill'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
        retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
        return retval

    def useUltimate(self):
        blastEnemies = min(3,self.numEnemies)
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit(['ultimate','transmigration'])
        retval.damage *= self.getTotalDmg(['ultimate','transmigration'])
        retval.damage = self.applyDamageMultipliers(retval.damage)
        retval.gauge = 60.0 * blastEnemies * (1.0 + self.breakEfficiency)
        retval.energy = ( 5.0 + self.bonusEnergyAttack['ultimate'] ) * ( 1.0 + self.ER )
        return retval