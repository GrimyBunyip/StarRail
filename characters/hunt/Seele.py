from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Seele(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                sheathedBladeUptime:float=1.0,
                e1Uptime:float=0.8,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Seele')
        
        self.sheathedBladeUptime = sheathedBladeUptime
        self.resurgence = False
        self.e1Uptime = e1Uptime

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=2.2, eidolonThreshold=3, eidolonBonus=0.22)]
        self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=4.25, eidolonThreshold=5, eidolonBonus=0.34)]

        # Talents
        self.percSpd += ( 0.25 * self.sheathedBladeUptime ) * (2.0 if self.eidolon >= 2 else 1.0)

        # Eidolons
        self.CR += (0.15 * self.e1Uptime) if self.eidolon >= 1 else 0.0
        # e6 not yet implemented
        
        # Gear
        self.equipGear()
        
    def useBasic(self):
        retval = BaseEffect()
        type = 'basic'
        retval.damage = self.getTotalMotionValue('basic')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = 'skill'
        retval.damage = self.getTotalMotionValue('skill')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 - 0.2 - min(1.0,self.getTotalStat('AdvanceForward','skill')) # advance forward 0.2 from passive
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = 'ultimate'
        retval.damage = self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 90.0 * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type) # too lazy to implement seele e6, who cares
        return retval
    
    def useResurgence(self):
        retval = BaseEffect()
        retval.actionvalue = -1.0
        retval.energy = ( 15.0 if self.eidolon >= 4 else 0.0 ) * self.getER(type)
        self.resurgence = True
        self.resPen += 0.20 # res pen from buffed state
        self.Dmg += 0.88 if self.eidolon >=3 else 0.8 # resurgence buff
        return retval

    def endTurn(self):
        retval = BaseEffect()
        if self.resurgence:
            self.resPen -= 0.20 # reset res pen from buffed state
            self.Dmg -= 0.88 if self.eidolon >=3 else 0.8 # resurgence buff
            self.resurgence = False
        return retval