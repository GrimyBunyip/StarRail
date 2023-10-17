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
#config['enemyType'] = 'basic'
config['enemySpeed'] = 132 / 1.125 # assume 25% action delay every 2 enemy turns from toughness break

#%% Clara Topaz Asta Luocha Characters
ClaraCharacter = Clara(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.physical'],
                                substats = {'CR': 8, 'CD': 12, 'ATK.percent': 3, 'SPD.flat': 5}),
                                lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=5.0, **config),
                                relicsetone = ChampionOfStreetwiseBoxing2pc(),
                                relicsettwo = ChampionOfStreetwiseBoxing4pc(),
                                planarset = FirmamentFrontlineGlamoth(stacks=2),
                                **config)

TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'ATK.percent', 'CR', 'ATK.percent'],
                                substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                                lightcone = Swordplay(**config),
                                relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                                **config)

AstaCharacter = Asta(RelicStats(mainstats = ['ER', 'ATK.percent', 'CR', 'ATK.percent'],
                                substats = {'CR': 8, 'CD': 12, 'HP.percent': 3, 'ATK.percent': 5}),
                                lightcone = MemoriesOfThePast(**config),
                                relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(uptime=0.5), planarset = BrokenKeel(),
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

# messenger 4 pc buffs:
ClaraCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
TopazCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5*3/4)

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

# Asta Ignite Buff
TopazCharacter.addStat('DMG.fire',description='trace',amount=0.18)

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
claraFollowups = (numEnhancedTalents + numUnenhancedTalents / TopazCharacter.numEnemies) * (topazTurns / TopazCharacter.getTotalStat('SPD')) / (claraTurns / ClaraCharacter.getTotalStat('SPD'))
numbyAdvanceForwards = topazTurns / 2 + claraFollowups * 3 / 8 # treat clara followups as 0.375 advances because they might be out of sync    
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

# Scale other character's rotation
TopazRotation = [x * ClaraRotationDuration / TopazRotationDuration for x in TopazRotation]
AstaRotation = [x * ClaraRotationDuration / AstaRotationDuration for x in AstaRotation]
LuochaRotation = [x * ClaraRotationDuration / LuochaRotationDuration for x in LuochaRotation]

ClaraEstimate = DefaultEstimator('Clara: 2E {:.1f}T 1Q'.format(numSvarogCounters), ClaraRotation, ClaraCharacter, config)
TopazEstimate = DefaultEstimator('Topaz: 1E 4N {:.1f}T Q Windfall(2T)'.format((numbyTurns + numbyAdvanceForwards)), TopazRotation, TopazCharacter, config)
AstaEstimate = DefaultEstimator('Slow Asta: 2E 1Q, S{:.0f} {}'.format(AstaCharacter.lightcone.superposition, AstaCharacter.lightcone.name), 
                                AstaRotation, AstaCharacter, config)
LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                  LuochaRotation, LuochaCharacter, config)

visualizationList.append([ClaraEstimate, TopazEstimate, LuochaEstimate, AstaEstimate])

#%% Jingliu Bronya Pela Luocha Characters
JingliuCharacter = Jingliu(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.ice'],
                            substats = {'CR': 12, 'CD': 8, 'SPD.flat': 3, 'ATK.percent': 5}),
            lightcone = OnTheFallOfAnAeon(uptime = 0.25, **config),
            relicsetone = HunterOfGlacialForest2pc(), relicsettwo = HunterOfGlacialForest4pc(uptime=0.4), planarset = RutilantArena(uptime=0.0),
            **config)

BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'HP.percent', 'CD', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
            lightcone = PastAndFuture(**config),
            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
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

#%% Jingliu Bronya Pela Luocha Team Buffs
# only enhanced skills have rutilant arena buff
JingliuCharacter.addStat('DMG',description='Rutilant Arena', amount=0.20, type=['enhancedSkill']) # take care of rutilant arena manually

# Broken Keel Buff
for character in [JingliuCharacter, BronyaCharacter, PelaCharacter]:
    character.addStat('CD',description='Broken Keel Luocha',amount=0.10)
for character in [JingliuCharacter, BronyaCharacter, LuochaCharacter]:
    character.addStat('CD',description='Broken Keel Pela',amount=0.10)
for character in [JingliuCharacter, PelaCharacter, LuochaCharacter]:
    character.addStat('CD',description='Broken Keel Bronya',amount=0.10)

# Bronya A6 and Messenger 4 pc
for character in [JingliuCharacter, PelaCharacter, LuochaCharacter]:
    character.addStat('DMG',description='Bronya A6',amount=0.10)
    character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/5.0)

