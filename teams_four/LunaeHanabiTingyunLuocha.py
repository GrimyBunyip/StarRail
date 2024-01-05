from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Lunae import Lunae
from characters.harmony.Hanabi import Hanabi
from characters.harmony.Tingyun import Tingyun
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.Chorus import Chorus
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def LunaeHanabiTingyunLuocha(config):
    #%% Lunae Hanabi Tingyun Luocha Characters
    
    LunaeCharacter = Lunae(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
                            substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                            lightcone = OnTheFallOfAnAeon(**config),
                            relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = WastelanderOfBanditryDesert4pc(), planarset = RutilantArena(),
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                            benedictionTarget=LunaeCharacter,
                            **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'DEF.percent', 'ER'],
                            substats = {'RES': 8, 'CD': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = Chorus(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                            benedictionTarget=LunaeCharacter,
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'RES': 3}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                            **config)
    
    team = [LunaeCharacter, HanabiCharacter, TingyunCharacter, LuochaCharacter]

    #%% Lunae Hanabi Tingyun Luocha Team Buffs
    # Penacony Buff
    for character in [LunaeCharacter, HanabiCharacter, TingyunCharacter]:
        character.addStat('DMG.imaginary',description='Penacony from Luocha',amount=0.1)
    for character in [LunaeCharacter, LuochaCharacter, TingyunCharacter]:
        character.addStat('CD',description='Broken Keel from Hanabi',amount=0.1)

    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=LunaeCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)
    
    # Hanabi Chorus Buff
    for character in team:
        character.addStat('ATK.percent',description='Chorus',amount=0.12)
            
    # Tingyun Messenger Buff
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)
    for character in [LunaeCharacter, HanabiCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(LunaeCharacter)
    TingyunCharacter.applyUltBuff(LunaeCharacter,targetSpdMult=1.5)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Lunae Hanabi Tingyun Luocha Rotations
    numBasicHanabi = 0.0
    numSkillHanabi = 3.0
    HanabiRotation = [HanabiCharacter.useBasic() * numBasicHanabi,
                       HanabiCharacter.useSkill() * numSkillHanabi,
                    HanabiCharacter.useUltimate()]
        
    # Lunae should be about the same speed as tingyun, estimate 2.3 turn rotations
    lunaeRotation = 2.3
    LunaeRotation = [  # 140 energy needed. EndTurn needed to factor in his buffs
                LunaeCharacter.useSkill() * 3 * lunaeRotation,
                LunaeCharacter.useEnhancedBasic3() * lunaeRotation, # -3 SP, 40 energy
                LunaeCharacter.useUltimate(), # +2 SP, 5 energy
                TingyunCharacter.useBenediction(['basic','enhancedBasic']) * 2, # apply benedictions with buffs
                TingyunCharacter.useBenediction(['ultimate']) * 1,
                LunaeCharacter.endTurn(),
                HanabiCharacter.useAdvanceForward() * lunaeRotation * 2.0 / 3.0, # Hanabi only advances forward 2 out of every 3 lunae turns
                TingyunCharacter.giveUltEnergy() * TingyunCharacter.getTotalStat('SPD') / LunaeCharacter.getTotalStat('SPD') / 1.5 , # rough estimate of rotation, tingyun is about 10% faster
    ]

    TingyunRotation = [ 
            TingyunCharacter.useBasic() * 2, 
            TingyunCharacter.useSkill(),
            TingyunCharacter.useUltimate(),
    ]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Lunae Hanabi Tingyun Luocha Rotation Math
    totalLunaeEffect = sumEffects(LunaeRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    LunaeRotationDuration = totalLunaeEffect.actionvalue * 100.0 / LunaeCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's rotation
    HanabiRotation = [x * LunaeRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    TingyunRotation = [x * LunaeRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    LuochaRotation = [x * LunaeRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    
    # calculate total number of breaks for Ruan Mei Talent
    totalEffect = sumEffects(LunaeRotation + TingyunRotation + HanabiRotation + LuochaRotation)
    numBreaks = totalEffect.gauge * HanabiCharacter.weaknessBrokenUptime / HanabiCharacter.enemyToughness
    HanabiRotation.append(HanabiCharacter.useTalent() * numBreaks)

    LunaeEstimate = DefaultEstimator(f'Lunae: {lunaeRotation:.1f}N^3 1Q', LunaeRotation, LunaeCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats', 
                                    TingyunRotation, TingyunCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([LunaeEstimate,HanabiEstimate,TingyunEstimate,LuochaEstimate])