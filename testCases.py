#Here I will crossreference my stats and damage numbers with Grimro's spreadsheet to check for errors     
#I don't do 8 cycle rotations, though, so this will just be crossreferencing stats and skill damage    

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
from characters.hunt.DanHeng import DanHeng
from characters.hunt.Seele import Seele
from characters.hunt.Sushang import Sushang
from characters.hunt.Yanqing import Yanqing
from characters.nihility.Kafka import Kafka
from characters.nihility.Luka import Luka
from characters.nihility.Sampo import Sampo
from characters.nihility.SilverWolf import SilverWolf

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

config = copy(Configuration)
config['numEnemies'] = 3 # Going to compare my numbers vs Grimro's 3 target numbers

print('##### Lunae #####')
LunaeCharacter = Lunae(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
                        substats = {'CR': 12, 'CD': 12}),
            lightcone = OnTheFallOfAnAeon(uptime = 0.0, stacks=4.0, **config), # Grimro assumes zero uptime on break
            relicsetone = MusketeerOfWildWheat2pc(),
            relicsettwo = MusketeerOfWildWheat4pc(),
            planarset = RutilantArena(),
            **config)

print('Atk - Mine: {} - Grimro: {}'.format(LunaeCharacter.getTotalStat('ATK',['basic']),2788.63616+4*0.16*1227.74))
print('CR - Mine: {} - Grimro: {}'.format(LunaeCharacter.getTotalStat('CR'),0.92392))
print('CD - Mine: {} - Grimro: {}'.format(LunaeCharacter.getTotalStat('CD'),1.43984))
print('Dmg - Mine: {} - Grimro: {}'.format(LunaeCharacter.getDmg(['basic'])-1.0,0.612803+0.3))
enhancedBasic = LunaeCharacter.useEnhancedBasic3()
print('Enhanced Basic Damage - Mine: {} - Grimro: {}'.format(enhancedBasic.damage,85045.71*0.95)) # 0.95 to factor in toughness multiplier
ultimate = LunaeCharacter.useUltimate()
LunaeCharacter.endTurn() # reset heart stacks
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,60593.375501*0.95)) # 0.95 to factor in toughness multiplier

print('##### Blade #####')
bladeCharacter = Blade(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'DMG.wind'],
                        substats = {'CR': 12, 'CD': 12}),
            lightcone = ASecretVow(uptime = 0.5, **config),
            relicsetone = LongevousDisciple2pc(),
            relicsettwo = LongevousDisciple4pc(),
            planarset = InertSalsotto(),
            hpLossTally=0.9, #looks like grimro uses an hp loss tally of 100%
            **config)


print('Atk - Mine: {} - Grimro: {}'.format(bladeCharacter.getTotalStat('ATK',['basic']),1372.3900))
print('HP - Mine: {} - Grimro: {}'.format(bladeCharacter.getTotalStat('HP',['basic']),5132.95776))
print('CR - Mine: {} - Grimro: {}'.format(bladeCharacter.getTotalStat('CR'),0.75992))
print('CD - Mine: {} - Grimro: {}'.format(bladeCharacter.getTotalStat('CD'),1.84784))
print('Dmg - Mine: {} - Grimro: {}'.format(bladeCharacter.getDmg(['basic'])-1.0,0.9880000+0.4))
enhancedBasic = bladeCharacter.useEnhancedBasic()
print('Enhanced Basic Damage - Mine: {} - Grimro: {}'.format(enhancedBasic.damage,27970.52941*0.95)) # 0.95 to factor in toughness multiplier
talent = bladeCharacter.useTalent()
print('Talent Damage - Mine: {} - Grimro: {}'.format(talent.damage,58792.58835*0.95)) # 0.95 to factor in toughness multiplier
ultimate = bladeCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,53896.22855*0.95)) # 0.95 to factor in toughness multiplier

print('##### Seele #####')
SeeleCharacter = Seele(relicstats = RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.quantum'],
                        substats = {'CR': 7, 'CD': 12, 'ATK.percent': 4}),
            lightcone = CruisingInTheStellarSea(uptimeHP=0.0, uptimeDefeat=0.0, **config), #unclear what uptime 
            relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo=GeniusOfBrilliantStars4pc(), planarset = RutilantArena(),
            **config)

