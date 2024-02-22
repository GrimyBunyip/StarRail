from copy import copy
from settings.BaseConfiguration import Configuration
from teams_four.Acheron.AcheronE2AstaPelaFuxuan import AcheronE2AstaPelaFuxuan
from teams_four.Acheron.AcheronE2S1BronyaPelaFuxuan import AcheronE2S1BronyaPelaLuocha
from teams_four.Acheron.AcheronE2HanabiPelaFuxuan import AcheronE2HanabiPelaFuxuan
from teams_four.Acheron.AcheronE2RuanMeiPelaFuxuan import AcheronE2RuanMeiPelaFuxuan
from teams_four.Acheron.AcheronE2S1HanabiPelaFuxuan import AcheronE2S1HanabiPelaFuxuan
from teams_four.Acheron.AcheronKafkaBlackSwanLuocha import AcheronKafkaBlackSwanLuocha
from teams_four.Acheron.AcheronKafkaPelaLuocha import AcheronKafkaPelaLuocha
from teams_four.Acheron.AcheronS1SilverWolfPelaFuxuan import AcheronS1SilverWolfPelaFuxuan
from teams_four.Acheron.AcheronSilverWolfPelaFuxuan import AcheronSilverWolfPelaFuxuan
from teams_four.Acheron.AcheronSilverWolfPelaLuocha import AcheronSilverWolfPelaLuocha
from teams_four.Acheron.AcheronWeltPelaFuxuan import AcheronWeltPelaFuxuan
from teams_four.Argenti.ArgentiBronyaPelaHuohuo import ArgentiBronyaPelaHuohuo
from teams_four.Argenti.ArgentiHanabiTingyunHuohuo import ArgentiHanabiTingyunHuohuo
from teams_four.Argenti.ArgentiHanyaRuanMeiHuohuo import ArgentiHanyaRuanMeiHuohuo
from teams_four.Argenti.ArgentiHanyaTingyunFuxuan import ArgentiHanyaTingyunFuxuan
from teams_four.Argenti.ArgentiHanyaTingyunHuohuo import ArgentiHanyaTingyunHuohuo
from teams_four.Argenti.ArgentiRuanMeiTingyunHuohuo import ArgentiRuanMeiTingyunHuohuo
from teams_four.Blade.BladeBronyaHanabiLuocha import BladeBronyaHanabiLuocha
from teams_four.Blade.BladeBronyaPelaFuxuan import BladeBronyaPelaFuxuan
from teams_four.Blade.BladeBronyaPelaLuocha import BladeBronyaPelaLuocha
from teams_four.Blade.BladeBronyaPelaLynx import BladeBronyaPelaLynx
from teams_four.Blade.BladeBronyaRuanMeiFuxuan import BladeBronyaRuanMeiFuxuan
from teams_four.Blade.BladeBronyaRuanMeiLuocha import BladeBronyaRuanMeiLuocha
from teams_four.Clara.ClaraSilverWolfPelaLuocha import ClaraSilverWolfPelaLuocha
from teams_four.Clara.ClaraTingyunHanabiAventurine import ClaraTingyunHanabiAventurine
from teams_four.Clara.ClaraTingyunHanabiFuxuan import ClaraTingyunHanabiFuxuan
from teams_four.Clara.ClaraTingyunHanabiFuxuanEscapade import ClaraTingyunHanabiFuxuanEscapade
from teams_four.Clara.ClaraTingyunHanabiLuocha import ClaraTingyunHanabiLuocha
from teams_four.Clara.ClaraTingyunHanyaLuocha import ClaraTingyunHanyaLuocha
from teams_four.Clara.ClaraTingyunPelaLuocha import ClaraTingyunPelaLuocha
from teams_four.Clara.ClaraTingyunTopazLuocha import ClaraTingyunTopazLuocha
from teams_four.Clara.ClaraTopazAstaLuocha import ClaraTopazAstaLuocha
from teams_four.Clara.ClaraTopazHanyaLuocha import ClaraTopazHanyaLuocha
from teams_four.Jingliu.JingliuBronyaHanabiLuocha import JingliuBronyaHanabiLuocha
from teams_four.Jingliu.JingliuBronyaPelaLuocha import JingliuBronyaPelaLuocha
from teams_four.Jingliu.JingliuBronyaRuanMeiLuocha import JingliuBronyaRuanMeiLuocha
from teams_four.Jingliu.JingliuBronyaTingyunLuocha import JingliuBronyaTingyunLuocha
from teams_four.Jingliu.JingliuHanyaBladeHuohuo import JingliuHanyaBladeHuohuo
from teams_four.Jingliu.JingliuRuanMeiBladeLuocha import JingliuRuanMeiBladeLuocha
from teams_four.Jingyuan.JingyuanTingyunAstaLuocha import JingyuanTingyunAstaLuocha
from teams_four.Jingyuan.JingyuanTingyunHanabiFuxuan import JingyuanTingyunHanabiFuxuan
from teams_four.Jingyuan.JingyuanTingyunHanabiLuocha import JingyuanTingyunHanabiLuocha
from teams_four.Jingyuan.JingyuanTingyunHanyaFuxuan import JingyuanTingyunHanyaFuxuan
from teams_four.Jingyuan.JingyuanTingyunTopazLuocha import JingyuanTingyunTopazLuocha
from teams_four.DotTeams.KafkaGuinaifenAstaLuocha import KafkaGuinaifenAstaLuocha
from teams_four.DotTeams.KafkaGuinaifenBlackSwanLuocha import KafkaGuinaifenBlackSwanLuocha
from teams_four.DotTeams.KafkaGuinaifenBlackSwanLuochaPatience import KafkaGuinaifenBlackSwanLuochaPatience
from teams_four.DotTeams.KafkaGuinaifenRuanMeiLuochaPatience import KafkaGuinaifenRuanMeiLuochaPatience
from teams_four.DotTeams.KafkaHanyaBlackSwanLuochaPatience import KafkaHanyaBlackSwanLuochaPatience
from teams_four.DotTeams.KafkaPelaBlackSwanLuochaPatience import KafkaPelaBlackSwanLuochaPatience
from teams_four.DotTeams.KafkaRuanMeiBlackSwanLuochaPatience import KafkaRuanMeiBlackSwanLuochaPatience
from teams_four.DotTeams.KafkaGuinaifenHanyaLuocha import KafkaGuinaifenHanyaLuocha
from teams_four.DotTeams.KafkaGuinaifenLukaLuocha import KafkaGuinaifenLukaLuocha
from teams_four.DotTeams.KafkaGuinaifenRuanMeiLuocha import KafkaGuinaifenRuanMeiLuocha
from teams_four.DotTeams.KafkaGuinaifenSampoLuocha import KafkaGuinaifenSampoLuocha
from teams_four.DotTeams.KafkaSampoRuanMeiLuocha import KafkaSampoRuanMeiLuocha
from teams_four.Lunae.LunaeHanabiTingyunLuocha import LunaeHanabiTingyunLuocha
from teams_four.Lunae.LunaeHanyaPelaLuocha import LunaeHanyaPelaLuocha
from teams_four.Lunae.LunaeHanyaTingyunLuocha import LunaeHanyaTingyunLuocha
from teams_four.Lunae.LunaeHanyaYukongLuocha import LunaeHanyaYukongLuocha
from teams_four.Lunae.LunaePelaTingyunLuocha import LunaePelaTingyunLuocha
from teams_four.Lunae.LunaePelaYukongLuocha import LunaePelaYukongLuocha
from teams_four.Lunae.LunaeRuanMeiTingyunLuocha import LunaeRuanMeiTingyunLuocha
from teams_four.Lunae.LunaeTingyunYukongLuocha import LunaeTingyunYukongLuocha
from teams_four.Qingque.QingqueHanabiPelaFuxuan import QingqueHanabiPelaFuxuan
from teams_four.Qingque.QingqueHanabiSilverWolfLuocha import QingqueHanabiSilverWolfLuocha
from teams_four.Qingque.QingqueHanyaPelaFuxuan import QingqueHanyaPelaFuxuan
from teams_four.Qingque.QingqueHanyaSilverWolfFuxuan import QingqueHanyaSilverWolfFuxuan
from teams_four.RatioTopaz.RatioBronyaSilverWolfLuocha import DrRatioBronyaSilverWolfLuocha
from teams_four.RatioTopaz.RatioHanabiSilverWolfLuocha import DrRatioHanabiSilverWolfLuocha
from teams_four.RatioTopaz.RatioHanyaSilverWolfFuxuan import DrRatioHanyaSilverWolfFuxuan
from teams_four.RatioTopaz.RatioRuanMeiSilverWolfLuocha import DrRatioRuanMeiSilverWolfLuocha
from teams_four.RatioTopaz.RatioTingyunSilverWolfLuocha import DrRatioTingyunSilverWolfLuocha
from teams_four.RatioTopaz.RatioTopazAstaLuocha import DrRatioTopazAstaLuocha
from teams_four.RatioTopaz.RatioHanyaSilverWolfLuocha import DrRatioHanyaSilverWolfLuocha
from teams_four.RatioTopaz.RatioTopazHanyaLuocha import DrRatioTopazHanyaLuocha
from teams_four.RatioTopaz.RatioTopazRuanMeiLuocha import DrRatioTopazRuanMeiLuocha
from teams_four.RatioTopaz.RatioTopazSilverWolfLuocha import DrRatioTopazSilverWolfLuocha
from teams_four.DotTeams.RuanMeiGuinaifenBlackSwanLuocha import RuanMeiGuinaifenBlackSwanLuocha
from teams_four.DotTeams.SampoGuinaifenBlackSwanLuocha import SampoGuinaifenBlackSwanLuocha
from teams_four.Seele.SeeleMaxSilverWolfBronyaLuocha import SeeleMaxSilverWolfBronyaLuocha
from teams_four.Seele.SeeleMaxSilverWolfHanabiFuxuan import SeeleMaxSilverWolfHanabiFuxuan
from teams_four.Seele.SeeleMaxSilverWolfRuanMeiFuxuan import SeeleMaxSilverWolfRuanMeiFuxuan
from teams_four.Seele.SeeleMaxSilverWolfTingyunFuxuan import SeeleMaxSilverWolfTingyunFuxuan
from teams_four.Seele.SeeleMidSilverWolfBronyaFuxuan import SeeleMidSilverWolfBronyaFuxuan
from teams_four.Seele.SeeleMidSilverWolfBronyaLuocha import SeeleMidSilverWolfBronyaLuocha
from teams_four.Seele.SeeleNoneSilverWolfHanabiFuxuan import SeeleNoneSilverWolfHanabiLuocha
from teams_four.RatioTopaz.TopazTingyunHanabiFuxuan import TopazTingyunHanabiFuxuan
from teams_four.RatioTopaz.TopazTingyunHanyaFuxuan import TopazTingyunHanyaFuxuan
from teams_four.Xueyi.XueyiAstaTopazFuxuan import XueyiAstaTopazFuxuan
from teams_four.Xueyi.XueyiHanabiPelaFuxuan import XueyiHanabiPelaFuxuan
from teams_four.Xueyi.XueyiHanabiTingyunFuxuan import XueyiHanabiTingyunFuxuan
from teams_four.Xueyi.XueyiHanyaPelaFuxuan import XueyiHanyaPelaFuxuan
from teams_four.Yanqing.YanqingTingyunHanabiGepard import YanqingTingyunHanabiGepard
from teams_four.Yanqing.YanqingTingyunRuanMeiGepard import YanqingTingyunRuanMeiGepard
from visualizer.visualizer import visualize

