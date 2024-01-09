from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Hanabi(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Hanabi')

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]

        # Talents
        self.addStat('BonusEnergyAttack', description='Hanabi Talent', amount=10, type=['basic'])

        # Eidolons
        
        # Gear
        self.equipGear()
        
    def applyTraceBuff(self, team:list, numQuantum:int=3):
        for character in team:
            character:BaseCharacter
            character.addStat('ATK.percent',description='Hanabi Trace',amount=0.15)
            character.addStat('DMG.quantum',description='Hanabi Trace',amount=0.3 if numQuantum >= 3 else 0.15 if numQuantum == 2 else 0.05)
            character.addStat('DMG',description='Hanabi Talent',amount=0.066 if self.eidolon >= 5 else 0.06, stacks=3)
            
    def applyUltBuff(self, team:list, uptime:float):
        for character in team:
            character:BaseCharacter
            character.addStat('DMG',description='Hanabi Ult',
                                amount=0.108 if self.eidolon >= 5 else 0.10,
                                stacks=3, uptime=uptime)
        
    def applySkillBuff(self,character:BaseCharacter,uptime:float):
        character.addStat('CD',description='Hanabi Skill',
                            amount=((0.396 * self.getTotalStat('CD') + 0.176) if self.eidolon >= 3 else (0.36 * self.getTotalStat('CD') + 0.16)),
                            uptime=uptime)
        
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
        retval.skillpoints = -1.0 + (0.5 if self.eidolon >= 1 else 0.0)
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.energy = 5.0 * self.getER(type)
        retval.skillpoints = 4.0
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval
    
    def useAdvanceForward(self, advanceAmount:float=0.5):
        retval = BaseEffect()
        retval.actionvalue = max(-0.5,-advanceAmount)
        self.addDebugInfo(retval,['Advance Forward'],'Hanabi Advance Forward')
        return retval