print('Atk - Mine: {} - Grimro: {}'.format(SeeleCharacter.getTotalStat('ATK',['basic']),3042.1576))
print('CR - Mine: {} - Grimro: {}'.format(SeeleCharacter.getTotalStat('CR'),0.81812))
print('CD - Mine: {} - Grimro: {}'.format(SeeleCharacter.getTotalStat('CD'),1.43984))
print('Dmg - Mine: {} - Grimro: {}'.format(SeeleCharacter.getDmg(['basic'])-1.0,0.488803))
skill = SeeleCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,13094.10486*0.95)) # 0.95 to factor in toughness multiplier
ultimate = SeeleCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,22299.76606*0.95)) # 0.95 to factor in toughness multiplier
SeeleCharacter.useResurgence()
skill = SeeleCharacter.useSkill()
print('Resurgence Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,23156.26923*0.95)) # 0.95 to factor in toughness multiplier
ultimate = SeeleCharacter.useUltimate()
print('Resurgence Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,41138.90539*0.95)) # 0.95 to factor in toughness multiplier

print('##### Kafka #####')
KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                        substats = {'EHR': 4, 'ATK.percent': 12, 'SPD.flat': 8}),
            lightcone = GoodNightAndSleepWell(**config),
            relicsetone = BandOfSizzlingThunder2pc(), relicsettwo = BandOfSizzlingThunder4pc(), planarset = SpaceSealingStation(),
            **config)

print('Atk - Mine: {} - Grimro: {}'.format(KafkaCharacter.getTotalStat('ATK',['basic']),3877.417024))
print('CR - Mine: {} - Grimro: {}'.format(KafkaCharacter.getTotalStat('CR'),0.05))
print('CD - Mine: {} - Grimro: {}'.format(KafkaCharacter.getTotalStat('CD'),0.50))
print('Dmg - Mine: {} - Grimro: {}'.format(KafkaCharacter.getDmg(['basic'])-1.0,1.208803))

dot = KafkaCharacter.useDot()
print('Dot Damage - Mine: {} - Grimro: {}'.format(dot.damage*config['numEnemies'],35481.29433*0.95)) # 0.95 to factor in toughness multiplier
skill = KafkaCharacter.useSkill()
skill -= dot * ( 0.78 if KafkaCharacter.eidolon >= 3 else 0.75 )
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,11704.74882*0.95)) # 0.95 to factor in toughness multiplier
ultimate = KafkaCharacter.useUltimate()
ultimate -= ( dot * config['numEnemies'] ) * ( 1.0 if KafkaCharacter.eidolon >= 5 else 1.04)
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,10032.64184*0.95)) # 0.95 to factor in toughness multiplier
talent = KafkaCharacter.useTalent()
print('Talent Damage - Mine: {} - Grimro: {}'.format(talent.damage,5852.374409*0.95)) # 0.95 to factor in toughness multiplier

print('##### Serval #####')
ServalCharacter = Serval(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.lightning'],
                        substats = {'CR': 7, 'ATK.percent': 4, 'CD': 12}),
            lightcone = TheSeriousnessOfBreakfast(**config),
            relicsetone = BandOfSizzlingThunder2pc(), relicsettwo = BandOfSizzlingThunder4pc(), planarset = SpaceSealingStation(),
            **config)

print('Atk - Mine: {} - Grimro: {}'.format(ServalCharacter.getTotalStat('ATK',['basic']),2912.739379))
print('CR - Mine: {} - Grimro: {}'.format(ServalCharacter.getTotalStat('CR'),0.76512))
print('CD - Mine: {} - Grimro: {}'.format(ServalCharacter.getTotalStat('CD'),1.19984))
print('Dmg - Mine: {} - Grimro: {}'.format(ServalCharacter.getDmg(['basic'])-1.0,0.728803))

dot = ServalCharacter.useDot() * config['numEnemies']
print('Dot Damage - Mine: {} - Grimro: {}'.format(dot.damage,9657.606147*0.95)) # 0.95 to factor in toughness multiplier
skill = ServalCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,(15436.24751+12823.95947)*0.95)) # 0.95 to factor in toughness multiplier
ultimate = ServalCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,(31476.99142+12823.95947)*0.95)) # 0.95 to factor in toughness multiplier

