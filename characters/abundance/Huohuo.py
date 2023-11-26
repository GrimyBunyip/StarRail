from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Huohuo(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Huohuo')

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='hp', value=0.5, eidolonThreshold=5, eidolonBonus=0.05)]

        # Talents

        # Eidolons
        # did not implement eidolons for huohuo
        
        # Gear
        self.equipGear()
        
    def applyUltBuff(self,team:list,uptime:float):
        for character in team:
            character:BaseCharacter
            character.addStat('ATK.percent',description='Huohuo Ult',
                              amount=0.432 if self.eidolon >= 3 else 0.40,
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
        
        retval += self.useTalent()
        return retval
    
    def giveUltEnergy(self,target:BaseCharacter):
        retval = BaseEffect()
        retval.energy = (0.21 if self.eidolon >= 3 else .20) * target.maxEnergy
        self.addDebugInfo(retval,['Huohuo Energy'],'Huohuo Ult Energy')
        return retval