from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Lynx(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Lynx')

        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]

        # Talents

        # Eidolons
        
        # Gear
        self.equipGear()
        
    def applySkillBuff(self,character:BaseCharacter,uptime:float):
        character.addStat('HP.flat',description='Lynx E6',
                            amount=(self.getTotalStat('HP') * 0.08 + 223) if self.eidolon >= 3 else (self.getTotalStat('HP') * 0.075 + 200),
                            uptime=min(1.0,uptime))
        character.addStat('Taunt.percent',description='Lynx Skill Taunt Boost',amount=5.0,uptime=min(1.0,2.0*uptime))
        if self.eidolon >= 4:
            atkBuff = self.getTotalStat('HP') * 0.03
            character.addStat('ATK.flat',description='Lynx E6',amount=atkBuff,uptime=min(1.0,uptime))
        if self.eidolon >= 6:
            character.addStat('HP.flat',description='Lynx E6',amount=self.getTotalStat('HP') * 0.06,uptime=min(1.0,uptime))
        
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