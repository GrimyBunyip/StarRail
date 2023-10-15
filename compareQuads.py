from copy import copy, deepcopy

from baseClasses.BaseEffect import BaseEffect
from settings.BaseConfiguration import Configuration
from baseClasses.RelicStats import RelicStats
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from visualizer.visualizer import visualize

from characters.abundance.Lynx import Lynx
from characters.abundance.Luocha import Luocha

from characters.destruction.Arlan import Arlan
from characters.destruction.Blade import Blade
from characters.destruction.Clara import Clara
from characters.destruction.Hook import Hook
from characters.destruction.Jingliu import Jingliu
from characters.destruction.Lunae import Lunae

from characters.erudition.Argenti import Argenti
from characters.erudition.Herta import Herta
from characters.erudition.Himeko import Himeko
from characters.erudition.JingYuan import JingYuan
from characters.erudition.Serval import Serval
from characters.erudition.Qingque import Qingque

from characters.harmony.Asta import Asta
from characters.harmony.Bronya import Bronya
from characters.harmony.Hanya import Hanya
from characters.harmony.Tingyun import Tingyun

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

from lightCones.abundance.PostOpConversation import PostOpConversation
from lightCones.abundance.Multiplication import Multiplication

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

from lightCones.harmony.ButTheBattleIsntOver import ButTheBattleIsntOver
from lightCones.harmony.CarveTheMoonWeaveTheClouds import CarveTheMoonWeaveTheClouds
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.MeshingCogs import MeshingCogs
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous

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
from relicSets.relicSets.GrandDukeIncineratedToAshes import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.GuardOfWutheringSnow import GuardOfWutheringSnow2pc
from relicSets.relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc, HunterOfGlacialForest4pc
from relicSets.relicSets.KnightOfPurityPalace import KnightOfPurityPalace2pc, KnightOfPurityPalace4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc, MusketeerOfWildWheat4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc
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

def sumEffects(effectList:list):
    totalEffects = BaseEffect()
    for effect in effectList:
        totalEffects += effect
    return totalEffects

#%% Configuration
visualizationList = []

config = copy(Configuration)
config['numEnemies'] = 2
config['enemySpeed'] = 132 / 1.125 # assume 25% action delay every 2 enemy turns from toughness break

#%% Clara Topaz Asta Luocha Characters
ClaraCharacter = Clara(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.physical'],
                                substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                                lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=5.0, **config),
                                relicsetone = ChampionOfStreetwiseBoxing2pc(),
                                relicsettwo = ChampionOfStreetwiseBoxing4pc(),
                                planarset = InertSalsotto(),
                                **config)

TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'ATK.percent', 'CR', 'ATK.percent'],
                                substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                                lightcone = Swordplay(**config),
                                relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = InertSalsotto(),
                                **config)

AstaCharacter = Asta(RelicStats(mainstats = ['ER', 'ATK.percent', 'CR', 'ATK.percent'],
                                substats = {'CR': 8, 'CD': 12, 'HP.percent': 3, 'ATK.percent': 5}),
                                lightcone = PostOpConversation(**config),
                                relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                                **config)

LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                substats = {'ATK.percent': 5, 'SPD.flat': 12, 'HP.percent': 4, 'RES': 7}),
                                lightcone = Multiplication(**config),
                                relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                                **config)

#%% Clara Topaz Asta Luocha Team Buffs
for character in [TopazCharacter, ClaraCharacter, AstaCharacter]:
    character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
    
for character in [TopazCharacter, ClaraCharacter, LuochaCharacter]:
    character.addStat('CD',description='Broken Keel from Asta',amount=0.1)

# assume full uptime on asta ultimate and talentwith 2 turn rotation
for character in [TopazCharacter, ClaraCharacter, AstaCharacter]:
    character.addStat('SPD.flat',description='Asta Ultimate',
                      amount=53 if AstaCharacter.eidolon >= 5 else 50)
    character.addStat('ATK.percent',description='Asta Talent',
                      amount=0.154 if AstaCharacter.eidolon >= 3 else 0.14,
                      stacks=5)
    
# Luocha's uptime is lower because he is very fast with the multiplication light cone
LuochaCharacter.addStat('SPD.flat',description='Asta Ultimate',
                        amount=53 if AstaCharacter.eidolon >= 5 else 50, 
                        uptime=0.75)
LuochaCharacter.addStat('ATK.percent',description='Asta Talent',
                        amount=0.154 if AstaCharacter.eidolon >= 3 else 0.14,
                        stacks=5, uptime=0.75)
    
#%% Clara Topaz Asta Luocha Print Statements
ClaraCharacter.print()
TopazCharacter.print()
AstaCharacter.print()
LuochaCharacter.print()

