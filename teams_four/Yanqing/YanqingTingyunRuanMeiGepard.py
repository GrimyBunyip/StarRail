from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Gepard import Gepard
from characters.hunt.Yanqing import Yanqing
from characters.harmony.Tingyun import Tingyun
from characters.harmony.RuanMei import RuanMei
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.LandausChoice import LandausChoice
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def YanqingTingyunRuanMeiGepard(config):
    #%% Yanqing Tingyun RuanMei Gepard Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                        substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = PenaconyLandOfDreams(),
                        **config)
    
    YanqingCharacter = Yanqing(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.ice'],
                            substats = {'CD': 12, 'CR': 3, 'SPD.flat': 8, 'ATK.percent': 5}),
                            lightcone = Swordplay(**config),
                            relicsetone = HunterOfGlacialForest2pc(),
                            relicsettwo = MusketeerOfWildWheat2pc(),
                            planarset = SpaceSealingStation(),
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                            benedictionTarget=YanqingCharacter,
                            **config)

    GepardCharacter = Gepard(RelicStats(mainstats = ['ER', 'SPD.flat', 'DEF.percent', 'DEF.percent'],
                            substats = {'DEF.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                            lightcone = LandausChoice(**config),
                            relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                            **config)
    
    team = [YanqingCharacter, TingyunCharacter, RuanMeiCharacter, GepardCharacter]

    #%% Yanqing Tingyun RuanMei Gepard Team Buffs
    for character in [TingyunCharacter, YanqingCharacter, RuanMeiCharacter]:
        character.addStat('DMG.icee',description='Penacony from Gepard',amount=0.1)
    for character in [TingyunCharacter, YanqingCharacter, GepardCharacter]:
        character.addStat('DMG.ice',description='Penacony from RuanMei',amount=0.1)

    # RuanMei Buffs, max skill uptime
    RuanMeiCharacter.applyWeaknessModifiers(team=team)
    RuanMeiCharacter.applyPassiveBuffs(team=team)
    RuanMeiCharacter.applySkillBuff(team=team,uptime=3.0/3.0)
    RuanMeiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)
        
    # messenger 4 pc buffs from Tingyun:
    YanqingCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    RuanMeiCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    GepardCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5*3/4)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(YanqingCharacter)
    TingyunCharacter.applyUltBuff(YanqingCharacter,targetSpdMult=RuanMeiCharacter.getTotalStat('SPD')/YanqingCharacter.getTotalStat('SPD'))

    #%% Print Statements
    for character in team:
        character.print()

    #%% Yanqing Tingyun RuanMei Gepard Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long
    numSkill = 2

    YanqingRotation = []
    
    YanqingRotation.append(YanqingCharacter.useSkill() * (numSkill - 1))
    YanqingRotation.append(TingyunCharacter.useBenediction(['skill']) * (numSkill - 1))

    YanqingRotation.append(YanqingCharacter.useTalent() * (numSkill - 1))
    YanqingRotation.append(TingyunCharacter.useBenediction(['talent','followup']) * (numSkill - 1))


    YanqingRotation.append(YanqingCharacter.useBliss())

    YanqingRotation.append(YanqingCharacter.useUltimate())
    YanqingRotation.append(TingyunCharacter.useBenediction(['ultimate']))

    YanqingRotation.append(YanqingCharacter.useSkill())
    YanqingRotation.append(TingyunCharacter.useBenediction(['skill']))

    YanqingRotation.append(YanqingCharacter.useTalent() * 2)
    YanqingRotation.append(TingyunCharacter.useBenediction(['talent','followup']) * 2)

    YanqingRotation.append(YanqingCharacter.endTurn())
    
    TingyunRotation = [ 
        TingyunCharacter.useBasic() * 2, 
        TingyunCharacter.useSkill(),
        TingyunCharacter.useUltimate(),
    ]

    numBasicRuanMei = 2.0
    numSkillRuanMei = 1.0
    RuanMeiRotation = [RuanMeiCharacter.useBasic() * numBasicRuanMei,
                       RuanMeiCharacter.useSkill() * numSkillRuanMei,
                    RuanMeiCharacter.useUltimate()]

    GepardRotation = [GepardCharacter.useBasic() * 3,
                    GepardCharacter.useUltimate() * 1,]

    #%% Yanqing Tingyun RuanMei Gepard Rotation Math

    totalYanqingEffect = sumEffects(YanqingRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalGepardEffect = sumEffects(GepardRotation)

    YanqingRotationDuration = totalYanqingEffect.actionvalue * 100.0 / YanqingCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    GepardRotationDuration = totalGepardEffect.actionvalue * 100.0 / GepardCharacter.getTotalStat('SPD')

    YanqingRotation.append(TingyunCharacter.giveUltEnergy() * YanqingRotationDuration / TingyunRotationDuration)
    
    print('##### Rotation Durations #####')
    print('Yanqing: ',YanqingRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('RuanMei: ',RuanMeiRotationDuration)
    print('Gepard: ',GepardRotationDuration)

    # Scale other character's rotation
    TingyunRotation = [x * YanqingRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    RuanMeiRotation = [x * YanqingRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    GepardRotation = [x * YanqingRotationDuration / GepardRotationDuration for x in GepardRotation]

    YanqingEstimate = DefaultEstimator(f'Yanqing: {numSkill:.1f}E 1Q', YanqingRotation, YanqingCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats',
                                    TingyunRotation, TingyunCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'RuanMei {numSkillRuanMei:.1f}E {numBasicRuanMei:.1f}N S{RuanMeiCharacter.lightcone.superposition:.0f} {RuanMeiCharacter.lightcone.name}, 12 Spd Substats', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    GepardEstimate = DefaultEstimator('Gepard: 3N 1Q, S{:.0f} {}'.format(GepardCharacter.lightcone.superposition, GepardCharacter.lightcone.name),
                                    GepardRotation, GepardCharacter, config)

    return([YanqingEstimate, TingyunEstimate, RuanMeiEstimate, GepardEstimate])