# Pela Debuffs, 3 turn pela rotation
pelaUltUptime = (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
pelaUltUptime = min(1.0, pelaUltUptime)
for character in [JingliuCharacter,BronyaCharacter,PelaCharacter,LuochaCharacter]:
    character.addStat('DefShred',description='Pela Ultimate',
                      amount=0.42 if PelaCharacter.eidolon >= 5 else 0.40,
                      uptime=pelaUltUptime)
    
# Resolution Shines as Pearls of Sweat uptime
sweatUptime = (1.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
sweatUptime += (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
sweatUptime = min(1.0, sweatUptime)
for character in [JingliuCharacter,BronyaCharacter,PelaCharacter,LuochaCharacter]:
    character.addStat('DefShred',description='Resolution Sweat',
                      amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                      uptime=sweatUptime)

#%% Jingliu Bronya Pela Luocha Print Statements
JingliuCharacter.print()
BronyaCharacter.print()
PelaCharacter.print()
LuochaCharacter.print()

#%% Jingliu Bronya Pela Luocha Rotations
BronyaRotation = [BronyaCharacter.useSkill() * 4,
                  BronyaCharacter.useUltimate(),]

# Assume Bronya skill buff applies to skills, and only applies a fraction of the time to the remaining abilities
numSkill = 2.0
numEnhanced = 3.0
numUlt = 1.0

JingliuRotation = []

# 1 skill should have bronya buff, 1 should not.
JingliuRotation += [JingliuCharacter.useSkill()]
JingliuCharacter.addStat('DMG',description='Bronya Skill', amount=0.726 if JingliuCharacter.eidolon >= 5 else 0.66)
JingliuCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition)
JingliuRotation += [JingliuCharacter.useSkill()]
JingliuCharacter.stats['DMG'].pop() # remove bronya skill buff
JingliuCharacter.stats['DMG'].pop() # remove past and future

# 2 enhanced skills will not have bronya buff
JingliuRotation += [JingliuCharacter.useEnhancedSkill() * 2]

# 1 enhanced skill and the ultimate will both have bronya buff
JingliuCharacter.addStat('DMG',description='Bronya Skill', amount=0.726 if JingliuCharacter.eidolon >= 5 else 0.66)
JingliuCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition)
JingliuCharacter.addStat('ATK.percent',description='Bronya Ult',
                       amount=0.594 if BronyaCharacter.eidolon >= 3 else 0.55,
                       uptime=0.5) # only get bronya ult buff every other rotation
JingliuCharacter.addStat('CD',description='Bronya Ult',
                       amount=(0.168 * BronyaCharacter.getTotalStat('CD') + 0.216) if BronyaCharacter.eidolon >= 3 else (0.16 * BronyaCharacter.getTotalStat('CD') + 0.2),
                       uptime=0.5) # only get bronya ult buff every other rotation
JingliuRotation += [JingliuCharacter.useEnhancedSkill()]
JingliuRotation += [JingliuCharacter.useUltimate()]
JingliuRotation += [JingliuCharacter.extraTurn() * 0.9] # multiply by 0.9 because it tends to overlap with skill advances
JingliuRotation += [BronyaCharacter.useAdvanceForward() * 2] #Jingliu rotation is basically 4 turns

PelaRotation = [PelaCharacter.useBasic() * 3,
                PelaCharacter.useUltimate(),]

LuochaRotation = [LuochaCharacter.useBasic() * 3,
                  LuochaCharacter.useUltimate() * 1,
                  LuochaCharacter.useSkill() * 1,]
LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast

#%% Jingliu Bronya Pela Luocha Rotation Math
totalJingliuEffect = sumEffects(JingliuRotation)
totalBronyaEffect = sumEffects(BronyaRotation)
totalPelaEffect = sumEffects(PelaRotation)
totalLuochaEffect = sumEffects(LuochaRotation)

JingliuRotationDuration = totalJingliuEffect.actionvalue * 100.0 / JingliuCharacter.getTotalStat('SPD')
BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

print('##### Rotation Durations #####')
print('Jingliu: ',JingliuRotationDuration)
print('Bronya: ',BronyaRotationDuration)
print('Pela: ',PelaRotationDuration)
print('Luocha: ',LuochaRotationDuration)

# scale other character's rotation
BronyaRotation = [x * JingliuRotationDuration / BronyaRotationDuration for x in BronyaRotation]
PelaRotation = [x * JingliuRotationDuration / PelaRotationDuration for x in PelaRotation]
LuochaRotation = [x * JingliuRotationDuration / LuochaRotationDuration for x in LuochaRotation]

JingliuEstimate = DefaultEstimator('Jingliu {:.0f}E {:.0f}Moon {:.0f}Q'.format(numSkill, numEnhanced, numUlt),
                                                JingliuRotation, JingliuCharacter, config)
BronyaEstimate = DefaultEstimator('E0 Bronya S{:.0f} {}, 12 Spd Substats'.format(BronyaCharacter.lightcone.superposition, BronyaCharacter.lightcone.name), 
                                  BronyaRotation, BronyaCharacter, config)
PelaEstimate = DefaultEstimator('Pela: 3N 1Q, S{:.0f} {}'.format(PelaCharacter.lightcone.superposition, PelaCharacter.lightcone.name), 
                                PelaRotation, PelaCharacter, config)
LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name),
                                  LuochaRotation, LuochaCharacter, config)

