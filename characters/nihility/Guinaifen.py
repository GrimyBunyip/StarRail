from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Guinaifen(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                firekissStacks:float=4.0,
                burnUptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Guinaifen')
        self.firekissStacks = firekissStacks
        self.burnUptime = burnUptime
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type=['basic'],area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(type=['skill'],area='single', stat='atk', value=1.2, eidolonThreshold=3, eidolonBonus=0.12),
                                        BaseMV(type=['skill'],area='adjacent', stat='atk', value=0.40, eidolonThreshold=3, eidolonBonus=0.04),]
        self.motionValueDict['dot'] = [BaseMV(type=['skill','dot'],area='single', stat='atk', value=2.1821, eidolonThreshold=3, eidolonBonus=0.21821)]
        
        self.motionValueDict['ultimate'] = [BaseMV(type=['ultimate'],area='all', stat='atk', value=1.2, eidolonThreshold=5, eidolonBonus=0.096)]
        
        # Talents
        self.addStat('Vulnerability',description='firekiss',
                     amount=0.076 if self.eidolon >= 5 else 0.07,
                     stacks=min(self.firekissStacks, 4.0 if self.eidolon >= 6 else 3.0))
        self.addStat('DMG',description='trace',amount=0.2,uptime=self.burnUptime)
        
        # Eidolons
        if self.eidolon >= 2:
            self.motionValueDict['dot'][0].value += 0.4
        if self.eidolon >= 4:
            self.addStat('BonusEnergyAttack',description='e2',amount=2.0,type=['dot'])
        
        # Gear
        self.equipGear()

    def useBasic(self):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useSkill(self):
        num_adjacent = min(2.0, self.numEnemies - 1.0)
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('skill')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 60.0 + 30.0 * num_adjacent ) * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        
        # assume we hit up to 3 enemies
        dotExplosion = self.useDot()
        dotExplosion.damage *= 0.96 if self.eidolon >= 4 else 0.92
        retval += dotExplosion
        return retval

    def useDot(self):
        retval = BaseEffect()
        type = ['dot']
        retval.damage = self.getTotalMotionValue('dot')
        # no crits on dots
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.energy = ( 0.0 + self.bonusEnergyAttack['dot'] ) * self.getER(type)
        retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['dot'])
        return retval