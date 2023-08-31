from characters.Blade import BladeV1
from characters.DanHeng import DanHengV1
from characters.Yanqing import YanqingV1
from settings.BaseConfiguration import Configuration
from visualizer.visualizer import visualize

if __name__ == '__main__':
    CharacterDict = {} # store character information here
    EffectDict = {} # store dps metrics here
    
    DanHengV1(Configuration, CharacterDict, EffectDict)
    YanqingV1(Configuration, CharacterDict, EffectDict)
    BladeV1(Configuration, CharacterDict, EffectDict)

    visualize(CharacterDict, EffectDict, Configuration)