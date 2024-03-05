from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Lunae import Lunae
from characters.harmony.Hanabi import Hanabi
from characters.harmony.Tingyun import Tingyun
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PastAndFuture import PastAndFuture
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def LunaeE2HanabiTingyunLuocha(config):
    #%% Lunae Hanabi Tingyun Luocha Characters
    
    originalFivestarEidolons = config['fivestarEidolons']
    config['fivestarEidolons'] = 2
    LunaeCharacter = Lunae(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
                            substats = {'CR': 11, 'CD': 9, 'ATK.percent': 5, 'BreakEffect': 3}),
                            lightcone = OnTheFallOfAnAeon(uptime=1.0,**config),
                            relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = WastelanderOfBanditryDesert4pc(), planarset = RutilantArena(),
                            **config)
    config['fivestarEidolons'] = originalFivestarEidolons

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                            benedictionTarget=LunaeCharacter,
                            **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'SPD.flat', 'ER'],
                            substats = {'CD': 8, 'SPD.flat': 12, 'RES': 5, 'DEF.percent': 3}),
                            lightcone = PastAndFuture(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'RES': 3}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                            **config)
    
    team = [LunaeCharacter, HanabiCharacter, TingyunCharacter, LuochaCharacter]

    #%% Lunae Hanabi Tingyun Luocha Team Buffs
    # Penacony Buff
    for character in [LunaeCharacter, HanabiCharacter, TingyunCharacter]:
        character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
    for character in [LunaeCharacter, LuochaCharacter, TingyunCharacter]:
        character.addStat('CD',description='Broken Keel from Hanabi',amount=0.1)

    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applyUltBuff(team=team,uptime=3.0/3.0)
    HanabiCharacter.applySkillBuff(character=LunaeCharacter,uptime=1.0,type=['ultimate']) # hanabi skill buff always applies to ultiamtes
    HanabiCharacter.applySkillBuff(character=LunaeCharacter,uptime=6.0/7.0,type=['enhancedBasic']) # hanabi skill buff applies to 6 of 7 enhanced basics 
            
    # Past and Future
    LunaeCharacter.addStat('DMG',description='Past and Future',amount=0.32,uptime=1.0,type=['ultimate'])
    LunaeCharacter.addStat('DMG',description='Past and Future',amount=0.32,uptime=6.0/7.0,type=['enhancedBasic'])
    
    # Tingyun Messenger Buff
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc Tingyun',amount=0.12,uptime=1.0/4.0)
    LunaeCharacter.addStat('SPD.percent',description='Messenger 4 pc Tingyun',amount=0.12,uptime=1.0/4.0)
    HanabiCharacter.addStat('SPD.percent',description='Messenger 4 pc Tingyun',amount=0.12,uptime=1.0/3.0)
    
    # Hanabi Messenger Buff
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc Hanabi',amount=0.12,uptime=1.0/4.0)
    LunaeCharacter.addStat('SPD.percent',description='Messenger 4 pc Hanabi',amount=0.12,uptime=1.0/4.0)
    HanabiCharacter.addStat('SPD.percent',description='Messenger 4 pc Hanabi',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(LunaeCharacter)
    TingyunCharacter.applyUltBuff(LunaeCharacter,ultUptime=2.0/3.0,type=['ultimate']) # tingyun ultimate bonus applies to 2 out of 3 ultimates
    TingyunCharacter.applyUltBuff(LunaeCharacter,ultUptime=3.0/7.0,type=['enhancedBasic']) # tingyun ultimate bonus applies to 3 out of 7 enhanceds

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
    numBasicLunae = 2.0 / 3.0
    numEnhancedLunae = 7.0 / 3.0
    
    LunaeRotation = [  # 140 energy needed. EndTurn needed to factor in his buffs
                LunaeCharacter.useBasic() * numBasicLunae,
                LunaeCharacter.endTurn(),
                LunaeCharacter.useSkill() * 3 * numEnhancedLunae,
                LunaeCharacter.useEnhancedBasic3() * numEnhancedLunae, # -3 SP, 40 energy
                LunaeCharacter.useUltimate(), # +2 SP, 5 energy
                TingyunCharacter.useBenediction(['basic']) * numBasicLunae, # apply benedictions with buffs
                TingyunCharacter.useBenediction(['basic','enhancedBasic']) * numEnhancedLunae, # apply benedictions with buffs
                TingyunCharacter.useBenediction(['ultimate']) * 1,
                LunaeCharacter.endTurn(),
                HanabiCharacter.useAdvanceForward(advanceAmount=1.0 - LunaeCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')) * (numBasicLunae + numEnhancedLunae - 1.0), 
    ]

    numBasicTingyun = 1.5
    numSkillTingyun = 1.5
    TingyunRotation = [ 
            TingyunCharacter.useBasic() * numBasicTingyun, 
            TingyunCharacter.useSkill() * numSkillTingyun,
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

    LunaeRotation.append(TingyunCharacter.giveUltEnergy() * LunaeRotationDuration / TingyunRotationDuration)

    # scale other character's rotation
    HanabiRotation = [x * LunaeRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    TingyunRotation = [x * LunaeRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    LuochaRotation = [x * LunaeRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    LunaeEstimate = DefaultEstimator(f'Lunae E{LunaeCharacter.eidolon:.0f}: {numBasicLunae:.1f}N {numEnhancedLunae:.1f}N^3 1Q', LunaeRotation, LunaeCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, {numBasicTingyun:.1f}N {numSkillTingyun:.1f}E 1Q, 12 spd substats', 
                                    TingyunRotation, TingyunCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([LunaeEstimate,HanabiEstimate,TingyunEstimate,LuochaEstimate])