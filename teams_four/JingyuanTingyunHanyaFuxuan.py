from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.erudition.JingYuan import JingYuan
from characters.harmony.Hanya import Hanya
from characters.harmony.Hanya import Hanya
from characters.harmony.Tingyun import Tingyun
from characters.preservation.Fuxuan import Fuxuan
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.erudition.GeniusesRepose import GeniusesRepose
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc

def JingyuanTingyunHanyaFuxuan(config):
    #%% JingYuan Tingyun Hanya Fuxuan Characters
    JingYuanCharacter = JingYuan(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.lightning'],
                            substats = {'CD': 11, 'CR': 7, 'SPD.flat': 7, 'ATK.percent': 3}), # get to 140 speed before buffs, to just guarantee battalia crush
                            lightcone = GeniusesRepose(**config),
                            relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(followupStacks=6.5,stacks=8.0,uptime=1.0), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                            benedictionTarget=JingYuanCharacter,
                            **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                            substats = {'CR': 8, 'SPD.flat': 12, 'CD': 5, 'ATK.percent': 3}),
                            lightcone = DanceDanceDance(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                            **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                            substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                            lightcone = DayOneOfMyNewLife(**config),
                            relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                            **config)
    
    team = [JingYuanCharacter, TingyunCharacter, HanyaCharacter, FuxuanCharacter]

    #%% JingYuan Tingyun Hanya Fuxuan Team Buffs
    # Penacony Buff
    for character in [JingYuanCharacter, TingyunCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel from Hanya',amount=0.1)
    for character in [JingYuanCharacter, TingyunCharacter, HanyaCharacter]:
        character.addStat('CD',description='Broken Keel from Fuxuan',amount=0.1)
    for character in [JingYuanCharacter, HanyaCharacter, FuxuanCharacter]:
        character.addStat('DMG.lightning',description='Penacony from Tingyun',amount=0.1)
        
    # Hanya Messenger 4 pc
    for character in [JingYuanCharacter, TingyunCharacter, FuxuanCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Messenger Buff
    for character in [JingYuanCharacter, HanyaCharacter, FuxuanCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(JingYuanCharacter,uptime=1.0)
    
    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(JingYuanCharacter)
    TingyunCharacter.applyUltBuff(JingYuanCharacter)

    # Tingyun and Jing Yuan are going to be out of sync so we just need to try and math out an average rotation
    print('Jing Yuan Speed: ', JingYuanCharacter.getTotalStat('SPD'), ' Tingyun Speed: ', TingyunCharacter.getTotalStat('SPD'))
    jyShortRotation = 2 / JingYuanCharacter.getTotalStat('SPD')
    jyLongRotation = 4 / JingYuanCharacter.getTotalStat('SPD')
    tyRotation = 3 / TingyunCharacter.getTotalStat('SPD')

    longToShort = (tyRotation - jyShortRotation) / jyLongRotation
    print('LongToShort Ratio', longToShort)

    # Use long to short ratio to estimate Jing Yuan Buff
    JingYuanCharacter.addStat('DMG',description='Tingyun Ult',
                            amount=0.65 if TingyunCharacter.eidolon >= 3 else 0.6,
                            uptime=1.0 - longToShort / 2)

    #%% Print Statements
    for character in team:
        character.print()

    #%% JingYuan Tingyun Hanya Fuxuan Rotations
    TingyunRotation = [ 
            TingyunCharacter.useBasic() * 2, 
            TingyunCharacter.useSkill(),
            TingyunCharacter.useUltimate(),
    ]
        
    lordSpeed = 0.85 # close enough of an estimate

    numSkill = 2.0 + 2.0 * longToShort
    numUlt = 1.0
    numTalents = ( 3 * numSkill * lordSpeed / JingYuanCharacter.getTotalStat('SPD') )  + 2 * numSkill + 3
    JingYuanRotation = [
        JingYuanCharacter.useSkill() * numSkill,
        JingYuanCharacter.useUltimate() * numUlt,
        JingYuanCharacter.useTalent() * numTalents,
        TingyunCharacter.useBenediction(['skill']) * numSkill,
        TingyunCharacter.useBenediction(['ultimate']),
        TingyunCharacter.giveUltEnergy(),
    ]
    
    numHanyaSkill = 4
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]

    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% JingYuan Tingyun Hanya Fuxuan Rotation Math
    totalJingYuanEffect = sumEffects(JingYuanRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    JingYuanRotationDuration = totalJingYuanEffect.actionvalue * 100.0 / JingYuanCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    # scale other character's rotation
    TingyunRotation = [x * JingYuanRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HanyaRotation = [x * JingYuanRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    FuxuanRotation = [x * JingYuanRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()
    DanceDanceDanceEffect.actionvalue = -0.24 * JingYuanRotationDuration / HanyaRotationDuration
    JingYuanCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    JingYuanRotation.append(DanceDanceDanceEffect)
    
    TingyunCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    TingyunRotation.append(DanceDanceDanceEffect)
    
    FuxuanCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    FuxuanRotation.append(DanceDanceDanceEffect)
    
    HanyaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    HanyaRotation.append(DanceDanceDanceEffect)

    JingYuanEstimate = DefaultEstimator(f'Jing Yuan {numSkill:.1f}E {numUlt:.0f}Q', JingYuanRotation, JingYuanCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats', 
                                    TingyunRotation, TingyunCharacter, config)
    HanyaEstimate = DefaultEstimator(f'Hanya {numHanyaSkill:.0f}E {numHanyaUlt:.0f}Q S{HanyaCharacter.lightcone.superposition:.0f} {HanyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanyaRotation, HanyaCharacter, config)
    FuxuanEstimate = DefaultEstimator('Fuxuan: 2N 1E 1Q, S{:.0f} {}'.format(FuxuanCharacter.lightcone.superposition, FuxuanCharacter.lightcone.name),
                                    FuxuanRotation, FuxuanCharacter, config)

    return([JingYuanEstimate,TingyunEstimate,HanyaEstimate,FuxuanEstimate])