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
from teams_four.Argenti.ArgentiBronyaPelaHuohuo import ArgentiBronyaPelaHuohuo
from teams_four.Argenti.ArgentiHanabiTingyunHuohuo import ArgentiHanabiTingyunHuohuo
from teams_four.Argenti.ArgentiHanyaRuanMeiHuohuo import ArgentiHanyaRuanMeiHuohuo
from teams_four.Argenti.ArgentiHanyaTingyunFuxuan import ArgentiHanyaTingyunFuxuan
from teams_four.Argenti.ArgentiHanyaTingyunHuohuo import ArgentiHanyaTingyunHuohuo
from teams_four.Argenti.ArgentiJadeTingyunHuohuo import ArgentiJadeTingyunHuohuo
from teams_four.Argenti.ArgentiRuanMeiTingyunHuohuo import ArgentiRuanMeiTingyunHuohuo
from teams_four.Blade.BladeBronyaHanabiLuocha import BladeBronyaHanabiLuocha
from teams_four.Blade.BladeBronyaJadeHanya import BladeBronyaJadeHanya
from teams_four.Blade.BladeBronyaJadeLuocha import BladeBronyaJadeLuocha
from teams_four.Blade.BladeBronyaPelaFuxuan import BladeBronyaPelaFuxuan
from teams_four.Blade.BladeBronyaPelaLuocha import BladeBronyaPelaLuocha
from teams_four.Blade.BladeBronyaPelaLynx import BladeBronyaPelaLynx
from teams_four.Blade.BladeBronyaRuanMeiFuxuan import BladeBronyaRuanMeiFuxuan
from teams_four.Blade.BladeBronyaRuanMeiLuocha import BladeBronyaRuanMeiLuocha
from teams_four.Blade.JadeBronyaRuanMeiLuocha import JadeBronyaRuanMeiLuocha
from teams_four.Boothill.BoothillBronyaRuanMeiGallagher import BoothillBronyaRuanMeiGallagher
from teams_four.Boothill.BoothillTraiblazerRuanMeiGallagher import BoothillTrailblazerRuanMeiGallagher
from teams_four.Clara.ClaraE1TingyunHanabiFuxuan import ClaraE1TingyunHanabiFuxuan
from teams_four.Clara.ClaraE3S1TingyunHanabiFuxuan import ClaraE3S1TingyunHanabiFuxuan
from teams_four.Clara.ClaraS1TingyunHanabiFuxuan import ClaraS1TingyunHanabiFuxuan
from teams_four.Clara.ClaraSilverWolfPelaLuocha import ClaraSilverWolfPelaLuocha
from teams_four.Clara.ClaraTingyunHanabiAventurine import ClaraTingyunHanabiAventurine
from teams_four.Clara.ClaraTingyunHanabiFuxuan import ClaraTingyunHanabiFuxuan
from teams_four.Clara.ClaraTingyunHanabiFuxuanEscapade import ClaraTingyunHanabiFuxuanEscapade
from teams_four.Clara.ClaraTingyunHanabiHuohuo import ClaraTingyunHanabiHuohuo
from teams_four.Clara.ClaraTingyunHanabiLuocha import ClaraTingyunHanabiLuocha
from teams_four.Clara.ClaraTingyunHanyaLuocha import ClaraTingyunHanyaLuocha
from teams_four.Clara.ClaraTingyunPelaLuocha import ClaraTingyunPelaLuocha
from teams_four.Clara.ClaraTingyunRobinHuohuo import ClaraTingyunRobinHuohuo
from teams_four.Clara.ClaraTingyunRuanMeiFuxuan import ClaraTingyunRuanMeiFuxuan
from teams_four.Clara.ClaraTingyunRuanMeiLuocha import ClaraTingyunRuanMeiLuocha
from teams_four.Clara.ClaraTingyunTopazLuocha import ClaraTingyunTopazLuocha
from teams_four.Clara.ClaraTopazAstaLuocha import ClaraTopazAstaLuocha
from teams_four.Clara.ClaraTopazHanyaLuocha import ClaraTopazHanyaLuocha
from teams_four.DotTeams.KafkaJiaoqiuBlackSwanLuocha import KafkaJiaoqiuBlackSwanLuocha
from teams_four.DotTeams.KafkaS1RobinBlackSwanGallagher import KafkaS1RobinBlackSwanGallagher
from teams_four.Firefly.FireflyTraiblazerRuanMeiGallagher import FireflyTrailblazerRuanMeiGallagher
from teams_four.Firefly.FireflyTraiblazerRuanMeiLingsha import FireflyTrailblazerRuanMeiLingsha
from teams_four.Jingliu.JingliuBronyaHanabiLuocha import JingliuBronyaHanabiLuocha
from teams_four.Jingliu.JingliuBronyaMarchLuocha import JingliuBronyaMarchLuocha
from teams_four.Jingliu.JingliuBronyaPelaLuocha import JingliuBronyaPelaLuocha
from teams_four.Jingliu.JingliuBronyaRuanMeiLuocha import JingliuBronyaRuanMeiLuocha
from teams_four.Jingliu.JingliuBronyaTingyunLuocha import JingliuBronyaTingyunLuocha
from teams_four.Jingliu.JingliuHanyaBladeHuohuo import JingliuHanyaBladeHuohuo
from teams_four.Jingliu.JingliuRuanMeiBladeLuocha import JingliuRuanMeiBladeLuocha
from teams_four.Jingyuan.JingyuanHanabiS1TingyunHuohuo import JingYuanHanabiS1TingyunHuohuo
from teams_four.Jingyuan.JingyuanHanabiTingyunHuohuo import JingYuanHanabiTingyunHuohuo
from teams_four.Jingyuan.JingyuanTingyunAstaLuocha import JingyuanTingyunAstaLuocha
from teams_four.Jingyuan.JingyuanTingyunHanabiFuxuan import JingyuanTingyunHanabiFuxuan
from teams_four.Jingyuan.JingyuanTingyunHanabiLuocha import JingyuanTingyunHanabiLuocha
from teams_four.Jingyuan.JingyuanTingyunHanyaFuxuan import JingyuanTingyunHanyaFuxuan
from teams_four.Jingyuan.JingyuanTingyunTopazLuocha import JingyuanTingyunTopazLuocha
from teams_four.DotTeams.KafkaGuinaifenBlackSwanLuocha import KafkaGuinaifenBlackSwanLuocha
from teams_four.DotTeams.KafkaS1RuanMeiBlackSwanLuocha import KafkaS1RuanMeiBlackSwanLuocha
from teams_four.DotTeams.KafkaGuinaifenLukaLuocha import KafkaGuinaifenLukaLuocha
from teams_four.DotTeams.KafkaGuinaifenSampoLuocha import KafkaGuinaifenSampoLuocha
from teams_four.Lunae.LunaeE2HanabiTingyunLuocha import LunaeE2HanabiTingyunLuocha
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
from teams_four.RatioTopaz.RatioTopazRobinAventurine import DrRatioTopazRobinAventurine
from teams_four.Robin.FeixiaoBronyaRobinGallagher import FeixiaoBronyaRobinGallagher
from teams_four.Robin.FeixiaoMarchRobinLingsha import FeixiaoMarchRobinLingsha
from teams_four.Robin.FeixiaoMarchTopazAventurine import FeixiaoMarchTopazAventurine
from teams_four.Robin.MarchTopazRobinGallagher import MarchTopazRobinGallagher
from teams_four.Seele.SilverWolfMarchRobinHuohuo import SilverWolfMarchRobinHuohuo
from teams_four.Robin.FeixiaoMarchRobinAventurine import FeixiaoMarchRobinAventurine
from teams_four.Robin.FeixiaoTopazRobinAventurine import FeixiaoTopazRobinAventurine
from teams_four.Robin.MarchBronyaRobinGallagher import MarchBronyaRobinGallagher
from teams_four.Robin.MarchTopazRobinAventurine import MarchTopazRobinAventurine
from teams_four.Seele.SeeleMaxSilverWolfBronyaLuocha import SeeleMaxSilverWolfBronyaLuocha
from teams_four.Seele.SeeleMaxSilverWolfHanabiFuxuan import SeeleMaxSilverWolfHanabiFuxuan
from teams_four.Seele.SeeleMaxSilverWolfRuanMeiFuxuan import SeeleMaxSilverWolfRuanMeiFuxuan
from teams_four.Seele.SeeleMaxSilverWolfTingyunFuxuan import SeeleMaxSilverWolfTingyunFuxuan
from teams_four.Seele.SeeleMidSilverWolfBronyaFuxuan import SeeleMidSilverWolfBronyaFuxuan
from teams_four.Seele.SeeleMidSilverWolfBronyaLuocha import SeeleMidSilverWolfBronyaLuocha
from teams_four.Seele.SeeleNoneSilverWolfHanabiFuxuan import SeeleNoneSilverWolfHanabiLuocha
from teams_four.Xueyi.XueyiAstaTopazFuxuan import XueyiAstaTopazFuxuan
from teams_four.Xueyi.XueyiHanabiPelaFuxuan import XueyiHanabiPelaFuxuan
from teams_four.Xueyi.XueyiHanabiTingyunFuxuan import XueyiHanabiTingyunFuxuan
from teams_four.Xueyi.XueyiHanyaPelaFuxuan import XueyiHanyaPelaFuxuan
from teams_four.Yanqing.YanqingTingyunHanabiAventurine import YanqingTingyunHanabiAventurine
from teams_four.Yanqing.YanqingTingyunHanabiGepard import YanqingTingyunHanabiGepard
from teams_four.Yanqing.YanqingTingyunRuanMeiGepard import YanqingTingyunRuanMeiGepard
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
# visualizationList.append(FireflyTrailblazerRuanMeiGallagher(config))
# visualizationList.append(KafkaGuinaifenBlackSwanLuocha(config))
# visualizationList.append(AcheronPelaJiaoqiuGallagher(config))
# visualizationList.append(ClaraTingyunHanabiFuxuan(config))
# visualizationList.append(YunliHanabiRobinHuohuo(config))