visualizationList = []

config = copy(Configuration)
config['numEnemies'] = 3
config['enemySpeed'] = 190 / 1.125 # assume 25% action delay every 2 enemy turns from toughness break

#%% Team Imports

# # Acheron Teams
visualizationList.append(AcheronE2S1HanabiPelaFuxuan(config))
visualizationList.append(AcheronE2S1BronyaPelaLuocha(config))
visualizationList.append(AcheronE2AstaPelaFuxuan(config))
visualizationList.append(AcheronE2RuanMeiPelaFuxuan(config))
visualizationList.append(AcheronE2HanabiPelaFuxuan(config))
visualizationList.append(AcheronS1SilverWolfPelaFuxuan(config))
visualizationList.append(AcheronSilverWolfPelaFuxuan(config))
visualizationList.append(AcheronWeltPelaFuxuan(config))
visualizationList.append(AcheronKafkaBlackSwanLuocha(config))
visualizationList.append(AcheronKafkaPelaLuocha(config))
# # visualizationList.append(AcheronSilverWolfPelaLuocha(config)) # retired, just use fuxuan

# # Argenti Teams
# visualizationList.append(ArgentiHanabiTingyunHuohuo(config))
# # visualizationList.append(ArgentiHanyaTingyunHuohuo(config))
# # visualizationList.append(ArgentiHanyaTingyunFuxuan(config))
# # visualizationList.append(ArgentiRuanMeiTingyunHuohuo(config))
# # visualizationList.append(ArgentiHanyaRuanMeiHuohuo(config))
# # visualizationList.append(ArgentiBronyaPelaHuohuo(config)) #calculation is suspicious to me

