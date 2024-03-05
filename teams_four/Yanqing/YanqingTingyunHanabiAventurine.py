from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Aventurine import Aventurine
from characters.hunt.Yanqing import Yanqing
from characters.harmony.Tingyun import Tingyun
from characters.harmony.Hanabi import Hanabi
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.DestinysThreadsForewoven import DestinysThreadsForewoven
from lightCones.preservation.LandausChoice import LandausChoice
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc
from relicSets.relicSets.KnightOfPurityPalace import KnightOfPurityPalace2pc, KnightOfPurityPalace4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc

def YanqingTingyunHanabiAventurine(config):
    #%% Yanqing Tingyun Hanabi Aventurine Characters
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

    AventurineCharacter = Aventurine(RelicStats(mainstats = ['DEF.percent', 'SPD.flat', 'DEF.percent', 'DEF.percent'],
                            substats = {'CR': 8, 'CD': 12, 'SPD.flat': 5, 'DEF.percent': 3}),
                            lightcone = DestinysThreadsForewoven(defense=3250,**config),
                            leverage_cr=0.48 * 3250 / 4000,
                            relicsetone = KnightOfPurityPalace2pc(), relicsettwo = KnightOfPurityPalace4pc(), planarset = BrokenKeel(),
                            **config)
    
    team = [YanqingCharacter, TingyunCharacter, HanabiCharacter, AventurineCharacter]

    #%% Yanqing Tingyun Hanabi Aventurine Team Buffs
    for character in [TingyunCharacter, YanqingCharacter, HanabiCharacter]:
        character.addStat('CD',description='Broken Keel from Aventurine',amount=0.1)
    for character in [TingyunCharacter, YanqingCharacter, AventurineCharacter]:
        character.addStat('CD',description='Broken Keel from Hanabi',amount=0.1)

    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=YanqingCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=3.0/3.0)
    
    # Past and Future
    YanqingCharacter.addStat('DMG',description='Past and Future',amount=0.32)
        
    # Hanabi Messenger 4 pc
    for character in [YanqingCharacter, TingyunCharacter, AventurineCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Messenger Buff
    for character in [YanqingCharacter, HanabiCharacter, AventurineCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(YanqingCharacter)
    TingyunCharacter.applyUltBuff(YanqingCharacter,targetSpdMult=HanabiCharacter.getTotalStat('SPD')/YanqingCharacter.getTotalStat('SPD'))

    # Aventurine Buffs
    AventurineCharacter.applyUltDebuff(team=team,rotationDuration=4.0,targetingUptime=1.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Yanqing Tingyun Hanabi Aventurine Rotations
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

    numBasicAventurine = 4.0
    numTalentAventurine = 4.0 # stacks from ultimate
    numTalentAventurine = 0.85 * numBasicAventurine # estimate 15% of the time yanqing fails to followup
    numEnemyAttacks = AventurineCharacter.numEnemies * AventurineCharacter.enemySpeed / AventurineCharacter.getTotalStat('SPD') # extra stacks from people getting hit per turn
    numEnemyAttacks *= (1.0 + (6*1) / (6*1 + 6 + 4 + 4)) # extra stacks from when Aventurine is Targeted
    numTalentAventurine += numBasicAventurine * numEnemyAttacks
    AventurineRotation = [AventurineCharacter.useBasic() * numBasicAventurine,
                           AventurineCharacter.useTalent() * numTalentAventurine,
                           AventurineCharacter.useUltimate() * 1,]
    #%% Yanqing Tingyun Hanabi Aventurine Rotation Math

    totalYanqingEffect = sumEffects(YanqingRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalAventurineEffect = sumEffects(AventurineRotation)

    YanqingRotationDuration = totalYanqingEffect.actionvalue * 100.0 / YanqingCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    AventurineRotationDuration = totalAventurineEffect.actionvalue * 100.0 / AventurineCharacter.getTotalStat('SPD')

    YanqingRotation.append(TingyunCharacter.giveUltEnergy() * YanqingRotationDuration / TingyunRotationDuration)
    
    print('##### Rotation Durations #####')
    print('Yanqing: ',YanqingRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Hanabi: ',HanabiRotationDuration)
    print('Aventurine: ',AventurineRotationDuration)

    # Scale other character's rotation
    TingyunRotation = [x * YanqingRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HanabiRotation = [x * YanqingRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    AventurineRotation = [x * YanqingRotationDuration / AventurineRotationDuration for x in AventurineRotation]

    YanqingEstimate = DefaultEstimator(f'Yanqing: {numSkill:.1f}E 1Q', YanqingRotation, YanqingCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats',
                                    TingyunRotation, TingyunCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    AventurineEstimate = DefaultEstimator(f'Aventurine: {numBasicAventurine:.0f}N {numTalentAventurine:.1f}T 1Q, S{AventurineCharacter.lightcone.superposition:.0f} {AventurineCharacter.lightcone.name}',
                                    AventurineRotation, AventurineCharacter, config)

    return([YanqingEstimate, TingyunEstimate, HanabiEstimate, AventurineEstimate])