#%% Clara Topaz Asta Luocha Rotations
# assume each elite performs 1 single target attack per turn
# times 2 as the rotation is 2 of her turns long
numEnemyAttacks = ClaraCharacter.enemySpeed * ClaraCharacter.numEnemies * 2 / ClaraCharacter.getTotalStat('SPD')
numEnhancedTalents = 2
numUnenhancedTalents = (numEnemyAttacks - numEnhancedTalents) * (5*6) / (5*6 + 3 + 4 + 4)
numSvarogCounters = numEnemyAttacks * (5*6) / (5*6 + 3 + 4 + 4)

ClaraCharacter.addStat('Vulnerability',description='Topaz Vulnerability',
                       amount=0.55 if TopazCharacter.eidolon>= 3 else 0.5,
                       uptime=1.0 / ClaraCharacter.numEnemies)
ClaraRotation = [ # 110 max energy
        ClaraCharacter.useSkill() * 2,
        ClaraCharacter.useMarkOfSvarog() * numSvarogCounters, 
        ClaraCharacter.useTalent(enhanced=True) * numEnhancedTalents,
        ClaraCharacter.useUltimate(),
]

ClaraCharacter.stats['Vulnerability'].pop() # remove the previous vulnerability buff
ClaraCharacter.addStat('Vulnerability',description='Topaz Vulnerability',
                       amount=0.55 if TopazCharacter.eidolon>= 3 else 0.5)
ClaraRotation.append(ClaraCharacter.useTalent(enhanced=False) * numUnenhancedTalents)

TopazRotation = [ # 130 max energy
        TopazCharacter.useBasic() * 4,
        TopazCharacter.useSkill(),
        TopazCharacter.useUltimate(),
        TopazCharacter.useTalent(windfall=True) * 2, # two talents from windfall
]

topazTurns = sum([x.actionvalue for x in TopazRotation])
claraTurns = sum([x.actionvalue for x in ClaraRotation])
numbyTurns = topazTurns * 80 / TopazCharacter.getTotalStat('SPD')
claraFollowups = (numEnhancedTalents + numUnenhancedTalents) * (topazTurns / TopazCharacter.getTotalStat('SPD')) / (claraTurns / ClaraCharacter.getTotalStat('SPD'))
numbyAdvanceForwards = (topazTurns + claraFollowups) * 3 / 8 # 6 topaz turns, treat each 50% advance forward as 37.5% of an advance forward    
TopazRotation.append(TopazCharacter.useTalent(windfall=False) * (numbyTurns + numbyAdvanceForwards)) # about 1 talent per basic/skill

AstaRotation = [AstaCharacter.useSkill() * 2,
                AstaCharacter.useUltimate() * 1,]

LuochaRotation = [LuochaCharacter.useBasic() * 3,
                  LuochaCharacter.useUltimate() * 1,
                  LuochaCharacter.useSkill() * 1,]
LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast

#%% Clara Topaz Asta Luocha Rotation Math

totalClaraEffect = sumEffects(ClaraRotation)
totalTopazEffect = sumEffects(TopazRotation)
totalAstaEffect = sumEffects(AstaRotation)
totalLuochaEffect = sumEffects(LuochaRotation)

ClaraRotationDuration = totalClaraEffect.actionvalue * 100.0 / ClaraCharacter.getTotalStat('SPD')
TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
AstaRotationDuration = totalAstaEffect.actionvalue * 100.0 / AstaCharacter.getTotalStat('SPD')
LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

print('##### Rotation Durations #####')
print('Clara: ',ClaraRotationDuration)
print('Topaz: ',TopazRotationDuration)
print('Asta: ',AstaRotationDuration)
print('Luocha: ',LuochaRotationDuration)

TopazRotation = [x * ClaraRotationDuration / TopazRotationDuration for x in TopazRotation]
AstaRotation = [x * ClaraRotationDuration / AstaRotationDuration for x in AstaRotation]
LuochaRotation = [x * ClaraRotationDuration / LuochaRotationDuration for x in LuochaRotation]

ClaraEstimate = DefaultEstimator('Clara: 2E {:.1f}T 1Q'.format(numSvarogCounters), ClaraRotation, ClaraCharacter, config)
TopazEstimate = DefaultEstimator('Topaz: 1E 4N {:.1f}T Q Windfall(2T)'.format((numbyTurns + numbyAdvanceForwards)), TopazRotation, TopazCharacter, config)
AstaEstimate = DefaultEstimator('Slow Asta: 2E 1Q, S5 Memories', AstaRotation, AstaCharacter, config)
LuochaEstimate = DefaultEstimator('Fast Luocha: 3N 1E 1Q, S5 Multiplication', LuochaRotation, LuochaCharacter, config)

visualizationList.append([ClaraEstimate, TopazEstimate, LuochaEstimate, AstaEstimate])

#%% Visualization
# Visualize
visualize(visualizationList, visualizerPath='visualizer\QuadVisual.png', **config)
    
from excelAPI.write2sheet import writeVisualizationList
writeVisualizationList(visualizationList,path='visualizer\QuadVisual.xlsx',sheetname='Quad vs Two')
