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
config['enemySpeed'] = 190 / 1.125 # assume 25% action delay every 2 enemy turns from toughness break

#%% Clara Silver Wolf Pela Characters
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

#%% Clara Silver Wolf Pela Team Buffs
for character in [SilverWolfCharacter, ClaraCharacter, PelaCharacter]:
    character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
    
for character in [SilverWolfCharacter, ClaraCharacter, LuochaCharacter]:
    character.addStat('CD',description='Broken Keel from Pela',amount=0.1)

# Pela Debuffs, 3 turn pela rotation
pelaUltUptime = (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
pelaUltUptime = min(1.0, pelaUltUptime)
for character in [ClaraCharacter, SilverWolfCharacter, PelaCharacter, LuochaCharacter]:
    character.addStat('DefShred',description='Pela Ultimate',
                      amount=0.42 if PelaCharacter.eidolon >= 5 else 0.40,
                      uptime=pelaUltUptime)
    
# Resolution Shines as Pearls of Sweat uptime
sweatUptime = (1.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
sweatUptime += (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
sweatUptime = min(1.0, sweatUptime)
for character in [ClaraCharacter, SilverWolfCharacter, PelaCharacter, LuochaCharacter]:
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
    
#%% Clara Silver Wolf Pela Print Statements
ClaraCharacter.print()
SilverWolfCharacter.print()
PelaCharacter.print()
LuochaCharacter.print()

#%% Clara Silver Wolf Pela Rotations

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

#%% Clara SilverWolf Pela Luocha Rotation Math

totalClaraEffect = sumEffects(ClaraRotation)
totalPelaEffect = sumEffects(PelaRotation)
totalSilverWolfEffect = sumEffects(SilverWolfRotation)
totalLuochaEffect = sumEffects(LuochaRotation)

ClaraRotationDuration = totalClaraEffect.actionvalue * 100.0 / ClaraCharacter.getTotalStat('SPD')
PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

print('##### Rotation Durations #####')
print('Clara: ',ClaraRotationDuration)
print('Pela: ',PelaRotationDuration)
print('SilverWolf: ',SilverWolfRotationDuration)
print('Luocha: ',LuochaRotationDuration)

# Scale other character's rotation
PelaRotation = [x * ClaraRotationDuration / PelaRotationDuration for x in PelaRotation]
SilverWolfRotation = [x * ClaraRotationDuration / SilverWolfRotationDuration for x in SilverWolfRotation]
LuochaRotation = [x * ClaraRotationDuration / LuochaRotationDuration for x in LuochaRotation]

ClaraEstimate = DefaultEstimator(f'Clara: 2E {numSvarogCounters:.1f}T 1Q', ClaraRotation, ClaraCharacter, config)
PelaEstimate = DefaultEstimator(f'Pela: 3N 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                PelaRotation, PelaCharacter, config)
SilverWolfEstimate = DefaultEstimator(f'SilverWolf {numSkillSW:.0f}E {numUltSW:.0f}Q', SilverWolfRotation, SilverWolfCharacter, config)
LuochaEstimate = DefaultEstimator(f'Luocha: 3N 1E 1Q, S{LuochaCharacter.lightcone.superposition:d} {LuochaCharacter.lightcone.name}', 
                                  LuochaRotation, LuochaCharacter, config)

visualizationList.append([ClaraEstimate, SilverWolfEstimate, PelaEstimate, LuochaEstimate])

#%% Kafka Guinaifen Asta Luocha Characters
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

AstaCharacter = Asta(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'ATK.percent'],
                                substats = {'EHR': 8, 'SPD.flat': 12, 'BreakEffect': 3, 'ATK.percent': 5}),
                                lightcone = MemoriesOfThePast(**config),
                                relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(uptime=0.5), planarset = FleetOfTheAgeless(),
                                **config)

LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                lightcone = Multiplication(**config),
                                relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                                **config)

#%% Kafka Guinaifen Asta Luocha Team Buffs
# Fleet of the Ageless Buff
for character in [KafkaCharacter, GuinaifenCharacter, AstaCharacter]:
    character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)
for character in [KafkaCharacter, GuinaifenCharacter, LuochaCharacter]:
    character.addStat('ATK.percent',description='Fleet Asta',amount=0.08)
    
