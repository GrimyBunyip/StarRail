from copy import copy
from settings.BaseConfiguration import Configuration
from teams_four.Acheron.AcheronE2BronyaJiaoqiuGallagher import AcheronE2BronyaJiaoqiuGallagher
from teams_four.Acheron.AcheronE2BronyaKafkaGallagher import AcheronE2BronyaKafkaGallagher
from teams_four.Acheron.AcheronE2BronyaPelaGallagher import AcheronE2BronyaPelaGallagher
from teams_four.Acheron.AcheronE2HanabiJiaoqiuGallagher import AcheronE2HanabiJiaoqiuGallagher
from teams_four.Acheron.AcheronE2HanabiKafkaGallagher import AcheronE2HanabiKafkaGallagher
from teams_four.Acheron.AcheronE2HanabiPelaGallagher import AcheronE2HanabiPelaGallagher
from teams_four.Acheron.AcheronGuinaifenPelaGallagher import AcheronGuinaifenPelaGallagher
from teams_four.Acheron.AcheronKafkaBlackSwanGallagher import AcheronKafkaBlackSwanGallagher
from teams_four.Acheron.AcheronPelaJiaoqiuGallagher import AcheronPelaJiaoqiuGallagher
from teams_four.Argenti.ArgentiHanabiTingyunHuohuo import ArgentiHanabiTingyunHuohuo
from teams_four.Blade.BladeBronyaJadeLuocha import BladeBronyaJadeLuocha
from teams_four.Boothill.BoothillBronyaRuanMeiGallagher import BoothillBronyaRuanMeiGallagher
from teams_four.Boothill.BoothillTraiblazerRuanMeiGallagher import BoothillTrailblazerRuanMeiGallagher
from teams_four.Clara.ClaraTingyunHanabiFuxuan import ClaraTingyunHanabiFuxuan
from teams_four.DotTeams.KafkaS1RobinBlackSwanGallagher import KafkaS1RobinBlackSwanGallagher
from teams_four.Firefly.FireflyTraiblazerRuanMeiGallagher import FireflyTrailblazerRuanMeiGallagher
from teams_four.Firefly.FireflyTraiblazerRuanMeiLingsha import FireflyTrailblazerRuanMeiLingsha
from teams_four.Jingliu.JingliuBronyaRuanMeiGallagher import JingliuBronyaRuanMeiGallagher
from teams_four.Jingyuan.JingyuanHanabiTingyunHuohuo import JingYuanHanabiTingyunHuohuo
from teams_four.Jingyuan.JingyuanTingyunHanabiFuxuan import JingyuanTingyunHanabiFuxuan
from teams_four.DotTeams.KafkaGuinaifenBlackSwanLuocha import KafkaGuinaifenBlackSwanLuocha
from teams_four.DotTeams.KafkaS1RuanMeiBlackSwanLuocha import KafkaS1RuanMeiBlackSwanLuocha
from teams_four.Lunae.LunaeHanabiTingyunGallagher import LunaeHanabiTingyunGallagher
from teams_four.Rappa.FireflyTraiblazerRappaGallagher import FireflyTrailblazerRappaGallagher
from teams_four.Rappa.RappaTraiblazerRuanMeiGallagher import RappaTrailblazerRuanMeiGallagher
from teams_four.RatioTopaz.RatioTopazRobinAventurine import DrRatioTopazRobinAventurine
from teams_four.Robin.FeixiaoTopazRobinAventurine import FeixiaoTopazRobinAventurine
from teams_four.Seele.SilverWolfMarchRobinHuohuo import SilverWolfMarchRobinHuohuo
from teams_four.Robin.FeixiaoMarchRobinAventurine import FeixiaoMarchRobinAventurine
from teams_four.Robin.MarchTopazRobinAventurine import MarchTopazRobinAventurine
from teams_four.Seele.SeeleMaxSilverWolfBronyaLuocha import SeeleMaxSilverWolfBronyaLuocha
from teams_four.Seele.SeeleMaxSilverWolfHanabiFuxuan import SeeleMaxSilverWolfHanabiFuxuan
from teams_four.Seele.SeeleMaxSilverWolfRuanMeiFuxuan import SeeleMaxSilverWolfRuanMeiFuxuan
from teams_four.Seele.SeeleMaxSilverWolfTingyunFuxuan import SeeleMaxSilverWolfTingyunFuxuan
from teams_four.Seele.SeeleMidSilverWolfBronyaFuxuan import SeeleMidSilverWolfBronyaFuxuan
from teams_four.Seele.SeeleMidSilverWolfBronyaLuocha import SeeleMidSilverWolfBronyaLuocha
from teams_four.Seele.SeeleNoneSilverWolfHanabiFuxuan import SeeleNoneSilverWolfHanabiLuocha
from teams_four.Yunli.YunliHanabiRobinHuohuo import YunliHanabiRobinHuohuo
from teams_four.Yunli.YunliTingyunHanabiHuohuo import YunliTingyunHanabiHuohuo
from teams_four.Yunli.YunliTingyunHanabiLynx import YunliTingyunHanabiLynx
from teams_four.Yunli.YunliTingyunRobinHuohuo import YunliTingyunRobinHuohuo
from visualizer.visualizer import visualize

