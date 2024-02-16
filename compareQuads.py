from copy import copy
from settings.BaseConfiguration import Configuration
from teams_four.ArgentiBronyaPelaHuohuo import ArgentiBronyaPelaHuohuo
from teams_four.ArgentiHanabiTingyunHuohuo import ArgentiHanabiTingyunHuohuo
from teams_four.ArgentiHanyaRuanMeiHuohuo import ArgentiHanyaRuanMeiHuohuo
from teams_four.ArgentiHanyaTingyunFuxuan import ArgentiHanyaTingyunFuxuan
from teams_four.ArgentiHanyaTingyunHuohuo import ArgentiHanyaTingyunHuohuo
from teams_four.ArgentiRuanMeiTingyunHuohuo import ArgentiRuanMeiTingyunHuohuo
from teams_four.BladeBronyaHanabiLuocha import BladeBronyaHanabiLuocha
from teams_four.BladeBronyaPelaFuxuan import BladeBronyaPelaFuxuan
from teams_four.BladeBronyaPelaLuocha import BladeBronyaPelaLuocha
from teams_four.BladeBronyaPelaLynx import BladeBronyaPelaLynx
from teams_four.BladeBronyaRuanMeiFuxuan import BladeBronyaRuanMeiFuxuan
from teams_four.BladeBronyaRuanMeiLuocha import BladeBronyaRuanMeiLuocha
from teams_four.ClaraSilverWolfPelaLuocha import ClaraSilverWolfPelaLuocha
from teams_four.ClaraTingyunHanabiFuxuan import ClaraTingyunHanabiFuxuan
from teams_four.ClaraTingyunHanabiFuxuanEscapade import ClaraTingyunHanabiFuxuanEscapade
from teams_four.ClaraTingyunHanabiLuocha import ClaraTingyunHanabiLuocha
from teams_four.ClaraTingyunHanyaLuocha import ClaraTingyunHanyaLuocha
from teams_four.ClaraTingyunPelaLuocha import ClaraTingyunPelaLuocha
from teams_four.ClaraTingyunTopazLuocha import ClaraTingyunTopazLuocha
from teams_four.ClaraTopazAstaLuocha import ClaraTopazAstaLuocha
from teams_four.ClaraTopazHanyaLuocha import ClaraTopazHanyaLuocha
from teams_four.JingliuBronyaHanabiLuocha import JingliuBronyaHanabiLuocha
from teams_four.JingliuBronyaPelaLuocha import JingliuBronyaPelaLuocha
from teams_four.JingliuBronyaRuanMeiLuocha import JingliuBronyaRuanMeiLuocha
from teams_four.JingliuHanyaBladeHuohuo import JingliuHanyaBladeHuohuo
from teams_four.JingliuRuanMeiBladeLuocha import JingliuRuanMeiBladeLuocha
from teams_four.JingyuanTingyunAstaLuocha import JingyuanTingyunAstaLuocha
from teams_four.JingyuanTingyunHanabiFuxuan import JingyuanTingyunHanabiFuxuan
from teams_four.JingyuanTingyunHanabiLuocha import JingyuanTingyunHanabiLuocha
from teams_four.JingyuanTingyunHanyaFuxuan import JingyuanTingyunHanyaFuxuan
from teams_four.JingyuanTingyunTopazLuocha import JingyuanTingyunTopazLuocha
from teams_four.KafkaGuinaifenAstaLuocha import KafkaGuinaifenAstaLuocha
from teams_four.KafkaGuinaifenBlackSwanLuocha import KafkaGuinaifenBlackSwanLuocha
from teams_four.KafkaGuinaifenBlackSwanLuochaPatience import KafkaGuinaifenBlackSwanLuochaPatience
from teams_four.KafkaGuinaifenRuanMeiLuochaPatience import KafkaGuinaifenRuanMeiLuochaPatience
from teams_four.KafkaHanyaBlackSwanLuochaPatience import KafkaHanyaBlackSwanLuochaPatience
from teams_four.KafkaRuanMeiBlackSwanLuochaPatience import KafkaRuanMeiBlackSwanLuochaPatience
from teams_four.KafkaGuinaifenHanyaLuocha import KafkaGuinaifenHanyaLuocha
from teams_four.KafkaGuinaifenLukaLuocha import KafkaGuinaifenLukaLuocha
from teams_four.KafkaGuinaifenRuanMeiLuocha import KafkaGuinaifenRuanMeiLuocha
from teams_four.KafkaGuinaifenSampoLuocha import KafkaGuinaifenSampoLuocha
from teams_four.KafkaSampoRuanMeiLuocha import KafkaSampoRuanMeiLuocha
from teams_four.KafkaTingyunRuanMeiLuocha import KafkaTingyunRuanMeiLuocha
from teams_four.LunaeHanabiTingyunLuocha import LunaeHanabiTingyunLuocha
from teams_four.LunaeHanyaPelaLuocha import LunaeHanyaPelaLuocha
from teams_four.LunaeHanyaTingyunLuocha import LunaeHanyaTingyunLuocha
from teams_four.LunaeHanyaYukongLuocha import LunaeHanyaYukongLuocha
from teams_four.LunaePelaTingyunLuocha import LunaePelaTingyunLuocha
from teams_four.LunaePelaYukongLuocha import LunaePelaYukongLuocha
from teams_four.LunaeRuanMeiTingyunLuocha import LunaeRuanMeiTingyunLuocha
from teams_four.LunaeTingyunYukongLuocha import LunaeTingyunYukongLuocha
from teams_four.QingqueHanabiPelaFuxuan import QingqueHanabiPelaFuxuan
from teams_four.QingqueHanabiSilverWolfLuocha import QingqueHanabiSilverWolfLuocha
from teams_four.QingqueHanyaPelaFuxuan import QingqueHanyaPelaFuxuan
from teams_four.QingqueHanyaSilverWolfFuxuan import QingqueHanyaSilverWolfFuxuan
from teams_four.RatioBronyaSilverWolfLuocha import DrRatioBronyaSilverWolfLuocha
from teams_four.RatioHanabiSilverWolfLuocha import DrRatioHanabiSilverWolfLuocha
from teams_four.RatioHanyaSilverWolfFuxuan import DrRatioHanyaSilverWolfFuxuan
from teams_four.RatioRuanMeiSilverWolfLuocha import DrRatioRuanMeiSilverWolfLuocha
from teams_four.RatioTingyunSilverWolfLuocha import DrRatioTingyunSilverWolfLuocha
from teams_four.RatioTopazAstaLuocha import DrRatioTopazAstaLuocha
from teams_four.RatioHanyaSilverWolfLuocha import DrRatioHanyaSilverWolfLuocha
from teams_four.RatioTopazHanyaLuocha import DrRatioTopazHanyaLuocha
from teams_four.RatioTopazRuanMeiLuocha import DrRatioTopazRuanMeiLuocha
from teams_four.RatioTopazSilverWolfLuocha import DrRatioTopazSilverWolfLuocha
from teams_four.RuanMeiGuinaifenBlackSwanLuocha import RuanMeiGuinaifenBlackSwanLuocha
from teams_four.SampoGuinaifenBlackSwanLuocha import SampoGuinaifenBlackSwanLuocha
from teams_four.SeeleMaxSilverWolfBronyaLuocha import SeeleMaxSilverWolfBronyaLuocha
from teams_four.SeeleMaxSilverWolfHanabiFuxuan import SeeleMaxSilverWolfHanabiFuxuan
from teams_four.SeeleMaxSilverWolfRuanMeiFuxuan import SeeleMaxSilverWolfRuanMeiFuxuan
from teams_four.SeeleMaxSilverWolfTingyunFuxuan import SeeleMaxSilverWolfTingyunFuxuan
from teams_four.SeeleMidSilverWolfBronyaFuxuan import SeeleMidSilverWolfBronyaFuxuan
from teams_four.SeeleMidSilverWolfBronyaLuocha import SeeleMidSilverWolfBronyaLuocha
from teams_four.SeeleNoneSilverWolfHanabiFuxuan import SeeleNoneSilverWolfHanabiLuocha
from teams_four.TopazTingyunHanabiFuxuan import TopazTingyunHanabiFuxuan
from teams_four.TopazTingyunHanyaFuxuan import TopazTingyunHanyaFuxuan
from teams_four.XueyiAstaTopazFuxuan import XueyiAstaTopazFuxuan
from teams_four.XueyiHanabiTingyunFuxuan import XueyiHanabiTingyunFuxuan
from teams_four.XueyiHanyaPelaFuxuan import XueyiHanyaPelaFuxuan
from teams_four.YanqingTingyunHanabiGepard import YanqingTingyunHanabiGepard
from teams_four.YanqingTingyunRuanMeiGepard import YanqingTingyunRuanMeiGepard
from visualizer.visualizer import visualize

