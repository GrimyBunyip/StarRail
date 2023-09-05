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

# Lunae
LunaeCharacter = Lunae(RelicStats(mainstats = ['percAtk', 'percAtk', 'CR', 'imagDmg'],
                        substats = {'CR': 12, 'CD': 12}),
            lightcone = OnTheFallOfAnAeon(uptime = 0.0, stacks=4.0, **config), # Grimro assumes zero uptime on break
            relicsetone = MusketeerOfWildWheat2pc(),
            relicsettwo = MusketeerOfWildWheat4pc(),
            planarset = RutilantArena(),
            **config)

print('Atk - Mine: {} - Grimro: {}'.format(LunaeCharacter.getTotalAtk('basic'),2786+4*0.08*1227))
print('CR - Mine: {} - Grimro: {}'.format(LunaeCharacter.CR,0.92392))
print('CD - Mine: {} - Grimro: {}'.format(LunaeCharacter.CD,1.43984))
print('Dmg - Mine: {} - Grimro: {}'.format(LunaeCharacter.getTotalDmg('basic')-1.0,0.6120+0.3))
enhancedBasic = LunaeCharacter.useEnhancedBasic3()
LunaeCharacter.endTurn() # reset heart stacks
print('Enhanced Basic Damage - Mine: {} - Grimro: {}'.format(enhancedBasic.damage,84950.65*0.95)) # 0.95 to factor in toughness multiplier