# # Team Comparisons
# visualizationList.append(ArgentiHanabiTingyunHuohuo(config))
# visualizationList.append(BladeBronyaJadeLuocha(config))
# visualizationList.append(JingliuBronyaRuanMeiLuocha(config))
# visualizationList.append(LunaeHanabiTingyunLuocha(config))
# visualizationList.append(MarchBronyaRobinGallagher(config))
# visualizationList.append(MarchTopazRobinAventurine(config))
# visualizationList.append(DrRatioTopazRobinAventurine(config))
# visualizationList.append(SeeleMaxSilverWolfHanabiFuxuan(config))

# low dps teams
# visualizationList.append(JingYuanHanabiTingyunHuohuo(config))
# visualizationList.append(QingqueHanabiPelaFuxuan(config))
# visualizationList.append(XueyiHanabiTingyunFuxuan(config,breakRatio=0.5))
# visualizationList.append(YanqingTingyunHanabiAventurine(config))

# # Acheron Teams

# # E2 Teams
# visualizationList.append(AcheronE2BronyaJiaoqiuGallagher(config, acheronSuperposition=1, jiaoqiuEidolon=2))
# visualizationList.append(AcheronE2HanabiJiaoqiuGallagher(config, acheronSuperposition=1, jiaoqiuEidolon=2))