# Give Guinaifen Vulnerability to all other characters
for character in [KafkaCharacter, AstaCharacter, LuochaCharacter]:
    character.addStat('Vulnerability',description='Guinaifen Vulnerability',
                        amount=0.076 if GuinaifenCharacter.eidolon >= 5 else 0.07,
                        stacks=min(GuinaifenCharacter.firekissStacks,4.0 if GuinaifenCharacter.eidolon >= 6 else 3.0))
    
# messenger 4 pc buffs:
KafkaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0 / 3.0)
GuinaifenCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0 / 3.0)
LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0 / 4.0)

# assume partial uptime on asta ultimate with ENN rotation
for character in [KafkaCharacter, GuinaifenCharacter, AstaCharacter]:
    character.addStat('SPD.flat',description='Asta Ultimate',
                      amount=53 if AstaCharacter.eidolon >= 5 else 50,
                      uptime=2.0/3.0)
    character.addStat('ATK.percent',description='Asta Talent',
                      amount=0.154 if AstaCharacter.eidolon >= 3 else 0.14,
                      stacks=5,
                      uptime=2.0/3.0)
    
# Luocha is faster so his uptime is a bit lower
LuochaCharacter.addStat('SPD.flat',description='Asta Ultimate',
                    amount=53 if AstaCharacter.eidolon >= 5 else 50,
                    uptime=2.0/4.0)
LuochaCharacter.addStat('ATK.percent',description='Asta Talent',
                    amount=0.154 if AstaCharacter.eidolon >= 3 else 0.14,
                    stacks=5,
                    uptime=2.0/4.0)

# Asta Ignite Buff
GuinaifenCharacter.addStat('DMG.fire',description='trace',amount=0.18)

#%% Kafka Guinaifen Asta Luocha Print Statements
KafkaCharacter.print()
GuinaifenCharacter.print()
AstaCharacter.print()
LuochaCharacter.print()

#%% Kafka Guinaifen Asta Luocha Rotations
numSkill = 3.0
numTalent = 3.0
numUlt = 1.0
GuinaifenDot = GuinaifenCharacter.useDot()
GuinaifenDot.energy = 0.0 # kafka shouldn't be getting energy for Guinaifen Dot
AstaDot = AstaCharacter.useDot()
AstaDot.energy = 0.0 # kafka shouldn't be getting energy for Guinaifen Dot
extraDots = [ GuinaifenDot, AstaDot]
extraDotsUlt = [ GuinaifenDot * KafkaCharacter.numEnemies, AstaDot * KafkaCharacter.numEnemies ]
KafkaRotation = [
        KafkaCharacter.useSkill(extraDots=extraDots) * numSkill,
        KafkaCharacter.useTalent() * numTalent,
        KafkaCharacter.useUltimate(extraDots=extraDotsUlt) * numUlt,
]

numSkillGuinaifen = 2.0
numBasicGuinaifen = 2.0
numUltGuinaifen = 1.0

numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)

GuinaifenRotation = [ # 
        GuinaifenCharacter.useSkill() * numSkillGuinaifen,
        GuinaifenCharacter.useBasic() * numBasicGuinaifen,
        GuinaifenCharacter.useUltimate() * numUlt,
]


AstaRotation = [AstaCharacter.useBasic() * 2,
                AstaCharacter.useSkill() * 1,
                AstaCharacter.useUltimate() * 1,]

LuochaRotation = [LuochaCharacter.useBasic() * 3,
                  LuochaCharacter.useUltimate() * 1,
                  LuochaCharacter.useSkill() * 1,]
LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast


#%% Kafka Guinaifen Asta Luocha Rotation Math
numDotGuinaifen = DotEstimator(GuinaifenRotation, GuinaifenCharacter, config, dotMode='alwaysBlast')
numDotGuinaifen = min(numDotGuinaifen, 2.0 * numSkillGuinaifen * min(3.0, GuinaifenCharacter.numEnemies))

totalKafkaEffect = sumEffects(KafkaRotation)
totalGuinaifenEffect = sumEffects(GuinaifenRotation)
totalAstaEffect = sumEffects(AstaRotation)
totalLuochaEffect = sumEffects(LuochaRotation)

KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
GuinaifenRotationDuration = totalGuinaifenEffect.actionvalue * 100.0 / GuinaifenCharacter.getTotalStat('SPD')
AstaRotationDuration = totalAstaEffect.actionvalue * 100.0 / AstaCharacter.getTotalStat('SPD')
LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

# scale other character's rotation
GuinaifenRotation = [x * KafkaRotationDuration / GuinaifenRotationDuration for x in GuinaifenRotation]
AstaRotation = [x * KafkaRotationDuration / AstaRotationDuration for x in AstaRotation]
LuochaRotation = [x * KafkaRotationDuration / LuochaRotationDuration for x in LuochaRotation]
numDotGuinaifen *= KafkaRotationDuration / GuinaifenRotationDuration

KafkaEstimate = DefaultEstimator('Kafka {:.0f}E {:.0f}T {:.0f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDotKafka),
                                 KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
GuinaifenEstimate = DefaultEstimator('E6 Guinaifen S5 GNSW {:.0f}N {:.0f}E {:.0f}Q {:.1f}Dot'.format(numBasicGuinaifen, numSkillGuinaifen, numUltGuinaifen, numDotGuinaifen),
                                     GuinaifenRotation, GuinaifenCharacter, config, numDot=numDotGuinaifen)
AstaEstimate = DefaultEstimator('Asta: 2N 1E 1Q, S{:.0f} {}'.format(AstaCharacter.lightcone.superposition, AstaCharacter.lightcone.name), 
                                AstaRotation, AstaCharacter, config)
LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                  LuochaRotation, LuochaCharacter, config)

visualizationList.append([KafkaEstimate, GuinaifenEstimate, LuochaEstimate, AstaEstimate])

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
    character.addStat('DMG',description='Burden',amount=(0.33 if HanyaCharacter.eidolon >= 5 else 0.30) + (0.10 if HanyaCharacter.eidolon >= 6 else 0.0))

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

KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'BreakEffect': 5, 'ATK.flat': 3}),
                        lightcone = GoodNightAndSleepWell(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

GuinaifenCharacter = Guinaifen(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'ATK.percent', 'DMG.fire'],
                        substats = {'ATK.percent': 12, 'SPD.flat': 8, 'EHR': 4, 'BreakEffect': 4}),
                        lightcone = GoodNightAndSleepWell(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = SpaceSealingStation(),
                        **config)

# I'm just going to assume 100% uptime on firmament frontline glamoth
# Kafka and Guinaifen are a few substats short of base 160 with a 12 substat cap
# But I'll just generously assume you are able to get there

LukaCharacter = Luka(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'ATK.percent', 'DMG.physical'],
                        substats = {'ATK.percent': 12, 'SPD.flat': 3, 'EHR': 8, 'BreakEffect': 5}),
                        lightcone = GoodNightAndSleepWell(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = SpaceSealingStation(),
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

# Give Luka Vulnerability to all other characters
for character in [KafkaCharacter, GuinaifenCharacter, LuochaCharacter]:
    character.addStat('Vulnerability',description='Luka Vulnerability',
                     amount=0.216 if LukaCharacter.eidolon >= 5 else 0.2,
                     uptime=(3.0/5.0)*LukaCharacter.ultDebuffUptime/LukaCharacter.numEnemies)

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
extraDots = [ GuinaifenDot, LukaDot ]
extraDotsUlt = [ GuinaifenDot * KafkaCharacter.numEnemies, LukaDot * min(2,KafkaCharacter.numEnemies) ]
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

#%% Lunae Hanya Yukong Luocha Characters
LunaeCharacter = Lunae(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
                        substats = {'CR': 8, 'CD': 12, 'ATK.percent': 3, 'SPD.flat': 5}),
                        lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=4.0, **config),
                        relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = WastelanderOfBanditryDesert4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                        substats = {'RES': 7, 'SPD.flat': 12, 'CD': 5, 'CR': 4}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

YukongCharacter = Yukong(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                        substats = {'CR': 5, 'CD': 8, 'SPD.flat': 12, 'RES': 3}),
                        lightcone = PlanetaryRendezvous(**config),
                        relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                        **config)

LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'RES': 3}),
                                lightcone = Multiplication(**config),
                                relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                                **config)

