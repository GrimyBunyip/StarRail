from copy import copy
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseEffect import BaseEffect
from baseClasses.BaseMV import BaseMV
from baseClasses.RelicSet import RelicSet
from baseClasses.RelicStats import RelicStats

class Yanqing(BaseCharacter):

  def __init__(self,
               relicstats:RelicStats,
               lightcone:BaseLightCone=None,
               relicsetone:RelicSet=None,
               relicsettwo:RelicSet=None,
               planarset:RelicSet=None,
               soulsteelUptime = 1.0,
               e4Uptime = 1.0,
               rainingBlissUptime = 0.25,
               **config):
    super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
    self.loadCharacterStats('Yanqing')

    self.soulsteelUptime = soulsteelUptime
    self.e4Uptime = e4Uptime
    self.rainingBlissUptime = rainingBlissUptime
    
    # Motion Values should be set before talents or gear
    self.motionValueDict['basic'] = [BaseMV(type='basic',area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1),
                                     BaseMV(type='basic',area='single', stat='atk', value=0.0, eidolonThreshold=1, eidolonBonus=0.6)]
    self.motionValueDict['skill'] = [BaseMV(type='skill',area='single', stat='atk', value=2.2, eidolonThreshold=3, eidolonBonus=0.22),
                                     BaseMV(type='skill',area='single', stat='atk', value=0.0, eidolonThreshold=1, eidolonBonus=0.6)]
    self.motionValueDict['ultimate'] = [BaseMV(type='ultimate',area='single', stat='atk', value=3.5, eidolonThreshold=5, eidolonBonus=0.28),
                                        BaseMV(type='ultimate',area='single', stat='atk', value=0.0, eidolonThreshold=1, eidolonBonus=0.6)]
    self.motionValueDict['talent'] = [BaseMV(type=['talent','followup'],area='single', stat='atk', value=0.5, eidolonThreshold=5, eidolonBonus=0.05)]
    
    # Talents
    self.ER += 0.10 * self.soulsteelUptime if self.eidolon >= 2 else 0.0
    self.resPen += 0.12 * self.e4Uptime if self.eidolon >= 4 else 0.0

    # Soulsteel
    self.CR += self.soulsteelUptime * ( 0.22 if self.eidolon >= 5 else 0.20 )
    self.CD += self.soulsteelUptime * ( 0.33 if self.eidolon >= 5 else 0.30 )
    self.CRType['bliss'] = 0.6 * self.rainingBlissUptime
    self.CDType['bliss'] = ( 0.54 if self.eidolon >= 5 else 0.5 ) * self.rainingBlissUptime
    
    # Bliss is always up for Ult
    self.CRType['blissUlt'] = 0.6
    self.CDType['blissUlt'] = 0.54 if self.eidolon >= 5 else 0.5
    self.percTaunt -= 0.6 * self.soulsteelUptime

    # Eidolons
    
    # Gear
    self.equipGear()
    #self.balanceCrit() do not balance crit on yanqing

  def useBasic(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('basic')
    retval.damage *= self.getTotalCrit(['basic','bliss'])
    retval.damage *= self.getTotalDmg('basic')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 20.0 + self.bonusEnergyType['basic'] ) * ( 1.0 + self.ER )
    retval.skillpoints = 1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['basic'])
    return retval

  def useSkill(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('skill')
    retval.damage *= self.getTotalCrit(['skill','bliss'])
    retval.damage *= self.getTotalDmg('skill')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergyType['skill'] ) * ( 1.0 + self.ER )
    retval.skillpoints = -1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
    return retval

  def useUltimate(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('ultimate')
    retval.damage *= self.getTotalCrit(['ultimate','blissUlt'])
    retval.damage *= self.getTotalDmg('ultimate')
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 90.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 5.0 + self.bonusEnergyType['ultimate'] ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['ultimate'])
    return retval

  def useTalent(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('talent')
    retval.damage *= self.getTotalCrit(['followup','talent','bliss'])
    retval.damage *= self.getTotalDmg(['followup','talent'])
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 10.0 + self.bonusEnergyType['talent'] + self.bonusEnergyType['followup'] ) * ( 1.0 + self.ER )
    retval.actionvalue = 0.0 - min(1.0,self.advanceForwardType['talent'] - self.advanceForwardType['followup'])
    
    procrate = 0.62 if self.eidolon >= 5 else 0.6
    retval *= procrate
    return retval