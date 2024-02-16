from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class BlackSwan(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                sacramentStacks:float=7.0,
                candleflameBuff:float=0.72,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Black Swan')
        self.sacramentStacks = sacramentStacks
        self.candleflameBuff = min(0.72,candleflameBuff)
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=0.9, eidolonThreshold=3, eidolonBonus=0.09),
                                        BaseMV(area='adjacent', stat='atk', value=0.9, eidolonThreshold=3, eidolonBonus=0.09),]
        self.motionValueDict['ultimate'] = [BaseMV(area='all', stat='atk', value=1.20, eidolonThreshold=5, eidolonBonus=0.096)]
        self.motionValueDict['dot'] = [BaseMV(area='single', stat='atk', value=0.24+0.12*self.sacramentStacks, eidolonThreshold=3, eidolonBonus=0.24+0.012*self.sacramentStacks)]
        self.motionValueDict['dotAOE'] = [BaseMV(area='single', stat='atk', value=1.8 if self.sacramentStacks >= 3 else 0.0, eidolonThreshold=3, eidolonBonus=0.18 if self.sacramentStacks >= 3 else 0.0),]
        
        # Talents
        self.addStat('DMG',description='Black Swan Candleflame Buff',amount=self.candleflameBuff)
        if self.sacramentStacks >= 7:
            self.addStat('DefShred',description='Black Swan Sacrament Def Shred',amount=0.20,type='dotAOE')
        
        # Eidolons
        
        # Gear
        self.equipGear()
        
    def setSacramentStacks(self,sacramentStacks:float):
        self.sacramentStacks = sacramentStacks
        self.motionValueDict['dot'] = [BaseMV(area='single', stat='atk', value=0.24+0.12*self.sacramentStacks, eidolonThreshold=3, eidolonBonus=0.24+0.012*self.sacramentStacks)]
        self.motionValueDict['dotAOE'] = [BaseMV(area='single', stat='atk', value=0.24+0.12*self.sacramentStacks, eidolonThreshold=3, eidolonBonus=0.24+0.012*self.sacramentStacks),
                                        BaseMV(area='adjacent', stat='atk', value=1.8 if self.sacramentStacks >= 3 else 0.0, eidolonThreshold=3, eidolonBonus=0.18 if self.sacramentStacks >= 3 else 0.0),]
        
    def applySkillDebuff(self,team:list,rotationDuration:float):
        uptime = (3.0 / rotationDuration) * self.getTotalStat('SPD') / self.enemySpeed
        uptime = min(1.0, uptime)
        for character in team:
            character:BaseCharacter
            character.addStat('DefShred',description='Black Swan Skill',
                        amount=0.22 if self.eidolon >= 3 else 0.208,uptime=uptime)
        
    def applyUltDebuff(self,team:list,rotationDuration:float):
        uptime = (2.0 / rotationDuration) * self.getTotalStat('SPD') / self.enemySpeed
        uptime = min(1.0, uptime)
        for character in team:
            character:BaseCharacter
            character.addStat('Vulnerability',description='Black Swan Ultimate',
                        amount=0.27 if self.eidolon >= 3 else 0.25,uptime=uptime)

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
        average_num_adjacents = 2 * (self.numEnemies - 1) / self.numEnemies
        # 1 enemy = 0 / 1 adjacents per enemy
        # 2 enemy = 2 / 2 adjacent per enemy
        # 3 enemy = 4 / 3 adjacents per enemy
        # 4 enemy = 6 / 4 adjacents per enemy
        # 5 enemy = 8 / 5 adjacents per enemy
        retval.damage = self.getTotalMotionValue('dotAOE',type) * average_num_adjacents + self.getTotalMotionValue('dot',type)
        # no crits on dots
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.energy = self.getBonusEnergyAttack(type) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        return retval

    def useDotDetonation(self):
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