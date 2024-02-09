from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.erudition.JingYuan import JingYuan
from characters.harmony.Hanabi import Hanabi
from characters.harmony.Hanabi import Hanabi
from characters.harmony.Tingyun import Tingyun
from characters.preservation.Fuxuan import Fuxuan
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.erudition.GeniusesRepose import GeniusesRepose
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc

def JingyuanTingyunHanabiFuxuan(config):
    #%% JingYuan Tingyun Hanabi Fuxuan Characters
    JingYuanCharacter = JingYuan(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.lightning'],
                            substats = {'CD': 10, 'CR': 10, 'ATK.percent': 5, 'BreakEffect': 3}), # get to 140 speed before buffs, to just guarantee battalia crush
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

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                            substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                            lightcone = DayOneOfMyNewLife(**config),
                            relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                            **config)
    
    team = [JingYuanCharacter, TingyunCharacter, HanabiCharacter, FuxuanCharacter]

    #%% JingYuan Tingyun Hanabi Fuxuan Team Buffs
    # Penacony Buff
    for character in [JingYuanCharacter, TingyunCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel from Hanabi',amount=0.1)
    for character in [JingYuanCharacter, TingyunCharacter, HanabiCharacter]:
        character.addStat('CD',description='Broken Keel from Fuxuan',amount=0.1)
    for character in [JingYuanCharacter, HanabiCharacter, FuxuanCharacter]:
        character.addStat('DMG.lightning',description='Penacony from Tingyun',amount=0.1)
        
    # Hanabi Messenger 4 pc
    for character in [JingYuanCharacter, TingyunCharacter, FuxuanCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Messenger Buff
    for character in [JingYuanCharacter, HanabiCharacter, FuxuanCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)

    # Hanabi Buffs
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=JingYuanCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)
    
    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(JingYuanCharacter)
    TingyunCharacter.applyUltBuff(JingYuanCharacter,targetSpdMult=HanabiCharacter.getTotalStat('SPD')/JingYuanCharacter.getTotalStat('SPD'))

    # Tingyun and Jing Yuan are going to be out of sync so we just need to try and math out an average rotation
    print('Jing Yuan Speed: ', HanabiCharacter.getTotalStat('SPD'), ' Tingyun Speed: ', TingyunCharacter.getTotalStat('SPD'))
    jyShortRotation = 2 / HanabiCharacter.getTotalStat('SPD')
    jyLongRotation = 4 / HanabiCharacter.getTotalStat('SPD')
    tyRotation = 3 / TingyunCharacter.getTotalStat('SPD')

    longToShort = (tyRotation - jyShortRotation) / jyLongRotation
    print('LongToShort Ratio', longToShort)

    #%% Print Statements
    for character in team:
        character.print()

    #%% JingYuan Tingyun Hanabi Fuxuan Rotations
    TingyunRotation = [ 
            TingyunCharacter.useBasic() * 2, 
            TingyunCharacter.useSkill(),
            TingyunCharacter.useUltimate(),
    ]
        
    lordSpeed = 0.85 # close enough of an estimate

    numSkill = 2.0 + 2.0 * longToShort
    numUlt = 1.0
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

    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% JingYuan Tingyun Hanabi Fuxuan Rotation Math
    totalJingYuanEffect = sumEffects(JingYuanRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    JingYuanRotationDuration = totalJingYuanEffect.actionvalue * 100.0 / JingYuanCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    JingYuanRotation.append(TingyunCharacter.giveUltEnergy() * JingYuanRotationDuration / TingyunRotationDuration)

    # scale other character's rotation
    TingyunRotation = [x * JingYuanRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HanabiRotation = [x * JingYuanRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    FuxuanRotation = [x * JingYuanRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()
    DanceDanceDanceEffect.actionvalue = -0.24 * JingYuanRotationDuration / HanabiRotationDuration
    JingYuanCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    JingYuanRotation.append(DanceDanceDanceEffect)
    
    TingyunCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    TingyunRotation.append(DanceDanceDanceEffect)
    
    FuxuanCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    FuxuanRotation.append(DanceDanceDanceEffect)
    
    HanabiCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    HanabiRotation.append(DanceDanceDanceEffect)

    JingYuanEstimate = DefaultEstimator(f'Jing Yuan {numSkill:.1f}E {numUlt:.0f}Q', JingYuanRotation, JingYuanCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats', 
                                    TingyunRotation, TingyunCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    FuxuanEstimate = DefaultEstimator('Fuxuan: 2N 1E 1Q, S{:.0f} {}'.format(FuxuanCharacter.lightcone.superposition, FuxuanCharacter.lightcone.name),
                                    FuxuanRotation, FuxuanCharacter, config)

    return([JingYuanEstimate,TingyunEstimate,HanabiEstimate,FuxuanEstimate])