#%% Lunae Hanya Yukong Luocha Team Buffs
# Broken Keel Buffs
for character in [LunaeCharacter, YukongCharacter, LuochaCharacter]:
    character.addStat('CD',description='Broken Keel from Hanya',amount=0.1)
    
# Penacony Buff
for character in [LunaeCharacter, LuochaCharacter]:
    character.addStat('DMG',description='Penacony from Yukong',amount=0.1)
for character in [LunaeCharacter, YukongCharacter]:
    character.addStat('DMG',description='Penacony from Luocha',amount=0.1)
    
# Yukong imaginary damage trace
for character in [LunaeCharacter, LuochaCharacter]:
    character.addStat('DMG',description='Yukong trace',amount=0.12,type=['imaginary'])

# Yukong Planetary Rendezvous
for character in [LunaeCharacter, LuochaCharacter]:
    character.addStat('DMG',description='Planetary Rendezvous',amount=0.09 + 0.03 * YukongCharacter.lightcone.superposition)

# Hanya Messenger Buff
LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)
for character in [LunaeCharacter, YukongCharacter]:
    character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)

# Hanya Buff
for character in [LunaeCharacter, YukongCharacter, LuochaCharacter]:
    character.addStat('ATK.percent',description='Hanya trace',amount=0.10,uptime=0.5)
    character.addStat('DMG',description='Burden',amount=(0.33 if HanyaCharacter.eidolon >= 5 else 0.30) + (0.10 if HanyaCharacter.eidolon >= 6 else 0.0))

# Hanya Ult Buff
LunaeCharacter.addStat('SPD.flat',description='Hanya Ult',amount=(0.21 if HanyaCharacter.eidolon >= 5 else 0.20) * HanyaCharacter.getTotalStat('SPD'))
LunaeCharacter.addStat('ATK.percent',description='Hanya Ult',amount=0.648 if HanyaCharacter.eidolon >= 5 else 0.60)

# Estimate Yukong Buffs.
# Yukong is speed tuned to be slightly faster than Lunae, and always going before him
LunaeCharacter.addStat('ATK.percent',description='Roaring Bowstrings',
                amount=0.88 if YukongCharacter.eidolon >= 3 else 0.80,
                uptime=3.0 / 4.0)
LunaeCharacter.addStat('CR',description='Yukong ultimate',
                amount=0.294 if YukongCharacter.eidolon >= 5 else 0.28,
                uptime=1.0 / 4.0 ) # 1 ult buff, 4 characters, 4 turn rotation
LunaeCharacter.addStat('CD',description='Yukong ultimate',
                amount=0.702 if YukongCharacter.eidolon >= 5 else 0.65,
                uptime=1.0 / 4.0 )

for character in [HanyaCharacter, LuochaCharacter]:
    character.addStat('ATK.percent',description='Roaring Bowstrings',
                    amount=0.88 if YukongCharacter.eidolon >= 3 else 0.80,
                    uptime=2.0 / 4.0 / 2.0) # 2 bowstrings, 2 characters, 4 turn rotation

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

numBasicYukong = 2
numSkillYukong = 2
numUltYukong = 1
YukongRotation = [ # 
            YukongCharacter.useEnhancedBasic() * numBasicYukong,
            YukongCharacter.useSkill() * numSkillYukong,
            YukongCharacter.useUltimate() * numUltYukong,
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
HanyaEstimate = DefaultEstimator('Hanya {:.0f}E {:.0f}Q S{:.0f} {}, 12 Spd Substats'.format(numHanyaSkill, numHanyaUlt,
                                HanyaCharacter.lightcone.superposition, HanyaCharacter.lightcone.name), 
                                HanyaRotation, HanyaCharacter, config)
YukongEstimate = DefaultEstimator(f'Yukong (Speed Tuned) {numBasicYukong:d}N {numSkillYukong:d}E {numUltYukong:d}Q S{YukongCharacter.lightcone.superposition:d} {YukongCharacter.lightcone.name}', 
                                  YukongRotation, YukongCharacter, config)
LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                  LuochaRotation, LuochaCharacter, config)

visualizationList.append([LunaeEstimate,HanyaEstimate,YukongEstimate,LuochaEstimate])

