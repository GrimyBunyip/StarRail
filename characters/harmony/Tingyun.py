from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Tingyun(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                benedictionTarget:BaseCharacter=None,
                speedUptime:float=1.0/3.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Tingyun')
        
        self.benedictionTarget = benedictionTarget
        self.speedUptime = speedUptime

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type=['basic'],area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]

        # Talents
        self.addStat('SPD.percent',description='trace',amount=0.20,uptime=self.speedUptime)
        self.addStat('DMG',description='trace',amount=0.40,type=['basic'])

        # Eidolons
        if self.eidolon >= 2:
            self.addStat('BonusEnergyTurn',description='trace',amount=5.0)
        
        # Gear
        self.equipGear()
        
    def useBasic(self):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        
        retval += self.useTalent()
        self.addDebugInfo(retval, type)
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.energy = ( 30.0 + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval, type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.energy = 5.0 * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval, type)
        return retval
    
    def useTalent(self):
        retval = BaseEffect()
        type = ['basic','talent']
        retval.damage = 0.66 if self.eidolon >= 5 else 0.6
        retval.damage *= self.benedictionTarget.getTotalStat('ATK',type,self.element)
        retval.damage *= self.benedictionTarget.getTotalCrit(type,self.element)
        retval.damage *= self.benedictionTarget.getDmg(type,self.element)
        retval.damage = self.benedictionTarget.applyDamageMultipliers(retval.damage,type,self.element)
        self.addDebugInfo(retval, type)
        return retval
    
    def useBenediction(self, type:list):
        retval = BaseEffect()
        retval.damage = self.benedictionTarget.getTotalStat('ATK',type,self.element) * (0.44 if self.eidolon >= 5 else 0.4)
        retval.damage *= self.benedictionTarget.getTotalCrit(type,self.element)
        retval.damage *= 1.0 + self.benedictionTarget.getTotalStat('DMG',type,self.element)
        retval.damage = self.benedictionTarget.applyDamageMultipliers(retval.damage,type,self.element)
        self.addDebugInfo(retval, type)
        return retval
    
    def giveUltEnergy(self):
        retval = BaseEffect()
        retval.energy = 60.0 if self.eidolon >= 6 else 50.0
        self.addDebugInfo(retval, type)
        return retval