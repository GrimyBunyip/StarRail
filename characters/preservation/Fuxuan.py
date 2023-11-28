from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Fuxuan(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Fu Xuan')

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='hp', value=0.5, eidolonThreshold=5, eidolonBonus=0.05)]
        self.motionValueDict['ultimate'] = [BaseMV(area='all', stat='hp', value=1.0, eidolonThreshold=5, eidolonBonus=0.08)]
        self.motionValueDict['ultimateE6'] = [BaseMV(area='all', stat='hp', value=1.2)]

        # Talents
        self.addStat('BonusEnergyTurn',description='Fuxuan Trace',amount=20.0,type=['skill'])

        # Eidolons
        
        # Gear
        self.equipGear()
        
    def applySkillBuff(self, team:list, uptime:float=1.0):
        for character in team:
            character:BaseCharacter
            character.addStat('CR',description='Matrix of Presience',amount=0.132 if self.eidolon >= 3 else 0.12,uptime=uptime)
            character.addStat('HP.flat',description='Matrix of Presience',amount=(0.066 if self.eidolon >= 3 else 0.06) * self.getTotalStat('HP'),uptime=uptime)
            character.addStat('DmgReduction',description='Bleak Breeds Bliss',amount=0.196 if self.eidolon >= 3 else 0.18,uptime=uptime)
            if self.eidolon >= 1:
                character.addStat('CD',description='Fu Xuan e1',amount=0.30,uptime=uptime)
        
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
        retval = BaseEffect()
        type = ['skill']
        retval.energy = ( 30.0 + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval
        
    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate',type) + (self.getTotalMotionValue('ultimateE6',type) if self.eidolon >= 6 else 0.0)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        return retval