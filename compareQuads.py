from copy import copy
from settings.BaseConfiguration import Configuration
from teams_four.ArgentiBronyaPelaHuohuo import ArgentiBronyaPelaHuohuo
from teams_four.ArgentiHanyaRuanMeiHuohuo import ArgentiHanyaRuanMeiHuohuo
from teams_four.ArgentiHanyaTingyunFuxuan import ArgentiHanyaTingyunFuxuan
from teams_four.ArgentiHanyaTingyunHuohuo import ArgentiHanyaTingyunHuohuo
from teams_four.ArgentiRuanMeiTingyunHuohuo import ArgentiRuanMeiTingyunHuohuo
from teams_four.BladeBronyaPelaFuxuan import BladeBronyaPelaFuxuan
from teams_four.BladeBronyaPelaLuocha import BladeBronyaPelaLuocha
from teams_four.BladeBronyaPelaLynx import BladeBronyaPelaLynx
from teams_four.BladeBronyaRuanMeiFuxuan import BladeBronyaRuanMeiFuxuan
from teams_four.BladeBronyaRuanMeiLuocha import BladeBronyaRuanMeiLuocha
from teams_four.ClaraSilverWolfPelaLuocha import ClaraSilverWolfPelaLuocha
from teams_four.ClaraTingyunHanabiLuocha import ClaraTingyunHanabiLuocha
from teams_four.ClaraTingyunHanyaLuocha import ClaraTingyunHanyaLuocha
from teams_four.ClaraTingyunPelaLuocha import ClaraTingyunPelaLuocha
from teams_four.ClaraTingyunTopazLuocha import ClaraTingyunTopazLuocha
from teams_four.ClaraTopazAstaLuocha import ClaraTopazAstaLuocha
from teams_four.ClaraTopazHanyaLuocha import ClaraTopazHanyaLuocha
from teams_four.JingliuBronyaPelaLuocha import JingliuBronyaPelaLuocha
from teams_four.JingliuBronyaRuanMeiLuocha import JingliuBronyaRuanMeiLuocha
from teams_four.JingliuHanyaBladeHuohuo import JingliuHanyaBladeHuohuo
from teams_four.JingliuRuanMeiBladeLuocha import JingliuRuanMeiBladeLuocha
from teams_four.JingyuanTingyunAstaLuocha import JingyuanTingyunAstaLuocha
from teams_four.JingyuanTingyunHanyaFuxuan import JingyuanTingyunHanyaFuxuan
from teams_four.JingyuanTingyunTopazLuocha import JingyuanTingyunTopazLuocha
from teams_four.KafkaBlackSwanRuanMeiHuohuo import KafkaBlackSwanRuanMeiHuohuo
from teams_four.KafkaBlackSwanRuanMeiLuocha import KafkaBlackSwanRuanMeiLuocha
from teams_four.KafkaGuinaifenAstaLuocha import KafkaGuinaifenAstaLuocha
from teams_four.KafkaGuinaifenBlackSwanLuocha import KafkaGuinaifenBlackSwanLuocha
from teams_four.KafkaGuinaifenHanyaLuocha import KafkaGuinaifenHanyaLuocha
from teams_four.KafkaGuinaifenLukaLuocha import KafkaGuinaifenLukaLuocha
from teams_four.KafkaGuinaifenRuanMeiLuocha import KafkaGuinaifenRuanMeiLuocha
from teams_four.KafkaGuinaifenSampoLuocha import KafkaGuinaifenSampoLuocha
from teams_four.KafkaSampoRuanMeiLuocha import KafkaSampoRuanMeiLuocha
from teams_four.KafkaTingyunRuanMeiLuocha import KafkaTingyunRuanMeiLuocha
from teams_four.LunaeHanabiHanyaLuocha import LunaeHanabiHanyaLuocha
from teams_four.LunaeHanabiHanyaLuochaSlow import LunaeHanabiHanyaLuochaSlow
from teams_four.LunaeHanabiTingyunLuocha import LunaeHanabiTingyunLuocha
from teams_four.LunaeHanabiTingyunLuochaSlow import LunaeHanabiTingyunLuochaSlow
from teams_four.LunaeHanyaPelaLuocha import LunaeHanyaPelaLuocha
from teams_four.LunaeHanyaTingyunLuocha import LunaeHanyaTingyunLuocha
from teams_four.LunaeHanyaYukongLuocha import LunaeHanyaYukongLuocha
from teams_four.LunaePelaTingyunLuocha import LunaePelaTingyunLuocha
from teams_four.LunaePelaYukongLuocha import LunaePelaYukongLuocha
from teams_four.LunaeRuanMeiTingyunLuocha import LunaeRuanMeiTingyunLuocha
from teams_four.LunaeTingyunYukongLuocha import LunaeTingyunYukongLuocha
from teams_four.QingqueHanabiSilverWolfLuocha import QingqueHanabiSilverWolfLuocha
from teams_four.QingqueHanyaPelaFuxuan import QingqueHanyaPelaFuxuan
from teams_four.QingqueHanyaSilverWolfFuxuan import QingqueHanyaSilverWolfFuxuan
from teams_four.RatioBronyaSilverWolfLuocha import DrRatioBronyaSilverWolfLuocha
from teams_four.RatioHanabiSilverWolfLuocha import DrRatioHanabiSilverWolfLuocha
from teams_four.RatioRuanMeiSilverWolfLuocha import DrRatioRuanMeiSilverWolfLuocha
from teams_four.RatioTingyunSilverWolfLuocha import DrRatioTingyunSilverWolfLuocha
from teams_four.RatioTopazAstaLuocha import DrRatioTopazAstaLuocha
from teams_four.RatioHanyaSilverWolfLuocha import DrRatioHanyaSilverWolfLuocha
from teams_four.RatioTopazHanyaLuocha import DrRatioTopazHanyaLuocha
from teams_four.RatioTopazRuanMeiLuocha import DrRatioTopazRuanMeiLuocha
from teams_four.RatioTopazSilverWolfLuocha import DrRatioTopazSilverWolfLuocha
from teams_four.SeeleMaxSilverWolfBronyaLuocha import SeeleMaxSilverWolfBronyaLuocha
from teams_four.SeeleMaxSilverWolfRuanMeiFuxuan import SeeleMaxSilverWolfRuanMeiFuxuan
from teams_four.SeeleMaxSilverWolfTingyunFuxuan import SeeleMaxSilverWolfTingyunFuxuan
from teams_four.SeeleMidSilverWolfBronyaFuxuan import SeeleMidSilverWolfBronyaFuxuan
from teams_four.SeeleMidSilverWolfBronyaLuocha import SeeleMidSilverWolfBronyaLuocha
from teams_four.TopazTingyunHanyaLuocha import TopazTingyunHanyaLuocha
from teams_four.XueyiAstaTopazFuxuan import XueyiAstaTopazFuxuan
from teams_four.XueyiHanyaPelaFuxuan import XueyiHanyaPelaFuxuan
from visualizer.visualizer import visualize

