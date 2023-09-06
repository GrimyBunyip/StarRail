#Here I will crossreference my stats and damage numbers with Grimro's spreadsheet to check for errors     
#I don't do 8 cycle rotations, though, so this will just be crossreferencing stats and skill damage    

from copy import copy
from settings.BaseConfiguration import Configuration
from baseClasses.RelicStats import RelicStats
from estimator.DefaultEstimator import DefaultEstimator
from visualizer.visualizer import visualize

from characters.destruction.Blade import Blade
from characters.destruction.Clara import Clara
from characters.hunt.DanHeng import DanHeng
from characters.destruction.Jingliu import Jingliu
from characters.nihility.Kafka import Kafka
from characters.destruction.Lunae import Lunae
from characters.hunt.Seele import Seele
from characters.erudition.Serval import Serval
from characters.hunt.Yanqing import Yanqing

from lightCones.destruction.ASecretVow import ASecretVow
from lightCones.erudition.TheSeriousnessOfBreakfast import TheSeriousnessOfBreakfast
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.nihility.Fermata import Fermata
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell

from relicSets.relicSets.BandOfSizzlingThunder import BandOfSizzlingThunder2pc, BandOfSizzlingThunder4pc
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.EagleOfTwilightLine import EagleOfTwilightLine2pc, EagleOfTwilightLine4pc
from relicSets.relicSets.GeniusOfBrilliantStars import GeniusOfBrilliantStars2pc, GeniusOfBrilliantStars4pc
from relicSets.relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc, HunterOfGlacialForest4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc, MusketeerOfWildWheat4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation

config = copy(Configuration)
config['numEnemies'] = 3 # Going to compare my numbers vs Grimro's 3 target numbers

print('##### Lunae #####')
LunaeCharacter = Lunae(RelicStats(mainstats = ['percAtk', 'percAtk', 'CR', 'imagDmg'],
                        substats = {'CR': 12, 'CD': 12}),
            lightcone = OnTheFallOfAnAeon(uptime = 0.0, stacks=4.0, **config), # Grimro assumes zero uptime on break
            relicsetone = MusketeerOfWildWheat2pc(),
            relicsettwo = MusketeerOfWildWheat4pc(),
            planarset = RutilantArena(),
            **config)

print('Atk - Mine: {} - Grimro: {}'.format(LunaeCharacter.getTotalAtk('basic'),2788.63616+4*0.16*1227.74))
print('CR - Mine: {} - Grimro: {}'.format(LunaeCharacter.CR,0.92392))
print('CD - Mine: {} - Grimro: {}'.format(LunaeCharacter.CD,1.43984))
print('Dmg - Mine: {} - Grimro: {}'.format(LunaeCharacter.getTotalDmg('basic')-1.0,0.612803+0.3))
enhancedBasic = LunaeCharacter.useEnhancedBasic3()
print('Enhanced Basic Damage - Mine: {} - Grimro: {}'.format(enhancedBasic.damage,85045.71*0.95)) # 0.95 to factor in toughness multiplier
ultimate = LunaeCharacter.useUltimate()
LunaeCharacter.endTurn() # reset heart stacks
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,60593.375501*0.95)) # 0.95 to factor in toughness multiplier

print('##### Blade #####')
bladeCharacter = Blade(RelicStats(mainstats = ['percHP', 'flatSpd', 'CD', 'windDmg'],
                        substats = {'CR': 12, 'CD': 12}),
            lightcone = ASecretVow(uptime = 0.5, **config),
            relicsetone = LongevousDisciple2pc(),
            relicsettwo = LongevousDisciple4pc(),
            planarset = InertSalsotto(),
            hpLossTally=0.9, #looks like grimro uses an hp loss tally of 100%
            **config)


