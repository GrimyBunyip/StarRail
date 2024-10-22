from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Fugue(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Fugue')
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['enhancedBasic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1),
                                                 BaseMV(area='adjacent', stat='atk', value=0.5, eidolonThreshold=3, eidolonBonus=0.05),]
        self.motionValueDict['ultimate'] = [BaseMV(area='all', stat='atk', value=2.0, eidolonThreshold=5, eidolonBonus=0.20)]
        
        # Talents
        
        # Eidolons
        
        # Gear
        self.equipGear()
        
        # Team Buffs
        def applyDefShred(team:list):
            for character in team:
                character:BaseCharacter
                character.addStat('DefShred', description='Fugue Def Shred', 
                                amount=0.20 if self.eidolon >= 3 else 0.18)
                
        def applySelfBuff(team:list):
            self.addStat('BreakEffect', description='Fugue Self Buff Trace', amount=0.30)
            
        def applyTeamBuff(team:list):
            for character in team:
                character:BaseCharacter
                character.addStat('BreakEffect', description='Fugue Team Buff Trace', amount=0.15)
                    
        self.teamBuffList.append(applyDefShred)
        self.teamBuffList.append(applySelfBuff)
        self.teamBuffList.append(applyTeamBuff)
        
    def applySkillBuff(self,character:BaseCharacter,uptime:float=1.0):
        character.addStat('BreakEffect',description='Fugue Skill',
                        amount=0.44 if self.eidolon >= 3 else 0.40,
                        uptime=uptime)
        if self.eidolon >= 1:
            character.addStat('BreakEfficiency', description='Fugue E1', amount=0.5)

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

    def useEnhancedBasic(self):
        num_adjacent = min(2.0, self.numEnemies - 1.0)
        retval = BaseEffect()
        type = ['basic','enhancedBasic']
        retval.damage = self.getTotalMotionValue('basic',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 30.0 + 15.0 * num_adjacent ) * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate',type) + (self.getTotalMotionValue('e6',type) * self.numEnemies if self.eidolon >= 6 else 0.0)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type) # unclear if this bonus energy is affected by ER
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval
                
    def useSuperBreak(self,character:BaseCharacter,baseGauge:float,extraTypes:list=[]):
        retval = BaseEffect()
        type = ['break','superBreak'] + extraTypes

        superBreakDamage = character.breakLevelMultiplier
        superBreakDamage *= baseGauge / 30.0
        superBreakDamage *= 1.0 # talent
        # superBreakDamage *= BREAK_MULTIPLIERS[character.element] # does not seem to scale off type
        superBreakDamage *= character.getBreakEffect(type)
        superBreakDamage *= character.getVulnerability(type)
        superBreakDamage = character.applyDamageMultipliers(superBreakDamage,type)

        retval.damage = superBreakDamage
        # factor in uptime
        retval *= character.weaknessBrokenUptime
        character.addDebugInfo(retval,type,f'Super Break Damage {character.name}')
        
        return retval