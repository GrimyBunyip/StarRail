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
        self.motionValueDict['basic_1'] = [BaseMV(area='single', stat='atk', value=0.3, eidolonThreshold=3, eidolonBonus=0.03)]
        self.motionValueDict['basic_2'] = [BaseMV(area='single', stat='atk', value=0.7, eidolonThreshold=3, eidolonBonus=0.07)]
        
        self.motionValueDict['enhancedBasic1_1'] = [BaseMV(area='single', stat='atk', value=2.6*0.33, eidolonThreshold=3, eidolonBonus=2.86*0.33)]
        self.motionValueDict['enhancedBasic1_2'] = self.motionValueDict['enhancedBasic1_1']
        self.motionValueDict['enhancedBasic1_3'] = [BaseMV(area='single', stat='atk', value=2.6*0.34, eidolonThreshold=3, eidolonBonus=2.86*0.34)]

        self.motionValueDict['enhancedBasic2_1'] = [BaseMV(area='single', stat='atk', value=3.8*0.2, eidolonThreshold=3, eidolonBonus=0.38*0.2)]
        self.motionValueDict['enhancedBasic2_2'] = self.motionValueDict['enhancedBasic2_1']
        self.motionValueDict['enhancedBasic2_3'] = self.motionValueDict['enhancedBasic2_1']
        self.motionValueDict['enhancedBasic2_4'] = [BaseMV(area='single', stat='atk', value=3.8*0.2, eidolonThreshold=3, eidolonBonus=0.38*0.2),
                                                    BaseMV(area='adjacent', stat='atk', value=0.6*0.5, eidolonThreshold=3, eidolonBonus=0.06*0.5),]
        self.motionValueDict['enhancedBasic2_5'] = self.motionValueDict['enhancedBasic2_4']

        self.motionValueDict['enhancedBasic3_1'] = [BaseMV(area='single', stat='atk', value=5.0*0.142, eidolonThreshold=3, eidolonBonus=0.5*0.142)]
        self.motionValueDict['enhancedBasic3_2'] = self.motionValueDict['enhancedBasic3_1']
        self.motionValueDict['enhancedBasic3_3'] = self.motionValueDict['enhancedBasic3_1']
        self.motionValueDict['enhancedBasic3_4'] = [BaseMV(area='single', stat='atk', value=5.0*0.142, eidolonThreshold=3, eidolonBonus=0.5*0.142),
                                                    BaseMV(area='adjacent', stat='atk', value=1.8*0.25, eidolonThreshold=3, eidolonBonus=0.18*0.25),]
        self.motionValueDict['enhancedBasic3_5'] = self.motionValueDict['enhancedBasic3_4']
        self.motionValueDict['enhancedBasic3_6'] = self.motionValueDict['enhancedBasic3_4']
        self.motionValueDict['enhancedBasic3_7'] = [BaseMV(area='single', stat='atk', value=5.0*0.148, eidolonThreshold=3, eidolonBonus=0.5*0.148),
                                                    BaseMV(area='adjacent', stat='atk', value=1.8*0.25, eidolonThreshold=3, eidolonBonus=0.18*0.25),]
        
        self.motionValueDict['ultimate_1'] = [BaseMV(area='single', stat='atk', value=3.0*0.3, eidolonThreshold=5, eidolonBonus=0.24*0.3),
                                            BaseMV(area='adjacent', stat='atk', value=1.4*0.3, eidolonThreshold=5, eidolonBonus=0.112*0.3),]
        self.motionValueDict['ultimate_2'] = self.motionValueDict['ultimate_1']
        self.motionValueDict['ultimate_3'] = [BaseMV(area='single', stat='atk', value=3.0*0.4, eidolonThreshold=5, eidolonBonus=0.24*0.4),
                                            BaseMV(area='adjacent', stat='atk', value=1.4*0.4, eidolonThreshold=5, eidolonBonus=0.112*0.4),]
        
        # Talents
        self.addStat('CD',description='Lunae Trace',amount=0.24,uptime=self.joltAnewUptime)
        
        # Eidolons
        if self.eidolon >= 2:
            self.addStat('AdvanceForward',description='Lunae E2',amount=1.0,type=['ultimate'])
        if self.eidolon >= 6:
            self.addStat('ResPen',description='Lunae E6',amount=0.2,stacks=self.reignStacks)

        # Gear
        self.equipGear()

    def useBasic(self, hitNum:int=None):
        retval = BaseEffect()
        type = ['basic']
        if hitNum is None:
            for i in range(2):
                retval += self.useBasic(hitNum=i+1)
        elif hitNum > 0:
            if hitNum == 1:
                retval.gauge = 30.0 * self.getBreakEfficiency(type)
                retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
                retval.skillpoints = 1.0
                retval.actionvalue = 1.0 + self.getAdvanceForward(type)
            retval.damage = self.getTotalMotionValue(f'basic_{hitNum:d}',type)
            retval.damage *= self.getTotalCrit(type)
            retval.damage *= self.getDmg(type)
            retval.damage *= self.getVulnerability(type)
            retval.damage = self.applyDamageMultipliers(retval.damage,type)
            self.addDebugInfo(retval,type,f'Lunae Basic Hit {hitNum:d}')
        
        self.addHeart()
        return retval

    def useEnhancedBasic1(self, hitNum:int=None):
        retval = BaseEffect()
        type = ['basic','enhancedBasic']
        if hitNum is None: #iterate through each subhit then apply energy, SP, and Action Values
            for i in range(3):
                retval += self.useEnhancedBasic1(hitNum=i+1)
        elif hitNum > 0: # individual hits
            if hitNum == 1:
                retval.gauge = 60.0 * self.getBreakEfficiency(type)
                retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
                retval.actionvalue = 1.0 + self.getAdvanceForward(type)
            retval.damage = self.getTotalMotionValue(f'enhancedBasic1_{hitNum:d}',type)
            retval.damage *= self.getTotalCrit(type)
            retval.damage *= self.getDmg(type)
            retval.damage *= self.getVulnerability(type)
            retval.damage = self.applyDamageMultipliers(retval.damage,type)
            self.addDebugInfo(retval,type,f'Lunae Enhanced1 Hit {hitNum:d}')
        
        self.addHeart()
        return retval

    def useEnhancedBasic2(self, hitNum:int):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        type = ['basic','enhancedBasic']

        if hitNum is None: #iterate through each subhit then apply energy, SP, and Action Values
            for i in range(5):
                retval += self.useEnhancedBasic2(hitNum=i+1)
        elif hitNum > 0: # individual hits
            if hitNum == 1:
                retval.gauge = ( 90.0 + 30.0 * num_adjacents ) * self.getBreakEfficiency(type)
                retval.energy = ( 35.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
                retval.actionvalue = 1.0 + self.getAdvanceForward(type)
            if hitNum >= 4:
                self.addRoar()
            retval.damage = self.getTotalMotionValue(f'enhancedBasic3_{hitNum}',type)
            retval.damage *= self.getTotalCrit(type)
            retval.damage *= self.getDmg(type)
            retval.damage *= self.getVulnerability(type)
            retval.damage = self.applyDamageMultipliers(retval.damage,type)
            self.addDebugInfo(retval,type,f'Lunae Enhanced2 Hit {hitNum}')
        
        self.addHeart()
        return retval

    def useEnhancedBasic3(self, hitNum:int=None):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        type = ['basic','enhancedBasic']
        if hitNum is None: #iterate through each subhit then apply energy, SP, and Action Values
            for i in range(7):
                retval += self.useEnhancedBasic3(hitNum=i+1)
        elif hitNum > 0: # individual hits
            if hitNum == 1:
                retval.gauge = ( 120.0 + 60.0 * num_adjacents ) * self.getBreakEfficiency(type)
                retval.energy = ( 40.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
                retval.actionvalue = 1.0 + self.getAdvanceForward(type)
            if hitNum >= 4:
                self.addRoar()
            retval.damage = self.getTotalMotionValue(f'enhancedBasic3_{hitNum}',type)
            retval.damage *= self.getTotalCrit(type)
            retval.damage *= self.getDmg(type)
            retval.damage *= self.getVulnerability(type)
            retval.damage = self.applyDamageMultipliers(retval.damage,type)
            self.addDebugInfo(retval,type,f'Lunae Enhanced3 Hit {hitNum}')
        
        self.addHeart()
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.skillpoints = -1.0
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self, hitNum:int=None):
        numBlast = min(3, self.numEnemies - 1)
        retval = BaseEffect()
        type = ['ultimate']
        if hitNum is None: #iterate through each subhit then apply energy, SP, and Action Values
            for i in range(3):
                retval += self.useUltimate(hitNum=i+1)
        elif hitNum > 0: # individual hits
            if hitNum == 1:
                retval.gauge = ( 60.0 * numBlast ) * self.getBreakEfficiency(type)
                retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
                retval.skillpoints = 3.0 if self.eidolon >= 2 else 2.0
                retval.actionvalue = 0.0 + self.getAdvanceForward(type)
            retval.damage = self.getTotalMotionValue(f'ultimate_{hitNum}',type)
            retval.damage *= self.getTotalCrit(type)
            retval.damage *= self.getDmg()
            retval.damage *= self.getVulnerability(type)
            retval.damage = self.applyDamageMultipliers(retval.damage,type)
            self.addDebugInfo(retval,type,f'Lunae Ultimate Hit {hitNum}')
        
        self.addHeart()
        return retval
    
    def addHeart(self):
        stacks = self.getTempBuffStacks('Righteous Heart')
        if stacks is None:
            self.addTempStat('DMG',description='Righteous Heart',
                             amount=0.11 if self.eidolon >= 5 else 0.1,
                             stacks=2 if self.eidolon >= 1 else 1,
                             duration=1)
        else:
            stacks += 2 if self.eidolon >= 1 else 1
            stacks = min(10 if self.eidolon >= 1 else 6,stacks)
            self.setTempBuffStacks('Righteous Heart',stacks)
    
    def addRoar(self):
        stacks = self.getTempBuffStacks('Outroar')
        if stacks is None:
            self.addTempStat('CD',description='Outroar',
                             amount=0.132 if self.eidolon >= 3 else 0.12,
                             stacks=1, duration=1)
        else:
            self.setTempBuffStacks('Outroar',min(4,stacks+1))