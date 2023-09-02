from copy import copy
from baseClasses.RelicStats import RelicStats
from characters.Serval import Serval, ServalEstimationV1
from characters.Blade import Blade, BladeEstimationsV1
from characters.DanHeng import DanHeng, DanHengEstimationV1
from characters.Yanqing import Yanqing, YanqingEstimationV1
from lightCones.destruction.ASecretVow import ASecretVow
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from relicSets.relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc, HunterOfGlacialForest4pc
from relicSets.relicSets.EagleOfTwilightLine import EagleOfTwilightLine2pc, EagleOfTwilightLine4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation
from settings.BaseConfiguration import Configuration
from visualizer.visualizer import visualize

if __name__ == '__main__':
    CharacterDict = {} # store character information here
    EffectDict = {} # store dps metrics here
    
    config = copy(Configuration)
    
    ServalCharacter = Serval(lightcone = CruisingInTheStellarSea(uptime = 0.5, **config),
                relicsetone = EagleOfTwilightLine2pc(),
                relicsettwo = EagleOfTwilightLine4pc(),
                planarset = SpaceSealingStation(),
                relicstats = RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'lighDmg'],
                            substats = {'CR': 10, 'CD': 10}),
                **config)
    
    ServalEstimationV1(ServalCharacter, Configuration, CharacterDict, EffectDict)
    
    DanHengCharacter = DanHeng(lightcone = CruisingInTheStellarSea(uptime = 0.5, **config),
                relicsetone = EagleOfTwilightLine2pc(),
                relicsettwo = EagleOfTwilightLine4pc(),
                planarset = SpaceSealingStation(),
                relicstats = RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'windDmg'],
                            substats = {'CR': 10, 'CD': 10}),
                talentUptime = 0.0,
                slowUptime = 1.0,
                fasterThanLightUptime = 1.0,
                **config)
    
    DanHengEstimationV1(DanHengCharacter, Configuration, CharacterDict, EffectDict)
    
    YanqingCharacter = Yanqing(CruisingInTheStellarSea(uptime = 0.5, **config),
                    HunterOfGlacialForest2pc(),
                    HunterOfGlacialForest4pc(),
                    SpaceSealingStation(),
                    RelicStats(mainstats = ['percAtk', 'flatSpd', 'CD', 'iceDmg'],
                            substats = {'percAtk': 8, 'CD': 12}),
                    soulsteelUptime = 1.0,
                    searingStingUptime = 1.0,
                    rainingBlissUptime = 0.25,
                    **config)
    
    YanqingEstimationV1(YanqingCharacter, Configuration, CharacterDict, EffectDict)

    bladeCharacter = Blade(ASecretVow(uptime = 0.5, **Configuration),
                LongevousDisciple2pc(),
                LongevousDisciple4pc(),
                InertSalsotto(),
                RelicStats(mainstats = ['percHP', 'flatSpd', 'CR', 'windDmg'],
                            substats = {'CR': 7, 'CD': 7, 'flatSpd': 6}),
                hpLossTally=0.5,
                **Configuration)
        
    BladeEstimationsV1(bladeCharacter, Configuration, CharacterDict, EffectDict)

    visualize(CharacterDict, EffectDict, Configuration)