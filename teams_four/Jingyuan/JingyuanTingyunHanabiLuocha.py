from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.erudition.JingYuan import JingYuan
from characters.harmony.Hanabi import Hanabi
from characters.harmony.Tingyun import Tingyun
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.erudition.GeniusesRepose import GeniusesRepose
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def JingyuanTingyunHanabiLuocha(config):
    #%% JingYuan Tingyun Hanabi Luocha Characters
    JingYuanCharacter = JingYuan(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.lightning'],
                            substats = {'CD': 9, 'CR': 11, 'ATK.percent': 5, 'BreakEffect': 3}),
                            lightcone = GeniusesRepose(**config),
                            relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(followupStacks=6.5,stacks=8.0,uptime=1.0), planarset = InertSalsotto(),
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                            benedictionTarget=JingYuanCharacter,
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
    
    team = [JingYuanCharacter, TingyunCharacter, HanabiCharacter, LuochaCharacter]

    #%% JingYuan Tingyun Hanabi Luocha Team Buffs
    # Penacony Buff
    for character in [JingYuanCharacter, TingyunCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel from Hanabi',amount=0.1)
    for character in [JingYuanCharacter, TingyunCharacter, HanabiCharacter]:
        character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
    for character in [JingYuanCharacter, LuochaCharacter, HanabiCharacter]:
        character.addStat('DMG.lightning',description='Penacony from Tingyun',amount=0.1)
        
    # Hanabi Messenger 4 pc
    for character in [JingYuanCharacter, TingyunCharacter, LuochaCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Messenger Buff
    for character in [JingYuanCharacter, HanabiCharacter, LuochaCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Hanabi Buffs
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=JingYuanCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(JingYuanCharacter)
    TingyunCharacter.applyUltBuff(JingYuanCharacter,targetSpdMult=HanabiCharacter.getTotalStat('SPD')/JingYuanCharacter.getTotalStat('SPD'))

    #%% Print Statements
    for character in team:
        character.print()

    #%% JingYuan Tingyun Hanabi Luocha Rotations
    numBasicTingyun = 2.0
    numSkillTingyun = 1.0
    TingyunRotation = [ 
            TingyunCharacter.useBasic() * numBasicTingyun, 
            TingyunCharacter.useSkill() * numSkillTingyun,
            TingyunCharacter.useUltimate(),
    ]
        
    # JingYuan & Tingyun Rotation
    TingyunEnergyPerTurn = (60.0 if TingyunCharacter.eidolon >= 6 else 50.0) / 3.0  # let's say half the time, huohuo can shave off a turn
    numSkill = (130.0 - 5.0) / (30.0 + TingyunEnergyPerTurn)
    numUlt = 1

    lordSpeed = 0.85 # close enough of an estimate
    numTalents = ( 3 * numSkill * lordSpeed / HanabiCharacter.getTotalStat('SPD') / 0.92 )  + 2 * numSkill + 3 # 0.92 to account for S5 dance dance Dance
    JingYuanRotation = [
        JingYuanCharacter.useSkill() * numSkill,
        JingYuanCharacter.useUltimate() * numUlt,
        JingYuanCharacter.useTalent() * numTalents,
        TingyunCharacter.useBenediction(['skill']) * numSkill,
        TingyunCharacter.useBenediction(['ultimate']),
        HanabiCharacter.useAdvanceForward(advanceAmount=1.0 - JingYuanCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')) * numSkill, 
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

    #%% JingYuan Tingyun Hanabi Luocha Rotation Math
    totalJingYuanEffect = sumEffects(JingYuanRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    JingYuanRotationDuration = totalJingYuanEffect.actionvalue * 100.0 / JingYuanCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()
    DanceDanceDanceEffect.actionvalue = -0.24 * JingYuanRotationDuration / HanabiRotationDuration
    JingYuanCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    JingYuanRotation.append(DanceDanceDanceEffect * JingYuanRotationDuration / HanabiRotationDuration)
    
    TingyunCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    TingyunRotation.append(DanceDanceDanceEffect * TingyunRotationDuration / HanabiRotationDuration)
    
    LuochaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    LuochaRotation.append(DanceDanceDanceEffect * LuochaRotationDuration / HanabiRotationDuration)
    
    HanabiCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    HanabiRotation.append(DanceDanceDanceEffect)
    
    totalJingYuanEffect = sumEffects(JingYuanRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    JingYuanRotationDuration = totalJingYuanEffect.actionvalue * 100.0 / JingYuanCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's rotation
    TingyunRotation = [x * JingYuanRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HanabiRotation = [x * JingYuanRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    LuochaRotation = [x * JingYuanRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    JingYuanEstimate = DefaultEstimator(f'Jing Yuan {numSkill:.1f}E {numUlt:.0f}Q', JingYuanRotation, JingYuanCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, {numBasicTingyun:.1f}N {numSkillTingyun:.1f}E 1Q, 12 spd substats', 
                                    TingyunRotation, TingyunCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([JingYuanEstimate,TingyunEstimate,HanabiEstimate,LuochaEstimate])