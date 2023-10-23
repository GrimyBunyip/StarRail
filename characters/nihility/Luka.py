from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Luka(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                ultDebuffUptime:float=1.0,
                bleedUptime:float=1.0,
                e2uptime:float=1.0,
                e4stacks:float=4.0,
                e4uptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Luka')
        self.ultDebuffUptime = ultDebuffUptime
        self.bleedUptime = bleedUptime
        self.e2uptime = e2uptime
        self.e4stacks = e4stacks
        self.e4uptime = e4uptime
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        
        crushMV = 0.8 + 0.2 * 3 * 1.5 # Crush Fighting Will
        self.motionValueDict['enhancedBasic'] = [BaseMV(area='single', stat='atk', value=crushMV, eidolonThreshold=5, eidolonBonus=crushMV/10)]

        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=1.2, eidolonThreshold=3, eidolonBonus=0.12)]
        self.motionValueDict['dot'] = [BaseMV(area='single', stat='atk', value=3.38, eidolonThreshold=3, eidolonBonus=0.338)]

        self.motionValueDict['ultimate'] = [BaseMV(area='single', stat='atk', value=3.3, eidolonThreshold=5, eidolonBonus=0.264)]
        
        # Talents
        self.addStat('Vulnerability',description='ultimate',
                     amount=0.216 if self.eidolon >= 5 else 0.2,
                     uptime=self.ultDebuffUptime / self.numEnemies)
        
        self.addStat('BonusEnergyAttack',description='trace',amount=6.0,type=['ultimate'])
        self.addStat('BonusEnergyAttack',description='trace',amount=3.0,type=['basic'])
        self.addStat('BonusEnergyAttack',description='trace',amount=-3.0,type=['enhancedBasic']) # enhanced basic does not proc cycle braking
        self.addStat('BonusEnergyAttack',description='trace',amount=3.0,type=['skill'])
        self.addStat('BonusEnergyAttack',description='trace',amount=3.0,type=['skill'],uptime=self.e2uptime)
        
        # Eidolons
        if self.eidolon >= 1:
            self.addStat('DMG',description='e1',amount=0.15,uptime=self.bleedUptime)
        if self.eidolon >+ 4:
            self.addStat('ATK.percent',description='e4',amount=0.05,stacks=self.e4stacks,uptime=self.e4uptime)
        
        # Gear
        self.equipGear()

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
        retval = BaseEffect()
        type = ['basic','enhancedBasic']
        retval.damage = self.getTotalMotionValue('enhancedBasic',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type) # enhanced basic doesn't benefit from cycle braking, change energy tag here
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type,'Luka Enhanced Basic')
        
        dotExplosion = self.useDot()
        dotExplosion.damage *= ( 0.884 if self.eidolon >= 3 else 0.85 ) + ( 0.08 * 3 * 1.5 if self.eidolon >= 6 else 0.0 )
        retval += dotExplosion
        self.addDebugInfo(dotExplosion,['dot'],'Luka Dot Explosion')
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
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
        retval.gauge = 90.0 * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useDot(self):
        bleedHP = self.enemyMaxHP * 0.24
        retval = BaseEffect()
        type = ['dot']
        retval.damage = min(bleedHP, self.getTotalMotionValue('dot',type))
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        return retval