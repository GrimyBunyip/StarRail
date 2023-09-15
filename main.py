from copy import copy

import numpy as np
from settings.BaseConfiguration import Configuration
from baseClasses.RelicStats import RelicStats
from estimator.DefaultEstimator import DefaultEstimator
from visualizer.visualizer import visualize

from characters.destruction.Blade import Blade
from characters.destruction.Clara import Clara
from characters.hunt.DanHeng import DanHeng
from characters.erudition.Himeko import Himeko
from characters.destruction.Hook import Hook
from characters.destruction.Jingliu import Jingliu
from characters.erudition.JingYuan import JingYuan
from characters.nihility.Kafka import Kafka
from characters.destruction.Lunae import Lunae
from characters.nihility.Sampo import Sampo
from characters.hunt.Seele import Seele
from characters.erudition.Serval import Serval
from characters.hunt.Topaz import Topaz
from characters.erudition.Qingque import Qingque
from characters.hunt.Yanqing import Yanqing

from lightCones.destruction.ASecretVow import ASecretVow
from lightCones.destruction.BrighterThanTheSun import BrighterThanTheSun
from lightCones.destruction.IShallBeMyOwnSword import IShallBeMyOwnSword
from lightCones.destruction.NowhereToRun import NowhereToRun
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.destruction.SomethingIrreplaceable import SomethingIrreplaceable
from lightCones.destruction.TheMolesWelcomeYou import TheMolesWelcomeYou
from lightCones.destruction.TheUnreachableSide import TheUnreachableSide
from lightCones.destruction.UnderTheBlueSky import UnderTheBlueSky
from lightCones.destruction.WoofWalkTime import WoofWalkTime

from lightCones.erudition.BeforeDawn import BeforeDawn
from lightCones.erudition.GeniusesRepose import GeniusesRepose
from lightCones.erudition.MakeTheWorldClamor import MakeTheWorldClamor
from lightCones.erudition.NightOnTheMilkyWay import NightOnTheMilkyWay
from lightCones.erudition.TheBirthOfTheSelf import TheBirthOfTheSelf
from lightCones.erudition.TheSeriousnessOfBreakfast import TheSeriousnessOfBreakfast
from lightCones.erudition.TodayIsAnotherPeacefulDay import TodayIsAnotherPeacefulDay

from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.InTheNight import InTheNight
from lightCones.hunt.OnlySilenceRemains import OnlySilenceRemains
from lightCones.hunt.ReturnToDarkness import ReturnToDarkness
from lightCones.hunt.RiverFlowsInSpring import RiverFlowsInSpring
from lightCones.hunt.SleepLikeTheDead import SleepLikeTheDead
from lightCones.hunt.Swordplay import Swordplay
from lightCones.hunt.WorrisomeBlissful import WorrisomeBlissful

from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.nihility.EyesOfThePrey import EyesOfThePrey
from lightCones.nihility.Fermata import Fermata
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.InTheNameOfTheWorld import InTheNameOfTheWorld
from lightCones.nihility.IncessantRain import IncessantRain
from lightCones.nihility.PatienceIsAllYouNeed import PatienceIsAllYouNeed
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from lightCones.nihility.SolitaryHealing import SolitaryHealing
from lightCones.nihility.WeWillMeetAgain import WeWillMeetAgain

from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from lightCones.preservation.LandausChoice import LandausChoice
from lightCones.preservation.MomentOfVictory import MomentOfVictory
from lightCones.preservation.SheAlreadyShutHerEyes import SheAlreadyShutHerEyes
from lightCones.preservation.TextureOfMemories import TextureOfMemories
from lightCones.preservation.ThisIsMe import ThisIsMe
from lightCones.preservation.TrendOfTheUniversalMarket import TrendOfTheUniversalMarket
from lightCones.preservation.WeAreWildfire import WeAreWildfire

from relicSets.relicSets.BandOfSizzlingThunder import BandOfSizzlingThunder2pc, BandOfSizzlingThunder4pc
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.EagleOfTwilightLine import EagleOfTwilightLine2pc, EagleOfTwilightLine4pc
from relicSets.relicSets.FiresmithOfLavaForging import FiresmithOfLavaForging2pc, FiresmithOfLavaForging4pc
from relicSets.relicSets.GeniusOfBrilliantStars import GeniusOfBrilliantStars2pc, GeniusOfBrilliantStars4pc
from relicSets.relicSets.GuardOfWutheringSnow import GuardOfWutheringSnow2pc
from relicSets.relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc, HunterOfGlacialForest4pc
from relicSets.relicSets.KnightOfPurityPalace import KnightOfPurityPalace2pc, KnightOfPurityPalace4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc, MusketeerOfWildWheat4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