# # Blade Teams
# visualizationList.append(BladeBronyaHanabiLuocha(config))
# # visualizationList.append(BladeBronyaRuanMeiLuocha(config))
# # visualizationList.append(BladeBronyaPelaLynx(config))
# # visualizationList.append(BladeBronyaPelaLuocha(config))

# # visualizationList.append(BladeBronyaPelaFuxuan(config)) # 100% vow uptime with fu xuan
# # visualizationList.append(BladeBronyaRuanMeiFuxuan(config)) # 100% vow uptime with fu xuan, unbalanced SP usage

# # Clara Teams
# visualizationList.append(ClaraTingyunHanabiFuxuan(config))
# # visualizationList.append(ClaraTingyunHanabiAventurine(config))
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

# Jingliu Teams
visualizationList.append(JingliuBronyaRuanMeiLuocha(config))
# visualizationList.append(JingliuBronyaHanabiLuocha(config))
# visualizationList.append(JingliuBronyaTingyunLuocha(config))
# visualizationList.append(JingliuBronyaPelaLuocha(config))
# visualizationList.append(JingliuRuanMeiBladeLuocha(config))
# visualizationList.append(JingliuHanyaBladeHuohuo(config))

# Jingyuan Teams
visualizationList.append(JingyuanTingyunHanabiFuxuan(config))
# visualizationList.append(JingyuanTingyunHanabiLuocha(config))
# visualizationList.append(JingyuanTingyunAstaLuocha(config))
# visualizationList.append(JingyuanTingyunHanyaFuxuan(config))
# visualizationList.append(JingyuanTingyunTopazLuocha(config))

