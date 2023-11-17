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
from characters.harmony.Yukong import Yukong

from characters.hunt.DanHeng import DanHeng
from characters.hunt.Seele import Seele
from characters.hunt.Sushang import Sushang
from characters.hunt.Topaz import Topaz
from characters.hunt.Yanqing import Yanqing

from characters.nihility.Guinaifen import Guinaifen
from characters.nihility.Kafka import Kafka
from characters.nihility.Luka import Luka
from characters.nihility.Pela import Pela
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
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
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
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.PanCosmicCommercialEnterprise import PanCosmicCommercialEnterprise
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.planarSets.TaliaKingdomOfBanditry import TaliaKingdomOfBanditry

def sumEffects(effectList:list):
    totalEffects = BaseEffect()
    for effect in effectList:
        totalEffects += effect
    return totalEffects

visualizationList = []

config = copy(Configuration)
config['numEnemies'] = 2
config['enemySpeed'] = 190 / 1.125 # assume 25% action delay every 2 enemy turns from toughness break

#%% Seele MID Silver Wolf Bronya Characters
SeeleCharacter = Seele(relicstats = RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.quantum'],
                        substats = {'CD': 12, 'CR': 8, 'ATK.percent': 5, 'SPD.flat': 3}),
                        lightcone = CruisingInTheStellarSea(**config),
                        relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo=GeniusOfBrilliantStars4pc(), planarset = RutilantArena(),
                        **config)

SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'BreakEffect'],
                        substats = {'SPD.flat':12,'BreakEffect':8, 'ATK.percent': 5, 'ATK.flat': 3}),
                        lightcone = BeforeTheTutorialMissionStarts(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = PenaconyLandOfDreams(),
                        **config)

BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'ER'],
                        substats = {'CD': 12, 'SPD.flat': 8, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = PastAndFuture(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)

#%% Seele MID Silver Wolf Bronya Team Buffs
for character in [SilverWolfCharacter, SeeleCharacter, BronyaCharacter]:
    character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
    
for character in [SilverWolfCharacter, SeeleCharacter, LuochaCharacter]:
    character.addStat('CD',description='Broken Keel from Bronya',amount=0.1)

for character in [SilverWolfCharacter, SeeleCharacter, LuochaCharacter]:
    character.addStat('DMG.quantum',description='Penacony from Silver Wolf',amount=0.1)

# Silver Wolf Debuffs, do not divide by speed since single target
swUltUptime = (2.0 / 2.0) * SilverWolfCharacter.getTotalStat('SPD') / SilverWolfCharacter.enemySpeed
swUltUptime = min(1.0, swUltUptime)
swSkillUptime = (3.0 * 3.0 / 2.0) * SilverWolfCharacter.getTotalStat('SPD') / SilverWolfCharacter.enemySpeed
swSkillUptime = min(1.0, swSkillUptime)

dmgResUptime:float=0.0 #we are already assuming we're hitting for weakness
allResUptime:float=swSkillUptime #might want to decrease this for large numbers of targets
defShredUptime:float=swUltUptime
talentAtkUptime:float=swSkillUptime
talentDefUptime:float=swSkillUptime
a6Uptime:float=swSkillUptime

# handle this separately for seele, assume it doesn't apply to her basics
for character in [SilverWolfCharacter, LuochaCharacter]:
    character.addStat('ResPen',description='talent',amount=0.20,uptime=dmgResUptime)
    character.addStat('ResPen',description='skill',
                    amount=0.105 if SilverWolfCharacter.eidolon >= 3 else 0.10,
                    uptime=allResUptime)
    character.addStat('DefShred',description='ultimate',
                    amount=0.468 if SilverWolfCharacter.eidolon >= 5 else 0.45,
                    uptime=defShredUptime)
    character.addStat('DefShred',description='talent',
                    amount=0.088 if SilverWolfCharacter.eidolon >= 3 else 0.08,
                    uptime=talentDefUptime)
    character.addStat('ResPen',description='trace',amount=0.03,uptime=a6Uptime)

# Bronya Messenger Buff
for character in [SeeleCharacter, SilverWolfCharacter, LuochaCharacter]:
    character.addStat('DMG',description='Bronya A6',amount=0.10)
    character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)

# Bronya Buffs
SeeleCharacter.addStat('DMG',description='Bronya Skill', amount=0.726 if BronyaCharacter.eidolon >= 5 else 0.66, uptime=0.5)
SeeleCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition, uptime=0.5)
SeeleCharacter.addStat('ATK.percent',description='Bronya Ult',
                       amount=0.594 if BronyaCharacter.eidolon >= 3 else 0.55,
                       uptime=0.25) # only get bronya ult buff every 4 rotations
SeeleCharacter.addStat('CD',description='Bronya Ult',
                       amount=(0.168 * BronyaCharacter.getTotalStat('CD') + 0.216) if BronyaCharacter.eidolon >= 3 else (0.16 * BronyaCharacter.getTotalStat('CD') + 0.2),
                       uptime=0.25) # only get bronya ult buff every 4 rotations
    
