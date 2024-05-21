from baseClasses.BaseCharacter import BREAK_MULTIPLIERS, BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class ImaginaryTrailblazer(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                overrideEidolon:int=6,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Imaginary Trailblazer')
        self.eidolon=overrideEidolon

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=0.5, eidolonThreshold=3, eidolonBonus=0.05)]

        # Talents

        # Eidolons
        
        # Gear
        self.equipGear()
        
    def applyE4Buff(self,team:list):
        for character in team:
            if character.name != self.name:
                character.addStat('BreakEffect',description='Imaginary Trailblazer E4',amount=0.15 * self.getTotalStat('BreakEffect'))
            
    def applyUltBuff(self,team:list, uptime=1.0):
        for character in team:
                character.addStat('BreakEffect',description='Imaginary Trailblazer Ultimate',
                                  amount=0.33 if self.eidolon >= 5 else 0.3,uptime=uptime)
                
    def useSuperBreak(self,character:BaseCharacter,baseGauge:float,extraTypes:list=[]):
        retval = BaseEffect()
        type = ['break','superBreak'] + extraTypes

        superBreakDamage = character.breakLevelMultiplier
        superBreakDamage *= baseGauge / 30.0
        superBreakDamage *= 1.7 - 0.1 * character.numEnemies # talent
        # superBreakDamage *= BREAK_MULTIPLIERS[character.element] # does not seem to scale off type
        superBreakDamage *= character.getBreakEffect(type)
        superBreakDamage *= character.getVulnerability(type)
        superBreakDamage = character.applyDamageMultipliers(superBreakDamage,type)

        retval.damage = superBreakDamage
        character.addDebugInfo(retval,type,f'Super Break Damage {character.name}')
        
        # factor in uptime
        retval *= character.weaknessBrokenUptime
        return retval
        

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
        numSkill = 7 if self.eidolon >= 6 else 5
        retval.damage = self.getTotalMotionValue('skill',type)
        retval.damage *= numSkill
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 15.0 * numSkill + 45.0 ) * self.getBreakEfficiency(type)
        retval.energy = ( 6.0 * numSkill + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval