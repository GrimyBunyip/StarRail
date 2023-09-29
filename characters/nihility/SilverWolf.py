from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class SilverWolf(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                dmgResUptime:float=0.0, #we are already assuming we're hitting for weakness
                allResUptime:float=1.0, #might want to decrease this for large numbers of targets
                defShredUptime:float=1.0,
                talentAtkUptime:float=0.5,
                talentDefUptime:float=0.5,
                talentSpdUptime:float=0.5,
                a6Uptime:float=1.0,
                numDebuffs:float=5.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Silver Wolf')
        self.dmgResUptime = dmgResUptime
        self.allResUptime = allResUptime
        self.defShredUptime = defShredUptime
        self.talentAtkUptime = talentAtkUptime
        self.talentDefUptime = talentDefUptime
        self.talentSpdUptime = talentSpdUptime
        self.a6Uptime = a6Uptime
        self.numDebuffs = numDebuffs
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]        
        self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=1.96, eidolonThreshold=3, eidolonBonus=0.196)]
        self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=3.8, eidolonThreshold=5, eidolonBonus=0.304)]
        
        # Talents
        self.resPen += 0.20 * self.dmgResUptime
        self.resPen += (0.105 if self.eidolon >= 3 else 0.10) * self.allResUptime
        self.defShred += (0.468 if self.eidolon >= 5 else 0.45) * self.defShredUptime
        self.defShred += (0.088 if self.eidolon >= 3 else 0.08) * self.talentDefUptime
        self.defShred += 0.03 * self.a6Uptime
        self.enemySpeed /= 1.0 - (0.06 if self.eidolon >= 3 else 0.066) * self.talentSpdUptime
        
        # Eidolons
        self.getBonusEnergyAttack(type) += (7.0 * min(5.0,self.numDebuffs)) if self.eidolon >= 1 else 0.0
        self.motionValueDict['ultimate'][0].value += (0.20 * min(5.0,self.numDebuffs)) if self.eidolon >= 4 else 0.0
        self.Dmg += (0.20 * min(5.0,self.numDebuffs)) if self.eidolon >= 6 else 0.0
        
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
        retval = BaseEffect()
        type = ['skill']
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
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 90.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        return retval