# Lunae Teams
visualizationList.append(LunaeHanabiTingyunLuocha(config))
# visualizationList.append(LunaeHanyaTingyunLuocha(config))
# visualizationList.append(LunaeHanyaYukongLuocha(config))
# visualizationList.append(LunaeHanyaPelaLuocha(config))
# visualizationList.append(LunaeRuanMeiTingyunLuocha(config))
# visualizationList.append(LunaeTingyunYukongLuocha(config))
# visualizationList.append(LunaePelaTingyunLuocha(config))
# visualizationList.append(LunaePelaYukongLuocha(config))

# Kafka Teams
# config['enemySpeed'] = 190 / 1.125
# config['numEnemies'] = 3
visualizationList.append(KafkaGuinaifenBlackSwanLuocha(config))
# visualizationList.append(SampoGuinaifenBlackSwanLuocha(config))
# visualizationList.append(KafkaGuinaifenSampoLuocha(config))
# visualizationList.append(KafkaGuinaifenRuanMeiLuocha(config))
# visualizationList.append(KafkaSampoRuanMeiLuocha(config))
# visualizationList.append(KafkaGuinaifenLukaLuocha(config))
# visualizationList.append(KafkaGuinaifenHanyaLuocha(config))
# visualizationList.append(RuanMeiGuinaifenBlackSwanLuocha(config))

# # visualizationList.append(KafkaGuinaifenRuanMeiLuochaPatience(config))
# # visualizationList.append(KafkaGuinaifenBlackSwanLuochaPatience(config))
# # visualizationList.append(KafkaPelaBlackSwanLuochaPatience(config))
# # visualizationList.append(KafkaRuanMeiBlackSwanLuochaPatience(config))
# # visualizationList.append(KafkaHanyaBlackSwanLuochaPatience(config))

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
# visualizationList.append(XueyiHanabiTingyunFuxuan(config,breakRatio=1.0))
# # visualizationList.append(XueyiHanabiTingyunFuxuan(config,breakRatio=0.5))
# # visualizationList.append(XueyiHanabiPelaFuxuan(config,breakRatio=0.5))
# # visualizationList.append(XueyiHanyaPelaFuxuan(config,breakRatio=0.5)) # dont like the break assumptions here
# # visualizationList.append(XueyiAstaTopazFuxuan(config)) # needs review, why is the SP so negative? also this team makes no sense

# # YanqingTeam
# visualizationList.append(YanqingTingyunHanabiGepard(config))
# # visualizationList.append(YanqingTingyunRuanMeiGepard(config))

#%% Visualization
# Visualize
visualize(visualizationList, visualizerPath='visualizer\QuadVisual.png', **config)
    
from excelAPI.write2sheet import writeVisualizationList
writeVisualizationList(visualizationList,path='visualizer\QuadVisual.xlsx',sheetname='Quad vs Two')