visualizationList.append([JingliuEstimate, BronyaEstimate, PelaEstimate, LuochaEstimate])

#%% Lunae Hanya Yukong Luocha Characters
LunaeCharacter = Lunae(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.imaginary'],
                        substats = {'CR': 8, 'CD': 12, 'ATK.percent': 3, 'SPD.flat': 5}),
                        lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=4.0, **config),
                        relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = WastelanderOfBanditryDesert4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                        substats = {'RES': 7, 'SPD.flat': 12, 'CD': 5, 'CR': 4}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

YukongCharacter = Yukong(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.imaginary'],
                        substats = {'CR': 3, 'CD': 6, 'SPD.flat': 12, 'RES': 7}),
                        lightcone = PlanetaryRendezvous(**config),
                        relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)

LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                substats = {'ATK.percent': 5, 'SPD.flat': 12, 'HP.percent': 4, 'RES': 7}),
                                lightcone = Multiplication(**config),
                                relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                                **config)

#%% Lunae Hanya Yukong Luocha Team Buffs
# Broken Keel Buffs
for character in [LunaeCharacter, YukongCharacter, LuochaCharacter]:
    character.addStat('CD',description='Broken Keel from Hanya',amount=0.1)
for character in [LunaeCharacter, HanyaCharacter, LuochaCharacter]:
    character.addStat('CD',description='Broken Keel from Yukong',amount=0.1)
for character in [LunaeCharacter, HanyaCharacter, YukongCharacter]:
    character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
    
# Planetary Rendezvous
for character in [LunaeCharacter, YukongCharacter, LuochaCharacter]:
    character.addStat('DMG',description='Planetary Rendeezvous',
                      amount=0.09 + 0.03 * YukongCharacter.lightcone.superposition,
                      type=['imaginary'])
    
# Yukong imaginary damage trace
for character in [LunaeCharacter, LuochaCharacter]:
    character.addStat('DMG',description='Yukong trace',amount=0.12,type=['imaginary'])

# apply buffs now that we calculated approximate rotation times
LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)
for character in [LunaeCharacter, YukongCharacter]:
    character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
for character in [LunaeCharacter, YukongCharacter, LuochaCharacter]:
    character.addStat('ATK.percent',description='Hanya trace',amount=0.10,uptime=0.5)
    character.addStat('DMG',description='Burden',amount=0.33 if HanyaCharacter.eidolon >= 5 else 0.30)

LunaeCharacter.addStat('SPD.flat',description='Hanya Ult',amount=(0.21 if HanyaCharacter.eidolon >= 5 else 0.20) * HanyaCharacter.getTotalStat('SPD'))
LunaeCharacter.addStat('ATK.percent',description='Hanya Ult',amount=0.648 if HanyaCharacter.eidolon >= 5 else 0.60)

# Estimate Yukong Buffs.
# Yukong rotation is 11% slower than Lunae per turn
# Yukong rotation generates 5 bowstrings and 1 ult buff per 4 turn rotation
# not going to assume meticulous speed tuning here
for character in [LunaeCharacter, HanyaCharacter, YukongCharacter, LuochaCharacter]:
    
    character.addStat('ATK.percent',description='Roaring Bowstrings',
                    amount=0.88 if YukongCharacter.eidolon >= 3 else 0.80,
                    uptime=5.0 / 4.0 / 4.0 / 1.11) # 5 bowstrings, 4 characters, 4 turn rotation, Yukong is 11% slower
    
    character.addStat('CR',description='Yukong ultimate',
                    amount=0.294 if YukongCharacter.eidolon >= 5 else 0.28,
                    uptime=1.0 / 4.0 / 4.0 / 1.11) # 1 ult buff, 4 characters, 4 turn rotation, Yukong is 11% slower
    character.addStat('CD',description='Yukong ultimate',
                    amount=0.702 if YukongCharacter.eidolon >= 5 else 0.65,
                    uptime=1.0 / 4.0 / 4.0 / 1.11)