visualizationList = []

config = copy(Configuration)
config['numEnemies'] = 3
config['enemySpeed'] = 190 / 1.125 # assume 25% action delay every 2 enemy turns from toughness break

#%% Team Imports

# Argenti Teams
# visualizationList.append(ArgentiHanabiTingyunHuohuo(config))
# visualizationList.append(ArgentiHanyaTingyunHuohuo(config))
# visualizationList.append(ArgentiHanyaTingyunFuxuan(config))
# visualizationList.append(ArgentiRuanMeiTingyunHuohuo(config))
# visualizationList.append(ArgentiHanyaRuanMeiHuohuo(config))
# visualizationList.append(ArgentiBronyaPelaHuohuo(config)) #calculation is suspicious to me

# Blade Teams
# visualizationList.append(BladeBronyaHanabiLuocha(config))
# # visualizationList.append(BladeBronyaRuanMeiLuocha(config))
# # visualizationList.append(BladeBronyaPelaLynx(config))
# # visualizationList.append(BladeBronyaPelaLuocha(config))

# # visualizationList.append(BladeBronyaPelaFuxuan(config)) # 100% vow uptime with fu xuan
# # visualizationList.append(BladeBronyaRuanMeiFuxuan(config)) # 100% vow uptime with fu xuan, unbalanced SP usage