from relicSets.planarSets.BelobogOfTheArchitects import BelobogOfTheArchitects
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.CelestialDifferentiator import CelestialDifferentiator
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.PanCosmicCommercialEnterprise import PanCosmicCommercialEnterprise
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.planarSets.TaliaKingdomOfBanditry import TaliaKingdomOfBanditry

if __name__ == '__main__':
    CharacterDict = {} # store character information here
    EffectDict = {} # store dps metrics here
    
    # Reminder not to use this as a true DPS comparison
    # SP and Energy surplus/deficits are not balanced
    # I haven't spent time optimizing builds either
    # This is mostly just a tutorial to show you how to use the calculator
    
    config = copy(Configuration)
    config['numEnemies'] = 2
    config['enemySpeed'] = 132 / 1.125 # assume 25% action delay every 2 enemy turns from toughness break
    
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
    
    DefaultEstimator('Kafka: 3E 3T 1Q', KafkaRotation, KafkaCharacter, config, CharacterDict, EffectDict, dotMode='alwaysAll')
    
    # Blade
    bladeCharacter = Blade(RelicStats(mainstats = ['percHP', 'flatSpd', 'CD', 'windDmg'],
                            substats = {'CR': 10, 'CD': 4, 'flatSpd': 6}),
                lightcone = ASecretVow(uptime = 0.5, **config),
                relicsetone = LongevousDisciple2pc(),
                relicsettwo = LongevousDisciple4pc(),
                planarset = InertSalsotto(),
                hpLossTally=1.0,
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
                **config)
    
    ClaraRotation = [ # 110 max energy
            ClaraCharacter.useSkill() * 2.5,
            ClaraCharacter.useMarkOfSvarog() * 2.5, # these are 3 instances of single target bonus damage
            ClaraCharacter.useTalent(enhanced=False), # 1 additional clara hit on top
            ClaraCharacter.useTalent(enhanced=True) * 2, # 2 reactions from ultimate
            ClaraCharacter.useUltimate(),
    ]
    # 2.5E as clara probably can't consistently pull off a 2E rotation depending on how much
    # energy enemies give when they hit her
    DefaultEstimator('Clara: 2.5E 3T 1Q', ClaraRotation, ClaraCharacter, config, CharacterDict, EffectDict)

    # Lunae
    LunaeCharacter = Lunae(RelicStats(mainstats = ['percAtk', 'percAtk', 'CR', 'imagDmg'],
                            substats = {'CR': 10, 'CD': 10}),
                lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=4.0, **config),
                relicsetone = MusketeerOfWildWheat2pc(),
                relicsettwo = MusketeerOfWildWheat4pc(),
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
                lightcone = TheSeriousnessOfBreakfast(**config),
                relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SpaceSealingStation(),
                **config)
    
    ServalRotation = [
            ServalCharacter.useBasic(shocked=True),
            ServalCharacter.useSkill(shocked=True) * 2,
            ServalCharacter.useUltimate(shocked=True),
    ]
    DefaultEstimator('Serval: 1N 2E 1Q', ServalRotation, ServalCharacter, config, CharacterDict, EffectDict, breakDotMode='alwaysAll', dotMode='alwaysAll')
    
    # Jing Yuan
    JingYuanCharacter = JingYuan(relicstats = RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'lighDmg'],
                            substats = {'CD': 12, 'CR': 1, 'flatSpd': 7}),
                lightcone = TheSeriousnessOfBreakfast(stacks=3,**config),
                relicsetone = BandOfSizzlingThunder2pc(), relicsettwo = BandOfSizzlingThunder4pc(), planarset = InertSalsotto(),
                **config)
    
    numSkills = 4
    numUltimates = 1
    ''' Formula we can use, but it's admittedly very generous. Easier to use the 140 speed estimate for solo.
    jingSpeed = JingYuanCharacter.getTotalSpd()
    # estimate lord's max speed given this rotation
    lordBaseSpeed = 0.6
    lordBonusSpeed = 0.1
    lordSpeed = 100.0 * ( lordBaseSpeed + np.sqrt(lordBaseSpeed * lordBaseSpeed + 4 * lordBonusSpeed * (2 * numSkills + 3 * numUltimates) / numSkills ) ) / 2
    
    numTalents = ( 3 * numSkills * lordSpeed / jingSpeed )  + 2 * numSkills + 3 * numUltimates'''
    
    numTalents = ( 3 * numSkills / 2 )  + 2 * numSkills + 3 * numUltimates
    
    JingYuanRotation = [
            JingYuanCharacter.useSkill() * numSkills, # 4 * 2 lord actions
            JingYuanCharacter.useUltimate() * numUltimates, # 3 lord actions
            JingYuanCharacter.useTalent() * numTalents, # hits generated from skill and ultimate
    ]
    DefaultEstimator('JingYuan: 4E 1Q 17T', JingYuanRotation, JingYuanCharacter, config, CharacterDict, EffectDict)
    
    # Seele
    SeeleCharacter = Seele(relicstats = RelicStats(mainstats = ['percAtk', 'percAtk', 'CD', 'quanDmg'],
                            substats = {'CR': 17, 'CD': 3}),
                lightcone = CruisingInTheStellarSea(uptimeHP=0.5, **config),
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
    DefaultEstimator('Seele: 4E 1Q No Resurgence', SeeleRotation, SeeleCharacter, config, CharacterDict, EffectDict)
    
    # Dan Heng
    DanHengCharacter = DanHeng(relicstats = RelicStats(mainstats = ['percAtk', 'flatSpd', 'CD', 'windDmg'],
                            substats = {'CR': 14, 'CD': 6}),
                lightcone = CruisingInTheStellarSea(uptimeHP=0.5, **config),
                relicsetone = EagleOfTwilightLine2pc(), relicsettwo=EagleOfTwilightLine4pc(), planarset = SpaceSealingStation(),
                talentUptime = 0.0,
                fasterThanLightUptime = 0.8,
                e1Uptime=0.5,
                **config)
    
    DanHengRotation = [
            #DanHengCharacter.useBasic(slowed=True) * 2,
            DanHengCharacter.useSkill() * 3,
            DanHengCharacter.useUltimate(slowed=True),
    ]
    DefaultEstimator('Dan Heng: 3E 1Q', DanHengRotation, DanHengCharacter, config, CharacterDict, EffectDict)
    
    #Yanqing
    YanqingCharacter = Yanqing(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CD', 'iceDmg'],
                            substats = {'percAtk': 8, 'CD': 12}),
                    lightcone = CruisingInTheStellarSea(uptimeHP=0.5, **config),
                    relicsetone = HunterOfGlacialForest2pc(), relicsettwo = HunterOfGlacialForest4pc(), planarset = SpaceSealingStation(),
                    soulsteelUptime = 1.0,
                    **config)
    
    YanqingRotation = [
            YanqingCharacter.useSkill() * 3,
            YanqingCharacter.useTalent() * 3,
            YanqingCharacter.useBliss(),
            YanqingCharacter.useUltimate(),
            YanqingCharacter.useSkill(),
            YanqingCharacter.useTalent() * 2,
            YanqingCharacter.endTurn(),
    ]
    DefaultEstimator('Yanqing: 3E3T Bliss(1E 1Q 2T)', YanqingRotation, YanqingCharacter, config, CharacterDict, EffectDict)
    
    # Jingliu
    JingliuCharacter = Jingliu(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CD', 'iceDmg'],
                            substats = {'CR': 13, 'CD': 7}),
                lightcone = OnTheFallOfAnAeon(uptime = 0.25, **config),
                relicsetone = HunterOfGlacialForest2pc(),
                relicsettwo = HunterOfGlacialForest4pc(),
                planarset = RutilantArena(),
                speedBoostUptime=0.5,
                **config)
    
    JingliuRotation = [ # 140 max energy
            JingliuCharacter.useSkill() * 2, # 60 energy, 2 stack
            JingliuCharacter.useEnhancedSkill() * 3, # 60 energy, -3 stacks
            JingliuCharacter.useUltimate(), # 5 energy, 1 stack
            JingliuCharacter.extraTurn()*1.5,
    ]
    DefaultEstimator('Jingliu 2E 3Moon 1Q', JingliuRotation, JingliuCharacter, config, CharacterDict, EffectDict)
    
    # Topaz
    TopazCharacter = Topaz(RelicStats(mainstats = ['percAtk', 'percAtk', 'CD', 'fireDmg'],
                            substats = {'CR': 10, 'CD': 10}),
                lightcone = CruisingInTheStellarSea(**config),
                relicsetone = FiresmithOfLavaForging2pc(),
                relicsettwo = MusketeerOfWildWheat2pc(),
                planarset = InertSalsotto(),
                **config)
    
    TopazRotation = [ # 130 max energy
            TopazCharacter.useSkill() * 3, 
            TopazCharacter.useUltimate(),
            TopazCharacter.useTalent(windfall=True) * 2, # two talents from windfall
    ]
    
    topazTurns = sum([x.actionvalue for x in TopazRotation])
    numbyTurns = topazTurns * 80 / TopazCharacter.getTotalSpd()
    
    TopazRotation.append(TopazCharacter.useTalent(windfall=False) * numbyTurns)
    
    DefaultEstimator('Topaz 4E 2.2T Q Windfall(2T)', TopazRotation, TopazCharacter, config, CharacterDict, EffectDict)

    # Qingque
    QingqueCharacter = Qingque(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'quanDmg'],
                            substats = {'CR': 6, 'CD': 13, 'flatSpd': 1}),
                lightcone = TheSeriousnessOfBreakfast(**config),
                relicsetone = GeniusOfBrilliantStars2pc(),
                relicsettwo = GeniusOfBrilliantStars4pc(),
                planarset = RutilantArena(),
                **config)
    
    QingqueRotation = [ # expect 2.3 SP used per basic
            QingqueCharacter.useSkill(),
            QingqueCharacter.useSkill(),
            QingqueCharacter.useSkill(),
            QingqueCharacter.useEnhancedBasic(), 
            QingqueCharacter.useSkill(),
            QingqueCharacter.useSkill(),
            QingqueCharacter.useEnhancedBasic(), 
            QingqueCharacter.useSkill(), 
            QingqueCharacter.useSkill(),
            QingqueCharacter.useEnhancedBasic(),
            QingqueCharacter.useUltimate(),
    ]
    
    DefaultEstimator('Qingque 7E 3N 1Q', QingqueRotation, QingqueCharacter, config, CharacterDict, EffectDict)
    
    # Himeko
    HimekoCharacter = Himeko(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'fireDmg'],
                            substats = {'CR': 3, 'CD': 11, 'flatSpd': 6}),
                lightcone = TheSeriousnessOfBreakfast(**config),
                relicsetone = FiresmithOfLavaForging2pc(),
                relicsettwo = MusketeerOfWildWheat2pc(),
                planarset = SpaceSealingStation(),
                **config)
    
    HimekoRotation = [ # 
            HimekoCharacter.useSkill() * 3,
            HimekoCharacter.useTalent() * 2,
            HimekoCharacter.useUltimate(),
    ]
    
    DefaultEstimator('Himeko 3E 2T 1Q', HimekoRotation, HimekoCharacter, config, CharacterDict, EffectDict)
    
    # Hook
    HookCharacter = Hook(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'fireDmg'],
                            substats = {'CR': 4, 'CD': 9, 'flatSpd': 7}),
                lightcone = OnTheFallOfAnAeon(**config),
                relicsetone = FiresmithOfLavaForging2pc(),
                relicsettwo = MusketeerOfWildWheat2pc(),
                planarset = RutilantArena(),
                **config)
    
    HookRotation = [ # 
            HookCharacter.useEnhancedSkill() * 1,
            HookCharacter.useSkill() * 2,
            HookCharacter.useUltimate(),
    ]
    
    DefaultEstimator('Hook 1Enh 2E 1Q', HookRotation, HookCharacter, config, CharacterDict, EffectDict, dotMode='alwaysBlast')
    
    # Sampo
    SampoCharacter = Sampo(RelicStats(mainstats = ['percAtk', 'flatSpd', 'percAtk', 'windDmg'],
                            substats = {'percAtk': 7, 'flatSpd': 3, 'EHR': 10}),
                lightcone = GoodNightAndSleepWell(**config),
                relicsetone = EagleOfTwilightLine2pc(),
                relicsettwo = MusketeerOfWildWheat2pc(),
                planarset = PanCosmicCommercialEnterprise(),
                **config)
    
    SampoRotation = [ # 
            SampoCharacter.useSkill() * 3,
            SampoCharacter.useUltimate(),
    ]
    
    DefaultEstimator('Sampo 2x5 Stacks 3E 1Q', SampoRotation, SampoCharacter, config, CharacterDict, EffectDict, dotMode='alwaysBlast')
    
    # Sampo
    SampoCharacter = Sampo(RelicStats(mainstats = ['percAtk', 'flatSpd', 'percAtk', 'windDmg'],
                            substats = {'percAtk': 7, 'flatSpd': 3, 'EHR': 10}),
                lightcone = GoodNightAndSleepWell(**config),
                relicsetone = EagleOfTwilightLine2pc(),
                relicsettwo = MusketeerOfWildWheat2pc(),
                planarset = PanCosmicCommercialEnterprise(),
                windshearStacks=3.0,
                **config)
    
    SampoRotation = [ # 
            SampoCharacter.useSkill() * 3,
            SampoCharacter.useUltimate(),
    ]
    
    DefaultEstimator('Sampo 2x3 Stacks 3E 1Q', SampoRotation, SampoCharacter, config, CharacterDict, EffectDict, dotMode='alwaysBlast')
        
    visualize(CharacterDict, EffectDict, **config)