print('Atk - Mine: {} - Grimro: {}'.format(bladeCharacter.getTotalAtk('basic'),1372.3900))
print('HP - Mine: {} - Grimro: {}'.format(bladeCharacter.getTotalHP('basic'),5132.95776))
print('CR - Mine: {} - Grimro: {}'.format(bladeCharacter.CR,0.75992))
print('CD - Mine: {} - Grimro: {}'.format(bladeCharacter.CD,1.84784))
print('Dmg - Mine: {} - Grimro: {}'.format(bladeCharacter.getTotalDmg('basic')-1.0,0.9880000))
enhancedBasic = bladeCharacter.useEnhancedBasic()
print('Enhanced Basic Damage - Mine: {} - Grimro: {}'.format(enhancedBasic.damage,27970.52941*0.95)) # 0.95 to factor in toughness multiplier
talent = bladeCharacter.useTalent()
print('Talent Damage - Mine: {} - Grimro: {}'.format(talent.damage,58792.58835*0.95)) # 0.95 to factor in toughness multiplier
ultimate = bladeCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,53896.22855*0.95)) # 0.95 to factor in toughness multiplier

print('##### Seele #####')
SeeleCharacter = Seele(relicstats = RelicStats(mainstats = ['percAtk', 'percAtk', 'CR', 'quanDmg'],
                        substats = {'CR': 7, 'CD': 12, 'percAtk': 4}),
            lightcone = CruisingInTheStellarSea(uptimeHP=0.0, uptimeDefeat=0.0, **config), #unclear what uptime 
            relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo=GeniusOfBrilliantStars4pc(), planarset = RutilantArena(),
            **config)

print('Atk - Mine: {} - Grimro: {}'.format(SeeleCharacter.getTotalAtk('basic'),3042.1576))
print('CR - Mine: {} - Grimro: {}'.format(SeeleCharacter.CR,0.81812))
print('CD - Mine: {} - Grimro: {}'.format(SeeleCharacter.CD,1.43984))
print('Dmg - Mine: {} - Grimro: {}'.format(SeeleCharacter.getTotalDmg('basic')-1.0,0.488803))
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
KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['percAtk', 'flatSpd', 'percAtk', 'lighDmg'],
                        substats = {'EHR': 4, 'percAtk': 12, 'flatSpd': 8}),
            lightcone = GoodNightAndSleepWell(**config),
            relicsetone = BandOfSizzlingThunder2pc(), relicsettwo = BandOfSizzlingThunder4pc(), planarset = SpaceSealingStation(),
            **config)

print('Atk - Mine: {} - Grimro: {}'.format(KafkaCharacter.getTotalAtk('basic'),3877.417024))
print('CR - Mine: {} - Grimro: {}'.format(KafkaCharacter.CR,0.05))
print('CD - Mine: {} - Grimro: {}'.format(KafkaCharacter.CD,0.50))
print('Dmg - Mine: {} - Grimro: {}'.format(KafkaCharacter.getTotalDmg('basic')-1.0,1.208803))

dot = KafkaCharacter.useDot()
print('Dot Damage - Mine: {} - Grimro: {}'.format(dot.damage,35481.29433*0.95)) # 0.95 to factor in toughness multiplier
skill = KafkaCharacter.useSkill()
breakDot = KafkaCharacter.useBreakDot()
skill -= ( dot + breakDot ) * ( 0.78 if KafkaCharacter.eidolon >= 3 else 0.75 ) / KafkaCharacter.numEnemies
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,11704.74882*0.95)) # 0.95 to factor in toughness multiplier
ultimate = KafkaCharacter.useUltimate()
ultimate -= ( dot + breakDot ) * ( 1.0 if KafkaCharacter.eidolon >= 5 else 1.04)
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,10032.64184*0.95)) # 0.95 to factor in toughness multiplier
talent = KafkaCharacter.useTalent()
print('Talent Damage - Mine: {} - Grimro: {}'.format(talent.damage,5852.374409*0.95)) # 0.95 to factor in toughness multiplier

print('##### Serval #####')
ServalCharacter = Serval(relicstats = RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'lighDmg'],
                        substats = {'CR': 7, 'percAtk': 4, 'CD': 12}),
            lightcone = TheSeriousnessOfBreakfast(stacks=3,**config),
            relicsetone = BandOfSizzlingThunder2pc(), relicsettwo = BandOfSizzlingThunder4pc(), planarset = SpaceSealingStation(),
            **config)