print('##### Dan Heng #####')
DanHengCharacter = DanHeng(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.wind'],
                        substats = {'CR': 10, 'CD': 12, 'ATK.percent': 2}),
            lightcone = CruisingInTheStellarSea(uptimeHP=1.0, uptimeDefeat=0.0, **config),
            relicsetone = EagleOfTwilightLine2pc(), relicsettwo=EagleOfTwilightLine4pc(), planarset = SpaceSealingStation(),
            talentUptime = 0.0,
            fasterThanLightUptime = 0.8,
            e1Uptime=0.0,
            **config)

print('Atk - Mine: {} - Grimro: {}'.format(DanHengCharacter.getTotalStat('ATK',['basic']),2429.29895))
print('CR - Mine: {} - Grimro: {}'.format(DanHengCharacter.getTotalStat('CR'),0.8256+0.16))
print('CD - Mine: {} - Grimro: {}'.format(DanHengCharacter.getTotalStat('CD'),1.19984))
print('Dmg - Mine: {} - Grimro: {}'.format(DanHengCharacter.getDmg(['basic'])-1.0,0.712803))

skill = DanHengCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,12368.0652*0.95)) # 0.95 to factor in toughness multiplier
ultimate = DanHengCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,24286.38257*0.95)) # 0.95 to factor in toughness multiplier

print('##### Yanqing #####')
YanqingCharacter = Yanqing(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.ice'],
                        substats = {'ATK.percent': 12, 'CD': 12}),
                lightcone = CruisingInTheStellarSea(uptimeHP=0.0, uptimeDefeat=0.0, **config),
                relicsetone = HunterOfGlacialForest2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SpaceSealingStation(),
                soulsteelUptime = 1.0,
                **config)

print('Atk - Mine: {} - Grimro: {}'.format(YanqingCharacter.getTotalStat('ATK',['basic']),3420.24359))
print('CR - Mine: {} - Grimro: {}'.format(YanqingCharacter.getTotalStat('CR'),0.21+0.2))
print('CD - Mine: {} - Grimro: {}'.format(YanqingCharacter.getTotalStat('CD'),1.84784+0.3))
print('Dmg - Mine: {} - Grimro: {}'.format(YanqingCharacter.getDmg(['basic'])-1.0,0.632803))

skill = YanqingCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,12502.91557*0.95)) # 0.95 to factor in toughness multiplier
YanqingCharacter.useBliss()
ultimate = YanqingCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,36863.01988*0.95)) # 0.95 to factor in toughness multiplier
YanqingCharacter.endTurn()
talent = YanqingCharacter.useTalent()
freezeDot = YanqingCharacter.useFreezeDot()
talent -= freezeDot
print('Talent Damage - Mine: {} - Grimro: {}'.format(talent.damage,4000.932983*0.95*0.6)) # 0.95 to factor in toughness multiplier

print('##### Clara #####')
ClaraCharacter = Clara(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.physical'],
                        substats = {'CR': 10, 'CD': 10}),
            lightcone = OnTheFallOfAnAeon(uptime = 0.0, stacks=4.0, **config),
            relicsetone = ChampionOfStreetwiseBoxing2pc(),
            relicsettwo = ChampionOfStreetwiseBoxing4pc(),
            planarset = InertSalsotto(),
            **config)

skill = ClaraCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,"None")) # 0.95 to factor in toughness multiplier
talent = ClaraCharacter.useTalent()
print('Talent Damage - Mine: {} - Grimro: {}'.format(talent.damage,"None")) # 0.95 to factor in toughness multiplier
enhancedTalent = ClaraCharacter.useTalent(enhanced=True)
print('Enhanced Talent Damage - Mine: {} - Grimro: {}'.format(enhancedTalent.damage,"None")) # 0.95 to factor in toughness multiplier