#%% Lunae Tingyun Yukong Luocha Characters
LunaeCharacter = Lunae(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
                        substats = {'CR': 8, 'CD': 12, 'ATK.percent': 3, 'SPD.flat': 5}),
                        lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=4.0, **config),
                        relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = WastelanderOfBanditryDesert4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                        benedictionTarget=LunaeCharacter,
                        **config)

YukongCharacter = Yukong(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'ER'],
                        substats = {'CR': 8, 'CD': 12, 'SPD.flat': 5, 'RES': 3}),
                        lightcone = PlanetaryRendezvous(**config),
                        relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                        **config)

LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 5, 'SPD.flat': 12, 'HP.percent': 4, 'RES': 7}),
                        lightcone = Multiplication(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                        **config)

#%% Lunae Tingyun Yukong Luocha Team Buffs
# Penacony Buff
for character in [LunaeCharacter, LuochaCharacter]:
    character.addStat('DMG',description='Penacony from Yukong',amount=0.1)
for character in [LunaeCharacter, YukongCharacter]:
    character.addStat('DMG',description='Penacony from Luocha',amount=0.1)
    
# Yukong imaginary damage trace
for character in [LunaeCharacter, LuochaCharacter]:
    character.addStat('DMG',description='Yukong trace',amount=0.12,type=['imaginary'])

# Yukong Planetary Rendezvous
for character in [LunaeCharacter, LuochaCharacter]:
    character.addStat('DMG',description='Planetary Rendezvous',amount=0.09 + 0.03 * YukongCharacter.lightcone.superposition)

# Tingyun Messenger Buff
LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)
for character in [LunaeCharacter, YukongCharacter]:
    character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/2.0)
    
LunaeCharacter.addStat('SPD.percent',description='Tingyun E1',amount=0.20,uptime=0.5)
LunaeCharacter.addStat('ATK.percent',description='Benediction',
                         amount=0.55 if TingyunCharacter.eidolon >= 5 else 0.50)
LunaeCharacter.addStat('DMG',description='Tingyun Ult',amount=0.65 if TingyunCharacter.eidolon >= 3 else 0.6) # tingyun ult buff never expires in this rotation

# Estimate Yukong Buffs.
# Yukong is speed tuned to be slightly faster than Lunae, and always going before him
LunaeCharacter.addStat('ATK.percent',description='Roaring Bowstrings',
                amount=0.88 if YukongCharacter.eidolon >= 3 else 0.80,
                uptime=3.0 / 4.0)
LunaeCharacter.addStat('CR',description='Yukong ultimate',
                amount=0.294 if YukongCharacter.eidolon >= 5 else 0.28,
                uptime=1.0 / 4.0 ) # 1 ult buff, 4 characters, 4 turn rotation
LunaeCharacter.addStat('CD',description='Yukong ultimate',
                amount=0.702 if YukongCharacter.eidolon >= 5 else 0.65,
                uptime=1.0 / 4.0 )

for character in [TingyunCharacter, LuochaCharacter]:
    character.addStat('ATK.percent',description='Roaring Bowstrings',
                    amount=0.88 if YukongCharacter.eidolon >= 3 else 0.80,
                    uptime=2.0 / 4.0 / 2.0) # 1 bowstrings, 2 characters, 4 turn rotation

#%% Lunae Tingyun Yukong Luocha Print Statements
LunaeCharacter.print()
TingyunCharacter.print()
YukongCharacter.print()
LuochaCharacter.print()

#%% Lunae Tingyun Yukong Luocha Rotations
TingyunRotation = [ 
        TingyunCharacter.useBasic() * 2, 
        TingyunCharacter.useSkill(),
        TingyunCharacter.useUltimate(),
]
    
LunaeRotation = [  # 140 energy needed. EndTurn needed to factor in his buffs
            LunaeCharacter.useSkill()*3,
            LunaeCharacter.useEnhancedBasic3(), # -3 SP, 40 energy
            LunaeCharacter.endTurn(),
            LunaeCharacter.useSkill()*3,
            LunaeCharacter.useEnhancedBasic3(), # -3 SP, 40 energy
            LunaeCharacter.useUltimate(), # +2 SP, 5 energy
            LunaeCharacter.endTurn(),
            TingyunCharacter.giveUltEnergy(),
]