#%% Lunae Hanya Yukong Luocha Print Statements
LunaeCharacter.print()
HanyaCharacter.print()
YukongCharacter.print()
LuochaCharacter.print()

#%% Lunae Hanya Yukong Luocha Rotations
numHanyaSkill = 3
numHanyaUlt = 1
HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                HanyaCharacter.useUltimate() * numHanyaUlt]
    
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
            LunaeCharacter.endTurn(),
]

YukongRotation = [ # 
            YukongCharacter.useEnhancedBasic() * 2,
            YukongCharacter.useSkill() * 2,
            YukongCharacter.useUltimate(),
    ]

LuochaRotation = [LuochaCharacter.useBasic() * 3,
                  LuochaCharacter.useUltimate() * 1,
                  LuochaCharacter.useSkill() * 1,]
LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast

#%% Lunae Hanya Yukong Luocha Rotation Math
totalLunaeEffect = sumEffects(LunaeRotation)
totalHanyaEffect = sumEffects(HanyaRotation)
totalYukongEffect = sumEffects(YukongRotation)
totalLuochaEffect = sumEffects(LuochaRotation)

LunaeRotationDuration = totalLunaeEffect.actionvalue * 100.0 / LunaeCharacter.getTotalStat('SPD')
HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
YukongRotationDuration = totalYukongEffect.actionvalue * 100.0 / YukongCharacter.getTotalStat('SPD')
LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

# scale other character's rotation
HanyaRotation = [x * LunaeRotationDuration / HanyaRotationDuration for x in HanyaRotation]
YukongRotation = [x * LunaeRotationDuration / YukongRotationDuration for x in YukongRotation]
LuochaRotation = [x * LunaeRotationDuration / LuochaRotationDuration for x in LuochaRotation]

LunaeEstimate = DefaultEstimator('Lunae: 2N^3 1Q', LunaeRotation, LunaeCharacter, config)
HanyaEstimate = DefaultEstimator('Hanya 2.5 SP per E {:.0f}E {:.0f}Q S{:.0f} {}, 12 Spd Substats'.format(numHanyaSkill, numHanyaUlt,
                                HanyaCharacter.lightcone.superposition, HanyaCharacter.lightcone.name), 
                                HanyaRotation, HanyaCharacter, config)
YukongEstimate = DefaultEstimator('Yukong (No Speed Tuning) 2N 2E 1Q S{:.0f} {}'.format(YukongCharacter.lightcone.superposition, YukongCharacter.lightcone.name), 
                                  YukongRotation, YukongCharacter, config)
LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                  LuochaRotation, LuochaCharacter, config)

visualizationList.append([LunaeEstimate,HanyaEstimate,YukongEstimate,LuochaEstimate])

#%% Kafka Guinaifen Hanya Luocha Characters
KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'BreakEffect': 5, 'ATK.flat': 3}),
                        lightcone = GoodNightAndSleepWell(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

GuinaifenCharacter = Guinaifen(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.fire'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'EHR': 4, 'BreakEffect': 4}),
                        lightcone = GoodNightAndSleepWell(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

# I'm just going to assume 100% uptime on firmament frontline glamoth
# Kafka and Guinaifen are a few substats short of base 160 with a 12 substat cap
# But I'll just generously assume you are able to get there

HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'CR': 5, 'BreakEffect': 3}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = FleetOfTheAgeless(),
                        **config)

LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                lightcone = Multiplication(**config),
                                relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                                **config)

#%% Kafka Guinaifen Hanya Luocha Team Buffs
# Fleet of the Ageless Buff
for character in [KafkaCharacter, GuinaifenCharacter, HanyaCharacter]:
    character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)
for character in [KafkaCharacter, GuinaifenCharacter, LuochaCharacter]:
    character.addStat('ATK.percent',description='Fleet Asta',amount=0.08)
    
# Give Guinaifen Vulnerability to all other characters
for character in [KafkaCharacter, HanyaCharacter, LuochaCharacter]:
    character.addStat('Vulnerability',description='Guinaifen Vulnerability',
                        amount=0.076 if GuinaifenCharacter.eidolon >= 5 else 0.07,
                        stacks=min(GuinaifenCharacter.firekissStacks,4.0 if GuinaifenCharacter.eidolon >= 6 else 3.0))
    