#%% Seele MID Silver Wolf Bronya Print Statements
SeeleCharacter.print()
SilverWolfCharacter.print()
BronyaCharacter.print()
LuochaCharacter.print()

#%% Seele MID Silver Wolf Bronya Rotations

SeeleRotation = [ # endTurn needed to factor in resurgence buff
        SeeleCharacter.useBasic(),
        SeeleCharacter.useUltimate(), # use ult to trigger resurgence, on an enemy that isn't debuffed yet
]

# Apply silver wolf debuffs to the main target only, assume it doesn't affect Seele's Basics
SeeleCharacter.addStat('ResPen',description='talent',amount=0.20,uptime=dmgResUptime)
SeeleCharacter.addStat('ResPen',description='skill',
                amount=0.105 if SilverWolfCharacter.eidolon >= 3 else 0.10,
                uptime=allResUptime)
SeeleCharacter.addStat('DefShred',description='ultimate',
                amount=0.468 if SilverWolfCharacter.eidolon >= 5 else 0.45,
                uptime=defShredUptime)
SeeleCharacter.addStat('DefShred',description='talent',
                amount=0.088 if SilverWolfCharacter.eidolon >= 3 else 0.08,
                uptime=talentDefUptime)
SeeleCharacter.addStat('ResPen',description='trace',amount=0.03,uptime=a6Uptime)

SeeleRotation += [ # endTurn needed to factor in resurgence buff
    SeeleCharacter.useBasic() * 1,
    SeeleCharacter.useResurgence(),
    SeeleCharacter.useSkill() * 2,
    SeeleCharacter.endTurn(),
    BronyaCharacter.useAdvanceForward() * 1.1, # minus 0.4, to ignore the two advance forwards from basics
]

numBasicSW = 2
numSkillSW = 1
numUltSW = 1
SilverWolfRotation = [ # 
        SilverWolfCharacter.useBasic() * numBasicSW,
        SilverWolfCharacter.useSkill() * numSkillSW, #
        SilverWolfCharacter.useUltimate() * numUltSW, #
]

BronyaRotation = [BronyaCharacter.useSkill() * 4,
                  BronyaCharacter.useUltimate(),]

LuochaRotation = [LuochaCharacter.useBasic() * 3,
                  LuochaCharacter.useUltimate() * 1,
                  LuochaCharacter.useSkill() * 1,]
LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast

#%% Seele MID SilverWolf Bronya Luocha Rotation Math

totalSeeleEffect = sumEffects(SeeleRotation)
totalBronyaEffect = sumEffects(BronyaRotation)
totalSilverWolfEffect = sumEffects(SilverWolfRotation)
totalLuochaEffect = sumEffects(LuochaRotation)

SeeleRotationDuration = totalSeeleEffect.actionvalue * 100.0 / SeeleCharacter.getTotalStat('SPD')
BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

print('##### Rotation Durations #####')
print('Seele: ',SeeleRotationDuration)
print('Bronya: ',BronyaRotationDuration)
print('SilverWolf: ',SilverWolfRotationDuration)
print('Luocha: ',LuochaRotationDuration)

# Scale other character's rotation
BronyaRotation = [x * SeeleRotationDuration / BronyaRotationDuration for x in BronyaRotation]
SilverWolfRotation = [x * SeeleRotationDuration / SilverWolfRotationDuration for x in SilverWolfRotation]
LuochaRotation = [x * SeeleRotationDuration / LuochaRotationDuration for x in LuochaRotation]

SeeleEstimate = DefaultEstimator('Seele Ult Resurgence: 2N 1Resurgence(2E1Q)', SeeleRotation, SeeleCharacter, config)
BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                  BronyaRotation, BronyaCharacter, config)
SilverWolfEstimate = DefaultEstimator(f'SilverWolf {numBasicSW:.0f}N {numSkillSW:.0f}E {numUltSW:.0f}Q', SilverWolfRotation, SilverWolfCharacter, config)
LuochaEstimate = DefaultEstimator(f'Luocha: 3N 1E 1Q, S{LuochaCharacter.lightcone.superposition:d} {LuochaCharacter.lightcone.name}', 
                                  LuochaRotation, LuochaCharacter, config)

#Seele is too fast for slow bronya. And we don't have enough SP to go faster
SeeleEstimate.effect.actionvalue *= (BronyaRotationDuration / 4) / (SeeleRotationDuration / 1.5 )

visualizationList.append([SeeleEstimate, SilverWolfEstimate, BronyaEstimate, LuochaEstimate])

#%% Visualization
# Visualize
visualize(visualizationList, visualizerPath='visualizer\QuadVisualMisc.png', **config)
    
from excelAPI.write2sheet import writeVisualizationList
writeVisualizationList(visualizationList,path='visualizer\QuadVisualMisc.xlsx',sheetname='Quad vs Two Misc')