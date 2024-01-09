from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Lunae import Lunae
from characters.harmony.Hanabi import Hanabi
from characters.harmony.Hanya import Hanya
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.Chorus import Chorus
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def LunaeHanabiHanyaLuocha(config):
    #%% Lunae Hanabi Hanya Luocha Characters
    
    LunaeCharacter = Lunae(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
                            substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                            lightcone = OnTheFallOfAnAeon(**config),
                            relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = WastelanderOfBanditryDesert4pc(), planarset = RutilantArena(),
                            **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                            substats = {'RES': 7, 'SPD.flat': 12, 'CD': 5, 'CR': 4}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                            **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'SPD.flat', 'DEF.percent', 'ER'],
                            substats = {'SPD.flat': 7, 'CD': 12, 'RES': 6, 'DEF.percent': 3}),
                            lightcone = Chorus(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'RES': 3}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                            **config)
    
    team = [LunaeCharacter, HanabiCharacter, HanyaCharacter, LuochaCharacter]

    #%% Lunae Hanabi Hanya Luocha Team Buffs
    # Penacony Buff
    for character in [LunaeCharacter, HanabiCharacter, HanyaCharacter]:
        character.addStat('DMG.imaginary',description='Penacony from Luocha',amount=0.1)
    for character in [LunaeCharacter, LuochaCharacter, HanabiCharacter]:
        character.addStat('CD',description='Broken Keel from Hanya',amount=0.1)
    for character in [LunaeCharacter, LuochaCharacter, HanyaCharacter]:
        character.addStat('CD',description='Broken Keel from Hanabi',amount=0.1)

    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=LunaeCharacter,uptime=2.0/3.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)
    
    # Hanabi Chorus Buff
    for character in team:
        character.addStat('ATK.percent',description='Chorus',amount=0.12)
            
    # Hanya Messenger Buff
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc Hanya',amount=0.12,uptime=1.0/4.0)
    for character in [LunaeCharacter, HanabiCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc Hanya',amount=0.12,uptime=1.0/3.0)
    
    # Hanabi Messenger Buff
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc Hanabi',amount=0.12,uptime=1.0/4.0)
    for character in [LunaeCharacter, HanabiCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc Hanabi',amount=0.12,uptime=1.0/3.0)
        
    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(LunaeCharacter,uptime=1.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Lunae Hanabi Hanya Luocha Rotations
    numBasicHanabi = 0.0
    numSkillHanabi = 3.0
    HanabiRotation = [HanabiCharacter.useBasic() * numBasicHanabi,
                       HanabiCharacter.useSkill() * numSkillHanabi,
                    HanabiCharacter.useUltimate()]
        
    # Lunae should be about the same speed as Hanya, estimate 2.3 turn rotations
    lunaeRotation = 3.0
    LunaeRotation = [  # 140 energy needed. EndTurn needed to factor in his buffs
                LunaeCharacter.useSkill() * 3 * lunaeRotation,
                LunaeCharacter.useEnhancedBasic3() * lunaeRotation, # -3 SP, 40 energy
                LunaeCharacter.useUltimate(), # +2 SP, 5 energy
                LunaeCharacter.endTurn(),
                HanabiCharacter.useAdvanceForward() * lunaeRotation * 2.0 / 3.0, 
    ]

    numHanyaSkill = 3
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Lunae Hanabi Hanya Luocha Rotation Math
    totalLunaeEffect = sumEffects(LunaeRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    LunaeRotationDuration = totalLunaeEffect.actionvalue * 100.0 / LunaeCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's rotation
    HanabiRotation = [x * LunaeRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    HanyaRotation = [x * LunaeRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    LuochaRotation = [x * LunaeRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    LunaeEstimate = DefaultEstimator(f'Lunae: {lunaeRotation:.1f}N^3 1Q', LunaeRotation, LunaeCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    HanyaEstimate = DefaultEstimator('Hanya {:.0f}E {:.0f}Q S{:.0f} {}, 12 Spd Substats'.format(numHanyaSkill, numHanyaUlt,
                                    HanyaCharacter.lightcone.superposition, HanyaCharacter.lightcone.name), 
                                    HanyaRotation, HanyaCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([LunaeEstimate,HanabiEstimate,HanyaEstimate,LuochaEstimate])