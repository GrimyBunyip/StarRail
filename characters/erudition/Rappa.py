from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Rappa(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                eidolon:int=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Rappa')
        self.eidolon = self.eidolon if eidolon is None else eidolon
        
        # Motion Values should be set before talents or gear
        # to do: check eidolons
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['enhancedBasic'] = [BaseMV(area='single', stat='atk', value=1.0*2, eidolonThreshold=5, eidolonBonus=0.1*2),
                                                 BaseMV(area='adjacent', stat='atk', value=0.5*2, eidolonThreshold=5, eidolonBonus=0.05*2),
                                                 BaseMV(area='all', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1),]

        self.motionValueDict['skill'] = [BaseMV(area='all', stat='atk', value=1.2, eidolonThreshold=3, eidolonBonus=0.12)]

        # Talents
        self.addStat('BreakEfficiency',description='Rappa Ult Buff',amount=0.5,type=['enhancedBasic'])
        self.addStat('BreakEffect',description='Rappa Ult Buff',amount=0.34 if self.eidolon >= 5 else 0.30,type=['enhancedBasic'])
        
        # Eidolons
        if self.eidolon >= 1:
            self.addStat('DefShred',description='Rappa Talent',amount=0.15,type=['enhancedBasic'])
            self.addStat('BonusEnergyAttack',description='Rappa Talent',amount=20.0,type=['ultimate'])
        
        # Gear
        self.equipGear()
        
        # Team Buffs
        def addVulnForTalent(team:list=[]):
            amount = min(0,self.getTotalStat('ATK')-2400)
            amount = 0.02 + amount * 0.01 / 100.0
            amount = min(0.08,amount)
            self.addStat('Vulnerability',
                         description='Rappa Vulnerability Talent',
                         amount=amount,
                         uptime=self.weaknessBrokenUptime,
                         type=['break','superBreak'])

        self.teamBuffList.append(addVulnForTalent)

    def useTalent(self,extraTypes:list=[],numCharges:int=1):
        retval = BaseEffect()
        type = ['break','enhancedBasic'] + extraTypes

        imagBreakDamage = 0.66 if self.eidolon >= 3 else 0.60
        imagBreakDamage += (0.55 if self.eidolon >= 3 else 0.50) * numCharges
        imagBreakDamage *= self.breakLevelMultiplier
        imagBreakDamage *= self.getBreakEffect(type)
        imagBreakDamage *= self.getVulnerability(type)
        imagBreakDamage = self.applyDamageMultipliers(imagBreakDamage,type)

        retval.damage = imagBreakDamage
        # factor weakness broken uptime into whether we apply gauge
        retval.gauge = (6.0 + 3.0 * numCharges) * self.numEnemies * self.getBreakEfficiency(type)
        self.addDebugInfo(retval,type,f'Rappa Talent {self.name}')
        return retval

    def useBasic(self):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useEnhancedBasic(self):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        type = ['basic','enhancedBasic']
        retval.damage = self.getTotalMotionValue('enhancedBasic',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 60.0 + 30.0 * num_adjacents + 15.0 * self.numEnemies ) * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.energy = (5.0 + self.getBonusEnergyAttack(type)) * self.getER(type)
        retval.actionvalue = -1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval
                
    def useSuperBreak(self,extraTypes:list=[]):
        retval = BaseEffect()
        type = ['break','enhancedBasic'] + extraTypes

        superBreakDamage = self.breakLevelMultiplier
        superBreakDamage *= 0.6 # trace
        # superBreakDamage *= BREAK_MULTIPLIERS[self.element] # does not seem to scale off type
        superBreakDamage *= self.getBreakEffect(type)
        superBreakDamage *= self.getVulnerability(type)
        superBreakDamage = self.applyDamageMultipliers(superBreakDamage,type)

        retval.damage = superBreakDamage
        # factor in uptime
        retval *= self.weaknessBrokenUptime
        self.addDebugInfo(retval,type,f'Super Break Damage {self.name}')
        
        return retval