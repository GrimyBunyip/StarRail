from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class RuanMei(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Ruan Mei')
        self.baseEnemySpeed = config['enemySpeed']
        self.baseWeaknessBrokenUptime = config['weaknessBrokenUptime']

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]

        # Talents
        self.addStat('BonusEnergyTurn',description='Ruan Mei Trace',amount=5.0)

        # Eidolons
        
        # Gear
        self.equipGear()
        
    def applyWeaknessModifiers(self,team:list,enemyTurnsPerBreak:float=2.0):
        # estimate weakness break uptime assuming we break every 2 enemy turns
        for character in team:
            character:BaseCharacter
            character.enemySpeed = self.baseEnemySpeed * enemyTurnsPerBreak / (enemyTurnsPerBreak + 0.25 + 0.10 + 0.20 * self.getTotalStat('BreakEffect'))
            character.weaknessBrokenUptime = 1.0 - (1.0 - self.baseWeaknessBrokenUptime) * (enemyTurnsPerBreak + 0.25) / (enemyTurnsPerBreak + 0.25 + 0.10 + 0.20 * self.getTotalStat('BreakEffect') )
                
    def applyPassiveBuffs(self,team:list):
        for character in team:
            character:BaseCharacter
            character.addStat('BreakEffect',description='Ruan Mei Trace',amount=0.20)
            character.addStat('DMG',description='Ruan Mei Trace',
                              amount=max(0.0,min(0.36,(self.getTotalStat('BreakEffect')-1.20) * 0.60)),
                              uptime=self.weaknessBrokenUptime)
            if character.name != 'Ruan Mei;':
                character.addStat('SPD.percent',description='talent',amount=0.104 if self.eidolon >= 3 else 0.10)
             
    def applyUltBuff(self,team:list,uptime:float):
        for character in team:
            character:BaseCharacter
            character.addStat('ResPen', description='Ruan Mei Ult', 
                              amount=0.27 if self.eidolon >= 3 else 0.25, uptime=uptime)
        
    def applySkillBuff(self,team:list,uptime:float):
        for character in team:
            character:BaseCharacter
            character.addStat('DMG',description='Ruan Mei Skill',
                                amount=0.3528 if self.eidolon >= 5 else 0.32,
                                uptime=uptime)
            character.addStat('BreakEfficiency',description='Ruan Mei Skill',
                                amount=0.50, uptime=uptime)
        
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
        retval.energy = 30.0 * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.energy = 5.0 * self.getER(type)
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        breakEffect = self.useBreak()
        retval.damage = (0.54 if self.eidolon >= 3 else 0.50) * breakEffect.damage
        self.addDebugInfo(retval,type)
        return retval
    
    def useTalent(self):
        retval = BaseEffect()
        type = ['talent']
        breakEffect = self.useBreak() # scale the damage to the weakness break uptime
        retval.damage = (1.32 if self.eidolon >= 3 else 1.2) * breakEffect.damage * self.weaknessBrokenUptime
        self.addDebugInfo(retval,type)
        return retval