# visualizationList.append(AcheronE2BronyaJiaoqiuGallagher(config, acheronSuperposition=1, jiaoqiuEidolon=1))
# visualizationList.append(AcheronE2HanabiJiaoqiuGallagher(config, acheronSuperposition=1, jiaoqiuEidolon=1))

# visualizationList.append(AcheronE2BronyaJiaoqiuGallagher(config, acheronSuperposition=1))
# visualizationList.append(AcheronE2HanabiJiaoqiuGallagher(config, acheronSuperposition=1))
# visualizationList.append(AcheronE2HanabiJiaoqiuGallagher(config, acheronSuperposition=0))

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
# visualizationList.append(ArgentiJadeTingyunHuohuo(config))
# # visualizationList.append(ArgentiHanyaTingyunHuohuo(config))
# # visualizationList.append(ArgentiHanyaTingyunFuxuan(config))
# # visualizationList.append(ArgentiRuanMeiTingyunHuohuo(config))
# # visualizationList.append(ArgentiHanyaRuanMeiHuohuo(config))
# # visualizationList.append(ArgentiBronyaPelaHuohuo(config)) #calculation is suspicious to me

# # Blade Teams
# visualizationList.append(BladeBronyaJadeLuocha(config))
# visualizationList.append(BladeBronyaHanabiLuocha(config))
# visualizationList.append(BladeBronyaRuanMeiLuocha(config))
# visualizationList.append(BladeBronyaPelaLuocha(config))
# # visualizationList.append(JadeBronyaRuanMeiLuocha(config))
# # visualizationList.append(BladeBronyaPelaLynx(config))