visualizationList = []

config = copy(Configuration)
config['numEnemies'] = 2
config['enemySpeed'] = 132 / 1.125 # assume 25% action delay every 2 enemy turns from toughness break

#%% Team Imports

# Argenti Teams
#visualizationList.append(ArgentiHanyaTingyunHuohuo(config))
#visualizationList.append(ArgentiHanyaTingyunFuxuan(config))
#visualizationList.append(ArgentiRuanMeiTingyunHuohuo(config))
#visualizationList.append(ArgentiHanyaRuanMeiHuohuo(config))
#visualizationList.append(ArgentiBronyaPelaHuohuo(config)) #calculation is suspicious to me

# Blade Teams
#visualizationList.append(BladeBronyaRuanMeiFuxuan(config)) # 100% vow uptime with fu xuan
#visualizationList.append(BladeBronyaPelaFuxuan(config)) # 100% vow uptime with fu xuan
#visualizationList.append(BladeBronyaRuanMeiLuocha(config))
#visualizationList.append(BladeBronyaPelaLynx(config))
#visualizationList.append(BladeBronyaPelaLuocha(config))

# Clara Teams
#visualizationList.append(ClaraTingyunHanabiLuocha(config))
#visualizationList.append(ClaraTingyunHanyaLuocha(config))
#visualizationList.append(ClaraTopazAstaLuocha(config))
#visualizationList.append(ClaraTopazHanyaLuocha(config))
#visualizationList.append(ClaraTingyunPelaLuocha(config))
#visualizationList.append(ClaraTingyunTopazLuocha(config))
#visualizationList.append(ClaraSilverWolfPelaLuocha(config))