visualizationList = []

config = copy(Configuration)
config['numEnemies'] = 3
config['enemyToughness'] = 300 # mostly consider tweaking this for boothill
config['enemySpeed'] = 158 / 1.125 # assume 25% action delay every 2 enemy turns from toughness break

#%% Team Imports

# # Backloaded Teams
visualizationList.append(RappaTrailblazerRuanMeiGallagher(config))
visualizationList.append(FireflyTrailblazerRuanMeiGallagher(config))
visualizationList.append(KafkaGuinaifenBlackSwanLuocha(config))
visualizationList.append(AcheronPelaJiaoqiuGallagher(config))
visualizationList.append(ClaraTingyunHanabiFuxuan(config))
visualizationList.append(YunliTingyunHanabiLynx(config))

# # Team Comparisons
visualizationList.append(ArgentiHanabiTingyunHuohuo(config))
visualizationList.append(BladeBronyaJadeLuocha(config))
visualizationList.append(FeixiaoTopazRobinAventurine(config))
visualizationList.append(JingliuBronyaRuanMeiGallagher(config))
visualizationList.append(JingYuanHanabiTingyunHuohuo(config))
visualizationList.append(LunaeHanabiTingyunGallagher(config))

# # Weaker Teams
# visualizationList.append(MarchTopazRobinAventurine(config))
# visualizationList.append(DrRatioTopazRobinAventurine(config))
# visualizationList.append(SeeleMaxSilverWolfHanabiFuxuan(config))

# # Acheron Teams

# # E2 Teams
# visualizationList.append(AcheronE2BronyaJiaoqiuGallagher(config, acheronSuperposition=1))
# visualizationList.append(AcheronE2HanabiJiaoqiuGallagher(config, acheronSuperposition=1))

# visualizationList.append(AcheronE2BronyaKafkaGallagher(config, acheronSuperposition=1))
# visualizationList.append(AcheronE2HanabiPelaGallagher(config, acheronSuperposition=1))

# visualizationList.append(AcheronE2HanabiKafkaGallagher(config, acheronSuperposition=1))
# visualizationList.append(AcheronE2BronyaPelaGallagher(config, acheronSuperposition=1)) 
# visualizationList.append(AcheronKafkaBlackSwanGallagher(config))

# # E0 teams
# visualizationList.append(AcheronPelaJiaoqiuGallagher(config))
# visualizationList.append(AcheronGuinaifenPelaGallagher(config))

# # Argenti Teams
# visualizationList.append(ArgentiHanabiTingyunHuohuo(config))

# # Blade Teams
# visualizationList.append(BladeBronyaJadeLuocha(config))

# # Boothill Teams
# visualizationList.append(BoothillTrailblazerRuanMeiGallagher(config))
# visualizationList.append(BoothillBronyaRuanMeiGallagher(config))

# Clara Teams
# visualizationList.append(ClaraTingyunHanabiFuxuan(config))

# # Firefly Teams
# visualizationList.append(FireflyTrailblazerRuanMeiGallagher(config))
# visualizationList.append(FireflyTrailblazerRuanMeiLingsha(config))

# # Jingliu Teams
# visualizationList.append(JingliuBronyaRuanMeiGallagher(config))

# # Jingyuan Teams
# visualizationList.append(JingYuanHanabiTingyunHuohuo(config))
# visualizationList.append(JingyuanTingyunHanabiFuxuan(config))

# # Lunae Teams
# visualizationList.append(LunaeHanabiTingyunGallagher(config))