# messenger 4 pc buffs:
KafkaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0 / 3.0)
GuinaifenCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0 / 3.0)
LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0 / 4.0)

for character in [KafkaCharacter, GuinaifenCharacter, LuochaCharacter]:
    character.addStat('ATK.percent',description='Hanya trace',amount=0.10,uptime=0.5)
    character.addStat('DMG',description='Burden',amount=0.33 if HanyaCharacter.eidolon >= 5 else 0.30)
KafkaCharacter.addStat('SPD.flat',description='Hanya Ult',amount=(0.21 if HanyaCharacter.eidolon >= 5 else 0.20) * HanyaCharacter.getTotalStat('SPD'))
KafkaCharacter.addStat('ATK.percent',description='Hanya Ult',amount=0.648 if HanyaCharacter.eidolon >= 5 else 0.60)

#%% Kafka Guinaifen Hanya Luocha Print Statements
KafkaCharacter.print()
GuinaifenCharacter.print()
HanyaCharacter.print()
LuochaCharacter.print()

#%% Kafka Guinaifen Hanya Luocha Rotations
numSkill = 3.0
numTalent = 3.0
numUlt = 1.0
GuinaifenDot = GuinaifenCharacter.useDot()
GuinaifenDot.energy = 0.0 # kafka shouldn't be getting energy for Guinaifen Dot
extraDots = [ GuinaifenDot ]
extraDotsUlt = [ GuinaifenDot * KafkaCharacter.numEnemies ]
KafkaRotation = [
        KafkaCharacter.useSkill(extraDots=extraDots) * numSkill,
        KafkaCharacter.useTalent() * numTalent,
        KafkaCharacter.useUltimate(extraDots=extraDotsUlt) * numUlt,
]

numSkillGuinaifen = 3.0
numUltGuinaifen = 1.0

numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)

GuinaifenRotation = [ # 
        GuinaifenCharacter.useSkill() * numSkillGuinaifen,
        GuinaifenCharacter.useUltimate() * numUlt,
]

numHanyaSkill = 3
numHanyaUlt = 1
HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                HanyaCharacter.useUltimate() * numHanyaUlt]
    
LuochaRotation = [LuochaCharacter.useBasic() * 3,
                  LuochaCharacter.useUltimate() * 1,
                  LuochaCharacter.useSkill() * 1,]
LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast


#%% Kafka Guinaifen Hanya Luocha Rotation Math
numDotGuinaifen = DotEstimator(GuinaifenRotation, GuinaifenCharacter, config, dotMode='alwaysBlast')
numDotGuinaifen = min(numDotGuinaifen, 2.0 * numSkillGuinaifen * min(3.0, GuinaifenCharacter.numEnemies))

totalKafkaEffect = sumEffects(KafkaRotation)
totalGuinaifenEffect = sumEffects(GuinaifenRotation)
totalHanyaEffect = sumEffects(HanyaRotation)
totalLuochaEffect = sumEffects(LuochaRotation)

KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
GuinaifenRotationDuration = totalGuinaifenEffect.actionvalue * 100.0 / GuinaifenCharacter.getTotalStat('SPD')
HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

# scale other character's character's rotation
GuinaifenRotation = [x * KafkaRotationDuration / GuinaifenRotationDuration for x in GuinaifenRotation]
HanyaRotation = [x * KafkaRotationDuration / HanyaRotationDuration for x in HanyaRotation]
LuochaRotation = [x * KafkaRotationDuration / LuochaRotationDuration for x in LuochaRotation]
numDotGuinaifen *= KafkaRotationDuration / GuinaifenRotationDuration

KafkaEstimate = DefaultEstimator('Kafka {:.0f}E {:.0f}T {:.0f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDotKafka),
                                 KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
GuinaifenEstimate = DefaultEstimator('E6 Guinaifen S5 GNSW {:.0f}E {:.0f}Q {:.1f}Dot'.format(numSkillGuinaifen, numUltGuinaifen, numDotGuinaifen),
                                     GuinaifenRotation, GuinaifenCharacter, config, numDot=numDotGuinaifen)
HanyaEstimate = DefaultEstimator('Hanya 2.5 SP per E {:.0f}E {:.0f}Q S{:.0f} {}, 12 Spd Substats'.format(numHanyaSkill, numHanyaUlt,
                                HanyaCharacter.lightcone.superposition, HanyaCharacter.lightcone.name), 
                                HanyaRotation, HanyaCharacter, config)
LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                  LuochaRotation, LuochaCharacter, config)

