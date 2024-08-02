from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Jiaoqiu(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                ehr:float=1.4,
                talentStacks:float=5.0,
                eidolon:int=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Jiaoqiu')
        self.eidolon = self.eidolon if eidolon is None else eidolon
        self.ehr=ehr
        self.talentStacks = talentStacks
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=1.5, eidolonThreshold=3, eidolonBonus=0.15),
                                        BaseMV(area='adjacent', stat='atk', value=0.9, eidolonThreshold=3, eidolonBonus=0.09),]
        self.motionValueDict['ultimate'] = [BaseMV(area='all', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.08)]
        self.motionValueDict['dot'] = [BaseMV(area='single', stat='atk', value=4.8 if self.eidolon >= 2 else 1.8, eidolonThreshold=5, eidolonBonus=0.18)] # check this
        
        # Talents
        hearthKindle = min(2.4, 0.6*int((self.ehr-0.8)/0.15))
        self.addStat('ATK.percent',description='Jiaoqiu EHR to ATK talent',amount=hearthKindle)
        
        # Eidolons        
        # E2: The Ashen Roast state can be seen as a Burn state. Each stack of Ashen Roast will deal Fire DoT equal to 300% of Jiaoqiu's ATK at the start of the enemy's turn.
        # E4: When the Field exists, reduces enemy target's ATK by 15%.
        # E6: When the enemy target is defeated, existing Roast the Ash stacks will be transferred to a surviving enemy with the lowest amount of Roast the Ash stacks. Increases max Roast the Ash stacks to 9. Every stack of Roast the Ash will reduce all enemies' All-Type RES by 3%.

        # Gear
        self.equipGear()
        
    def applyTalentDebuff(self,team:list):
        roastBonus = 0.165 if self.eidolon >= 5 else 0.15
        roastBonus += (0.055 if self.eidolon >= 5 else 0.05) * (self.talentStacks - 1.0)
        for character in team:
            character:BaseCharacter
            character.addStat('Vulnerability',description='Ashen Roast',
                     amount=roastBonus,
                     )
            if self.eidolon >= 1:
                character.addStat('DMG', description='Jiaoqiu E1',
                                  amount=0.40)
        
    def applyUltDebuff(self,team:list,uptime:float=1.0):
        for character in team:
            character:BaseCharacter
            character.addStat('Vulnerability',description='Ashen Roast',
                     amount=0.162 if self.eidolon >= 5 else 0.15,
                     uptime=uptime,
                     type=['ultimate'])

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
        num_adjacent = min(2.0, self.numEnemies - 1.0)
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 60.0 + 30.0 * num_adjacent ) * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
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
        retval.gauge = 60.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useDot(self):
        retval = BaseEffect()
        type = ['dot']
        retval.damage = self.getTotalMotionValue('dot',type)
        # no crits on dots
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.energy = self.getBonusEnergyAttack(type) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        return retval