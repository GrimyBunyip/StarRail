from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Topaz(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                e1Stacks:float=2.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Topaz')
        
        self.e1Stacks = e1Stacks

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type=['basic','followup'],area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(type=['skill','followup'],area='single', stat='atk', value=1.5, eidolonThreshold=3, eidolonBonus=0.15)]
        self.motionValueDict['talent'] = [BaseMV(type=['ultimate','followup'],area='single', stat='atk', value=1.5, eidolonThreshold=5, eidolonBonus=0.15)]
        
        # Talents
        self.addStat('DMG',description='trace',amount=0.15) # Financial Turmoil
        self.addStat('Vulnerability',description='skill',amount=0.55 if self.eidolon >= 3 else 0.5)
        self.addStat('BonusEnergyAttack',description='trace',amount=10.0,type='windfall')
        
        self.addStat('DMG',description='windfall',
                     amount=1.65 if self.eidolon >= 5 else 1.5,
                     type='windfall')
        self.addStat('CD',description='windfall',amount=0.25,type='windfall')

        # Eidolons
        if self.eidolon >= 1:
            self.addStat('CD',description='e1',amount=0.25,type=['followup'],stacks=self.e1Stacks)
        if self.eidolon >= 2:
            self.addStat('BonusEnergyAttack',description='e2',amount=5.0,type=['talent'])
        if self.eidolon >= 4:
            self.addStat('AdvanceForward',description='e4',amount=0.2,type=['talent'])
        if self.eidolon >= 6:
            self.addStat('ResPen',description='e6',amount=0.10,type=['fire','windfall'])
        
        # Gear
        self.equipGear()
        
    def useBasic(self):
        retval = BaseEffect()
        type = ['basic','followup']
        retval.damage = self.getTotalMotionValue('basic')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useSkill(self):
        retval = BaseEffect()
        type = ['skill','followup']
        retval.damage = self.getTotalMotionValue('skill')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = ['ultimate']
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type)
        return retval

    def useTalent(self, windfall=False):
        retval = BaseEffect()
        type = ['talent','followup'] + ['windfall'] if windfall else []
        retval.damage = self.getTotalMotionValue('talent')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.getBreakEfficiency(type)
        retval.energy = self.getBonusEnergyAttack(type) * self.getER(type)
        retval.actionvalue = -0.2 if self.eidolon >= 4 else 0.0
        return retval