print('##### Jing Yuan #####')
JingYuanCharacter = JingYuan(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.lightning'],
                        substats = {'CR': 7, 'CD': 12, 'SPD.flat': 5}),
            lightcone = TheSeriousnessOfBreakfast(**config),
            relicsetone = BandOfSizzlingThunder2pc(),
            relicsettwo = BandOfSizzlingThunder4pc(),
            planarset = InertSalsotto(),
            **config)

skill = JingYuanCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,14611.98532*0.95)) # 0.95 to factor in toughness multiplier
ultimate = JingYuanCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,31759.59534*0.95)) # 0.95 to factor in toughness multiplier
talent = JingYuanCharacter.useTalent()
print('Talent Damage - Mine: {} - Grimro: {}'.format(talent.damage,5156.021606*0.95)) # 0.95 to factor in toughness multiplier

print('##### Himeko #####')
HimekoCharacter = Himeko(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.fire'],
                        substats = {'CR': 12, 'CD': 12}),
            lightcone = TheSeriousnessOfBreakfast(**config),
            relicsetone = FiresmithOfLavaForging2pc(),
            relicsettwo = MusketeerOfWildWheat2pc(),
            planarset = SpaceSealingStation(),
            **config)

skill = HimekoCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,23287.76966*0.95)) # 0.95 to factor in toughness multiplier
ultimate = HimekoCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,44634.89184*0.95)) # 0.95 to factor in toughness multiplier
talent = HimekoCharacter.useTalent()
print('Talent Damage - Mine: {} - Grimro: {}'.format(talent.damage,27169.0646*0.95)) # 0.95 to factor in toughness multiplier

print('##### Hook #####')
HookCharacter = Hook(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.fire'],
                        substats = {'CR': 10, 'CD': 12, 'SPD.flat': 2}),
            lightcone = OnTheFallOfAnAeon(uptime = 0.0, stacks=4.0, **config),
            relicsetone = FiresmithOfLavaForging2pc(),
            relicsettwo = MusketeerOfWildWheat2pc(),
            planarset = RutilantArena(),
            burnedUptime=1.0,
            **config)

print('Grimro does not apply skill damage multiplier to talent damage')
skill = HookCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,(15043.63538+5604.461434)*0.95)) # 0.95 to factor in toughness multiplier
enhancedSkill = HookCharacter.useEnhancedSkill()
print('Enhanced Skill Damage - Mine: {} - Grimro: {}'.format(enhancedSkill.damage,(30500.3661+5604.461434*3)*0.95)) # 0.95 to factor in toughness multiplier
ultimate = HookCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,(22010.24854+5604.461434)*0.95)) # 0.95 to factor in toughness multiplier

print('##### Sampo #####')
SampoCharacter = Sampo(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'ATK.percent', 'DMG.wind'],
                        substats = {'ATK.percent': 12, 'SPD.flat': 8, 'EHR': 4}),
            lightcone = GoodNightAndSleepWell(**config),
            relicsetone = EagleOfTwilightLine2pc(),
            relicsettwo = MusketeerOfWildWheat2pc(),
            planarset = SpaceSealingStation(),
            ultUptime=1.0,
            **config)

skill = SampoCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,(16234.03438+9801.510376)*0.95)) # 0.95 to factor in toughness multiplier
dot = SampoCharacter.useDot() * config['numEnemies']
print('Dot Damage - Mine: {} - Grimro: {}'.format(dot.damage,61259.43985*0.95)) # 0.95 to factor in toughness multiplier
ultimate = SampoCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,22769.81446*0.95)) # 0.95 to factor in toughness multiplier

print('##### Luka #####')
LukaCharacter = Luka(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.physical'],
                        substats = {'ATK.percent': 10, 'SPD.flat': 6, 'EHR': 8}),
            lightcone = GoodNightAndSleepWell(**config),
            relicsetone = ChampionOfStreetwiseBoxing2pc(),
            relicsettwo = ChampionOfStreetwiseBoxing4pc(),
            planarset = SpaceSealingStation(),
            **config)

