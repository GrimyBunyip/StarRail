from copy import copy

from settings.BaseConfiguration import Configuration
from baseClasses.RelicStats import RelicStats
from estimator.DefaultEstimator import DefaultEstimator
from visualizer.visualizer import visualize

from characters.destruction.Arlan import Arlan
from characters.destruction.Blade import Blade
from characters.destruction.Clara import Clara
from characters.destruction.Hook import Hook
from characters.destruction.Jingliu import Jingliu
from characters.destruction.Lunae import Lunae
from characters.erudition.Herta import Herta
from characters.erudition.Himeko import Himeko
from characters.erudition.JingYuan import JingYuan
from characters.erudition.Serval import Serval
from characters.erudition.Qingque import Qingque
from characters.hunt.DanHeng import DanHeng
from characters.hunt.Seele import Seele
from characters.hunt.Sushang import Sushang
from characters.hunt.Topaz import Topaz
from characters.hunt.Yanqing import Yanqing
from characters.nihility.Kafka import Kafka
from characters.nihility.Luka import Luka
from characters.nihility.Sampo import Sampo
from characters.nihility.SilverWolf import SilverWolf
from characters.nihility.Welt import Welt

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
    VisualizationDict = {}
    VisualizationDict['CharacterDict'] = {} # store character information here
    VisualizationDict['EffectDict'] = {} # store dps metrics here, not including breaks or constantly ticking dots. May include limited dots like Yanqing
    VisualizationDict['DotDict'] = {} # store dot damage here, not including dot detonations
    VisualizationDict['BreakDict'] = {} # store break damage here, not including dot detonations
    
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
                lightcone = GoodNightAndSleepWell(**config),
                relicsetone = BandOfSizzlingThunder2pc(), relicsettwo = BandOfSizzlingThunder4pc(), planarset = SpaceSealingStation(),
                **config)
    
    KafkaRotation = [
            KafkaCharacter.useSkill() * 3,
            KafkaCharacter.useTalent() * 3,
            KafkaCharacter.useUltimate(),
    ]
    
    DefaultEstimator('Kafka: 3E 3T 1Q', KafkaRotation, KafkaCharacter, config, VisualizationDict, dotMode='alwaysAll')
    
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
    DefaultEstimator('Blade: 0.5S 2N 0.9T 1Q, get hit once', BladeRotation, bladeCharacter, config, VisualizationDict)
    
    # Clara
    ClaraCharacter = Clara(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'physDmg'],
                            substats = {'CR': 7, 'CD': 13}),
                lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=5.0, **config),
                relicsetone = ChampionOfStreetwiseBoxing2pc(),
                relicsettwo = ChampionOfStreetwiseBoxing4pc(),
                planarset = InertSalsotto(),
                **config)
    
    ClaraRotation = [ # 110 max energy
            ClaraCharacter.useSkill() * 3,
            ClaraCharacter.useMarkOfSvarog() * 3, # these are 3 instances of single target bonus damage
            ClaraCharacter.useTalent(enhanced=False), # 1 additional clara hit on top
            ClaraCharacter.useTalent(enhanced=True) * 2, # 2 reactions from ultimate
            ClaraCharacter.useUltimate(),
    ]
    # 2.5E as clara probably can't consistently pull off a 2E rotation depending on how much
    # energy enemies give when they hit her
    DefaultEstimator('Clara: 2.5E 3T 1Q', ClaraRotation, ClaraCharacter, config, VisualizationDict)

    # Lunae
    LunaeCharacter = Lunae(RelicStats(mainstats = ['percAtk', 'percAtk', 'CR', 'imagDmg'],
                            substats = {'CR': 10, 'CD': 10}),
                lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=4.0, **config),
                relicsetone = MusketeerOfWildWheat2pc(),
                relicsettwo = MusketeerOfWildWheat4pc(),
                planarset = RutilantArena(),
                **config)
     
    LunaeRotation = [  # 140 energy needed. EndTurn needed to factor in his buffs
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
    DefaultEstimator('Lunae: 3N^3 1Q', LunaeRotation, LunaeCharacter, config, VisualizationDict)
    
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
    DefaultEstimator('Serval: 1N 2E 1Q', ServalRotation, ServalCharacter, config, VisualizationDict, breakDotMode='alwaysAll', dotMode='alwaysAll')
    
    # Jing Yuan
    JingYuanCharacter = JingYuan(relicstats = RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'lighDmg'],
                            substats = {'CD': 8, 'CR': 5, 'flatSpd': 7}),
                lightcone = GeniusesRepose(**config),
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
    DefaultEstimator('JingYuan: 4E 1Q 17T', JingYuanRotation, JingYuanCharacter, config, VisualizationDict)
    
    # Seele
    SeeleCharacter = Seele(relicstats = RelicStats(mainstats = ['percAtk', 'percAtk', 'CR', 'quanDmg'],
                            substats = {'CR': 10, 'CD': 10}),
                lightcone = Swordplay(**config),
                relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo=GeniusOfBrilliantStars4pc(), planarset = SpaceSealingStation(),
                **config)
    
    SeeleRotation = [ # endTurn needed to factor in resurgence buff
            SeeleCharacter.useSkill() * 3,
            SeeleCharacter.useResurgence(),
            SeeleCharacter.useSkill(),
            SeeleCharacter.useUltimate(),
            SeeleCharacter.endTurn(),
    ]
    DefaultEstimator('Seele: 3E Resurgence(1E1Q)', SeeleRotation, SeeleCharacter, config, VisualizationDict)
    
    SeeleRotation = [
            SeeleCharacter.useSkill() * 4,
            SeeleCharacter.useUltimate(),
    ]
    DefaultEstimator('Seele: 4E 1Q No Resurgence', SeeleRotation, SeeleCharacter, config, VisualizationDict)
    
    # Dan Heng
    DanHengCharacter = DanHeng(relicstats = RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'windDmg'],
                            substats = {'CR': 7, 'CD': 13}),
                lightcone = Swordplay(**config),
                relicsetone = EagleOfTwilightLine2pc(), relicsettwo=EagleOfTwilightLine4pc(), planarset = SpaceSealingStation(),
                **config)
    
    DanHengRotation = [
            #DanHengCharacter.useBasic(slowed=True) * 2,
            DanHengCharacter.useSkill() * 3,
            DanHengCharacter.useUltimate(slowed=True),
    ]
    DefaultEstimator('Dan Heng: 3E 1Q', DanHengRotation, DanHengCharacter, config, VisualizationDict)
    
    #Yanqing
    YanqingCharacter = Yanqing(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CD', 'iceDmg'],
                            substats = {'CR': 5, 'CD': 15}),
                    lightcone = Swordplay(uptimeHP=0.5, **config),
                    relicsetone = HunterOfGlacialForest2pc(), relicsettwo = HunterOfGlacialForest4pc(), planarset = SpaceSealingStation(),
                    soulsteelUptime = 1.0,
                    **config)
    
    YanqingRotation = [ # endTurn needed to factor in limited buffs
            YanqingCharacter.useSkill() * 2.5,
            YanqingCharacter.useTalent() * 2.5,
            YanqingCharacter.useBliss(),
            YanqingCharacter.useUltimate(),
            YanqingCharacter.useSkill(),
            YanqingCharacter.useTalent() * 2,
            YanqingCharacter.endTurn(),
    ]
    DefaultEstimator('Yanqing: 2E2T Bliss(1E 1Q 2T)', YanqingRotation, YanqingCharacter, config, VisualizationDict)
    
    # Jingliu
    JingliuCharacter = Jingliu(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CD', 'iceDmg'],
                            substats = {'CR': 13, 'CD': 7}),
                lightcone = OnTheFallOfAnAeon(uptime = 0.25, **config),
                relicsetone = HunterOfGlacialForest2pc(), relicsettwo = HunterOfGlacialForest4pc(), planarset = RutilantArena(),
                **config)
    
    JingliuRotation = [ # 140 max energy
            JingliuCharacter.useSkill() * 2, # 60 energy, 2 stack
            JingliuCharacter.useEnhancedSkill() * 3, # 60 energy, -3 stacks
            JingliuCharacter.useUltimate(), # 5 energy, 1 stack
            JingliuCharacter.extraTurn()*1.5,
    ]
    DefaultEstimator('Jingliu 2E 3Moon 1Q', JingliuRotation, JingliuCharacter, config, VisualizationDict)
    
    # Topaz
    TopazCharacter = Topaz(RelicStats(mainstats = ['percAtk', 'percAtk', 'CR', 'fireDmg'],
                            substats = {'CR': 6, 'CD': 14}),
                lightcone = Swordplay(**config),
                relicsetone = FiresmithOfLavaForging2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = InertSalsotto(),
                **config)
    
    TopazRotation = [ # 130 max energy
            TopazCharacter.useSkill() * 3, 
            TopazCharacter.useUltimate(),
            TopazCharacter.useTalent(windfall=True) * 2, # two talents from windfall
    ]
    
    topazTurns = sum([x.actionvalue for x in TopazRotation])
    numbyTurns = topazTurns * 80 / TopazCharacter.getTotalSpd()
    
    TopazRotation.append(TopazCharacter.useTalent(windfall=False) * numbyTurns)
    
    DefaultEstimator('Topaz 4E 2.2T Q Windfall(2T)', TopazRotation, TopazCharacter, config, VisualizationDict)

    # Qingque
    QingqueCharacter = Qingque(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'quanDmg'],
                            substats = {'CR': 6, 'CD': 13, 'flatSpd': 1}),
                lightcone = TheSeriousnessOfBreakfast(**config),
                relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo = GeniusOfBrilliantStars4pc(), planarset = RutilantArena(),
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
    
    DefaultEstimator('Qingque 7E 3N 1Q', QingqueRotation, QingqueCharacter, config, VisualizationDict)
    
    # Himeko
    HimekoCharacter = Himeko(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'fireDmg'],
                            substats = {'CR': 3, 'CD': 11, 'flatSpd': 6}),
                lightcone = TheSeriousnessOfBreakfast(**config),
                relicsetone = FiresmithOfLavaForging2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SpaceSealingStation(),
                **config)
    
    HimekoRotation = [ # 
            HimekoCharacter.useSkill() * 3,
            HimekoCharacter.useTalent() * 2,
            HimekoCharacter.useUltimate(),
    ]
    
    DefaultEstimator('Himeko 3E 2T 1Q', HimekoRotation, HimekoCharacter, config, VisualizationDict)
    
    # Hook
    HookCharacter = Hook(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'fireDmg'],
                            substats = {'CR': 4, 'CD': 9, 'flatSpd': 7}),
                lightcone = OnTheFallOfAnAeon(**config),
                relicsetone = FiresmithOfLavaForging2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = RutilantArena(),
                **config)
    
    HookRotation = [ # 
            HookCharacter.useEnhancedSkill() * 1,
            HookCharacter.useSkill() * 2,
            HookCharacter.useUltimate(),
    ]
    
    DefaultEstimator('Hook 1Enh 2E 1Q', HookRotation, HookCharacter, config, VisualizationDict, dotMode='alwaysBlast')
    
    # Sampo
    SampoCharacter = Sampo(RelicStats(mainstats = ['percAtk', 'flatSpd', 'percAtk', 'windDmg'],
                            substats = {'percAtk': 7, 'flatSpd': 3, 'EHR': 10}),
                lightcone = GoodNightAndSleepWell(**config),
                relicsetone = EagleOfTwilightLine2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = PanCosmicCommercialEnterprise(),
                **config)
    
    SampoRotation = [ # 
            SampoCharacter.useSkill() * 3.5,
            SampoCharacter.useUltimate(),
    ]
    
    DefaultEstimator('Sampo 2x5 Stacks 3.5E 1Q', SampoRotation, SampoCharacter, config, VisualizationDict, dotMode='alwaysBlast')
    
    # Luka
    LukaCharacter = Luka(RelicStats(mainstats = ['percAtk', 'flatSpd', 'percAtk', 'physDmg'],
                        substats = {'percAtk': 4, 'flatSpd': 3, 'EHR': 13}),
                lightcone = GoodNightAndSleepWell(**config),
                relicsetone = ChampionOfStreetwiseBoxing2pc(), relicsettwo = ChampionOfStreetwiseBoxing4pc(), planarset = SpaceSealingStation(),
                **config)
    
    LukaRotation = [ # 
            LukaCharacter.useEnhancedBasic() * 3, # -6 Fighting Will
            LukaCharacter.useSkill() * 2, # +4 Fighting Will
            LukaCharacter.useUltimate(), # +2 Fighting Will
    ]
    
    DefaultEstimator('Luka 3EB 2S 1Q', LukaRotation, LukaCharacter, config, VisualizationDict, dotMode='alwaysBlast')

    # Sushang
    SushangCharacter = Sushang(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CD', 'physDmg'],
                        substats = {'CR': 13, 'CD': 7}),
                        lightcone = Swordplay(**config),
                        relicsetone = ChampionOfStreetwiseBoxing2pc(), relicsettwo = ChampionOfStreetwiseBoxing4pc(), planarset = RutilantArena(),
                        **config)
    
    SushangRotation = [ # do not multiply here, repeat entries as these uses factor in end turn and ultimate buff
            SushangCharacter.useUltimate(),
            SushangCharacter.useSkill(),
            SushangCharacter.useSkill(),
            SushangCharacter.useSkill(),
            SushangCharacter.useSkill(),
    ]
    
    DefaultEstimator('Sushang 4E 1Q', SushangRotation, SushangCharacter, config, VisualizationDict)
    
    # Welt
    WeltCharacter = Welt(RelicStats(mainstats = ['ER', 'flatSpd', 'CR', 'percAtk'],
                        substats = {'CD': 11, 'CR': 6, 'flatSpd':3}),
                lightcone = GoodNightAndSleepWell(**config),
                relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = WastelanderOfBanditryDesert4pc(), planarset = SpaceSealingStation(),
                **config)
    
    WeltRotation = [ # 
            WeltCharacter.useSkill() * 2, #
            WeltCharacter.useUltimate(), #
    ]
    
    DefaultEstimator('Welt 2E 1Q', WeltRotation, WeltCharacter, config, VisualizationDict)
    
    # SilverWolf
    SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['ER', 'flatSpd', 'EHR', 'breakEffect'],
                        substats = {'flatSpd':12,'breakEffect':8}),
                lightcone = BeforeTheTutorialMissionStarts(**config),
                relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo = GeniusOfBrilliantStars2pc(), planarset = SprightlyVonwacq(),
                **config)
    
    SilverWolfRotation = [ # 
            SilverWolfCharacter.useSkill() * 2, #
            SilverWolfCharacter.useUltimate(), #
    ]
    
    DefaultEstimator('SilverWolf 2E 1Q', SilverWolfRotation, SilverWolfCharacter, config, VisualizationDict)
    
    # Herta
    HertaCharacter = Herta(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'iceDmg'],
                        substats = {'CR':6,'CD':14}),
                lightcone = TheSeriousnessOfBreakfast(**config),
                relicsetone = HunterOfGlacialForest2pc(), relicsettwo = HunterOfGlacialForest4pc(), planarset = SpaceSealingStation(),
                **config)
    
    HertaRotation = [ # sequencing and end turn mechanic exists her to factor in her ult buff
            HertaCharacter.useSkill() * 2,
            HertaCharacter.useTalent(),
            HertaCharacter.useUltimate(),
            HertaCharacter.useSkill(),
            HertaCharacter.useTalent(),
            HertaCharacter.endTurn(),
    ]
    
    DefaultEstimator('Herta 3E 2T 1Q', HertaRotation, HertaCharacter, config, VisualizationDict)
    
    # Arlan
    ArlanCharacter = Arlan(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'lighDmg'],
                        substats = {'CR':7,'CD':13}),
                lightcone = ASecretVow(**config),
                relicsetone = BandOfSizzlingThunder2pc(), relicsettwo = BandOfSizzlingThunder4pc(), planarset = RutilantArena(),
                **config)
    
    ArlanRotation = [ # 
            ArlanCharacter.useSkill() * 3.5,
            ArlanCharacter.useUltimate(),
    ]
    
    DefaultEstimator('Arlan 3.5E 1Q', ArlanRotation, ArlanCharacter, config, VisualizationDict)

    visualize(VisualizationDict, **config)