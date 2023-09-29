from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BuffEffect import BuffEffect
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
        self.reignStacks = reignStacks
        
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
        self.addStat('CD',description='trace',type='transmigration',amount=0.24,uptime=self.joltAnewUptime)
        
        # Eidolons
        if self.eidolon >= 6:
            self.addStat('ResPen',description='e6',type='transmigration',amount=0.2,stacks=self.reignStacks)

        # Gear
        self.equipGear()

    def useBasic(self, hitNum:int=None):
        retval = BaseEffect()
        type = ['basic','outroarStacks']
        if hitNum is None:
            for i in range(2):
                retval.gauge = 30.0 * self.getBreakEfficiency(type)
                retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
                retval.skillpoints = 1.0
                retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        elif hitNum > 0:
            retval.damage = self.getTotalMotionValue('basic_{}'.format(i+1))
            retval.damage *= self.getTotalCrit(type)
            retval.damage *= self.getDmg(type) + 0.125 * self.heartStacks
            retval.damage = self.applyDamageMultipliers(retval.damage,type)
        
        self.addHeart()
        return retval

    def useEnhancedBasic1(self, hitNum:int=None):
        retval = BaseEffect()
        type = ['basic','outroarStacks']
        if hitNum is None: #iterate through each subhit then apply energy, SP, and Action Values
            for i in range(3):
                retval += self.useEnhancedBasic1(hitNum=i+1)
            retval.gauge = 60.0 * self.getBreakEfficiency(type)
            retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
            retval.skillpoints = 0.0
            retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        elif hitNum > 0: # individual hits
            retval.damage = self.getTotalMotionValue('enhancedBasic1_{}'.format(hitNum))
            retval.damage *= self.getTotalCrit(type)
            retval.damage *= self.getDmg(type) + 0.125 * self.heartStacks
            retval.damage = self.applyDamageMultipliers(retval.damage,type)
        
        self.addHeart()
        return retval

    def useEnhancedBasic2(self, hitNum:int):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        type = ['basic','outroarStacks']

        if hitNum is None: #iterate through each subhit then apply energy, SP, and Action Values
            for i in range(5):
                retval += self.useEnhancedBasic2(hitNum=i+1)
            retval.gauge = ( 90.0 + 30.0 * num_adjacents ) * self.getBreakEfficiency(type)
            retval.energy = ( 35.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
            retval.skillpoints = 0.0
            retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        elif hitNum > 0: # individual hits
            if hitNum >= 4:
                self.addRoar()
            retval.damage = self.getTotalMotionValue('enhancedBasic3_{}'.format(hitNum))
            retval.damage *= self.getTotalCrit(type)
            retval.damage *= self.getDmg(type) + 0.125 * self.heartStacks
            retval.damage = self.applyDamageMultipliers(retval.damage,type)
        
        self.addHeart()
        return retval

    def useEnhancedBasic3(self, hitNum:int=None):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        type = ['basic','outroar']
        if hitNum is None: #iterate through each subhit then apply energy, SP, and Action Values
            for i in range(7):
                retval += self.useEnhancedBasic3(hitNum=i+1)
            retval.gauge = ( 120.0 + 60.0 * num_adjacents ) * self.getBreakEfficiency(type)
            retval.energy = ( 40.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
            retval.skillpoints = 0.0
            retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        elif hitNum > 0: # individual hits
            if hitNum >= 4:
                self.addRoar()
            retval.damage = self.getTotalMotionValue('enhancedBasic3_{}'.format(hitNum))
            retval.damage *= self.getTotalCrit(type)
            retval.damage *= self.getDmg(type)
            retval.damage = self.applyDamageMultipliers(retval.damage,type)
        
        self.addHeart()
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.skillpoints = -1.0
        return retval

    def useUltimate(self, hitNum:int=None):
        numBlast = min(3, self.numEnemies - 1)
        retval = BaseEffect()
        type = ['ultimate','outroar']
        if hitNum is None: #iterate through each subhit then apply energy, SP, and Action Values
            for i in range(3):
                retval += self.useUltimate(hitNum=i+1)
            retval.gauge = ( 60.0 * numBlast ) * self.getBreakEfficiency(type)
            retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
            retval.skillpoints = 3.0 if self.eidolon >= 2 else 2.0
            retval.actionvalue = -1.0 if self.eidolon >= 2 else 0.0
        elif hitNum > 0: # individual hits
            retval.damage = self.getTotalMotionValue('ultimate_{}'.format(hitNum))
            retval.damage *= self.getTotalCrit(type)
            retval.damage *= self.getDmg()
            retval.damage = self.applyDamageMultipliers(retval.damage,type)
        
        self.addHeart()
        return retval
    
    def addHeart(self):
        tempStat:BuffEffect = next(x for x in self.tempStats['DMG'] if x.description == 'Righteous Heart')
        if tempStat is not None:
            tempStat.stacks += 2 if self.eidolon >= 1 else 1
            tempStat.stacks = min(10 if self.eidolon >= 1 else 6,tempStat.stacks)
        else:
            self.addTempStat('DMG',description='Righteous Heart',
                             amount=0.11 if self.eidolon >= 5 else 0.1,
                             stacks=2 if self.eidolon >= 1 else 1,
                             duration=1)
    
    def addRoar(self):
        tempStat:BuffEffect = next(x for x in self.tempStats['CD'] if x.description == 'Outroar')
        if tempStat is not None:
            tempStat.stacks = min(4,tempStat.stacks+1)
        else:
            self.addTempStat('CD',description='Outroar',
                             amount=0.132 if self.eidolon >= 3 else 0.12,
                             stacks=1, duration=1)