enhancedBasic = LukaCharacter.useEnhancedBasic()
print('Enhanced Basic Damage - Mine: {} - Grimro: {}'.format(enhancedBasic.damage,30644.0875*0.95)) # 0.95 to factor in toughness multiplier
skill = LukaCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,6337.789357*0.95)) # 0.95 to factor in toughness multiplier
dot = LukaCharacter.useDot()
print('Dot Damage - Mine: {} - Grimro: {}'.format(dot.damage,17416.03905*0.95)) # 0.95 to factor in toughness multiplier
ultimate = LukaCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,17112.03126*0.95)) # 0.95 to factor in toughness multiplier

print('##### Sushang #####')
SushangCharacter = Sushang(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.physical'],
                        substats = {'CR': 7, 'CD': 12, 'ATK.percent': 5}),
                        lightcone = CruisingInTheStellarSea(uptimeHP=0.0, uptimeDefeat=0.0, **config),
                        relicsetone = ChampionOfStreetwiseBoxing2pc(),
                        relicsettwo = ChampionOfStreetwiseBoxing4pc(),
                        planarset = RutilantArena(),
                        **config)

skill = SushangCharacter.useSkill() - SushangCharacter.useSwordStance() * (SushangCharacter.weaknessBrokenUptime + (1.0 - SushangCharacter.weaknessBrokenUptime) * 0.33)
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,9980.537896*0.95)) # 0.95 to factor in toughness multiplier
swordStance = SushangCharacter.useSwordStance()
print('Sword Stance Damage - Mine: {} - Grimro: {}'.format(swordStance.damage,5456.188223*0.95)) # 0.95 to factor in toughness multiplier
ultimate = SushangCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,13163.57782*0.95)) # 0.95 to factor in toughness multiplier

print('##### SilverWolf #####')
SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.quantum'],
                        substats = {'SPD.flat': 4, 'CR': 4, 'CD': 8, 'EHR': 8}),
                        lightcone = BeforeTheTutorialMissionStarts(**config),
                        relicsetone = GeniusOfBrilliantStars2pc(),
                        relicsettwo = GeniusOfBrilliantStars4pc(),
                        planarset = PanCosmicCommercialEnterprise(),
                        talentDefUptime = 1.0,
                        **config)

print((80 + 20 ) / ( ( SilverWolfCharacter.enemyLevel + 20 ) * ( 1 - SilverWolfCharacter.getDefShred(['skill']) ) + 80 + 20 ))
print(SilverWolfCharacter.getDefShred(['skill']))
print(SilverWolfCharacter.getResPen(['skill']))

skill = SilverWolfCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,10035.72419*0.95)) # 0.95 to factor in toughness multiplier
ultimate = SilverWolfCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,19457.01629*0.95)) # 0.95 to factor in toughness multiplier

print('##### Herta #####')
HertaCharacter = Herta(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.ice'],
                        substats = {'SPD.flat': 2, 'CR': 10, 'CD': 12}),
                        lightcone = TheSeriousnessOfBreakfast(**config),
                        relicsetone = HunterOfGlacialForest2pc(),
                        relicsettwo = MusketeerOfWildWheat2pc(),
                        planarset = SpaceSealingStation(),
                        hpThresholdUptime=0.0,
                        frozenUptime=0.0,
                        e2Stacks=5.0,
                        e4Stacks=1.0,
                        **config)

skill = HertaCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,15817.83837*0.95)) # 0.95 to factor in toughness multiplier
talent = HertaCharacter.useTalent()
print('Talent Damage - Mine: {} - Grimro: {}'.format(talent.damage,6499.975867*0.95)) # 0.95 to factor in toughness multiplier
ultimate = HertaCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,31060.48263*0.95)) # 0.95 to factor in toughness multiplier

print('##### Arlan #####')
ArlanCharacter = Arlan(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.lightning'],
                        substats = {'SPD.flat': 2, 'CR': 10, 'CD': 12}),
                        lightcone = OnTheFallOfAnAeon(uptime = 0.0, stacks=4.0, **config),
                        relicsetone = BandOfSizzlingThunder2pc(),
                        relicsettwo = BandOfSizzlingThunder4pc(),
                        planarset = RutilantArena(),
                        **config)

skill = ArlanCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,16828.36764*0.95)) # 0.95 to factor in toughness multiplier
ultimate = ArlanCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,63064.6214*0.95)) # 0.95 to factor in toughness multiplier