visualizationList.append([KafkaEstimate, GuinaifenEstimate, HanyaEstimate, LuochaEstimate])

#%% Kafka Guinaifen Sampo Luocha
KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'BreakEffect': 5, 'ATK.flat': 3}),
                        lightcone = GoodNightAndSleepWell(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

GuinaifenCharacter = Guinaifen(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.fire'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'EHR': 4, 'BreakEffect': 4}),
                        lightcone = GoodNightAndSleepWell(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

# I'm just going to assume 100% uptime on firmament frontline glamoth
# Kafka and Guinaifen are a few substats short of base 160 with a 12 substat cap
# But I'll just generously assume you are able to get there

SampoCharacter = Sampo(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.wind'],
                                substats = {'ATK.percent': 5, 'SPD.flat': 12, 'EHR': 8, 'BreakEffect': 3}),
                                lightcone = GoodNightAndSleepWell(**config),
                                relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                                **config)

LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                lightcone = Multiplication(**config),
                                relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                                **config)

#%% Kafka Guinaifen Sampo Luocha Team Buffs
# Fleet of the Ageless Buff
for character in [KafkaCharacter, GuinaifenCharacter, SampoCharacter]:
    character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)
    
# Give Guinaifen Vulnerability to all other characters
for character in [KafkaCharacter, SampoCharacter, LuochaCharacter]:
    character.addStat('Vulnerability',description='Guinaifen Vulnerability',
                        amount=0.076 if GuinaifenCharacter.eidolon >= 5 else 0.07,
                        stacks=min(GuinaifenCharacter.firekissStacks,4.0 if GuinaifenCharacter.eidolon >= 6 else 3.0))
    
for character in [KafkaCharacter, GuinaifenCharacter, LuochaCharacter]:
    character.addStat('Vulnerability',description='Sampo Vulnerability',
                       amount=0.32 if SampoCharacter.eidolon >= 5 else 0.3,
                       uptime=SampoCharacter.ultUptime)

#%% Kafka Guinaifen Sampo Luocha Print Statements
KafkaCharacter.print()
GuinaifenCharacter.print()
SampoCharacter.print()
LuochaCharacter.print()

#%% Kafka Guinaifen Sampo Luocha Rotations
numSkill = 3.0
numTalent = 3.0
numUlt = 1.0
GuinaifenDot = GuinaifenCharacter.useDot()
GuinaifenDot.energy = 0.0 # kafka shouldn't be getting energy for Guinaifen Dot
SampoDot = SampoCharacter.useDot()
SampoDot.energy = 0.0
extraDots = [ GuinaifenDot, SampoDot, SampoDot * KafkaCharacter.numEnemies ]
extraDotsUlt = [ GuinaifenDot * KafkaCharacter.numEnemies ]
KafkaRotation = [
        KafkaCharacter.useSkill(extraDots=extraDots) * numSkill,
        KafkaCharacter.useTalent() * numTalent,
        KafkaCharacter.useUltimate(extraDots=extraDotsUlt) * numUlt,
]

numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)

numBasicGuinaifen = 2.0
numSkillGuinaifen = 2.0
numUltGuinaifen = 1.0
GuinaifenRotation = [ # 
        GuinaifenCharacter.useBasic() * numBasicGuinaifen,
        GuinaifenCharacter.useSkill() * numSkillGuinaifen,
        GuinaifenCharacter.useUltimate() * numUlt,
]

numBasicSampo = 2
numSkillSampo = 2
numUltSampo = 1
SampoRotation = [
                SampoCharacter.useBasic() * numBasicSampo,
                SampoCharacter.useSkill() * numSkillSampo,
                SampoCharacter.useUltimate() * numUltSampo]
    
LuochaRotation = [LuochaCharacter.useBasic() * 3,
                  LuochaCharacter.useUltimate() * 1,
                  LuochaCharacter.useSkill() * 1,]
LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast


#%% Kafka Guinaifen Sampo Luocha Rotation Math
numDotGuinaifen = DotEstimator(GuinaifenRotation, GuinaifenCharacter, config, dotMode='alwaysBlast')
numDotGuinaifen = min(numDotGuinaifen, 2.0 * numSkillGuinaifen * min(3.0, GuinaifenCharacter.numEnemies))
numDotSampo = DotEstimator(SampoRotation, SampoCharacter, config, dotMode='alwaysBlast')
numDotSampo = min(numDotSampo, 3.0 * (numSkillSampo + numUltSampo) * SampoCharacter.numEnemies)