numBasicYukong = 2
numSkillYukong = 2
numUltYukong = 1
YukongRotation = [ # 
            YukongCharacter.useEnhancedBasic() * numBasicYukong,
            YukongCharacter.useSkill() * numSkillYukong,
            YukongCharacter.useUltimate() * numUltYukong,
    ]

LuochaRotation = [LuochaCharacter.useBasic() * 3,
                  LuochaCharacter.useUltimate() * 1,
                  LuochaCharacter.useSkill() * 1,]
LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast

#%% Lunae Tingyun Yukong Luocha Rotation Math
totalLunaeEffect = sumEffects(LunaeRotation)
totalTingyunEffect = sumEffects(TingyunRotation)
totalYukongEffect = sumEffects(YukongRotation)
totalLuochaEffect = sumEffects(LuochaRotation)

LunaeRotationDuration = totalLunaeEffect.actionvalue * 100.0 / LunaeCharacter.getTotalStat('SPD')
TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
YukongRotationDuration = totalYukongEffect.actionvalue * 100.0 / YukongCharacter.getTotalStat('SPD')
LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

# scale other character's rotation
TingyunRotation = [x * LunaeRotationDuration / TingyunRotationDuration for x in TingyunRotation]
YukongRotation = [x * LunaeRotationDuration / YukongRotationDuration for x in YukongRotation]
LuochaRotation = [x * LunaeRotationDuration / LuochaRotationDuration for x in LuochaRotation]

LunaeEstimate = DefaultEstimator('Lunae: 2N^3 1Q', LunaeRotation, LunaeCharacter, config)
TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.1f} Tingyun S{TingyunCharacter.lightcone.superposition:.1f} {TingyunCharacter.lightcone.name}, 12 spd substats', [totalTingyunEffect], TingyunCharacter, config)
YukongEstimate = DefaultEstimator(f'Yukong (Speed Tuned) {numBasicYukong:d}N {numSkillYukong:d}E {numUltYukong:d}Q S{YukongCharacter.lightcone.superposition:d} {YukongCharacter.lightcone.name}', 
                                  YukongRotation, YukongCharacter, config)
LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                  LuochaRotation, LuochaCharacter, config)

visualizationList.append([LunaeEstimate,TingyunEstimate,YukongEstimate,LuochaEstimate])

#%% Lunae Hanya Pela Luocha Characters
LunaeCharacter = Lunae(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
                        substats = {'CR': 8, 'CD': 12, 'ATK.percent': 3, 'SPD.flat': 5}),
                        lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=4.0, **config),
                        relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = WastelanderOfBanditryDesert4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                        substats = {'RES': 7, 'SPD.flat': 12, 'CD': 5, 'CR': 4}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                        substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
                        lightcone = ResolutionShinesAsPearlsOfSweat(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
                        **config)

LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'RES': 3}),
                                lightcone = Multiplication(**config),
                                relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                                **config)

#%% Lunae Hanya Pela Luocha Team Buffs
# Broken Keel Buffs
for character in [LunaeCharacter, PelaCharacter, LuochaCharacter]:
    character.addStat('CD',description='Broken Keel from Hanya',amount=0.1)
for character in [LunaeCharacter, HanyaCharacter, LuochaCharacter]:
    character.addStat('CD',description='Broken Keel from Pela',amount=0.1)
    
# Penacony Buff
for character in [LunaeCharacter, PelaCharacter]:
    character.addStat('DMG',description='Penacony from Luocha',amount=0.1)
    
# Hanya Messenger Buff
LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)
for character in [LunaeCharacter, PelaCharacter]:
    character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)

# Hanya Buff
for character in [LunaeCharacter, PelaCharacter, LuochaCharacter]:
    character.addStat('ATK.percent',description='Hanya trace',amount=0.10,uptime=0.5)
    character.addStat('DMG',description='Burden',amount=(0.33 if HanyaCharacter.eidolon >= 5 else 0.30) + (0.10 if HanyaCharacter.eidolon >= 6 else 0.0))