print('Atk - Mine: {} - Grimro: {}'.format(ServalCharacter.getTotalAtk('basic'),2912.739379))
print('CR - Mine: {} - Grimro: {}'.format(ServalCharacter.CR,0.76512))
print('CD - Mine: {} - Grimro: {}'.format(ServalCharacter.CD,1.19984))
print('Dmg - Mine: {} - Grimro: {}'.format(ServalCharacter.getTotalDmg('basic')-1.0,0.728803))

dot = ServalCharacter.useDot()
print('Dot Damage - Mine: {} - Grimro: {}'.format(dot.damage,9657.606147*0.95)) # 0.95 to factor in toughness multiplier
skill = ServalCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,(15436.24751+12823.95947)*0.95)) # 0.95 to factor in toughness multiplier
ultimate = ServalCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,(31476.99142+12823.95947)*0.95)) # 0.95 to factor in toughness multiplier

print('##### Dan Heng #####')
DanHengCharacter = DanHeng(relicstats = RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'windDmg'],
                        substats = {'CR': 10, 'CD': 12, 'percAtk': 2}),
            lightcone = CruisingInTheStellarSea(uptimeHP=1.0, uptimeDefeat=0.0, **config),
            relicsetone = EagleOfTwilightLine2pc(), relicsettwo=EagleOfTwilightLine4pc(), planarset = SpaceSealingStation(),
            talentUptime = 0.0,
            fasterThanLightUptime = 0.8,
            e1Uptime=0.0,
            **config)

print('Atk - Mine: {} - Grimro: {}'.format(DanHengCharacter.getTotalAtk('basic'),2429.29895))
print('CR - Mine: {} - Grimro: {}'.format(DanHengCharacter.CR,0.8256))
print('CD - Mine: {} - Grimro: {}'.format(DanHengCharacter.CD,1.19984))
print('Dmg - Mine: {} - Grimro: {}'.format(DanHengCharacter.getTotalDmg('basic')-1.0,0.712803))

skill = DanHengCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,12368.0652*0.95)) # 0.95 to factor in toughness multiplier
ultimate = DanHengCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,24286.38257*0.95)) # 0.95 to factor in toughness multiplier

print('##### Yanqing #####')
YanqingCharacter = Yanqing(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CD', 'iceDmg'],
                        substats = {'percAtk': 12, 'CD': 12}),
                lightcone = CruisingInTheStellarSea(uptimeHP=0.0, uptimeDefeat=0.0, **config),
                relicsetone = HunterOfGlacialForest2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SpaceSealingStation(),
                soulsteelUptime = 1.0,
                **config)

print('Atk - Mine: {} - Grimro: {}'.format(YanqingCharacter.getTotalAtk('basic'),3420.24359))
print('CR - Mine: {} - Grimro: {}'.format(YanqingCharacter.CR,0.21+0.2))
print('CD - Mine: {} - Grimro: {}'.format(YanqingCharacter.CD,1.84784+0.3))
print('Dmg - Mine: {} - Grimro: {}'.format(YanqingCharacter.getTotalDmg('basic')-1.0,0.632803))

skill = YanqingCharacter.useSkill()
print('Skill Damage - Mine: {} - Grimro: {}'.format(skill.damage,12502.91557*0.95)) # 0.95 to factor in toughness multiplier
ultimate = YanqingCharacter.useUltimate()
print('Ultimate Damage - Mine: {} - Grimro: {}'.format(ultimate.damage,36863.01988*0.95)) # 0.95 to factor in toughness multiplier
talent = YanqingCharacter.useTalent()
freezeDot = YanqingCharacter.useFreezeDot()
talent -= freezeDot
print('Talent Damage - Mine: {} - Grimro: {}'.format(talent.damage,4000.932983*0.95*0.6)) # 0.95 to factor in toughness multiplier

print('##### Clara #####')
ClaraCharacter = Clara(RelicStats(mainstats = ['percAtk', 'flatSpd', 'CR', 'physDmg'],
                        substats = {'CR': 10, 'CD': 10}),
            lightcone = OnTheFallOfAnAeon(uptime = 0.0, stacks=5.0, **config),
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
