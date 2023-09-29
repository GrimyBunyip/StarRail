from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Luka(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                ultDebuffUptime:float=0.5,
                bleedUptime:float=1.0,
                e2uptime:float=1.0,
                e4stacks:float=4.0,
                e4uptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Luka')
        self.ultDebuffUptime = ultDebuffUptime
        self.bleedUptime = bleedUptime
        self.e2uptime = e2uptime
        self.e4stacks = e4stacks
        self.e4uptime = e4uptime
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        
        crushMV = 0.8 + 0.2 * 3 * 1.5 # Crush Fighting Will
        self.motionValueDict['enhancedBasic'] = [BaseMV(type='basic',area='single', stat='atk', value=crushMV, eidolonThreshold=5, eidolonBonus=crushMV/10)]

        self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=1.2, eidolonThreshold=3, eidolonBonus=0.12)]
        self.motionValueDict['dot'] = [BaseMV(type=['skill','dot'],area='single', stat='atk', value=3.38, eidolonThreshold=3, eidolonBonus=0.338)]

        self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=3.3, eidolonThreshold=5, eidolonBonus=0.264)]
        
        # Talents
        self.Vulnerability += (0.216 if self.eidolon >= 5 else 0.2) * self.ultDebuffUptime
        self.getBonusEnergyAttack(type) += 6.0 # cycle braking
        self.getBonusEnergyAttack(type) += 3.0 # cycle braking
        self.getBonusEnergyAttack(type) += 3.0 + 3.0 * self.e2uptime # cycle braking and e2
        
        # Eidolons
        self.Dmg += 0.15 * self.bleedUptime # e1
        self.percAtk += 0.05 * self.e4stacks * self.e4uptime
        
        # Gear
        self.equipGear()

    def useBasic(self):
        retval = BaseEffect()
        type = 'basic'
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

    def useEnhancedBasic(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('enhancedBasic')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.bonusEnergyAttack['enhancedBasic'] + self.getBonusEnergyTurn(type) ) * self.getER(type) # enhanced basic doesn't benefit from cycle braking, change energy tag here
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        
        dotExplosion = self.useDot()
        dotExplosion.damage *= ( 0.884 if self.eidolon >= 3 else 0.85 ) + ( 0.08 * 3 * 1.5 if self.eidolon >= 6 else 0.0 )
        retval += dotExplosion
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = 'skill'
        retval.damage = self.getTotalMotionValue('skill')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = 'ultimate'
        retval.damage = self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 90.0 * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        return retval

    def useDot(self):
        bleedHP = self.enemyMaxHP * 0.24
        retval = BaseEffect()
        retval.damage = min(bleedHP, self.getTotalMotionValue('dot'))
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        return retval