# # Clara Teams
# visualizationList.append(ClaraTingyunHanabiFuxuan(config))
# # visualizationList.append(ClaraTingyunHanabiLuocha(config))
# # visualizationList.append(ClaraTingyunHanyaLuocha(config))
# # visualizationList.append(ClaraTopazAstaLuocha(config))
# # visualizationList.append(ClaraTopazHanyaLuocha(config))
# # visualizationList.append(ClaraTingyunPelaLuocha(config))
# # visualizationList.append(ClaraTingyunTopazLuocha(config))
# # visualizationList.append(ClaraSilverWolfPelaLuocha(config))
# # visualizationList.append(ClaraTingyunHanabiFuxuanEscapade(config))

# # Dr Ratio Teams
# visualizationList.append(DrRatioHanyaSilverWolfFuxuan(config))
# # visualizationList.append(DrRatioHanyaSilverWolfLuocha(config))
# # visualizationList.append(DrRatioHanabiSilverWolfLuocha(config))
# # visualizationList.append(DrRatioTingyunSilverWolfLuocha(config))
# # visualizationList.append(DrRatioTopazAstaLuocha(config))
# # visualizationList.append(DrRatioTopazHanyaLuocha(config))
# # visualizationList.append(DrRatioTopazRuanMeiLuocha(config))
# # visualizationList.append(DrRatioRuanMeiSilverWolfLuocha(config))
# # visualizationList.append(DrRatioTopazSilverWolfLuocha(config))
# # visualizationList.append(DrRatioBronyaSilverWolfLuocha(config)) # might be a bit of an underbaked team.

# # Jingliu Teams
# visualizationList.append(JingliuBronyaRuanMeiLuocha(config))
# # visualizationList.append(JingliuBronyaHanabiLuocha(config))
# # visualizationList.append(JingliuBronyaPelaLuocha(config))
# # visualizationList.append(JingliuRuanMeiBladeLuocha(config))
# # visualizationList.append(JingliuHanyaBladeHuohuo(config))

