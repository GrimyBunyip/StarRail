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
               **config):
    super().__init__(lightcone=lightcone, relicstats=relicstats, relicsetone=relicsetone, relicsettwo=relicsettwo, planarset=planarset, **config)
    self.loadCharacterStats('Topaz')

    # Motion Values should be set before talents or gear
    self.motionValueDict['basic'] = [BaseMV(type=['basic','followup'],area='single', stat='atk', value=1.0, eidolonThreshold=3, eidolonBonus=0.1)]
    self.motionValueDict['skill'] = [BaseMV(type=['skill','followup'],area='single', stat='atk', value=1.5, eidolonThreshold=3, eidolonBonus=0.15)]
    self.motionValueDict['talent'] = [BaseMV(type=['ultimate','followup'],area='single', stat='atk', value=1.5, eidolonThreshold=5, eidolonBonus=0.15)]
    
    # Talents
    self.Dmg += 0.15 # Financial Turmoil
    self.DmgType['followup'] += 0.55 if self.eidolon >= 3 else 0.5
    self.DmgType['followup'] += 0.5 if self.eidolon >= 1 else 0.0
    self.DmgType['windfall'] = 1.65 if self.eidolon >= 5 else 1.5
    self.CRType['windfall'] = 0.0
    self.CDType['windfall'] = 0.25

    # Eidolons
    
    # Gear
    self.equipGear()
    
  def useBasic(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('basic')
    retval.damage *= self.getTotalCrit(['basic','followup'])
    retval.damage *= self.getTotalDmg(['basic','followup'])
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 30.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 20.0 + self.bonusEnergyAttack['basic'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
    retval.skillpoints = 1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['basic'])
    return retval

  def useSkill(self):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('skill')
    retval.damage *= self.getTotalCrit(['skill','followup'])
    retval.damage *= self.getTotalDmg(['skill','followup'])
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 30.0 + self.bonusEnergyAttack['skill'] + self.bonusEnergyAttack['turn'] ) * ( 1.0 + self.ER )
    retval.skillpoints = -1.0
    retval.actionvalue = 1.0 - min(1.0,self.advanceForwardType['skill'])
    return retval

  def useUltimate(self):
    retval = BaseEffect()
    retval.energy = ( 5.0 + self.bonusEnergyAttack['ultimate'] ) * ( 1.0 + self.ER )
    return retval

  def useTalent(self, windfall=False):
    retval = BaseEffect()
    retval.damage = self.getTotalMotionValue('talent')
    if windfall:
      retval.damage *= self.getTotalCrit(['talent','followup','windfall'])
      retval.damage *= self.getTotalDmg(['talent','followup','windfall'])
    else:
      retval.damage *= self.getTotalCrit(['talent','followup'])
      retval.damage *= self.getTotalDmg(['talent','followup'])
    retval.damage = self.applyDamageMultipliers(retval.damage)
    retval.gauge = 60.0 * (1.0 + self.breakEfficiency)
    retval.energy = ( 
                     ( 10.0 if windfall else 0.0 ) + 
                     ( 5.0 if self.eidolon >= 2 else 0.0 ) + 
                     self.bonusEnergyAttack['talent'] 
                    ) * ( 1.0 + self.ER )
    retval.actionvalue = -0.2 if self.eidolon >= 4 else 0.0
    return retval
