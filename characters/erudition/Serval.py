from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Serval(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Serval')
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=1.4, eidolonThreshold=3, eidolonBonus=0.14),
                                        BaseMV(area='adjacent', stat='atk', value=0.6, eidolonThreshold=3, eidolonBonus=0.06)]
        self.motionValueDict['dot'] = [BaseMV(area='single', stat='atk', value=1.04, eidolonThreshold=3, eidolonBonus=0.104)]
        self.motionValueDict['ultimate'] = [BaseMV(area='all', stat='atk', value=1.8, eidolonThreshold=5, eidolonBonus=0.144)]
        self.motionValueDict['shockedBasic'] = [BaseMV(area='all', stat='atk', value=0.72, eidolonThreshold=5, eidolonBonus=0.072)]
        self.motionValueDict['shockedSkill'] = [BaseMV(area='all', stat='atk', value=0.72, eidolonThreshold=5, eidolonBonus=0.072)]
        self.motionValueDict['shockedUltimate'] = [BaseMV(area='all', stat='atk', value=0.72, eidolonThreshold=5, eidolonBonus=0.072)]
        
        # Talents
        
        # Eidolons
        if self.eidolon >= 1 and self.numEnemies >= 2:
            self.motionValueDict['basic'].append(BaseMV(area='single', stat='atk', value=0.6))
        
        # Gear
        self.equipGear()

    def useBasic(self, shocked = True):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic',type)
        retval.damage += self.getTotalMotionValue('shockedBasic',type) if shocked else 0.0
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type) + 0.3 if (shocked and self.eidolon >= 6) else 0.0
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 30.0 * self.numEnemies if shocked else 30.0 ) * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) + 4.0 if (shocked and self.eidolon >= 2) else 0.0 ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useSkill(self, shocked = True):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill',type)
        retval.damage += self.getTotalMotionValue('shockedSkill',type) if shocked else 0.0
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type) + 0.3 if (shocked and self.eidolon >= 6) else 0.0
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) + 4.0 if (shocked and self.eidolon >= 2) else 0.0 ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self, shocked = True):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate',type)
        retval.damage += self.getTotalMotionValue('shockedUltimate',type) if shocked else 0.0
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type) + 0.3 if (shocked and self.eidolon >= 6) else 0.0
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) + 4.0 if (shocked and self.eidolon >= 2) else 0.0 ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useDot(self, shocked = True):
        retval = BaseEffect()
        type = ['dot']
        retval.damage = self.getTotalMotionValue('dot',type)
        # no crits on dots
        retval.damage *= self.getDmg(type) + ( 0.3 if (shocked and self.eidolon >= 6) else 0.0 )
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.energy = ( 0.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = 0.0 - self.getAdvanceForward(type)
        return retval