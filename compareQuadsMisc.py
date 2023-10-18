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

#%% Kafka Guinaifen Sampo Luocha
KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 16, 'BreakEffect': 5, 'ATK.flat': 3}),
                        lightcone = GoodNightAndSleepWell(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

GuinaifenCharacter = Guinaifen(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.fire'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 13, 'EHR': 4, 'BreakEffect': 4}),
                        lightcone = GoodNightAndSleepWell(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

# I'm just going to assume 100% uptime on firmament frontline glamoth
# Kafka and Guinaifen are a few substats short of base 160 with a 12 substat cap
# But I'll just generously assume you are able to get there

SampoCharacter = Sampo(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.wind'],
                                substats = {'ATK.percent': 5, 'SPD.flat': 15, 'EHR': 8, 'BreakEffect': 3}),
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
                        substats = {'ATK.percent': 8, 'SPD.flat': 16, 'BreakEffect': 5, 'ATK.flat': 3}),
                        lightcone = GoodNightAndSleepWell(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

GuinaifenCharacter = Guinaifen(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.fire'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 13, 'EHR': 4, 'BreakEffect': 4}),
                        lightcone = GoodNightAndSleepWell(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

# I'm just going to assume 100% uptime on firmament frontline glamoth
# Kafka and Guinaifen are a few substats short of base 160 with a 12 substat cap
# But I'll just generously assume you are able to get there

LukaCharacter = Luka(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.physical'],
                                substats = {'ATK.percent': 5, 'SPD.flat': 14, 'EHR': 8, 'BreakEffect': 3}),
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