# visualizationList.append(BladeBronyaJadeHanya(config))
# # visualizationList.append(BladeBronyaPelaFuxuan(config)) # 100% vow uptime with fu xuan
# # visualizationList.append(BladeBronyaRuanMeiFuxuan(config)) # 100% vow uptime with fu xuan, unbalanced SP usage

# # Boothill Teams
# visualizationList.append(BoothillTrailblazerRuanMeiGallagher(config))
# visualizationList.append(BoothillBronyaRuanMeiGallagher(config))

# Clara Teams
# visualizationList.append(ClaraS1TingyunHanabiFuxuan(config))
# visualizationList.append(ClaraE1TingyunHanabiFuxuan(config))
# visualizationList.append(ClaraE3S1TingyunHanabiFuxuan(config))

# visualizationList.append(ClaraTingyunHanabiFuxuan(config))
# visualizationList.append(ClaraTingyunRobinHuohuo(config))
# visualizationList.append(ClaraTingyunHanabiHuohuo(config))
# visualizationList.append(ClaraTingyunHanabiAventurine(config))
# visualizationList.append(ClaraTingyunHanabiLuocha(config))
# # visualizationList.append(ClaraTingyunRuanMeiFuxuan(config))
# # visualizationList.append(ClaraTingyunRuanMeiLuocha(config))
# # visualizationList.append(ClaraTingyunHanyaLuocha(config))
# visualizationList.append(ClaraTopazAstaLuocha(config))
# visualizationList.append(ClaraTopazHanyaLuocha(config))
# # # visualizationList.append(ClaraTingyunPelaLuocha(config))
# visualizationList.append(ClaraTingyunTopazLuocha(config))
# # # visualizationList.append(ClaraSilverWolfPelaLuocha(config))
# # # visualizationList.append(ClaraTingyunHanabiFuxuanEscapade(config))

# # Firefly Teams
# visualizationList.append(FireflyTrailblazerRuanMeiGallagher(config))
# visualizationList.append(FireflyTrailblazerRuanMeiGallagher(config, fireflyEidolon=2))
# visualizationList.append(FireflyTrailblazerRuanMeiGallagher(config, fireflyEidolon=2, fireflySuperposition=1))
# visualizationList.append(FireflyTrailblazerRuanMeiLingsha(config))
# visualizationList.append(FireflyTrailblazerRuanMeiLingsha(config, fireflyEidolon=2))
# visualizationList.append(FireflyTrailblazerRuanMeiLingsha(config, fireflyEidolon=2,lingshaSuperposition=1))
# visualizationList.append(FireflyTrailblazerRuanMeiLingsha(config, fireflyEidolon=2,lingshaEidolon=1))
# visualizationList.append(FireflyTrailblazerRuanMeiLingsha(config, fireflyEidolon=2,lingshaEidolon=2))
# visualizationList.append(FireflyTrailblazerRuanMeiLingsha(config, fireflyEidolon=2,lingshaEidolon=2,lingshaSuperposition=1))
# visualizationList.append(FireflyTrailblazerRuanMeiLingsha(config, fireflyEidolon=2, fireflySuperposition=1))

# # Jingliu Teams
# visualizationList.append(JingliuBronyaRuanMeiLuocha(config))
# # visualizationList.append(JingliuBronyaHanabiLuocha(config))
# visualizationList.append(JingliuBronyaTingyunLuocha(config))
# visualizationList.append(JingliuBronyaMarchLuocha(config))
# visualizationList.append(JingliuBronyaPelaLuocha(config))
# # visualizationList.append(JingliuRuanMeiBladeLuocha(config))
# # visualizationList.append(JingliuHanyaBladeHuohuo(config))

# # Jingyuan Teams
# visualizationList.append(JingYuanHanabiTingyunHuohuo(config))
# # visualizationList.append(JingyuanTingyunHanabiFuxuan(config))
# # visualizationList.append(JingyuanTingyunHanabiLuocha(config))
# # visualizationList.append(JingyuanTingyunAstaLuocha(config))
# # visualizationList.append(JingyuanTingyunHanyaFuxuan(config))
# # visualizationList.append(JingyuanTingyunTopazLuocha(config))
# visualizationList.append(JingYuanHanabiS1TingyunHuohuo(config))

