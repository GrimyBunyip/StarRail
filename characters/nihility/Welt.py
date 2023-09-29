from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Welt(BaseCharacter):
    def __init__(self,
                relicstats:RelicStats,
                lightcone:BaseLightCone=None,
                relicsetone:RelicSet=None,
                relicsettwo:RelicSet=None,
                planarset:RelicSet=None,
                ultUptime:float=1.0,
                slowUptime:float=1.0,
                **config):
        super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
        self.loadCharacterStats('Welt')
        self.ultUptime = ultUptime
        self.slowUptime = slowUptime
        self.e6Count = 0
        
        # Motion Values should be set before talents or gear
        self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=5, eidolonBonus=0.1)]
        self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=0.72, eidolonThreshold=3, eidolonBonus=0.072)]
        self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='all', stat='atk', value=1.5, eidolonThreshold=5, eidolonBonus=0.12)]
        self.motionValueDict['talent'] = [BaseMV(type='talent',area='single', stat='atk', value=0.6, eidolonThreshold=5, eidolonBonus=0.06)]
        
        # Talents
        self.Vulnerability += 0.12 * self.ultUptime
        self.getBonusEnergyAttack(type) += 10.0
        self.Dmg += 0.20 * config['weaknessBrokenUptime']
        
        # Eidolons
        self.getBonusEnergyAttack(type) += 3.0 if self.eidolon >= 2 else 0.0
        
        # Gear
        self.equipGear()

    def useBasic(self):
        retval = BaseEffect()
        type = 'basic'
        retval.damage = self.getTotalMotionValue('basic')
        retval.damage *= 1.5 if self.eidolon >= 6 else 1.0
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 30.0 * self.getBreakEfficiency(type)
        retval.energy = ( 20.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = 1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        
        retval += self.useTalent() * self.slowUptime
        self.e6Count = max(0,self.e6Count-1)
        return retval

    def useSkill(self):
        num_hits = 4.0 if self.eidolon >= 6 else 3.0
        num_hits += 0.8 if self.eidolon >= 1 else 0.0
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('skill') * num_hits
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 90.0 * self.getBreakEfficiency(type)
        retval.energy = ( 30.0 + self.getBonusEnergyAttack(type) + self.getBonusEnergyTurn(type) ) * self.getER(type)
        retval.skillpoints = -1.0
        retval.actionvalue = 1.0 + self.getAdvanceForward(type)
        
        retval += self.useTalent() * num_hits * self.slowUptime
        self.e6Count = max(0,self.e6Count-1)
        return retval

    def useUltimate(self):
        retval = BaseEffect()
        type = 'ultimate'
        retval.damage = self.getTotalMotionValue('ultimate')
        retval.damage *= self.getTotalCrit(type)
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.gauge = 60.0 * self.numEnemies * self.getBreakEfficiency(type)
        retval.energy = ( 5.0 + self.getBonusEnergyAttack(type) ) * self.getER(type) # unclear if this bonus energy is affected by ER
        retval.actionvalue = self.getAdvanceForward(type)
        
        retval += self.useTalent() * self.numEnemies * self.slowUptime
        self.e6Count += 2
        return retval

    def useTalent(self):
        retval = BaseEffect()
        retval.damage = self.getTotalMotionValue('talent')
        retval.damage *= self.getTotalCrit(type) # hmm, is this additive MV? fix this later
        retval.damage *= self.getDmg(type)
        retval.damage *= self.getVulnerability(type)
        retval.damage = self.applyDamageMultipliers(retval.damage,type)
        retval.energy = self.getBonusEnergyAttack(type) * self.getER(type) # unclear if this bhonus energy is affected by ER
        return retval