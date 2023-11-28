from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Sampo(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                windshearUptime:float=1.0,
                windshearStacks:float=5.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Sampo')
        self.windshearUptime = windshearUptime
        self.windshearStacks = windshearStacks
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=0.56, eidolonThreshold=3, eidolonBonus=0.056)]
        self.motionValueDict['ultimate'] = [BaseMV(area='all', stat='atk', value=1.6, eidolonThreshold=5, eidolonBonus=0.128)]
        self.motionValueDict['dot'] = [BaseMV(area='single', stat='atk', value=0.52, eidolonThreshold=5, eidolonBonus=0.052)]
        self.motionValueDict['dote6'] = [BaseMV(area='single', stat='atk', value=0.52+0.15, eidolonThreshold=5, eidolonBonus=0.052)]
        
        # Talents
        self.addStat('BonusEnergyAttack',description='Sampo Trace',amount=10.0,type=['ultimate'])
        
        # Eidolons
        
        # Gear
        self.equipGear()
        
    def applyUltDebuff(self,team:list,rotationDuration:float):
        uptime = (2.0 / rotationDuration) * self.getTotalStat('SPD') / self.enemySpeed
        uptime = min(1.0, uptime)
        for character in team:
            character:BaseCharacter
            character.addStat('Vulnerability',description='ultimate',
                        amount=0.32 if self.eidolon >= 5 else 0.3,
                        type=['dot'],uptime=uptime)

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

    def useSkill(self):
        num_hits = 6.0 if self.eidolon >= 1 else 5.0
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill',type) * num_hits
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 15.0 + 15.0 * num_hits ) * self.getBreakEfficiency(type)
        retval.energy = ( 6.0 * num_hits + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        
        # assume we hit up to 3 enemies
        dotExplosion = self.useDot() * num_hits
        dotExplosion.damage *= 0.08 if self.eidolon >= 4 else 0.0
        retval += dotExplosion
        self.addDebugInfo(dotExplosion,['dot'],'Sampo Dot Explosion')
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useDot(self):
        retval = BaseEffect()
        type = ['dot']
        retval.damage = self.getTotalMotionValue('dote6',type) if self.eidolon >= 6 else self.getTotalMotionValue('dot',type)
        # no crits on dots
        retval.damage *= self.windshearStacks * self.windshearUptime
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.energy = self.getBonusEnergyAttack(type) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        return retval