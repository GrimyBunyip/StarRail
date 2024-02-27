from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Kafka(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Kafka')
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(area='single', stat='atk', value=1.6, eidolonThreshold=3, eidolonBonus=0.16),
                                        BaseMV(area='adjacent', stat='atk', value=0.6, eidolonThreshold=3, eidolonBonus=0.06)]
        self.motionValueDict['dot'] = [BaseMV(area='single', stat='atk', value=2.90, eidolonThreshold=5, eidolonBonus=0.2828)]
        self.motionValueDict['ultimate'] = [BaseMV(area='all', stat='atk', value=0.8, eidolonThreshold=5, eidolonBonus=0.064)]
        self.motionValueDict['talent'] = [BaseMV(area='single', stat='atk', value=1.4, eidolonThreshold=5, eidolonBonus=0.196)]
        
        # Talents
        
        # Eidolons
        if self.eidolon >= 4:
            self.addStat('BonusEnergyAttack',description='Kafka e4',amount=2.0,type=['dot'])
        
        # Gear
        self.equipGear()
        
    def applyE1Debuff(self,team:list):
        if self.eidolon >= 1:
            uptime = 2.0 * self.getTotalStat('SPD') / self.enemySpeed / self.numEnemies
            uptime = min(1.0, uptime)
            for character in team:
                character:BaseCharacter
                character.addStat('Vulnerability',description='Kafka E1',
                            amount=0.30,uptime=uptime,type=['dot'])

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

    def useSkill(self, extraDots:list=None):
        num_adjacents = min( self.numEnemies - 1, 2 )
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 60.0 + 30.0 * num_adjacents ) * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        
        dotExplosion = self.useDot()
        if extraDots is not None:
            for extraDot in extraDots:
                dotExplosion += extraDot
        dotExplosion.damage *= 0.78 if self.eidolon >= 3 else 0.75
        dotExplosion.energy = 0.0
        dotExplosion.actionvalue = 0.0
        dotExplosion.skillpoints = 0.0
        self.addDebugInfo(dotExplosion,type,'Skill Dot Explosion')
        
        retval += dotExplosion
        return retval

    def useUltimate(self, extraDots:list=None):
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
        
        # assume breakDot single target, usualDot AOE
        dotExplosion = self.useDot() * self.numEnemies
        if extraDots is not None:
            for extraDot in extraDots:
                dotExplosion += extraDot
        dotExplosion.damage *= 1.0 if self.eidolon >= 5 else 1.04
        dotExplosion.energy = 0.0
        dotExplosion.actionvalue = 0.0
        dotExplosion.skillpoints = 0.0
        self.addDebugInfo(dotExplosion,type,'Ultimate Dot Explosion')
        
        retval += dotExplosion
        return retval

    def useTalent(self):
        retval = BaseEffect()
        type = ['talent','followup']
        retval.damage = self.getTotalMotionValue('talent',type)
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 10.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.skillpoints = 0.0
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useDot(self):
        retval = BaseEffect()
        type = ['dot']
        retval.damage = self.getTotalMotionValue('dot',type)
        # no crits on dots
        retval.damage *= self.getDmg(type) + (1.56 if self.eidolon >= 6 else 0.0)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.energy = self.getBonusEnergyAttack(type) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        return retval