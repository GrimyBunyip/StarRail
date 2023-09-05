from copy import copy
from characters.destruction.Jingliu import Jingliu
from characters.hunt.Seele import Seele
from relicSets.relicSets.GeniusOfBrilliantStars import GeniusOfBrilliantStars2pc, GeniusOfBrilliantStars4pc
from settings.BaseConfiguration import Configuration
from baseClasses.RelicStats import RelicStats
from estimator.DefaultEstimator import DefaultEstimator
from visualizer.visualizer import visualize

from characters.destruction.Blade import Blade
from characters.destruction.Clara import Clara
from characters.hunt.DanHeng import DanHeng
from characters.nihility.Kafka import Kafka
from characters.destruction.Lunae import Lunae
from characters.erudition.Serval import Serval
from characters.hunt.Yanqing import Yanqing

from lightCones.destruction.ASecretVow import ASecretVow
from lightCones.erudition.TheSeriousnessOfBreakfast import TheSeriousnessOfBreakfast
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.nihility.Fermata import Fermata
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell

from relicSets.relicSets.BandOfSizzlingThunder import BandOfSizzlingThunder2pc, BandOfSizzlingThunder4pc
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.EagleOfTwilightLine import EagleOfTwilightLine2pc, EagleOfTwilightLine4pc
from relicSets.relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc, HunterOfGlacialForest4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.RutilantArena import RutilantArena
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
    
    # Clara
    ClaraCharacter = Clara(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'physDmg'],
                            substats = {'CR': 10, 'CD': 10}),
                lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=5.0, **config),
                relicsetone = ChampionOfStreetwiseBoxing2pc(),
                relicsettwo = ChampionOfStreetwiseBoxing4pc(),
                planarset = InertSalsotto(),
                hpLossTally=0.5,
                **config)
    
    ClaraRotation = [ # 110 max energy
            ClaraCharacter.useSkill() * 3,
            ClaraCharacter.useMarkOfSvarog() * 3, # these are 3 instances of single target bonus damage
            ClaraCharacter.useTalent(enhanced=False), # 1 additional clara hit on top
            ClaraCharacter.useTalent(enhanced=True) * 3, # 2 reactions from ultimate
            ClaraCharacter.useUltimate(),
    ]
    DefaultEstimator('Clara: 3E 3T 1Q', ClaraRotation, ClaraCharacter, config, CharacterDict, EffectDict)
    
    # Jingliu
    JingliuCharacter = Jingliu(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CD', 'iceDmg'],
                            substats = {'CR': 8, 'CD': 8, 'flatSpd': 4}),
                lightcone = ASecretVow(uptime = 0.5, **config),
                relicsetone = HunterOfGlacialForest2pc(),
                relicsettwo = HunterOfGlacialForest4pc(),
                planarset = RutilantArena(),
                transmigrationPercAtk=1.5,
                **config)
    
    JingliuRotation = [ # 140 max energy
            JingliuCharacter.useSkill() * 2, # 60 energy, 2 stack
            JingliuCharacter.useEnhancedSkill() * 3, # 60 energy, -3 stacks
            JingliuCharacter.useUltimate(), # 5 energy, 1 stack
            JingliuCharacter.extraTurn()*1.5,
    ]
    DefaultEstimator('Jingliu 2E 3Moon 1Q', JingliuRotation, JingliuCharacter, config, CharacterDict, EffectDict)
    
    # Lunae
    LunaeCharacter = Lunae(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'imagDmg'],
                            substats = {'CR': 8, 'CD': 9, 'flatSpd':3}),
                lightcone = OnTheFallOfAnAeon(uptime = 0.5, stacks=4.0, **config),
                relicsetone = WastelanderOfBanditryDesert2pc(),
                relicsettwo = WastelanderOfBanditryDesert4pc(),
                planarset = RutilantArena(),
                **config)
    
    LunaeRotation = [  # 140 energy needed
                LunaeCharacter.useSkill()*3,
                LunaeCharacter.useEnhancedBasic3(), # -3 SP, 40 energy
                LunaeCharacter.endTurn(),
                
                LunaeCharacter.useBasic(), # 1 SP, 20 energy
                LunaeCharacter.endTurn(),
                
                LunaeCharacter.useBasic(), # 1 SP, 20 energy
                LunaeCharacter.endTurn(),
                
                LunaeCharacter.useBasic(), # 1 SP, 20 energy
                LunaeCharacter.endTurn(),
                
                LunaeCharacter.useSkill()*3,
                LunaeCharacter.useEnhancedBasic3(), # -3 SP, 40 energy
                LunaeCharacter.useUltimate(), # +2 SP, 5 energy
                LunaeCharacter.endTurn()
    ]
    DefaultEstimator('Lunae: 3N 2N^3 1Q', LunaeRotation, LunaeCharacter, config, CharacterDict, EffectDict)
    
    # Lunae
    LunaeCharacter = Lunae(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'imagDmg'],
                            substats = {'CR': 8, 'CD': 9, 'flatSpd':3}),
                lightcone = OnTheFallOfAnAeon(uptime = 0.5, stacks=4.0, **config),
                relicsetone = WastelanderOfBanditryDesert2pc(),
                relicsettwo = WastelanderOfBanditryDesert4pc(),
                planarset = RutilantArena(),
                **config)
    
    LunaeRotation = [  # 140 energy needed
                LunaeCharacter.useSkill()*3,
                LunaeCharacter.useEnhancedBasic3(), # -3 SP, 40 energy
                LunaeCharacter.endTurn(),
                LunaeCharacter.useSkill()*3,
                LunaeCharacter.useEnhancedBasic3(), # -3 SP, 40 energy
                LunaeCharacter.endTurn(),
                
                LunaeCharacter.useSkill()*3,
                LunaeCharacter.useEnhancedBasic3(), # -3 SP, 40 energy
                LunaeCharacter.useUltimate(), # +2 SP, 5 energy
                LunaeCharacter.endTurn()
    ]
    DefaultEstimator('Lunae: 3N^3 1Q', LunaeRotation, LunaeCharacter, config, CharacterDict, EffectDict)
    
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
    
    # Seele
    SeeleCharacter = Seele(relicstats = RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'quanDmg'],
                            substats = {'CR': 10, 'CD': 10}),
                lightcone = CruisingInTheStellarSea(uptimeHP=0.5, uptimeDefeat=1.0, **config),
                relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo=GeniusOfBrilliantStars4pc(), planarset = SpaceSealingStation(),
                **config)
    
    SeeleRotation = [
            SeeleCharacter.useSkill() * 3,
            SeeleCharacter.useResurgence(),
            SeeleCharacter.useSkill(),
            SeeleCharacter.useUltimate(),
            SeeleCharacter.endTurn(),
    ]
    DefaultEstimator('Seele: 3E Resurgence(1E1Q)', SeeleRotation, SeeleCharacter, config, CharacterDict, EffectDict)
    
    SeeleRotation = [
            SeeleCharacter.useSkill() * 4,
            SeeleCharacter.useUltimate(),
    ]
    DefaultEstimator('Seele: 4 1Q No Resurgence', SeeleRotation, SeeleCharacter, config, CharacterDict, EffectDict)
    
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
        
    visualize(CharacterDict, EffectDict, **config)