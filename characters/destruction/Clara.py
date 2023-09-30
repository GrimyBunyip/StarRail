from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats
from baseClasses.BaseMV import BaseMV

class Clara(BaseCharacter):

    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                aTightEmbraceUptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Clara')
        
        self.aTightEmbraceUptime = aTightEmbraceUptime

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type=['basic'],area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(type=['skill'],area='all', stat='atk', value=1.2, eidolonThreshold=3, eidolonBonus=0.12)]
        
        self.motionValueDict['markOfSvarog'] = [BaseMV(type=['skill'],area='single', stat='atk', value=1.2, eidolonThreshold=3, eidolonBonus=0.12)]
        
        #I believe the revenge ascension is an MV buff
        self.motionValueDict['talent'] = [BaseMV(type=['talent','followup'],area='single', stat='atk', value=1.6, eidolonThreshold=5, eidolonBonus=0.16)]        
        
        # Talents
        self.addStat('DMG',description='trace',type=['followup'],amount=0.3)
        
        # Eidolons
        # handle handle e1 manually, by using the argument in the useSkill call
        if self.eidolon >= 2.0:
            self.addStat('ATK.percent',description='e2',amount=0.30,uptime=self.aTightEmbraceUptime)
        # better to handle e6 manually

        # Gear
        self.equipGear()

    def useBasic(self):
        retval = BaseEffect()
        type = ['basic']
        retval.damage = self.getTotalMotionValue('basic')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type)) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('skill')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useMarkOfSvarog(self):
        retval = BaseEffect()
        type = ['skill']
        retval.damage = self.getTotalMotionValue('markOfSvarog')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        self.addDebugInfo(retval,type,'Mark of Svarog Damage')
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = self.getAdvanceForward(type)
        self.addDebugInfo(retval,type)
        return retval

    def useTalent(self, enhanced=False):
        num_adjacent = min(2, self.numEnemies-1)
        retval = BaseEffect()
        type = ['followup','talent']
        retval.damage = self.getTotalMotionValue('talent')
        retval.damage *= ( 1.0 + num_adjacent / 2.0 ) if enhanced else 1.0        
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type) + ( (1.728 if self.eidolon >= 5 else 1.6) if enhanced else 0.0)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = ( 30.0 + ( 30.0 * num_adjacent if enhanced else 0.0 ) ) * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        retval.actionvalue = 0.0 - self.getAdvanceForward(type)
        self.addDebugInfo(retval,type,'Clara Talent {}'.format('enhanced' if enhanced else ''))
        return retval