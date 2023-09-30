from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Sushang(BaseCharacter):

    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                weaknessBrokenUptime:float = 0.5,
                weaknessBrokenStacks:float=2.0,
                ripostedStacks:float=10.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Sushang')
        
        self.weaknessBrokenUptime = weaknessBrokenUptime
        self.weaknessBrokenStacks = weaknessBrokenStacks
        self.riposteStacks = ripostedStacks
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type=['basic'],area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(type=['skill'],area='single', stat='atk', value=2.1, eidolonThreshold=3, eidolonBonus=0.21)]
        self.motionValueDict['swordStance'] = [BaseMV(type=['skill','swordStance'],area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['ultimate'] = [BaseMV(type=['ultimate'],area='single', stat='atk', value=3.2, eidolonThreshold=5, eidolonBonus=0.256)]
        
        # Talents
        self.addStat('SPD.percent',description='talent',
                     amount=0.21 if self.eidolon >= 5 else 0.2,
                     stacks=weaknessBrokenStacks if self.eidolon >= 6 else 1.0,
                     uptime=self.weaknessBrokenUptime)
        self.addStat('DMG',description='trace',amount=0.0249999996740371,type=['swordStance'],stacks=self.riposteStacks)
        self.addStat('AdvanceForward',description='trace',amount=0.15,type=['basic'],uptime=self.weaknessBrokenUptime)
        self.addStat('AdvanceForward',description='trace',amount=0.15,type=['skill'],uptime=self.weaknessBrokenUptime)
        self.addStat('AdvanceForward',description='ultimate',amount=1.0,type=['ultimate'])

        # Eidolons
        if self.eidolon >= 2:
            self.addStat('DmgReduction',description='e2',amount=0.2)
        if self.eidolon >= 4:
            self.addStat('BreakEffect',description='e4',amount=0.40)
        
        # Gear
        self.equipGear()

    def useBasic(self):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic')
        retval.damage *= self.getTotalCrit(['basic'])
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.endTurn()
        self.addDebugInfo(retval, type)
        return retval

    def useSkill(self):
        stanceChance = self.weaknessBrokenUptime + (1.0 - self.weaknessBrokenUptime) * 0.33
        
        ultBuffDuration = self.getTempBuffDuration('ultimate')
        if ultBuffDuration is not None and self.getTempBuffDuration('ultimate') > 0.0:
            stanceChance *= 2 # 2 more chances at half damage, is essentially 1 more full chance
        
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0 + (self.weaknessBrokenUptime if self.eidolon >= 1 else 0.0)
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        
        retval += stanceChance * self.useSwordStance()
        
        self.endTurn()
        self.addDebugInfo(retval, type)
        return retval

    def useSwordStance(self):
        retval = BaseEffect()
        type = ['skill','swordStance']
        retval.damage = self.getTotalMotionValue('swordStance')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        self.addDebugInfo(retval, type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.damage = self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit(['ultimate'])
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 90.0 * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        
        self.addTempStat('ATK.percent',description='ultimate',
                         amount=0.324 if self.eidolon >= 5 else 0.3,
                         duration=2)
        self.addDebugInfo(retval, type)
        return retval

    def useTalent(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('talent')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 10.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = 0.0 - self.getAdvanceForward(type)
        self.addDebugInfo(retval, type)
        return retval
        