# # Jingyuan Teams
# visualizationList.append(JingyuanTingyunHanabiFuxuan(config))
# # visualizationList.append(JingyuanTingyunHanabiLuocha(config))
# # visualizationList.append(JingyuanTingyunAstaLuocha(config))
# # visualizationList.append(JingyuanTingyunHanyaFuxuan(config))
# # visualizationList.append(JingyuanTingyunTopazLuocha(config))

# # Lunae Teams
# visualizationList.append(LunaeHanabiTingyunLuocha(config))
# # visualizationList.append(LunaeHanyaTingyunLuocha(config))
# # visualizationList.append(LunaeHanyaYukongLuocha(config))
# # visualizationList.append(LunaeHanyaPelaLuocha(config))
# # visualizationList.append(LunaeRuanMeiTingyunLuocha(config))
# # visualizationList.append(LunaeTingyunYukongLuocha(config))
# # visualizationList.append(LunaePelaTingyunLuocha(config))
# # visualizationList.append(LunaePelaYukongLuocha(config))

# # Kafka Teams
config['enemySpeed'] = 190 / 1.125
config['numEnemies'] = 3
visualizationList.append(KafkaGuinaifenBlackSwanLuocha(config))
visualizationList.append(SampoGuinaifenBlackSwanLuocha(config))
visualizationList.append(KafkaGuinaifenSampoLuocha(config))
visualizationList.append(KafkaGuinaifenRuanMeiLuocha(config))
visualizationList.append(KafkaSampoRuanMeiLuocha(config))
visualizationList.append(KafkaGuinaifenLukaLuocha(config))
visualizationList.append(KafkaGuinaifenHanyaLuocha(config))
visualizationList.append(RuanMeiGuinaifenBlackSwanLuocha(config))

# visualizationList.append(KafkaGuinaifenRuanMeiLuochaPatience(config))
# visualizationList.append(KafkaGuinaifenBlackSwanLuochaPatience(config))
# visualizationList.append(KafkaRuanMeiBlackSwanLuochaPatience(config))
# visualizationList.append(KafkaHanyaBlackSwanLuochaPatience(config))

# visualizationList.append(KafkaTingyunRuanMeiLuocha(config)) # mediocre, retiring this

# # Qingque Teams
# visualizationList.append(QingqueHanabiPelaFuxuan(config))
# # visualizationList.append(QingqueHanabiSilverWolfLuocha(config))
# # visualizationList.append(QingqueHanyaSilverWolfFuxuan(config))
# # visualizationList.append(QingqueHanyaPelaFuxuan(config))

# # Seele Teams
# visualizationList.append(SeeleMaxSilverWolfHanabiFuxuan(config))
# # visualizationList.append(SeeleMaxSilverWolfTingyunFuxuan(config))
# # visualizationList.append(SeeleMaxSilverWolfRuanMeiFuxuan(config))
# # visualizationList.append(SeeleMaxSilverWolfBronyaLuocha(config))
# # visualizationList.append(SeeleMidSilverWolfBronyaLuocha(config))
# # visualizationList.append(SeeleMidSilverWolfBronyaFuxuan(config))
# # visualizationList.append(SeeleNoneSilverWolfHanabiLuocha(config))

# # Solo Topaz Teams
# visualizationList.append(TopazTingyunHanabiFuxuan(config))
# # visualizationList.append(TopazTingyunHanyaFuxuan(config))

# # Xueyi Teams
# visualizationList.append(XueyiHanabiTingyunFuxuan(config,breakRatio=0.5))
# # visualizationList.append(XueyiHanabiTingyunFuxuan(config,breakRatio=1.0))
# # visualizationList.append(XueyiHanyaPelaFuxuan(config)) # dont like the break assumptions here
# # visualizationList.append(XueyiAstaTopazFuxuan(config)) # needs review, why is the SP so negative? also this team makes no sense

# # YanqingTeam
# visualizationList.append(YanqingTingyunHanabiGepard(config))
# # visualizationList.append(YanqingTingyunRuanMeiGepard(config))

#%% Visualization
# Visualize
visualize(visualizationList, visualizerPath='visualizer\QuadVisual.png', **config)
    
from excelAPI.write2sheet import writeVisualizationList
writeVisualizationList(visualizationList,path='visualizer\QuadVisual.xlsx',sheetname='Quad vs Two')