# # Kafka Teams
# # config['enemySpeed'] = 190 / 1.125
# # config['numEnemies'] = 2
# # E0 S0 Teams
# visualizationList.append(KafkaGuinaifenBlackSwanLuocha(config))

# # S1 Teams
# visualizationList.append(KafkaGuinaifenBlackSwanLuocha(config, kafkaSuperposition=True))
# visualizationList.append(KafkaS1RuanMeiBlackSwanLuocha(config))
# visualizationList.append(KafkaS1RobinBlackSwanGallagher(config))

# # Robin Teams

# Feixiao Teams
# visualizationList.append(FeixiaoTopazRobinAventurine(config, robinEidolon=2))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, feixiaoSuperposition=1))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, feixiaoSuperposition=1, feixiaoLightCone='InTheNight'))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, feixiaoSuperposition=1, feixiaoLightCone='BaptismOfPureThought'))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, robinEidolon=0))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, robinEidolon=0, feixiaoLightCone='IVentureForthToHunt'))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, robinEidolon=0, feixiaoEidolon=1))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, robinEidolon=0, feixiaoEidolon=2))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, robinEidolon=1))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, robinEidolon=2))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, robinEidolon=0, robinLightCone='PoisedToBloom'))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, robinEidolon=0, feixiaoLightCone='IVentureForthToHunt', feixiaoEidolon=1))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, robinEidolon=0, feixiaoLightCone='IVentureForthToHunt', feixiaoEidolon=2))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, robinEidolon=0, robinLightCone='CarveTheMoonWeaveTheClouds'))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, robinEidolon=0, robinLightCone='ForTomorrowsJourney'))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, robinEidolon=0, robinLightCone='FlowingNightglow'))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, robinEidolon=2, feixiaoLightCone='IVentureForthToHunt'))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, robinEidolon=2, feixiaoEidolon=1))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, robinEidolon=2, feixiaoEidolon=2))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, robinEidolon=2, feixiaoLightCone='IVentureForthToHunt'))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, robinEidolon=2, robinLightCone='FlowingNightglow'))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, robinEidolon=0))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, robinEidolon=0, feixiaoLightCone='IVentureForthToHunt'))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, robinEidolon=0, feixiaoEidolon=1))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, robinEidolon=0, feixiaoEidolon=2))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, robinEidolon=1))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, robinEidolon=2))
# visualizationList.append(FeixiaoTopazRobinAventurine(config, robinEidolon=2))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, robinEidolon=2))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, robinEidolon=0, robinLightCone='CarveTheMoonWeaveTheClouds'))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, robinEidolon=0, robinLightCone='ForTomorrowsJourney'))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, robinEidolon=0, robinLightCone='FlowingNightglow'))

# the old guard
# visualizationList.append(MarchTopazRobinAventurine(config))

# # Yunli Team
# visualizationList.append(YunliTingyunHanabiLynx(config))
# visualizationList.append(YunliTingyunHanabiHuohuo(config))
# visualizationList.append(YunliTingyunRobinHuohuo(config))
# visualizationList.append(YunliHanabiRobinHuohuo(config))

# visualizationList.append(YunliTingyunRobinHuohuo(config, yunliSuperposition=1))
# visualizationList.append(YunliHanabiRobinHuohuo(config, yunliSuperposition=1))
# visualizationList.append(YunliTingyunRobinHuohuo(config, yunliEidolon=1, yunliSuperposition=1))
# visualizationList.append(YunliTingyunRobinHuohuo(config, yunliEidolon=2, yunliSuperposition=1))
# visualizationList.append(YunliTingyunHanabiHuohuo(config, yunliSuperposition=1))

# Rappa Team
# config['numEnemies'] = 5
# config['enemyToughness'] = 60 # mostly consider tweaking this for boothill
# config['enemyType'] = 'basic'

# visualizationList.append(ArgentiHanabiTingyunHuohuo(config, extraArgentiEnergy=50.0))
# visualizationList.append(BladeBronyaJadeLuocha(config))
# visualizationList.append(RappaTrailblazerRuanMeiGallagher(config, rappaLightcone='AfterTheCharmonyFall', rappaNumSkillOverride=1))

#%% Visualization
# Visualize
visualize(visualizationList, visualizerPath='visualizer\QuadVisual.png', **config)
    
from excelAPI.write2sheet import writeVisualizationList
writeVisualizationList(visualizationList,path='visualizer\QuadVisual.xlsx',sheetname='Quad vs Two')