totalKafkaEffect = sumEffects(KafkaRotation)
totalGuinaifenEffect = sumEffects(GuinaifenRotation)
totalSampoEffect = sumEffects(SampoRotation)
totalLuochaEffect = sumEffects(LuochaRotation)

KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
GuinaifenRotationDuration = totalGuinaifenEffect.actionvalue * 100.0 / GuinaifenCharacter.getTotalStat('SPD')
SampoRotationDuration = totalSampoEffect.actionvalue * 100.0 / SampoCharacter.getTotalStat('SPD')
LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

# scale other character's character's rotation
GuinaifenRotation = [x * KafkaRotationDuration / GuinaifenRotationDuration for x in GuinaifenRotation]
SampoRotation = [x * KafkaRotationDuration / SampoRotationDuration for x in SampoRotation]
LuochaRotation = [x * KafkaRotationDuration / LuochaRotationDuration for x in LuochaRotation]
numDotGuinaifen *= KafkaRotationDuration / GuinaifenRotationDuration
numDotSampo *= KafkaRotationDuration / SampoRotationDuration

KafkaEstimate = DefaultEstimator('Kafka {:.0f}E {:.0f}T {:.0f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDotKafka),
                                 KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
GuinaifenEstimate = DefaultEstimator('E6 Guinaifen S5 GNSW {:.0f}N {:.0f}E {:.0f}Q {:.1f}Dot'.format(numBasicGuinaifen, numSkillGuinaifen, numUltGuinaifen, numDotGuinaifen),
                                     GuinaifenRotation, GuinaifenCharacter, config, numDot=numDotGuinaifen)
SampoEstimate = DefaultEstimator('Sampo {:.0f}N {:.0f}E {:.0f}Q {:.1f}Dot'.format(numBasicSampo, numSkillSampo, numUltSampo, numDotSampo), 
                                 SampoRotation, SampoCharacter, config, numDot=numDotSampo)
LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                  LuochaRotation, LuochaCharacter, config)

visualizationList.append([KafkaEstimate, GuinaifenEstimate, SampoEstimate, LuochaEstimate])

#%% Kafka Guinaifen Sampo Luocha
KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'BreakEffect': 5, 'ATK.flat': 3}),
                        lightcone = GoodNightAndSleepWell(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

GuinaifenCharacter = Guinaifen(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.fire'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'EHR': 4, 'BreakEffect': 4}),
                        lightcone = GoodNightAndSleepWell(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

# I'm just going to assume 100% uptime on firmament frontline glamoth
# Kafka and Guinaifen are a few substats short of base 160 with a 12 substat cap
# But I'll just generously assume you are able to get there

LukaCharacter = Luka(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.physical'],
                                substats = {'ATK.percent': 5, 'SPD.flat': 12, 'EHR': 8, 'BreakEffect': 3}),
                                lightcone = GoodNightAndSleepWell(**config),
                                relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                                **config)

LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                lightcone = Multiplication(**config),
                                relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                                **config)

#%% Kafka Guinaifen Luka Luocha Team Buffs
# Fleet of the Ageless Buff
for character in [KafkaCharacter, GuinaifenCharacter, LukaCharacter]:
    character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)
    
# Give Guinaifen Vulnerability to all other characters
for character in [KafkaCharacter, LukaCharacter, LuochaCharacter]:
    character.addStat('Vulnerability',description='Guinaifen Vulnerability',
                        amount=0.076 if GuinaifenCharacter.eidolon >= 5 else 0.07,
                        stacks=min(GuinaifenCharacter.firekissStacks,4.0 if GuinaifenCharacter.eidolon >= 6 else 3.0))


for character in [KafkaCharacter, GuinaifenCharacter, LuochaCharacter]:
    character.addStat('Vulnerability',description='Luka Vulnerability',
                     amount=0.216 if LukaCharacter.eidolon >= 5 else 0.2,
                     uptime=LukaCharacter.ultDebuffUptime/LukaCharacter.numEnemies)

#%% Kafka Guinaifen Luka Luocha Print Statements
KafkaCharacter.print()
GuinaifenCharacter.print()
LukaCharacter.print()
LuochaCharacter.print()

