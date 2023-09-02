from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class BeforeTheTutorialMissionStarts(BaseLightCone):
  def __init__(self,
               uptime:float = 1.0,
               **config):
    self.loadConeStats('Before the Tutorial Mission Starts')
    self.setSuperposition(config)
    self.uptime=uptime

  def equipTo(self, char:BaseCharacter):
    self.addBaseStats(char)
    if char.path == 'nihility':
      char.EHR += 0.15 + 0.05 * self.superposition
      char.bonusEnergyBasic += ( 3.0+ 1.0 * self.superposition ) * self.uptime
      char.bonusEnergySkill += ( 3.0+ 1.0 * self.superposition ) * self.uptime
      char.bonusEnergyUlt += ( 3.0+ 1.0 * self.superposition ) * self.uptime
      char.bonusEnergyTalent += ( 3.0+ 1.0 * self.superposition ) * self.uptime
      
if __name__ == '__main__':
  from settings.BaseConfiguration import Configuration
  BeforeTheTutorialMissionStarts(**Configuration).print()