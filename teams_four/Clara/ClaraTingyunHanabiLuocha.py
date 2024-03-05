from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Clara import Clara
from characters.harmony.Tingyun import Tingyun
from characters.harmony.Hanabi import Hanabi
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def ClaraTingyunHanabiLuocha(config):
    #%% Clara Tingyun Hanabi Luocha Characters
    ClaraCharacter = Clara(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.physical'],
                            substats = {'CD': 8, 'CR': 12, 'ATK.percent': 5, 'BreakEffect': 5}),
                            lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=5.0, **config),
                            relicsetone = ChampionOfStreetwiseBoxing2pc(),
                            relicsettwo = ChampionOfStreetwiseBoxing4pc(),
                            planarset = InertSalsotto(),
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                            benedictionTarget=ClaraCharacter,
                            **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'SPD.flat', 'ER'],
                            substats = {'CD': 8, 'SPD.flat': 12, 'RES': 5, 'DEF.percent': 3}),
                            lightcone = DanceDanceDance(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 5, 'SPD.flat': 12, 'HP.percent': 4, 'RES': 7}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                            **config)
    
    team = [ClaraCharacter, TingyunCharacter, HanabiCharacter, LuochaCharacter]

    #%% Clara Tingyun Hanabi Luocha Team Buffs
    for character in [TingyunCharacter, ClaraCharacter, HanabiCharacter]:
        character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
    for character in [TingyunCharacter, ClaraCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel from Hanabi',amount=0.1)

    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=ClaraCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=3.0/3.0)
            
    # Hanabi Messenger 4 pc
    for character in [ClaraCharacter, TingyunCharacter, LuochaCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Messenger Buff
    for character in [ClaraCharacter, HanabiCharacter, LuochaCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(ClaraCharacter)
    TingyunCharacter.applyUltBuff(ClaraCharacter,targetSpdMult=HanabiCharacter.getTotalStat('SPD')/ClaraCharacter.getTotalStat('SPD'))

    #%% Print Statements
    for character in team:
        character.print()

    #%% Clara Tingyun Hanabi Luocha Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long
    numSkillClara = 1.25
    numEnemyAttacks = ClaraCharacter.enemySpeed * ClaraCharacter.numEnemies * numSkillClara / (HanabiCharacter.getTotalStat('SPD') / 0.92 ) # enemy attacks now scale to hanabi speed, account for S5 dance dance in denominator
    numEnhancedTalents = 2
    numUnenhancedTalents = (numEnemyAttacks - numEnhancedTalents) * (5*6) / (5*6 + 4 + 4 + 4)
    numSvarogCounters = numEnemyAttacks * (5*6) / (5*6 + 4 + 4 + 4)

    ClaraRotation = [ # 110 max energy
            ClaraCharacter.useSkill() * numSkillClara,
            ClaraCharacter.useMarkOfSvarog() * numSvarogCounters, 
            ClaraCharacter.useTalent(enhanced=True) * numEnhancedTalents,
            ClaraCharacter.useUltimate(),
            ClaraCharacter.useTalent(enhanced=False) * numUnenhancedTalents,
            TingyunCharacter.useBenediction(['skill']) * numSkillClara,
            TingyunCharacter.useBenediction(['talent','followup']) * numEnhancedTalents,
            TingyunCharacter.useBenediction(['talent','followup']) * numUnenhancedTalents,
            HanabiCharacter.useAdvanceForward(advanceAmount=1.0 - ClaraCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')) * numSkillClara,
    ]
    
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

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Clara Tingyun Hanabi Luocha Rotation Math

    totalClaraEffect = sumEffects(ClaraRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    ClaraRotationDuration = totalClaraEffect.actionvalue * 100.0 / ClaraCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()
    DanceDanceDanceEffect.actionvalue = -0.24 * ClaraRotationDuration / HanabiRotationDuration
    ClaraCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    ClaraRotation.append(DanceDanceDanceEffect * ClaraRotationDuration / HanabiRotationDuration)
    
    TingyunCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    TingyunRotation.append(DanceDanceDanceEffect * TingyunRotationDuration / HanabiRotationDuration)
    
    LuochaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    LuochaRotation.append(DanceDanceDanceEffect * LuochaRotationDuration / HanabiRotationDuration)
    
    HanabiCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    HanabiRotation.append(DanceDanceDanceEffect)
    
    totalClaraEffect = sumEffects(ClaraRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    ClaraRotationDuration = totalClaraEffect.actionvalue * 100.0 / ClaraCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    ClaraRotation.append(TingyunCharacter.giveUltEnergy() * ClaraRotationDuration / TingyunRotationDuration)
    
    print('##### Rotation Durations #####')
    print('Clara: ',ClaraRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Hanabi: ',HanabiRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # Scale other character's rotation
    TingyunRotation = [x * ClaraRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HanabiRotation = [x * ClaraRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    LuochaRotation = [x * ClaraRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    ClaraEstimate = DefaultEstimator(f'Clara: {numSkillClara:.1f}E {numSvarogCounters:.1f}T 1Q', ClaraRotation, ClaraCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats',
                                    TingyunRotation, TingyunCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    LuochaEstimate = DefaultEstimator(f'Luocha: 3N 1E 1Q, S{LuochaCharacter.lightcone.superposition:d} {LuochaCharacter.lightcone.name}', 
                                    LuochaRotation, LuochaCharacter, config)

    return([ClaraEstimate, TingyunEstimate, HanabiEstimate, LuochaEstimate])