# Dr Ratio Teams
#visualizationList.append(DrRatioHanabiSilverWolfLuocha(config))
#visualizationList.append(DrRatioTingyunSilverWolfLuocha(config))
#visualizationList.append(DrRatioHanyaSilverWolfLuocha(config))
#visualizationList.append(DrRatioTopazAstaLuocha(config))
#visualizationList.append(DrRatioTopazHanyaLuocha(config))
#visualizationList.append(DrRatioTopazRuanMeiLuocha(config))
#visualizationList.append(DrRatioRuanMeiSilverWolfLuocha(config))
#visualizationList.append(DrRatioTopazSilverWolfLuocha(config))
#visualizationList.append(DrRatioBronyaSilverWolfLuocha(config))

# Jingliu Teams
#visualizationList.append(JingliuBronyaRuanMeiLuocha(config))
#visualizationList.append(JingliuBronyaPelaLuocha(config))
#visualizationList.append(JingliuRuanMeiBladeLuocha(config))
#visualizationList.append(JingliuHanyaBladeHuohuo(config))

# Jingyuan Teams
#visualizationList.append(JingyuanTingyunAstaLuocha(config))
#visualizationList.append(JingyuanTingyunHanyaFuxuan(config))
#visualizationList.append(JingyuanTingyunTopazLuocha(config))

# Lunae Teams
visualizationList.append(LunaeHanabiTingyunLuocha(config)) # Retired, we dont need full SP rotations
visualizationList.append(LunaeHanabiHanyaLuocha(config)) # Retired, we dont need full Sp rotations
visualizationList.append(LunaeHanyaTingyunLuocha(config))
visualizationList.append(LunaeHanabiHanyaLuochaSlow(config)) # Retired, we dont need full SP rotations
visualizationList.append(LunaeHanabiTingyunLuochaSlow(config))
visualizationList.append(LunaeHanyaYukongLuocha(config))
visualizationList.append(LunaeHanyaPelaLuocha(config))
visualizationList.append(LunaeRuanMeiTingyunLuocha(config))
visualizationList.append(LunaeTingyunYukongLuocha(config))
visualizationList.append(LunaePelaTingyunLuocha(config))
visualizationList.append(LunaePelaYukongLuocha(config))

# Kafka Teams
#visualizationList.append(KafkaGuinaifenBlackSwanLuocha(config))
#visualizationList.append(KafkaGuinaifenSampoLuocha(config))
#visualizationList.append(KafkaGuinaifenRuanMeiLuocha(config))
#visualizationList.append(KafkaSampoRuanMeiLuocha(config))
#visualizationList.append(KafkaGuinaifenLukaLuocha(config))
#visualizationList.append(KafkaGuinaifenHanyaLuocha(config))

#visualizationList.append(KafkaBlackSwanRuanMeiHuohuo(config)) # Night of Fright lightcone, retiring this
#visualizationList.append(KafkaBlackSwanRuanMeiLuocha(config)) # patience lightcone, retiring this
#visualizationList.append(KafkaTingyunRuanMeiLuocha(config)) # mediocre, retiring this

# Qingque Teams
#visualizationList.append(QingqueHanabiSilverWolfLuocha(config))
#visualizationList.append(QingqueHanyaSilverWolfFuxuan(config))
#visualizationList.append(QingqueHanyaPelaFuxuan(config))

# Seele Teams
#visualizationList.append(SeeleMaxSilverWolfTingyunFuxuan(config))
#visualizationList.append(SeeleMaxSilverWolfRuanMeiFuxuan(config))
#visualizationList.append(SeeleMaxSilverWolfBronyaLuocha(config))
#visualizationList.append(SeeleMidSilverWolfBronyaLuocha(config))
#visualizationList.append(SeeleMidSilverWolfBronyaFuxuan(config))

# Solo Topaz Teams
#visualizationList.append(TopazTingyunHanyaLuocha(config))

# Xueyi Teams
#visualizationList.append(XueyiHanyaPelaFuxuan(config))
#visualizationList.append(XueyiAstaTopazFuxuan(config))

#%% Visualization
# Visualize
visualize(visualizationList, visualizerPath='visualizer\QuadVisual.png', **config)
    
from excelAPI.write2sheet import writeVisualizationList
writeVisualizationList(visualizationList,path='visualizer\QuadVisual.xlsx',sheetname='Quad vs Two')