# Hanya Ult Buff
LunaeCharacter.addStat('SPD.flat',description='Hanya Ult',amount=(0.21 if HanyaCharacter.eidolon >= 5 else 0.20) * HanyaCharacter.getTotalStat('SPD'))
LunaeCharacter.addStat('ATK.percent',description='Hanya Ult',amount=0.648 if HanyaCharacter.eidolon >= 5 else 0.60)

# Pela Debuffs, 3 turn pela rotation
pelaUltUptime = (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
pelaUltUptime = min(1.0, pelaUltUptime)
for character in [LunaeCharacter, HanyaCharacter, PelaCharacter, LuochaCharacter]:
    character.addStat('DefShred',description='Pela Ultimate',
                      amount=0.42 if PelaCharacter.eidolon >= 5 else 0.40,
                      uptime=pelaUltUptime)
    
# Resolution Shines as Pearls of Sweat uptime
sweatUptime = (1.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
sweatUptime += (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
sweatUptime = min(1.0, sweatUptime)
for character in [LunaeCharacter,HanyaCharacter,PelaCharacter,LuochaCharacter]:
    character.addStat('DefShred',description='Resolution Sweat',
                      amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                      uptime=sweatUptime)


#%% Lunae Hanya Pela Luocha Print Statements
LunaeCharacter.print()
HanyaCharacter.print()
PelaCharacter.print()
LuochaCharacter.print()

#%% Lunae Hanya Pela Luocha Rotations
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

PelaRotation = [PelaCharacter.useBasic() * 3,
                PelaCharacter.useUltimate(),]

LuochaRotation = [LuochaCharacter.useBasic() * 3,
                  LuochaCharacter.useUltimate() * 1,
                  LuochaCharacter.useSkill() * 1,]
LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast

#%% Lunae Hanya Pela Luocha Rotation Math
totalLunaeEffect = sumEffects(LunaeRotation)
totalHanyaEffect = sumEffects(HanyaRotation)
totalPelaEffect = sumEffects(PelaRotation)
totalLuochaEffect = sumEffects(LuochaRotation)

LunaeRotationDuration = totalLunaeEffect.actionvalue * 100.0 / LunaeCharacter.getTotalStat('SPD')
HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

# scale other character's rotation
HanyaRotation = [x * LunaeRotationDuration / HanyaRotationDuration for x in HanyaRotation]
PelaRotation = [x * LunaeRotationDuration / PelaRotationDuration for x in PelaRotation]
LuochaRotation = [x * LunaeRotationDuration / LuochaRotationDuration for x in LuochaRotation]

LunaeEstimate = DefaultEstimator('Lunae: 2N^3 1Q', LunaeRotation, LunaeCharacter, config)
HanyaEstimate = DefaultEstimator('Hanya {:.0f}E {:.0f}Q S{:.0f} {}, 12 Spd Substats'.format(numHanyaSkill, numHanyaUlt,
                                HanyaCharacter.lightcone.superposition, HanyaCharacter.lightcone.name), 
                                HanyaRotation, HanyaCharacter, config)
PelaEstimate = DefaultEstimator(f'Pela: 3N 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                PelaRotation, PelaCharacter, config)
LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                  LuochaRotation, LuochaCharacter, config)

visualizationList.append([LunaeEstimate,HanyaEstimate,PelaEstimate,LuochaEstimate])

#%% Lunae Tingyun Pela Luocha Characters
LunaeCharacter = Lunae(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
                        substats = {'CR': 8, 'CD': 12, 'ATK.percent': 3, 'SPD.flat': 5}),
                        lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=4.0, **config),
                        relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = WastelanderOfBanditryDesert4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                        benedictionTarget=LunaeCharacter,
                        **config)

PelaCharacter = Pela(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'ER'],
                        substats = {'CR': 8, 'CD': 12, 'SPD.flat': 5, 'RES': 3}),
                        lightcone = PlanetaryRendezvous(**config),
                        relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                        **config)

LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 5, 'SPD.flat': 12, 'HP.percent': 4, 'RES': 7}),
                        lightcone = Multiplication(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                        **config)

#%% Visualization
# Visualize
visualize(visualizationList, visualizerPath='visualizer\QuadVisualMisc.png', **config)
    
from excelAPI.write2sheet import writeVisualizationList
writeVisualizationList(visualizationList,path='visualizer\QuadVisualMisc.xlsx',sheetname='Quad vs Two Misc')