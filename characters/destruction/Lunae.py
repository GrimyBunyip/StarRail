from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from baseClasses.BaseMV import BaseMV

class Lunae(BaseCharacter):

    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                joltAnewUptime:float=1.0,
                reignStacks:float=3.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Lunae')
        self.joltAnewUptime = joltAnewUptime
        self.heartStacks = 0
        self.outroarStacks = 0
        self.reignStacks = reignStacks
        self.DmgType['heartStacks'] = 0.0
        self.CRType['outroarStacks'] = 0.0 # Doesn't do anything. Suppresses error messages that notify me of misnamed dictionary keys
        self.CDType['outroarStacks'] = 0.0

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic_1'] = [BaseMV(type='basic',area='single', stat='atk', value=0.3, eidolonThreshold=3, eidolonBonus=0.03)]
        self.motionValueDict['basic_2'] = [BaseMV(type='basic',area='single', stat='atk', value=0.7, eidolonThreshold=3, eidolonBonus=0.07)]
        
        self.motionValueDict['enhancedBasic1_1'] = [BaseMV(type='basic',area='single', stat='atk', value=2.6*0.33, eidolonThreshold=3, eidolonBonus=2.86*0.33)]
        self.motionValueDict['enhancedBasic1_2'] = self.motionValueDict['enhancedBasic1_1']
        self.motionValueDict['enhancedBasic1_3'] = [BaseMV(type='basic',area='single', stat='atk', value=2.6*0.34, eidolonThreshold=3, eidolonBonus=2.86*0.34)]

        self.motionValueDict['enhancedBasic2_1'] = [BaseMV(type='basic',area='single', stat='atk', value=3.8*0.2, eidolonThreshold=3, eidolonBonus=0.38*0.2)]
        self.motionValueDict['enhancedBasic2_2'] = self.motionValueDict['enhancedBasic2_1']
        self.motionValueDict['enhancedBasic2_3'] = self.motionValueDict['enhancedBasic2_1']
        self.motionValueDict['enhancedBasic2_4'] = [BaseMV(type='basic',area='single', stat='atk', value=3.8*0.2, eidolonThreshold=3, eidolonBonus=0.38*0.2),
                                                    BaseMV(type='basic',area='adjacent', stat='atk', value=0.6*0.5, eidolonThreshold=3, eidolonBonus=0.06*0.5),]
        self.motionValueDict['enhancedBasic2_5'] = self.motionValueDict['enhancedBasic2_4']

        self.motionValueDict['enhancedBasic3_1'] = [BaseMV(type='basic',area='single', stat='atk', value=5.0*0.142, eidolonThreshold=3, eidolonBonus=0.5*0.142)]
        self.motionValueDict['enhancedBasic3_2'] = self.motionValueDict['enhancedBasic3_1']
        self.motionValueDict['enhancedBasic3_3'] = self.motionValueDict['enhancedBasic3_1']
        self.motionValueDict['enhancedBasic3_4'] = [BaseMV(type='basic',area='single', stat='atk', value=5.0*0.142, eidolonThreshold=3, eidolonBonus=0.5*0.142),
                                                    BaseMV(type='basic',area='adjacent', stat='atk', value=1.8*0.25, eidolonThreshold=3, eidolonBonus=0.18*0.25),]
        self.motionValueDict['enhancedBasic3_5'] = self.motionValueDict['enhancedBasic3_4']
        self.motionValueDict['enhancedBasic3_6'] = self.motionValueDict['enhancedBasic3_4']
        self.motionValueDict['enhancedBasic3_7'] = [BaseMV(type='basic',area='single', stat='atk', value=5.0*0.148, eidolonThreshold=3, eidolonBonus=0.5*0.148),
                                                    BaseMV(type='basic',area='adjacent', stat='atk', value=1.8*0.25, eidolonThreshold=3, eidolonBonus=0.18*0.25),]
        
        self.motionValueDict['ultimate_1'] = [BaseMV(type='ultimate',area='single', stat='atk', value=3.0*0.3, eidolonThreshold=5, eidolonBonus=0.24*0.3),
                                            BaseMV(type='ultimate',area='adjacent', stat='atk', value=1.4*0.3, eidolonThreshold=5, eidolonBonus=0.112*0.3),]
        self.motionValueDict['ultimate_2'] = self.motionValueDict['ultimate_1']
        self.motionValueDict['ultimate_3'] = [BaseMV(type='ultimate',area='single', stat='atk', value=3.0*0.4, eidolonThreshold=5, eidolonBonus=0.24*0.4),
                                            BaseMV(type='ultimate',area='adjacent', stat='atk', value=1.4*0.4, eidolonThreshold=5, eidolonBonus=0.112*0.4),]
        
        # Talents
        self.CD += 0.24 * self.joltAnewUptime
        
        # Eidolons
        self.resPen += ( 0.20 * self.reignStacks ) if self.eidolon >= 6 else 0.0

        # Gear
        self.equipGear()

    def useBasic(self, hitNum:int=None):
        retval = BaseEffect()
        if hitNum is None:
            for i in range(2):
                retval.gauge = 30.0 * (1.0 + self.breakEfficiency)
                retval.energy = ( 20.0 + self.bonusEnergyAttack['basic'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
                retval.skillpoints = 1.0
                retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['basic'])
        elif hitNum > 0:
            retval.damage = self.getTotalMotionValue('basic_{}'.format(i+1))
            retval.damage *= self.getTotalCrit(['basic','outroarStacks'])
            retval.damage *= self.getTotalDmg(['basic', 'heartStacks']) + 0.125 * self.heartStacks
            retval.damage = self.applyDamageMultipliers(retval.damage)
        
        self.addHeart()
        return retval

    def useEnhancedBasic1(self, hitNum:int=None):
        retval = BaseEffect()
        if hitNum is None: #iterate through each subhit then apply energy, SP, and Action Values
            for i in range(3):
                retval += self.useEnhancedBasic1(hitNum=i+1)
            retval.gauge = 60.0 * (1.0 + self.breakEfficiency)
            retval.energy = ( 30.0 + self.bonusEnergyAttack['basic'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
            retval.skillpoints = 0.0
            retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['basic'])
        elif hitNum > 0: # individual hits
            retval.damage = self.getTotalMotionValue('enhancedBasic1_{}'.format(hitNum))
            retval.damage *= self.getTotalCrit(['basic','outroarStacks'])
            retval.damage *= self.getTotalDmg(['basic', 'heartStacks']) + 0.125 * self.heartStacks
            retval.damage = self.applyDamageMultipliers(retval.damage)
        
        self.addHeart()
        return retval

    def useEnhancedBasic2(self, hitNum:int):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()

        if hitNum is None: #iterate through each subhit then apply energy, SP, and Action Values
            for i in range(5):
                retval += self.useEnhancedBasic2(hitNum=i+1)
            retval.gauge = ( 90.0 + 30.0 * num_adjacents ) * (1.0 + self.breakEfficiency)
            retval.energy = ( 35.0 + self.bonusEnergyAttack['basic'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
            retval.skillpoints = 0.0
            retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['basic'])
        elif hitNum > 0: # individual hits
            if hitNum >= 4:
                self.addRoar()
            retval.damage = self.getTotalMotionValue('enhancedBasic3_{}'.format(hitNum))
            retval.damage *= self.getTotalCrit(['basic','outroarStacks'])
            retval.damage *= self.getTotalDmg(['basic', 'heartStacks']) + 0.125 * self.heartStacks
            retval.damage = self.applyDamageMultipliers(retval.damage)
        
        self.addHeart()
        return retval

    def useEnhancedBasic3(self, hitNum:int=None):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        if hitNum is None: #iterate through each subhit then apply energy, SP, and Action Values
            for i in range(7):
                retval += self.useEnhancedBasic3(hitNum=i+1)
            retval.gauge = ( 120.0 + 60.0 * num_adjacents ) * (1.0 + self.breakEfficiency)
            retval.energy = ( 40.0 + self.bonusEnergyAttack['basic'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
            retval.skillpoints = 0.0
            retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['basic'])
        elif hitNum > 0: # individual hits
            if hitNum >= 4:
                self.addRoar()
            retval.damage = self.getTotalMotionValue('enhancedBasic3_{}'.format(hitNum))
            retval.damage *= self.getTotalCrit(['basic','outroarStacks'])
            retval.damage *= self.getTotalDmg(['basic', 'heartStacks'])
            retval.damage = self.applyDamageMultipliers(retval.damage)
        
        self.addHeart()
        return retval

    def useSkill(self):
        retval = BaseEffect()
        retval.skillpoints = -1.0
        return retval

    def useUltimate(self, hitNum:int=None):
        numBlast = min(3, self.numEnemies - 1)
        retval:BaseEffect = BaseEffect()
        if hitNum is None: #iterate through each subhit then apply energy, SP, and Action Values
            for i in range(3):
                retval += self.useUltimate(hitNum=i+1)
            retval.gauge = ( 60.0 * numBlast ) * (1.0 + self.breakEfficiency)
            retval.energy = ( 5.0 + self.bonusEnergyAttack['ultimate'] ) * ( 1.0 + self.ER )
            retval.skillpoints = 3.0 if self.eidolon >= 2 else 2.0
            retval.actionvalue = -1.0 if self.eidolon >= 2 else 0.0
        elif hitNum > 0: # individual hits
            retval.damage = self.getTotalMotionValue('ultimate_{}'.format(hitNum))
            retval.damage *= self.getTotalCrit(['ultimate','outroarStacks'])
            retval.damage *= self.getTotalDmg(['ultimate', 'heartStacks'])
            retval.damage = self.applyDamageMultipliers(retval.damage)
        
        self.addHeart()
        return retval
    
    def addHeart(self):
        if self.eidolon >= 1:
            self.heartStacks += 2
            self.heartStacks = min(10,self.heartStacks)
        else:
            self.heartStacks += 1
            self.heartStacks = min(6,self.heartStacks)
        self.DmgType['heartStacks'] = self.heartStacks * ( 0.11 if self.eidolon >= 5 else 0.1 )
    
    def addRoar(self):
        self.outroarStacks += 1
        self.outroarStacks = min(4, self.outroarStacks)
        self.CDType['outroarStacks'] = self.outroarStacks * ( 0.132 if self.eidolon >= 3 else 0.12 )
        
    def endTurn(self):
        retval = BaseEffect()
        self.heartStacks= 0
        if self.eidolon < 4:
            self.outroarStacks = 0
        self.DmgType['heartStacks'] = self.heartStacks * ( 0.11 if self.eidolon >= 5 else 0.1 )
        self.CDType['outroarStacks'] = self.outroarStacks * ( 0.132 if self.eidolon >= 3 else 0.12 )
        return retval