#%% Kafka Guinaifen Luka Luocha Rotations
numSkill = 3.0
numTalent = 3.0
numUlt = 1.0
GuinaifenDot = GuinaifenCharacter.useDot()
GuinaifenDot.energy = 0.0 # kafka shouldn't be getting energy for Guinaifen Dot
LukaDot = LukaCharacter.useDot()
LukaDot.energy = 0.0
extraDots = [ GuinaifenDot, LukaDot, LukaDot * min(2,KafkaCharacter.numEnemies) ]
extraDotsUlt = [ GuinaifenDot * KafkaCharacter.numEnemies ]
KafkaRotation = [
        KafkaCharacter.useSkill(extraDots=extraDots) * numSkill,
        KafkaCharacter.useTalent() * numTalent,
        KafkaCharacter.useUltimate(extraDots=extraDotsUlt) * numUlt,
]

numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)

numBasicGuinaifen = 2.0
numSkillGuinaifen = 2.0
numUltGuinaifen = 1.0
GuinaifenRotation = [ # 
        GuinaifenCharacter.useBasic() * numBasicGuinaifen,
        GuinaifenCharacter.useSkill() * numSkillGuinaifen,
        GuinaifenCharacter.useUltimate() * numUlt,
]

numEnhancedLuka = 3.0
numSkillLuka = 2.0
numUltLuka = 1.0

LukaRotation = [ # 
        LukaCharacter.useEnhancedBasic() * numEnhancedLuka, # -6 Fighting Will
        LukaCharacter.useSkill() * numSkillLuka, # +4 Fighting Will
        LukaCharacter.useUltimate() * numUltLuka, # +2 Fighting Will
]
    
LuochaRotation = [LuochaCharacter.useBasic() * 3,
                  LuochaCharacter.useUltimate() * 1,
                  LuochaCharacter.useSkill() * 1,]
LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast


#%% Kafka Guinaifen Luka Luocha Rotation Math
numDotGuinaifen = DotEstimator(GuinaifenRotation, GuinaifenCharacter, config, dotMode='alwaysBlast')
numDotGuinaifen = min(numDotGuinaifen, 2.0 * numSkillGuinaifen * min(3.0, GuinaifenCharacter.numEnemies))
numDotLuka = DotEstimator(LukaRotation, LukaCharacter, config, dotMode='alwaysBlast')
numDotLuka = min(numDotLuka, 3.0 * numSkillLuka)

totalKafkaEffect = sumEffects(KafkaRotation)
totalGuinaifenEffect = sumEffects(GuinaifenRotation)
totalLukaEffect = sumEffects(LukaRotation)
totalLuochaEffect = sumEffects(LuochaRotation)

KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
GuinaifenRotationDuration = totalGuinaifenEffect.actionvalue * 100.0 / GuinaifenCharacter.getTotalStat('SPD')
LukaRotationDuration = totalLukaEffect.actionvalue * 100.0 / LukaCharacter.getTotalStat('SPD')
LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

# scale other character's character's rotation
GuinaifenRotation = [x * KafkaRotationDuration / GuinaifenRotationDuration for x in GuinaifenRotation]
LukaRotation = [x * KafkaRotationDuration / LukaRotationDuration for x in LukaRotation]
LuochaRotation = [x * KafkaRotationDuration / LuochaRotationDuration for x in LuochaRotation]
numDotGuinaifen *= KafkaRotationDuration / GuinaifenRotationDuration
numDotLuka *= KafkaRotationDuration / LukaRotationDuration

KafkaEstimate = DefaultEstimator('Kafka {:.0f}E {:.0f}T {:.0f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDotKafka),
                                 KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
GuinaifenEstimate = DefaultEstimator('E6 Guinaifen S5 GNSW {:.0f}N {:.0f}E {:.0f}Q {:.1f}Dot'.format(numBasicGuinaifen, numSkillGuinaifen, numUltGuinaifen, numDotGuinaifen),
                                     GuinaifenRotation, GuinaifenCharacter, config, numDot=numDotGuinaifen)
LukaEstimate = DefaultEstimator('E6 Luka S5 GNSW {:.0f}Enh {:.0f}S {:.0f}Q {:.1f}Dot'.format(numEnhancedLuka, numSkillLuka, numUltLuka, numDotLuka), 
                                LukaRotation, LukaCharacter, config, numDot=numDotLuka)
LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                  LuochaRotation, LuochaCharacter, config)

visualizationList.append([KafkaEstimate, GuinaifenEstimate, LukaEstimate, LuochaEstimate])

#%% Visualization
# Visualize
visualize(visualizationList, visualizerPath='visualizer\QuadVisual.png', **config)
    
from excelAPI.write2sheet import writeVisualizationList
writeVisualizationList(visualizationList,path='visualizer\QuadVisual.xlsx',sheetname='Quad vs Two')
