from copy import copy
from settings.BaseConfiguration import Configuration
from baseClasses.RelicStats import RelicStats
from estimator.DefaultEstimator import DefaultEstimator
from visualizer.visualizer import visualize

from characters.erudition.Serval import Serval
from characters.destruction.Blade import Blade
from characters.hunt.DanHeng import DanHeng
from characters.hunt.Yanqing import Yanqing
from characters.nihility.Kafka import Kafka

from lightCones.destruction.ASecretVow import ASecretVow
from lightCones.erudition.TheSeriousnessOfBreakfast import TheSeriousnessOfBreakfast
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.nihility.Fermata import Fermata
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell

from relicSets.relicSets.BandOfSizzlingThunder import BandOfSizzlingThunder2pc, BandOfSizzlingThunder4pc
from relicSets.relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc, HunterOfGlacialForest4pc
from relicSets.relicSets.EagleOfTwilightLine import EagleOfTwilightLine2pc, EagleOfTwilightLine4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation

if __name__ == '__main__':
    CharacterDict = {} # store character information here
    EffectDict = {} # store dps metrics here
    
    # Reminder not to use this as a true DPS comparison
    # SP and Energy surplus/deficits are not balanced
    # I haven't spent time optimizing builds either
    # This is mostly just a tutorial to show you how to use the calculator
    
    config = copy(Configuration)
    config['numEnemies'] = 2
    config['enemySpeed'] = 132
    
    # Kafka
    KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['percAtk', 'flatSpd', 'percAtk', 'lighDmg'],
                            substats = {'EHR': 5, 'percAtk': 3, 'flatSpd': 12}),
                lightcone = GoodNightAndSleepWell(stacks=3,**config),
                relicsetone = BandOfSizzlingThunder2pc(), relicsettwo = BandOfSizzlingThunder4pc(), planarset = SpaceSealingStation(),
                **config)
    
    KafkaRotation = [
            KafkaCharacter.useSkill() * 3,
            KafkaCharacter.useTalent() * 3,
            KafkaCharacter.useUltimate(),
    ]
    DefaultEstimator('Kafka: 3E 3T 1Q', KafkaRotation, KafkaCharacter, config, CharacterDict, EffectDict)
    
    # Serval
    ServalCharacter = Serval(relicstats = RelicStats(mainstats = ['breakEffect', 'flatSpd', 'percAtk', 'lighDmg'],
                            substats = {'breakEffect': 10, 'percAtk': 8, 'flatSpd': 2}),
                lightcone = TheSeriousnessOfBreakfast(stacks=3,**config),
                relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SpaceSealingStation(),
                **config)
    
    ServalRotation = [
            ServalCharacter.useBasic(shocked=True),
            ServalCharacter.useSkill(shocked=True) * 2,
            ServalCharacter.useUltimate(shocked=True),
    ]
    DefaultEstimator('Serval: 1N 2E 1Q', ServalRotation, ServalCharacter, config, CharacterDict, EffectDict, breakDotMode='alwaysAll')
    
    # Dan Heng
    DanHengCharacter = DanHeng(relicstats = RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'windDmg'],
                            substats = {'CR': 10, 'CD': 10}),
                lightcone = CruisingInTheStellarSea(uptimeHP=0.5, uptimeDefeat=1.0, **config),
                relicsetone = EagleOfTwilightLine2pc(), relicsettwo=EagleOfTwilightLine4pc(), planarset = SpaceSealingStation(),
                talentUptime = 0.0,
                fasterThanLightUptime = 0.8,
                **config)
    
    DanHengRotation = [
            DanHengCharacter.useSkill() * 3,
            DanHengCharacter.useUltimate(slowed=True),
    ]
    DefaultEstimator('Dan Heng: 3E 1Q', DanHengRotation, DanHengCharacter, config, CharacterDict, EffectDict)
    
    #Yanqing
    YanqingCharacter = Yanqing(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CD', 'iceDmg'],
                            substats = {'percAtk': 8, 'CD': 12}),
                    lightcone = CruisingInTheStellarSea(uptimeHP=0.5, uptimeDefeat=1.0, **config),
                    relicsetone = HunterOfGlacialForest2pc(), relicsettwo = HunterOfGlacialForest4pc(), planarset = SpaceSealingStation(),
                    soulsteelUptime = 1.0,
                    searingStingUptime = 1.0,
                    rainingBlissUptime = 0.25,
                    **config)
    
    YanqingRotation = [
            YanqingCharacter.useSkill() * 4,
            YanqingCharacter.useTalent() * 5,
            YanqingCharacter.useUltimate(),
    ]
    DefaultEstimator('Yanqing: 4E 1Q 5T', YanqingRotation, YanqingCharacter, config, CharacterDict, EffectDict)
    
    # Blade
    bladeCharacter = Blade(RelicStats(mainstats = ['percHP', 'flatSpd', 'CD', 'windDmg'],
                            substats = {'CR': 7, 'CD': 7, 'flatSpd': 6}),
                lightcone = ASecretVow(uptime = 0.5, **config),
                relicsetone = LongevousDisciple2pc(),
                relicsettwo = LongevousDisciple4pc(),
                planarset = InertSalsotto(),
                hpLossTally=0.5,
                **config)
    
    BladeRotation = [ # 130 max energy
            bladeCharacter.useSkill() * 0.5, # 5 energy, 0.5 charges, only need half a usage per ult or so
            bladeCharacter.useEnhancedBasic() * 2, # 80 energy, 2 charge
            bladeCharacter.useTalent() * 0.9, # 30 energy, requires 5 charges if e0
            bladeCharacter.takeDamage(), # 10 energy, 1 charge, assume we get once
            bladeCharacter.useUltimate(), # 15 energy, 1 charge
    ]
    DefaultEstimator('Blade: 0.5S 2N 0.9T 1Q, get hit once', BladeRotation, bladeCharacter, config, CharacterDict, EffectDict)
        
    visualize(CharacterDict, EffectDict, **config)