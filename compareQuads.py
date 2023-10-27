from copy import copy
from settings.BaseConfiguration import Configuration
from teams_four.BladeBronyaPelaFuxuan import BladeBronyaPelaFuxuan
from teams_four.BladeBronyaPelaLuocha import BladeBronyaPelaLuocha
from teams_four.BladeBronyaPelaLynx import BladeBronyaPelaLynx
from teams_four.ClaraSilverWolfPelaLuocha import ClaraSilverWolfPelaLuocha
from teams_four.ClaraTingyunPelaLuocha import ClaraTingyunPelaLuocha
from teams_four.ClaraTopazAstaLuocha import ClaraTopazAstaLuocha
from teams_four.ClaraTopazHanyaLuocha import ClaraTopazHanyaLuocha
from teams_four.JingliuBronyaPelaLuocha import JingliuBronyaPelaLuocha
from teams_four.JingliuHanyaBladeHuohuo import JingliuHanyaBladeHuohuo
from teams_four.JingyuanTingyunAstaLuocha import JingyuanTingyunAstaLuocha
from teams_four.JingyuanTingyunTopazLuocha import JingyuanTingyunTopazLuocha
from teams_four.KafkaGuinaifenAstaLuocha import KafkaGuinaifenAstaLuocha
from teams_four.KafkaGuinaifenHanyaLuocha import KafkaGuinaifenHanyaLuocha
from teams_four.KafkaGuinaifenLukaLuocha import KafkaGuinaifenLukaLuocha
from teams_four.KafkaGuinaifenSampoLuocha import KafkaGuinaifenSampoLuocha
from teams_four.LunaeHanyaPelaLuocha import LunaeHanyaPelaLuocha
from teams_four.LunaeHanyaTingyunLuocha import LunaeHanyaTingyunLuocha
from teams_four.LunaeHanyaYukongLuocha import LunaeHanyaYukongLuocha
from teams_four.LunaePelaYukongLuocha import LunaePelaYukongLuocha
from teams_four.LunaeTingyunYukongLuocha import LunaeTingyunYukongLuocha
from teams_four.SeeleMaxSilverWolfBronyaLuocha import SeeleMaxSilverWolfBronyaLuocha
from teams_four.SeeleMidSilverWolfBronyaLuocha import SeeleMidSilverWolfBronyaLuocha
from teams_four.TopazTingyunHanyaLuocha import TopazTingyunHanyaLuocha
from visualizer.visualizer import visualize

visualizationList = []

config = copy(Configuration)
config['numEnemies'] = 2
config['enemySpeed'] = 132 / 1.125 # assume 25% action delay every 2 enemy turns from toughness break

#%% Team Imports
visualizationList.append(BladeBronyaPelaFuxuan(config))
#visualizationList.append(BladeBronyaPelaLuocha(config))
#visualizationList.append(BladeBronyaPelaLynx(config))
#visualizationList.append(ClaraSilverWolfPelaLuocha(config))
#visualizationList.append(ClaraTingyunPelaLuocha(config))
visualizationList.append(ClaraTopazAstaLuocha(config))
#visualizationList.append(ClaraTopazHanyaLuocha(config))
visualizationList.append(JingliuBronyaPelaLuocha(config))
visualizationList.append(JingliuHanyaBladeHuohuo(config))
visualizationList.append(JingyuanTingyunAstaLuocha(config))
#visualizationList.append(JingyuanTingyunTopazLuocha(config))
#visualizationList.append(KafkaGuinaifenAstaLuocha(config))
#visualizationList.append(KafkaGuinaifenHanyaLuocha(config))
#visualizationList.append(KafkaGuinaifenLukaLuocha(config))
visualizationList.append(KafkaGuinaifenSampoLuocha(config))
#visualizationList.append(LunaeHanyaPelaLuocha(config))
visualizationList.append(LunaeHanyaTingyunLuocha(config))
#visualizationList.append(LunaeHanyaYukongLuocha(config))
#visualizationList.append(LunaePelaYukongLuocha(config))
#visualizationList.append(LunaeTingyunYukongLuocha(config))
visualizationList.append(SeeleMaxSilverWolfBronyaLuocha(config))
visualizationList.append(SeeleMidSilverWolfBronyaLuocha(config))
#visualizationList.append(TopazTingyunHanyaLuocha(config))

#%% Visualization
# Visualize
visualize(visualizationList, visualizerPath='visualizer\QuadVisual.png', **config)
    
from excelAPI.write2sheet import writeVisualizationList
writeVisualizationList(visualizationList,path='visualizer\QuadVisual.xlsx',sheetname='Quad vs Two')
