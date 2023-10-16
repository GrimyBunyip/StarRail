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

#%% Clara Clara Silver Wolf Pela Characters
ClaraCharacter = Clara(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.physical'],
                                substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                                lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=5.0, **config),
                                relicsetone = ChampionOfStreetwiseBoxing2pc(),
                                relicsettwo = ChampionOfStreetwiseBoxing4pc(),
                                planarset = InertSalsotto(),
                                **config)

SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'BreakEffect'],
                        substats = {'SPD.flat':12,'BreakEffect':8, 'ATK.percent': 5, 'ATK.flat': 3}),
                        lightcone = BeforeTheTutorialMissionStarts(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = BrokenKeel(),
                        **config)

PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                        substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
            lightcone = ResolutionShinesAsPearlsOfSweat(**config),
            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
            **config)

LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                lightcone = Multiplication(**config),
                                relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                                **config)

#%% Clara Clara Silver Wolf Pela Team Buffs
for character in [SilverWolfCharacter, ClaraCharacter, PelaCharacter]:
    character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
    
for character in [SilverWolfCharacter, ClaraCharacter, LuochaCharacter]:
    character.addStat('CD',description='Broken Keel from Pela',amount=0.1)

# Pela Debuffs, 3 turn pela rotation
pelaUltUptime = (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
pelaUltUptime = min(1.0, pelaUltUptime)
for character in [ClaraCharacter,SilverWolfCharacter,PelaCharacter,LuochaCharacter]:
    character.addStat('DefShred',description='Pela Ultimate',
                      amount=0.42 if PelaCharacter.eidolon >= 5 else 0.40,
                      uptime=pelaUltUptime)
    
# Resolution Shines as Pearls of Sweat uptime
sweatUptime = (1.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
sweatUptime += (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
sweatUptime = min(1.0, sweatUptime)
for character in [ClaraCharacter,SilverWolfCharacter,PelaCharacter,LuochaCharacter]:
    character.addStat('DefShred',description='Resolution Sweat',
                      amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                      uptime=sweatUptime)

# Silver Wolf Debuffs
swUltUptime = (2.0 / 2.0) * SilverWolfCharacter.getTotalStat('SPD') / SilverWolfCharacter.enemySpeed / SilverWolfCharacter.numEnemies
swUltUptime = min(1.0, swUltUptime)
swSkillUptime = (3.0 * 3.0 / 2.0) * SilverWolfCharacter.getTotalStat('SPD') / SilverWolfCharacter.enemySpeed / SilverWolfCharacter.numEnemies
swSkillUptime = min(1.0, swSkillUptime)

dmgResUptime:float=0.0 #we are already assuming we're hitting for weakness
allResUptime:float=swSkillUptime #might want to decrease this for large numbers of targets
defShredUptime:float=swUltUptime
talentAtkUptime:float=swSkillUptime
talentDefUptime:float=swSkillUptime
a6Uptime:float=swSkillUptime

for character in [ClaraCharacter, SilverWolfCharacter, PelaCharacter, LuochaCharacter]:
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
    
#%% Clara Clara Silver Wolf Pela Print Statements
ClaraCharacter.print()
SilverWolfCharacter.print()
PelaCharacter.print()
LuochaCharacter.print()

#%% Clara Clara Silver Wolf Pela Rotations

# assume each elite performs 1 single target attack per turn
# times 2 as the rotation is 2 of her turns long
numEnemyAttacks = ClaraCharacter.enemySpeed * ClaraCharacter.numEnemies * 2 / ClaraCharacter.getTotalStat('SPD')
numEnhancedTalents = 2
numUnenhancedTalents = (numEnemyAttacks - numEnhancedTalents) * (5*6) / (5*6 + 3 + 4 + 4)
numSvarogCounters = numEnemyAttacks * (5*6) / (5*6 + 3 + 4 + 4)

ClaraRotation = [ # 110 max energy
        ClaraCharacter.useSkill() * 2,
        ClaraCharacter.useMarkOfSvarog() * numSvarogCounters, 
        ClaraCharacter.useTalent(enhanced=True) * numEnhancedTalents,
        ClaraCharacter.useUltimate(),
        ClaraCharacter.useTalent(enhanced=False) * numUnenhancedTalents,
]

numSkillSW = 2
numUltSW = 1
SilverWolfRotation = [ # 
        SilverWolfCharacter.useSkill() * numSkillSW, #
        SilverWolfCharacter.useUltimate() * numUltSW, #
]

PelaRotation = [PelaCharacter.useBasic() * 3,
                PelaCharacter.useUltimate(),]

LuochaRotation = [LuochaCharacter.useBasic() * 3,
                  LuochaCharacter.useUltimate() * 1,
                  LuochaCharacter.useSkill() * 1,]
LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast

totalClaraEffect = sumEffects(ClaraRotation)
totalSilverWolfEffect = sumEffects(SilverWolfRotation)
totalPelaEffect = sumEffects(PelaRotation)
totalLuochaEffect = sumEffects(LuochaRotation)

ClaraRotationDuration = totalClaraEffect.actionvalue * 100.0 / ClaraCharacter.getTotalStat('SPD')
SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

print('##### Rotation Durations #####')
print('Clara: ',ClaraRotationDuration)
print('Silver Wolf: ',SilverWolfRotationDuration)
print('Pela: ',PelaRotationDuration)
print('Luocha: ',LuochaRotationDuration)

SilverWolfRotation = [x * ClaraRotationDuration / SilverWolfRotationDuration for x in SilverWolfRotation]
PelaRotation = [x * ClaraRotationDuration / PelaRotationDuration for x in PelaRotation]
LuochaRotation = [x * ClaraRotationDuration / LuochaRotationDuration for x in LuochaRotation]

ClaraEstimate = DefaultEstimator('Clara: 2E {:.1f}T 1Q'.format(numSvarogCounters), ClaraRotation, ClaraCharacter, config)
SilverWolfEstimate = DefaultEstimator('SilverWolf {:.0f}E {:.0f}Q'.format(numSkillSW, numUltSW), SilverWolfRotation, SilverWolfCharacter, config)
PelaEstimate = DefaultEstimator('Pela: 3N 1Q, S5 Sweat', PelaRotation, PelaCharacter, config)
LuochaEstimate = DefaultEstimator('Fast Luocha: 3N 1E 1Q, S5 Multiplication', LuochaRotation, LuochaCharacter, config)

visualizationList.append([ClaraEstimate, SilverWolfEstimate, PelaEstimate, LuochaEstimate])

#%% Visualization
# Visualize
visualize(visualizationList, visualizerPath='visualizer\QuadVisual.png', **config)
    
from excelAPI.write2sheet import writeVisualizationList
writeVisualizationList(visualizationList,path='visualizer\QuadVisual.xlsx',sheetname='Quad vs Two')