from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Jingliu import Jingliu
from characters.harmony.Bronya import Bronya
from characters.harmony.Tingyun import Tingyun
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PastAndFuture import PastAndFuture
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc, HunterOfGlacialForest4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def JingliuBronyaTingyunLuocha(config):
    #%% Jingliu Bronya Tingyun Luocha Characters
    JingliuCharacter = Jingliu(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.ice'],
                        substats = {'CR': 12, 'CD': 8, 'SPD.flat': 3, 'ATK.percent': 5}),
                        lightcone = OnTheFallOfAnAeon(**config),
                        relicsetone = HunterOfGlacialForest2pc(), relicsettwo = HunterOfGlacialForest4pc(uptime=0.4), planarset = RutilantArena(uptime=0.0),
                        **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'HP.percent', 'CD', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = PastAndFuture(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                            benedictionTarget=JingliuCharacter,
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [JingliuCharacter, BronyaCharacter, TingyunCharacter, LuochaCharacter]

    #%% Jingliu Bronya Tingyun Luocha Team Buffs
    # only enhanced skills have rutilant arena buff
    JingliuCharacter.addStat('DMG',description='Rutilant Arena', amount=0.20, type=['enhancedSkill']) # take care of rutilant arena manually

    # Broken Keel and Penacony Buff
    for character in [JingliuCharacter, BronyaCharacter, TingyunCharacter]:
        character.addStat('CD',description='Broken Keel Luocha',amount=0.10)
    for character in [JingliuCharacter, TingyunCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel Bronya',amount=0.10)

    # Messenger 4 pc Bronya
    for character in [JingliuCharacter, TingyunCharacter, LuochaCharacter]: # uptime 1.0 because bronya casts every 4 jingliu turns
        character.addStat('SPD.percent',description='Messenger 4 pc Bronya',amount=0.12,uptime=1.0/4.0)

    # Messenger 4 pc Tingyun
    for character in [JingliuCharacter, BronyaCharacter, LuochaCharacter]: # uptime 1.0 because tingyun casts every 2.5 jingliu turns
        character.addStat('SPD.percent',description='Messenger 4 pc Tingyun',amount=0.12,uptime=1.0/2.5)
        
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Jingliu Bronya Tingyun Luocha Rotations
    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    # This rotation is really complicated so I will map it out over 12 turns
    # energy    moon  turn    description
    # 65	    1	    0	skill advance tingyun ultimate enhanced bronya enhanced
    # 115	    0	    1	enhanced bronya skill
    # 65	    1	    2	skill advance ultimate enhanced bronya enhanced
    # 35	    0	    3	Tingyun enhanced Ultimate bronya enhanced
    # 105	    1	    4	skill bronya skill advance enhanced
    # 65	    0	    5	tingyun ultimate enhanced bronya enhanced
    # 135	    1	    6	skill bronya skill advance enhanced
    # 65	    0	    7	ultimate enhanced bronya enhanced
    # 35	    2	    8	skill bronya skill advance tingyun ultimate enhanced
    # 95	    0	    9	enhanced bronya enhanced
    # 95	    2	    10	skill bronya skill advance ultimate tingyun enhanced
    # 5	        1	    11	enhanced bronya enhanced ultimate
    # 55	    0	    12	enhanced bronya skill
    
    # this is a 12 skill, 20 enhanced, 8 ultimate rotation
    # 6 skills are bronya buffed
    # 6 skills are not
    # 7 enhanceds are bronya buffed (there are 13 bronya skill casts total)
    # 5 ultimates and 10 enhanceds are tingyun ult buffed (there are 5 tingyun ultimates total)
    # 15 enhanceds should be tingyun buffed
    # 6 enhanceds should be bronya ult buffed
    # 3 ultimates should be bronya ult buffed

    # Assume Bronya skill buff applies to skills, and only applies a fraction of the time to the remaining abilities
    numSkill = 12.0 / 8.0 # 1.5
    numEnhanced = 20.0 / 8.0 # 2.5
    numUlt = 8.0 / 8.0 # 1.0

    JingliuRotation = []
    
    # Calculate Jingliu Skills
    BronyaCharacter.applySkillBuff(JingliuCharacter,uptime=0.5) # Bronya buff applies to half of skills
    JingliuCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition, uptime=0.5)
    JingliuRotation += [JingliuCharacter.useSkill() * numSkill]
    JingliuCharacter.stats['DMG'].pop() # remove bronya skill buff
    JingliuCharacter.stats['DMG'].pop() # remove past and future

    # Calculate Jingliu Enhanced Skills
    TingyunCharacter.applySkillBuff(JingliuCharacter,uptime=15.0/20.0)
    TingyunCharacter.applyUltBuff(JingliuCharacter,ultUptime=10.0/20.0)
    BronyaCharacter.applySkillBuff(JingliuCharacter,uptime=7.0/20.0) # Bronya skill buff applies to 7 enhanceds out of 20
    JingliuCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition, uptime=7.0/20.0)
    BronyaCharacter.applyUltBuff(JingliuCharacter,uptime=6.0/20.0) # Bronya ult buff applies to 6 enhanceds out of 20
    JingliuRotation += [JingliuCharacter.useEnhancedSkill() * numEnhanced]
    JingliuRotation += [TingyunCharacter.useBenediction(['enhancedSkill']) * numEnhanced * 15.0 / 20.0]
    JingliuCharacter.stats['DMG'].pop() # remove bronya skill buff
    JingliuCharacter.stats['DMG'].pop() # remove bronya skill buff
    JingliuCharacter.stats['DMG'].pop() # remove Tingyun ult buff
    JingliuCharacter.stats['CD'].pop() # remove bronya ult buff
    JingliuCharacter.stats['ATK'].pop() # remove bronya ult buff
    JingliuCharacter.stats['ATK'].pop() # remove Tingyun Skill buff

    # Calculate Jingliu Ultimates
    TingyunCharacter.applySkillBuff(JingliuCharacter)
    TingyunCharacter.applyUltBuff(JingliuCharacter)
    BronyaCharacter.applySkillBuff(JingliuCharacter,uptime=0.5) # Bronya buff applies to half of ultimates
    JingliuCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition, uptime=0.5)
    BronyaCharacter.applyUltBuff(JingliuCharacter,uptime=3.0/8.0) # Bronya ult buff applies to 3 enhanceds out of 8 ultimates
    JingliuRotation += [JingliuCharacter.useUltimate()]
    JingliuRotation += [TingyunCharacter.useBenediction(['ultimate'])]

    # adjust number of turns
    JingliuRotation += [JingliuCharacter.extraTurn() * 0.9 * numSkill / 2.0] # multiply by 0.9 because it tends to overlap with skill advances
    JingliuRotation += [BronyaCharacter.useAdvanceForward() * (numSkill / 4.0 + numEnhanced / 2.0)] #This jingliu rotation is 2.5 + 0.75 = 3.25 turns

    numBasicTingyun = 2.0
    numSkillTingyun = 1.0
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

    #%% Jingliu Bronya Tingyun Luocha Rotation Math
    totalJingliuEffect = sumEffects(JingliuRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    JingliuRotationDuration = totalJingliuEffect.actionvalue * 100.0 / JingliuCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Jingliu: ',JingliuRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # scale other character's rotation
    BronyaRotation = [x * JingliuRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    TingyunRotation = [x * JingliuRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    LuochaRotation = [x * JingliuRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    
    JingliuRotation.append(TingyunCharacter.giveUltEnergy() * JingliuRotationDuration / TingyunRotationDuration)

    JingliuEstimate = DefaultEstimator('Jingliu {:.1f}E {:.1f}Moon {:.0f}Q'.format(numSkill, numEnhanced, numUlt),
                                                    JingliuRotation, JingliuCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, {numBasicTingyun:.1f}N {numSkillTingyun:.1f}E 1Q, 12 spd substats', 
                                    TingyunRotation, TingyunCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name),
                                    LuochaRotation, LuochaCharacter, config)

    return([JingliuEstimate, BronyaEstimate, TingyunEstimate, LuochaEstimate])