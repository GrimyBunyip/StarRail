from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Moze(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                e4uptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Moze')
        self.e4uptime = e4uptime

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=1.5, eidolonThreshold=5, eidolonBonus=0.15)]
        self.motionValueDict['ultimate'] = [BaseMV(area='single', stat='atk', value=2.5, eidolonThreshold=3, eidolonBonus=0.2)]
        self.motionValueDict['additionalDamage'] = [BaseMV(area='single', stat='atk', value=0.3, eidolonThreshold=3, eidolonBonus=0.03)]
        self.motionValueDict['talent'] = [BaseMV(area='single', stat='atk', value=1.85 if self.eidolon >= 6 else 1.6, eidolonThreshold=3, eidolonBonus=0.16)]

        # Talents

        # Eidolons
        if self.eidolon >= 1:
            self.addStat('BonusEnergyAttack',description='Moze E1',amount=2,type=['additionalDamage'])
            
        if self.eidolon >= 4:
            self.addStat('DMG',description='Moze E4',amount=0.3,uptime=self.e4uptime)
        
        # Gear
        self.equipGear()
        
    def applyDebuff(self,team:list,uptime:float=0.5):
        for character in team:
            character:BaseCharacter
            character.addStat('Vulnerability',description='Moze Debuff',amount=0.25,type=['followup'],uptime=uptime)
        
        if self.eidolon >= 2:
            for character in team:
                character:BaseCharacter
                character.addStat('CD',description='Moze E2',amount=0.40,uptime=uptime)
        
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

    def useSkill(self, skillpoints:float=0.0, actionvalue:float=1.0):
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = skillpoints
        retval.actionvalue = actionvalue
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 90.0 * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useAdditionalDamage(self):
        retval = BaseEffect()
        type = ['additionalDamage']
        retval.damage = self.getTotalMotionValue('additionalDamage',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.energy = self.getBonusEnergyAttack(type) * self.getER(type)
        self.addDebugInfo(retval,type)
        return retval

    def useTalent(self):
        retval = BaseEffect()
        type = ['followup']
        retval.damage = self.getTotalMotionValue('talent',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 10.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval
