from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from baseClasses.BaseMV import BaseMV

class Hook(BaseCharacter):

    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                burnedUptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Hook')
        self.burnedUptime = burnedUptime
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type=['basic'],area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        
        self.motionValueDict['skill'] = [BaseMV(type=['skill'],area='single', stat='atk', value=2.4, eidolonThreshold=3, eidolonBonus=0.24)]
        self.motionValueDict['dot'] = [BaseMV(type=['skill','dot'],area='single', stat='atk', value=0.65, eidolonThreshold=3, eidolonBonus=0.065)]

        self.motionValueDict['enhancedSkill'] = [BaseMV(type=['skill'],area='single', stat='atk', value=2.8, eidolonThreshold=3, eidolonBonus=0.28),
                                                BaseMV(type=['skill'],area='adjacent', stat='atk', value=0.8, eidolonThreshold=3, eidolonBonus=0.08)]
                
        self.motionValueDict['ultimate'] = [BaseMV(type=['ultimate'],area='single', stat='atk', value=4.0, eidolonThreshold=5, eidolonBonus=0.32)]
        self.motionValueDict['talent'] = [BaseMV(type=['talent'],area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        
        # Talents
        self.addStat('AdvanceForward',description='trace',type=['ultimate'],amount=0.2)
        self.addStat('BonusEnergyAttack',description='trace',type=['ultimate'],amount=5.0)
        
        # Eidolons
        if self.eidolon >= 1:
            self.addStat('DMG',description='e1',type=['enhancedSkill'],amount=0.2)
        if self.eidolon >= 6:
            self.addStat('DMG',description='e6',amount=0.2,uptime=self.burnedUptime)

        # Gear
        self.equipGear()

    def useBasic(self):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic') + self.getTotalMotionValue('talent') * self.burnedUptime
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill') + self.getTotalMotionValue('talent') * self.burnedUptime
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useEnhancedSkill(self):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        type = ['skill','enhancedSkill']
        retval.damage = self.getTotalMotionValue('enhancedSkill') + self.getTotalMotionValue('talent') * self.burnedUptime * (1 + num_adjacents)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type,'Hook Enhanced Skill')
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate') + self.getTotalMotionValue('talent') * self.burnedUptime
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 90.0 * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval
    
    def useDot(self):
        retval = BaseEffect()
        type = ['dot']
        retval.damage = self.getTotalMotionValue('dot')
        # no crits on dots
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        return retval