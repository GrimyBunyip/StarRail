from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Gepard import Gepard
from characters.hunt.Yanqing import Yanqing
from characters.harmony.Tingyun import Tingyun
from characters.harmony.Hanabi import Hanabi
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from lightCones.preservation.LandausChoice import LandausChoice
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def YanqingTingyunHanabiGepard(config):
    #%% Yanqing Tingyun Hanabi Gepard Characters
    YanqingCharacter = Yanqing(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CD', 'DMG.ice'],
                            substats = {'CD': 12, 'CR': 5, 'ATK.percent': 8, 'ATK.flat': 3}),
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
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'SPD.flat', 'ER'],
                            substats = {'CD': 8, 'SPD.flat': 12, 'RES': 5, 'DEF.percent': 3}),
                            lightcone = PastAndFuture(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                            **config)

    GepardCharacter = Gepard(RelicStats(mainstats = ['ER', 'SPD.flat', 'DEF.percent', 'DEF.percent'],
                            substats = {'DEF.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                            lightcone = LandausChoice(**config),
                            relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                            **config)
    
    team = [YanqingCharacter, TingyunCharacter, HanabiCharacter, GepardCharacter]

    #%% Yanqing Tingyun Hanabi Gepard Team Buffs
    for character in [TingyunCharacter, YanqingCharacter, HanabiCharacter]:
        character.addStat('DMG.icee',description='Penacony from Gepard',amount=0.1)
    for character in [TingyunCharacter, YanqingCharacter, GepardCharacter]:
        character.addStat('CD',description='Broken Keel from Hanabi',amount=0.1)

    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=YanqingCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)
    
    # Past and Future
    YanqingCharacter.addStat('DMG',description='Past and Future',amount=0.32)
        
    # Hanabi Messenger 4 pc
    for character in [YanqingCharacter, TingyunCharacter, GepardCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Messenger Buff
    for character in [YanqingCharacter, HanabiCharacter, GepardCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(YanqingCharacter)
    TingyunCharacter.applyUltBuff(YanqingCharacter,targetSpdMult=HanabiCharacter.getTotalStat('SPD')/YanqingCharacter.getTotalStat('SPD'))

    #%% Print Statements
    for character in team:
        character.print()

    #%% Yanqing Tingyun Hanabi Gepard Rotations
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

    YanqingRotation.append(HanabiCharacter.useAdvanceForward(advanceAmount=1.0 - YanqingCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')) * numSkill)
    
    TingyunRotation = [ 
        TingyunCharacter.useBasic() * 2, 
        TingyunCharacter.useSkill(),
        TingyunCharacter.useUltimate(),
    ]
    
    numBasicHanabi = 0.0
    numSkillHanabi = 3.0
    HanabiRotation = [HanabiCharacter.useBasic() * numBasicHanabi,
                       HanabiCharacter.useSkill() * numSkillHanabi,
                    HanabiCharacter.useUltimate()]

    GepardRotation = [GepardCharacter.useBasic() * 3,
                    GepardCharacter.useUltimate() * 1,]

    #%% Yanqing Tingyun Hanabi Gepard Rotation Math

    totalYanqingEffect = sumEffects(YanqingRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalGepardEffect = sumEffects(GepardRotation)

    YanqingRotationDuration = totalYanqingEffect.actionvalue * 100.0 / YanqingCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    GepardRotationDuration = totalGepardEffect.actionvalue * 100.0 / GepardCharacter.getTotalStat('SPD')

    YanqingRotation.append(TingyunCharacter.giveUltEnergy() * YanqingRotationDuration / TingyunRotationDuration)
    
    print('##### Rotation Durations #####')
    print('Yanqing: ',YanqingRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Hanabi: ',HanabiRotationDuration)
    print('Gepard: ',GepardRotationDuration)

    # Scale other character's rotation
    TingyunRotation = [x * YanqingRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HanabiRotation = [x * YanqingRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    GepardRotation = [x * YanqingRotationDuration / GepardRotationDuration for x in GepardRotation]

    YanqingEstimate = DefaultEstimator(f'Yanqing: {numSkill:.1f}E 1Q', YanqingRotation, YanqingCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats',
                                    TingyunRotation, TingyunCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    GepardEstimate = DefaultEstimator('Gepard: 3N 1Q, S{:.0f} {}'.format(GepardCharacter.lightcone.superposition, GepardCharacter.lightcone.name),
                                    GepardRotation, GepardCharacter, config)

    return([YanqingEstimate, TingyunEstimate, HanabiEstimate, GepardEstimate])