# # Lunae Teams
# visualizationList.append(LunaeHanabiTingyunLuocha(config))
# visualizationList.append(LunaeHanyaTingyunLuocha(config))
# visualizationList.append(LunaeHanyaYukongLuocha(config))
# # visualizationList.append(LunaeHanyaPelaLuocha(config))
# # visualizationList.append(LunaeRuanMeiTingyunLuocha(config))
# # visualizationList.append(LunaeTingyunYukongLuocha(config))
# visualizationList.append(LunaePelaTingyunLuocha(config))
# # visualizationList.append(LunaePelaYukongLuocha(config))
# # # visualizationList.append(LunaeE2HanabiTingyunLuocha(config))

# # Kafka Teams
# # config['enemySpeed'] = 190 / 1.125
# # config['numEnemies'] = 2
# # E0 S0 Teams
# visualizationList.append(KafkaGuinaifenBlackSwanLuocha(config))
# visualizationList.append(KafkaJiaoqiuBlackSwanLuocha(config))
# # visualizationList.append(KafkaGuinaifenSampoLuocha(config))
# # visualizationList.append(KafkaGuinaifenLukaLuocha(config))

# # S1 Teams
# visualizationList.append(KafkaGuinaifenBlackSwanLuocha(config, kafkaSuperposition=True))
# visualizationList.append(KafkaS1RuanMeiBlackSwanLuocha(config))
# visualizationList.append(KafkaJiaoqiuBlackSwanLuocha(config,kafkaSuperposition=True))
# visualizationList.append(KafkaS1RobinBlackSwanGallagher(config))

# # E2 Jiaoqiu Teams
# visualizationList.append(KafkaJiaoqiuBlackSwanLuocha(config,kafkaSuperposition=True,jiaoqiuEidolon=2))
# visualizationList.append(KafkaJiaoqiuBlackSwanLuocha(config,jiaoqiuEidolon=2))

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

# # Robin Teams

# to do:
# e2 robin teams
# feixiao march bronya
# er rope march

# visualizationList.append(MarchTopazRobinAventurine(config))
# visualizationList.append(MarchTopazRobinGallagher(config, robinEidolon=2))
visualizationList.append(FeixiaoMarchRobinAventurine(config))
# visualizationList.append(FeixiaoMarchRobinAventurine(config, feixiaoEidolon=2))
# visualizationList.append(FeixiaoMarchRobinLingsha(config, robinEidolon=2))

# # aventurine variants
# visualizationList.append(FeixiaoTopazRobinAventurine(config))
# visualizationList.append(FeixiaoMarchRobinAventurine(config))
# visualizationList.append(FeixiaoMarchRobinLingsha(config))

# the old guard
# visualizationList.append(MarchBronyaRobinGallagher(config))
# visualizationList.append(DrRatioTopazRobinAventurine(config))
# visualizationList.append(MarchTopazRobinAventurine(config))

# Retire these teams for various reasons
# visualizationList.append(FeixiaoMarchTopazAventurine(config))
# visualizationList.append(FeixiaoBronyaRobinGallagher(config))

# # Xueyi Teams
# # visualizationList.append(XueyiHanabiTingyunFuxuan(config,breakRatio=1.0))
# visualizationList.append(XueyiHanabiTingyunFuxuan(config,breakRatio=0.5))
# # visualizationList.append(XueyiHanabiPelaFuxuan(config,breakRatio=0.5))
# # visualizationList.append(XueyiHanyaPelaFuxuan(config,breakRatio=0.5)) # dont like the break assumptions here
# # visualizationList.append(XueyiAstaTopazFuxuan(config)) # needs review, why is the SP so negative? also this team makes no sense

# # Yanqing Team
# visualizationList.append(YanqingTingyunHanabiAventurine(config))
# # visualizationList.append(YanqingTingyunHanabiGepard(config))
# # visualizationList.append(YanqingTingyunRuanMeiGepard(config))

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

#%% Visualization
# Visualize
visualize(visualizationList, visualizerPath='visualizer\QuadVisual.png', **config)
    
from excelAPI.write2sheet import writeVisualizationList
writeVisualizationList(visualizationList,path='visualizer\QuadVisual.xlsx',sheetname='Quad vs Two')
