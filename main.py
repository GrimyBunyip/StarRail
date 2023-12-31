from copy import copy

from settings.BaseConfiguration import Configuration
from baseClasses.RelicStats import RelicStats
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
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
from characters.harmony.Yukong import Yukong
from characters.hunt.DanHeng import DanHeng
from characters.hunt.Seele import Seele
from characters.hunt.Sushang import Sushang
from characters.hunt.Topaz import Topaz
from characters.hunt.Yanqing import Yanqing
from characters.nihility.Guinaifen import Guinaifen
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

from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast

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
    visualizationList = []

    processes = []

    config = copy(Configuration)
    config['numEnemies'] = 2
    config['enemySpeed'] = 132 / 1.125 # assume 25% action delay every 2 enemy turns from toughness break

    # Kafka
    KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                            substats = {'EHR': 3, 'ATK.percent': 5, 'SPD.flat': 12}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = BandOfSizzlingThunder2pc(), relicsettwo = BandOfSizzlingThunder4pc(), planarset = SpaceSealingStation(),
                            **config)

    numSkill = 3.0
    numTalent = 3.0
    numUlt = 1.0

    KafkaRotation = [
            KafkaCharacter.useSkill() * numSkill,
            KafkaCharacter.useTalent() * numTalent,
            KafkaCharacter.useUltimate() * numUlt,
    ]

    numDot = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
    numDot = min(numDot, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)
    
    #num_breaks = sum([x.gauge for x in KafkaRotation]) * config['weaknessBrokenUptime'] / config['enemyToughness']
    #breakDotUptime = 2.0 * num_breaks * KafkaCharacter.getTotalStat('SPD') / KafkaCharacter.enemySpeed / sum([x.actionvalue for x in KafkaRotation])
    
    # change the skills to include break dots in dot explosions
    #KafkaRotation[0] = KafkaCharacter.useSkill(extraDots=[KafkaCharacter.useBreakDot() * breakDotUptime]) * numSkill
    #KafkaRotation[2] = KafkaCharacter.useUltimate(extraDots=[KafkaCharacter.useBreakDot() * breakDotUptime]) * numUlt

    visualizationList.append(DefaultEstimator('Kafka: {:.0f}E {:.0f}T {:.0f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDot), 
                                                    KafkaRotation, KafkaCharacter, config, numDot=numDot))

    # Blade
    BladeCharacter = Blade(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'DMG.wind'],
                            substats = {'CR': 10, 'CD': 4, 'SPD.flat': 6}),
                            lightcone = ASecretVow(uptime = 0.5, **config),
                            relicsetone = LongevousDisciple2pc(),
                            relicsettwo = LongevousDisciple4pc(),
                            planarset = InertSalsotto(),
                            hpLossTally=1.0,
                            **config)

    numBasic = 3.0
    numUlt = 1.0

    BladeRotation = [ # 130 max energy, Assume 3 enhanced basics per ultimate
            BladeCharacter.useSkill() * numBasic / 4.0,
            BladeCharacter.useEnhancedBasic() * numBasic,
            BladeCharacter.useUltimate(), # 15 energy, 1 charge
    ]

    # assume each elite performs 1 single target attack per turn
    numEnemyAttacks = BladeCharacter.enemySpeed * BladeCharacter.numEnemies * sum([x.actionvalue for x in BladeRotation]) / BladeCharacter.getTotalStat('SPD')
    numHitsTaken = numEnemyAttacks * 5 / (5 + 4 + 4 + 4) # assume 4 average threat teammates
    numTalent = (0.75 + 3 + 1 + numHitsTaken) / 5.0
    BladeRotation.append(BladeCharacter.useTalent() * numTalent)

    visualizationList.append(DefaultEstimator('Blade: {:.1f}N {:.1f}T {:.0f}Q'.format(numBasic, numTalent, numUlt), 
                                            BladeRotation, BladeCharacter, config))

    # Clara
    ClaraCharacter = Clara(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.physical'],
                            substats = {'CR': 7, 'CD': 13}),
            lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=5.0, **config),
            relicsetone = ChampionOfStreetwiseBoxing2pc(),
            relicsettwo = ChampionOfStreetwiseBoxing4pc(),
            planarset = InertSalsotto(),
            **config)

    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long
    numEnemyAttacks = ClaraCharacter.enemySpeed * ClaraCharacter.numEnemies * 2 / ClaraCharacter.getTotalStat('SPD')
    numEnhancedTalents = 2.0
    numUnenhancedTalents = (numEnemyAttacks - numEnhancedTalents) * (5*6) / (5*6 + 4 + 4 + 4) # assume 4 average threat teammates
    numSvarogCounters = numEnemyAttacks * (5*6) / (5*6 + 4 + 4 + 4)

    numSkill = 2.0
    numUlt = 1.0

    ClaraRotation = [ # 110 max energy
            ClaraCharacter.useSkill() * numSkill,
            ClaraCharacter.useMarkOfSvarog() * numSvarogCounters,
            ClaraCharacter.useTalent(enhanced=False) * numUnenhancedTalents, 
            ClaraCharacter.useTalent(enhanced=True) * numEnhancedTalents,
            ClaraCharacter.useUltimate() * numUlt,
    ]

    visualizationList.append(DefaultEstimator('Clara: {:.0f}E {:.1f}T {:.0f}Q'.format(numSkill, numSvarogCounters, numUlt),
                                            ClaraRotation, ClaraCharacter, config))

    # Lunae
    LunaeCharacter = Lunae(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
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
    visualizationList.append(DefaultEstimator('Lunae: 3N^3 1Q', LunaeRotation, LunaeCharacter, config))

    # Serval
    ServalCharacter = Serval(relicstats = RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                            substats = {'BreakEffect': 10, 'ATK.percent': 8, 'SPD.flat': 2}),
            lightcone = TheSeriousnessOfBreakfast(**config),
            relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SpaceSealingStation(),
            **config)
    
    numBasic = 1.0
    numSkill = 2.0
    numUlt = 1.0

    ServalRotation = [
            ServalCharacter.useBasic(shocked=True) * numBasic,
            ServalCharacter.useSkill(shocked=True) * numSkill,
            ServalCharacter.useUltimate(shocked=True) * numUlt,
    ]

    numDot = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
    
    visualizationList.append(DefaultEstimator('Serval: {:.0f}N {:.0f}E {:.0f}Q'.format(numBasic, numSkill, numUlt), 
                                                ServalRotation, ServalCharacter, config, breakDotMode='alwaysAll', numDot=numDot))

    # Jing Yuan
    JingYuanCharacter = JingYuan(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.lightning'],
                            substats = {'CD': 8, 'CR': 5, 'SPD.flat': 7}),
            lightcone = GeniusesRepose(**config),
            relicsetone = BandOfSizzlingThunder2pc(), relicsettwo = BandOfSizzlingThunder4pc(), planarset = InertSalsotto(),
            **config)

    numSkill = 4.0
    numUlt = 1.0
    ''' Formula we can use, but it's admittedly very generous. Easier to use the 140 speed estimate for solo.
    jingSpeed = JingYuanCharacter.getTotalStat('SPD')
    # estimate lord's max speed given this rotation
    lordBaseSpeed = 0.6
    lordBonusSpeed = 0.1
    lordSpeed = 100.0 * ( lordBaseSpeed + np.sqrt(lordBaseSpeed * lordBaseSpeed + 4 * lordBonusSpeed * (2 * numSkill + 3 * numUlt) / numSkill ) ) / 2

    numTalent = ( 3 * numSkill * lordSpeed / jingSpeed )  + 2 * numSkill + 3 * numUlt'''

    numTalent = ( 3 * numSkill / 2 )  + 2 * numSkill + 3 * numUlt

    JingYuanRotation = [
            JingYuanCharacter.useSkill() * numSkill, # 4 * 2 lord actions
            JingYuanCharacter.useUltimate() * numUlt, # 3 lord actions
            JingYuanCharacter.useTalent() * numTalent, # hits generated from skill and ultimate
    ]
    visualizationList.append(DefaultEstimator('JingYuan: {:.0f}E {:.0f}Q {:.0f}T'.format(numSkill, numUlt, numTalent), 
                                                JingYuanRotation, JingYuanCharacter, config))

    # Seele
    SeeleCharacter = Seele(relicstats = RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CD', 'DMG.quantum'],
                            substats = {'CR': 16, 'CD': 4}),
            lightcone = CruisingInTheStellarSea(**config),
            relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo=GeniusOfBrilliantStars4pc(), planarset = RutilantArena(),
            **config)

    SeeleRotation = [ # endTurn needed to factor in resurgence buff
            SeeleCharacter.useSkill() * 3,
            SeeleCharacter.useResurgence(),
            SeeleCharacter.useSkill(),
            SeeleCharacter.useUltimate(),
            SeeleCharacter.endTurn(),
    ]
    visualizationList.append(DefaultEstimator('Seele: 3E Resurgence(1E1Q)', SeeleRotation, SeeleCharacter, config))

    # Dan Heng
    DanHengCharacter = DanHeng(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.wind'],
                            substats = {'CR': 7, 'CD': 13}),
            lightcone = CruisingInTheStellarSea(**config),
            relicsetone = EagleOfTwilightLine2pc(), relicsettwo=EagleOfTwilightLine4pc(), planarset = SpaceSealingStation(),
            **config)
    
    numSkill = 3.0
    numUlt = 1.0

    DanHengRotation = [
            #DanHengCharacter.useBasic(slowed=True) * 2,
            DanHengCharacter.useSkill() * numSkill,
            DanHengCharacter.useUltimate(slowed=True) * numUlt,
    ]
    visualizationList.append(DefaultEstimator('Dan Heng: {:.0f}E {:.0f}Q'.format(numSkill, numUlt), 
                                                DanHengRotation, DanHengCharacter, config))

    #Yanqing
    YanqingCharacter = Yanqing(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.ice'],
                            substats = {'CR': 5, 'CD': 15}),
                    lightcone = CruisingInTheStellarSea(uptimeHP=0.5, **config),
                    relicsetone = HunterOfGlacialForest2pc(), relicsettwo = HunterOfGlacialForest4pc(uptime=2.0/3.5), planarset = SpaceSealingStation(),
                    soulsteelUptime = 1.0,
                    **config)

    numSkill = 2.5
    numTalent = 2.5

    YanqingRotation = [ # endTurn needed to factor in limited buffs
            YanqingCharacter.useSkill() * numSkill,
            YanqingCharacter.useTalent() * numTalent,
            YanqingCharacter.useBliss(),
            YanqingCharacter.useUltimate(),
            YanqingCharacter.useSkill(),
            YanqingCharacter.useTalent() * 2,
            YanqingCharacter.endTurn(),
    ]
    visualizationList.append(DefaultEstimator('Yanqing: {:.1f}E {:.1f}T Bliss(1E 1Q 2T)'.format(numSkill, numTalent), 
                                                YanqingRotation, YanqingCharacter, config))

    # Jingliu
    JingliuCharacter = Jingliu(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.ice'],
                            substats = {'CR': 12, 'CD': 6, 'SPD.flat': 2}),
            lightcone = OnTheFallOfAnAeon(uptime = 0.25, **config),
            relicsetone = HunterOfGlacialForest2pc(), relicsettwo = HunterOfGlacialForest4pc(uptime=0.4), planarset = RutilantArena(uptime=0.0),
            **config)
    
    numSkill = 2.0
    numEnhanced = 3.0
    numUlt = 1.0
    
    JingliuRotation = [JingliuCharacter.useSkill() * numSkill]
    JingliuCharacter.addStat('DMG',description='Rutilant Arena', amount=0.20, type=['skill']) # take care of rutilant arena manually
    JingliuRotation += [ # 140 max energy
            JingliuCharacter.useEnhancedSkill() * numEnhanced, # 60 energy, -3 stacks
            JingliuCharacter.useUltimate() * numUlt, # 5 energy, 1 stack
            JingliuCharacter.extraTurn() * 0.9 * numEnhanced / 2.0, # multiply by 0.9 because it tends to overlap with skill advances
    ]
    visualizationList.append(DefaultEstimator('Jingliu {:.0f}E {:.0f}Moon {:.0f}Q'.format(numSkill, numEnhanced, numUlt),
                                                JingliuRotation, JingliuCharacter, config))

    # Topaz
    TopazCharacter = Topaz(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.fire'],
                            substats = {'CR': 6, 'CD': 14}),
            lightcone = CruisingInTheStellarSea(**config),
            relicsetone = FiresmithOfLavaForging2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = InertSalsotto(),
            **config)
    
    numBasic = 4.0
    numSkill = 1.0
    numUlt = 1.0

    TopazRotation = [ # 130 max energy
            TopazCharacter.useBasic() * numBasic,
            TopazCharacter.useSkill() * numSkill,
            TopazCharacter.useUltimate() * numUlt,
            TopazCharacter.useTalent(windfall=True) * 2, # two talents from windfall
    ]

    topazTurns = sum([x.actionvalue for x in TopazRotation])
    numbyTurns = topazTurns * 80 / TopazCharacter.getTotalStat('SPD')
    numbyAdvanceForwards = 6 * 3 / 8 # 4 skill usages, treat each 50% advance forward as 37.5% of an advance forward    
    TopazRotation.append(TopazCharacter.useTalent(windfall=False) * (numbyTurns + numbyAdvanceForwards)) # about 1 talent per basic/skill

    visualizationList.append(DefaultEstimator('Topaz {:.0f}E {:.0f}N {:.1f}T {:.0f}Q Windfall(2T)'.format(numSkill, numBasic, (numbyTurns + numbyAdvanceForwards), numUlt), 
                                                TopazRotation, TopazCharacter, config))

    # Qingque
    QingqueCharacter = Qingque(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.quantum'],
                            substats = {'CR': 9, 'CD': 10, 'SPD.flat': 1}),
            lightcone = TheSeriousnessOfBreakfast(**config),
            relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo = GeniusOfBrilliantStars4pc(), planarset = RutilantArena(),
            **config)

    QingqueRotation = [ # expect 2.3 SP used per basic, estimating with 1 2 2 3 4 split
            QingqueCharacter.useSkill(),
            QingqueCharacter.useSkill(),
            QingqueCharacter.useSkill(),
            QingqueCharacter.useSkill(),
            QingqueCharacter.useEnhancedBasic(),
            QingqueCharacter.drawTileFromAlly(),
            QingqueCharacter.useSkill(),
            QingqueCharacter.useSkill(),
            QingqueCharacter.useSkill(),
            QingqueCharacter.useEnhancedBasic(),
            QingqueCharacter.drawTileFromAlly(),
            QingqueCharacter.useSkill(), 
            QingqueCharacter.useSkill(),
            QingqueCharacter.useEnhancedBasic(),
            QingqueCharacter.useSkill(),
            QingqueCharacter.useSkill(),
            QingqueCharacter.useEnhancedBasic(),
            QingqueCharacter.drawTileFromAlly(),
            QingqueCharacter.useSkill(),
            QingqueCharacter.useUltimate(),
            QingqueCharacter.useEnhancedBasic(),
            QingqueCharacter.drawTileFromAlly(),
    ]

    visualizationList.append(DefaultEstimator('Qingque 12E 5N 1Q', QingqueRotation, QingqueCharacter, config))

    # Himeko
    HimekoCharacter = Himeko(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.fire'],
                            substats = {'CR': 3, 'CD': 11, 'SPD.flat': 6}),
            lightcone = TheSeriousnessOfBreakfast(**config),
            relicsetone = FiresmithOfLavaForging2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SpaceSealingStation(),
            **config)
    
    numSkill = 3.0
    numTalent = 2.0
    numUlt = 1.0

    HimekoRotation = [ # 
            HimekoCharacter.useSkill() * numSkill,
            HimekoCharacter.useTalent() * numTalent,
            HimekoCharacter.useUltimate() * numUlt,
    ]

    numDot = DotEstimator(HimekoRotation, HimekoCharacter, config, dotMode='alwaysAll')
    numDot = min(numDot, 2.0 * (numSkill * min(3.0, HimekoCharacter.numEnemies) + (numTalent + numUlt) * HimekoCharacter.numEnemies) * 0.5) # halve it because of himeko's base chance

    visualizationList.append(DefaultEstimator('Himeko {:.0f}E {:.0f}T {:.0f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDot), 
                                                HimekoRotation, HimekoCharacter, config, numDot=numDot))

    # Hook
    HookCharacter = Hook(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.fire'],
                            substats = {'CR': 4, 'CD': 9, 'SPD.flat': 7}),
            lightcone = OnTheFallOfAnAeon(**config),
            relicsetone = FiresmithOfLavaForging2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SpaceSealingStation(),
            **config)
    
    numEnhanced = 1.0
    numSkill = 2.0
    numUlt = 1.0

    HookRotation = [ # 
            HookCharacter.useEnhancedSkill() * numEnhanced,
            HookCharacter.useSkill() * numSkill,
            HookCharacter.useUltimate() * numUlt,
    ]

    numDot = DotEstimator(HookRotation, HookCharacter, config, dotMode='alwaysBlast')
    numDot = min(numDot, (numEnhanced + numSkill) * (3.0 if HookCharacter.eidolon >= 2 else 2.0))

    visualizationList.append(DefaultEstimator('Hook {:.0f}Enh {:.0f}E {:.0f}Q {:.1f}Dot'.format(numEnhanced, numSkill, numUlt, numDot),
                                                HookRotation, HookCharacter, config, numDot=numDot))

    # Sampo
    SampoCharacter = Sampo(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.wind'],
                            substats = {'ATK.percent': 7, 'SPD.flat': 3, 'EHR': 10}),
            lightcone = GoodNightAndSleepWell(**config),
            relicsetone = EagleOfTwilightLine2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = PanCosmicCommercialEnterprise(),
            **config)

    numSkill = 3.5
    numUlt = 1.0

    SampoRotation = [ # 
            SampoCharacter.useSkill() * numSkill,
            SampoCharacter.useUltimate() * numUlt,
    ]

    numDot = DotEstimator(SampoRotation, SampoCharacter, config, dotMode='alwaysBlast')
    numDot = min(numDot, 3.0 * (numSkill + numUlt) * SampoCharacter.numEnemies)

    visualizationList.append(DefaultEstimator('Sampo {:.1f}E {:.0f}Q {:.1f}Dot'.format(numSkill, numUlt, numDot),
                                                SampoRotation, SampoCharacter, config, numDot=numDot))

    # Luka
    LukaCharacter = Luka(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.physical'],
                    substats = {'ATK.percent': 4, 'SPD.flat': 3, 'EHR': 13}),
            lightcone = GoodNightAndSleepWell(**config),
            relicsetone = ChampionOfStreetwiseBoxing2pc(), relicsettwo = ChampionOfStreetwiseBoxing4pc(), planarset = SpaceSealingStation(),
            **config)
    
    numEnhanced = 3.0
    numSkill = 2.0
    numUlt = 1.0

    LukaRotation = [ # 
            LukaCharacter.useEnhancedBasic() * numEnhanced, # -6 Fighting Will
            LukaCharacter.useSkill() * numSkill, # +4 Fighting Will
            LukaCharacter.useUltimate() * numUlt, # +2 Fighting Will
    ]

    numDot = DotEstimator(LukaRotation, LukaCharacter, config, dotMode='alwaysBlast')
    numDot = min(numDot, 3.0 * numSkill)

    visualizationList.append(DefaultEstimator('Luka {:.0f}Enh {:.0f}S {:.0f}Q {:.1f}Dot'.format(numEnhanced, numSkill, numUlt, numDot),
                                                LukaRotation, LukaCharacter, config, numDot=numDot))

    # Guinaifen
    GuinaifenCharacter = Guinaifen(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.fire'],
                            substats = {'ATK.percent': 12, 'SPD.flat': 4, 'EHR': 4}),
            lightcone = GoodNightAndSleepWell(**config),
            relicsetone = FiresmithOfLavaForging2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SpaceSealingStation(),
            **config)
    
    numSkill = 3.0
    numUlt = 1.0

    GuinaifenRotation = [ # 
            GuinaifenCharacter.useSkill() * numSkill,
            GuinaifenCharacter.useUltimate() * numUlt,
    ]

    numDot = DotEstimator(GuinaifenRotation, GuinaifenCharacter, config, dotMode='alwaysBlast')
    numDot = min(numDot, 2.0 * numSkill * min(3.0, GuinaifenCharacter.numEnemies))

    visualizationList.append(DefaultEstimator('Guinaifen {:.0f}E {:.0f}Q {:.1f}Dot'.format(numSkill, numUlt, numDot), GuinaifenRotation, GuinaifenCharacter, config, numDot=numDot))

    # Sushang
    SushangCharacter = Sushang(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.physical'],
                    substats = {'CR': 9, 'CD': 11}),
                    lightcone = CruisingInTheStellarSea(**config),
                    relicsetone = ChampionOfStreetwiseBoxing2pc(), relicsettwo = ChampionOfStreetwiseBoxing4pc(), planarset = RutilantArena(),
                    **config)

    SushangRotation = [ # do not multiply here, repeat entries as these uses factor in end turn and ultimate buff
            SushangCharacter.useUltimate(),
            SushangCharacter.useSkill(),
            SushangCharacter.useSkill(),
            SushangCharacter.useSkill(),
            SushangCharacter.useSkill(),
    ]

    visualizationList.append(DefaultEstimator('Sushang 4E 1Q', SushangRotation, SushangCharacter, config))

    # Welt
    WeltCharacter = Welt(RelicStats(mainstats = ['ER', 'SPD.flat', 'CR', 'ATK.percent'],
                    substats = {'CD': 12, 'CR': 5, 'SPD.flat':3}),
            lightcone = GoodNightAndSleepWell(**config),
            relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = WastelanderOfBanditryDesert4pc(), planarset = SpaceSealingStation(),
            **config)
    
    numBasic = 1.0
    numSkill = 2.0
    numUlt = 1.0

    WeltRotation = [ # 
            WeltCharacter.useBasic() * numBasic, #
            WeltCharacter.useSkill() * numSkill, #
            WeltCharacter.useUltimate() * numUlt, #
    ]

    visualizationList.append(DefaultEstimator('Welt {:.0f}N {:.0f}E {:.0f}Q'.format(numBasic, numSkill, numUlt), WeltRotation, WeltCharacter, config))

    # SilverWolf
    SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'BreakEffect'],
                    substats = {'SPD.flat':12,'BreakEffect':8}),
            lightcone = BeforeTheTutorialMissionStarts(**config),
            relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo = GeniusOfBrilliantStars2pc(), planarset = SprightlyVonwacq(),
            **config)
    
    numSkill = 2.0
    numUlt = 1.0

    SilverWolfRotation = [ # 
            SilverWolfCharacter.useSkill() * numSkill, #
            SilverWolfCharacter.useUltimate() * numUlt, #
    ]

    visualizationList.append(DefaultEstimator('SilverWolf {:.0f}E {:.0f}Q'.format(numSkill, numUlt), SilverWolfRotation, SilverWolfCharacter, config))

    # Herta
    HertaCharacter = Herta(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.ice'],
                    substats = {'CR':6,'CD':14}),
            lightcone = TheSeriousnessOfBreakfast(**config),
            relicsetone = HunterOfGlacialForest2pc(), relicsettwo = HunterOfGlacialForest4pc(uptime=2.0/3.0), planarset = SpaceSealingStation(),
            **config)

    HertaRotation = [ # sequencing and end turn mechanic exists her to factor in her ult buff
            HertaCharacter.useSkill() * 2,
            HertaCharacter.useTalent(),
            HertaCharacter.useUltimate(),
            HertaCharacter.useSkill(),
            HertaCharacter.useTalent(),
            HertaCharacter.endTurn(),
    ]

    visualizationList.append(DefaultEstimator('Herta 3E 2T 1Q', HertaRotation, HertaCharacter, config))

    # Arlan
    ArlanCharacter = Arlan(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.lightning'],
                    substats = {'CR':9,'CD':11}),
            lightcone = ASecretVow(**config),
            relicsetone = BandOfSizzlingThunder2pc(), relicsettwo = BandOfSizzlingThunder4pc(), planarset = RutilantArena(),
            **config)
    
    numSkill = 3.5
    numUlt = 1.0

    ArlanRotation = [ # 
            ArlanCharacter.useSkill() * numSkill,
            ArlanCharacter.useUltimate() * numUlt,
    ]

    visualizationList.append(DefaultEstimator('Arlan {:.1f}E {:.0f}Q'.format(numSkill, numUlt), ArlanRotation, ArlanCharacter, config))

    #Yukong
    '''
    YukongCharacter = Yukong(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.imaginary'],
                            substats = {'CR': 4, 'CD': 7, 'SPD.flat': 9}),
            lightcone = MemoriesOfThePast(**config),
            relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SpaceSealingStation(),
            **config)

    spd = YukongCharacter.getTotalStat('SPD')

    YukongRotation = [ # 
            YukongCharacter.useEnhancedBasic() * 2,
            YukongCharacter.useSkill() * 2,
            YukongCharacter.useUltimate(),
    ]

    visualizationList.append(DefaultEstimator('Yukong 2 Enh 2S 1Q', YukongRotation, YukongCharacter, config))
    '''

    visualize(visualizationList, visualizerPath='visualizer\SoloVisual.png', **config)
        
    from excelAPI.write2sheet import writeVisualizationList
    writeVisualizationList(visualizationList,path='visualizer\SoloVisual.xlsx',sheetname='Solo vs Two')