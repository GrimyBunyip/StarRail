from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Lunae import Lunae
from characters.harmony.Tingyun import Tingyun
from characters.harmony.Yukong import Yukong
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def LunaeTingyunYukongLuocha(config):
    #%% Lunae Tingyun Yukong Luocha Characters
    LunaeCharacter = Lunae(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
                            substats = {'CR': 8, 'CD': 12, 'ATK.percent': 3, 'SPD.flat': 5}),
                            lightcone = OnTheFallOfAnAeon(**config),
                            relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = WastelanderOfBanditryDesert4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                            benedictionTarget=LunaeCharacter,
                            **config)

    YukongCharacter = Yukong(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'ER'],
                            substats = {'CR': 8, 'CD': 12, 'SPD.flat': 5, 'RES': 3}),
                            lightcone = PlanetaryRendezvous(**config),
                            relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 5, 'SPD.flat': 12, 'HP.percent': 4, 'RES': 7}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                            **config)
    
    team = [LunaeCharacter, TingyunCharacter, YukongCharacter, LuochaCharacter]

    #%% Lunae Tingyun Yukong Luocha Team Buffs
    # Penacony Buff
    for character in [LunaeCharacter, TingyunCharacter, LuochaCharacter]:
        character.addStat('DMG.imaginary',description='Penacony from Yukong',amount=0.1)
    for character in [LunaeCharacter, TingyunCharacter, YukongCharacter]:
        character.addStat('DMG.imaginary',description='Penacony from Luocha',amount=0.1)
        
    # Yukong imaginary damage trace
    for character in [LunaeCharacter, LuochaCharacter]:
        character.addStat('DMG.imaginary',description='Yukong trace',amount=0.12)

    # Yukong Planetary Rendezvous
    for character in [LunaeCharacter, LuochaCharacter]:
        character.addStat('DMG',description='Planetary Rendezvous',amount=0.09 + 0.03 * YukongCharacter.lightcone.superposition)

    # Tingyun Messenger Buff
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)
    for character in [LunaeCharacter, YukongCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/2.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(LunaeCharacter)
    TingyunCharacter.applyUltBuff(LunaeCharacter)

    # Estimate Yukong Buffs.
    # Yukong is speed tuned to be slightly faster than Lunae, and always going before him
    LunaeCharacter.addStat('ATK.percent',description='Roaring Bowstrings',
                    amount=0.88 if YukongCharacter.eidolon >= 3 else 0.80,
                    uptime=3.0 / 4.0)
    LunaeCharacter.addStat('CR',description='Yukong ultimate',
                    amount=0.294 if YukongCharacter.eidolon >= 5 else 0.28,
                    uptime=1.0 / 4.0 ) # 1 ult buff, 4 characters, 4 turn rotation
    LunaeCharacter.addStat('CD',description='Yukong ultimate',
                    amount=0.702 if YukongCharacter.eidolon >= 5 else 0.65,
                    uptime=1.0 / 4.0 )

    for character in [TingyunCharacter, LuochaCharacter]:
        character.addStat('ATK.percent',description='Roaring Bowstrings',
                        amount=0.88 if YukongCharacter.eidolon >= 3 else 0.80,
                        uptime=2.0 / 4.0 / 2.0) # 1 bowstrings, 2 characters, 4 turn rotation

    #%% Print Statements
    for character in team:
        character.print()

    #%% Lunae Tingyun Yukong Luocha Rotations
    TingyunRotation = [ 
            TingyunCharacter.useBasic() * 2, 
            TingyunCharacter.useSkill(),
            TingyunCharacter.useUltimate(),
    ]
        
    LunaeRotation = [  # 140 energy needed. EndTurn needed to factor in his buffs
                LunaeCharacter.useSkill()*3,
                LunaeCharacter.useEnhancedBasic3(), # -3 SP, 40 energy
                LunaeCharacter.endTurn(),
                LunaeCharacter.useSkill()*3,
                LunaeCharacter.useEnhancedBasic3(), # -3 SP, 40 energy
                LunaeCharacter.useUltimate(), # +2 SP, 5 energy
                TingyunCharacter.useBenediction(['basic','enhancedBasic']) * 2, # apply benedictions with buffs
                TingyunCharacter.useBenediction(['ultimate']) * 1,
                LunaeCharacter.endTurn(),
                TingyunCharacter.giveUltEnergy(),
    ]

    numBasicYukong = 2
    numSkillYukong = 2
    numUltYukong = 1
    YukongRotation = [ # 
                YukongCharacter.useEnhancedBasic() * numBasicYukong,
                YukongCharacter.useSkill() * numSkillYukong,
                YukongCharacter.useUltimate() * numUltYukong,
        ]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Lunae Tingyun Yukong Luocha Rotation Math
    totalLunaeEffect = sumEffects(LunaeRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalYukongEffect = sumEffects(YukongRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    LunaeRotationDuration = totalLunaeEffect.actionvalue * 100.0 / LunaeCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    YukongRotationDuration = totalYukongEffect.actionvalue * 100.0 / YukongCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's rotation
    TingyunRotation = [x * LunaeRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    YukongRotation = [x * LunaeRotationDuration / YukongRotationDuration for x in YukongRotation]
    LuochaRotation = [x * LunaeRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    LunaeEstimate = DefaultEstimator('Lunae: 2N^3 1Q', LunaeRotation, LunaeCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats',
                                    TingyunRotation, TingyunCharacter, config)
    YukongEstimate = DefaultEstimator(f'Yukong (Speed Tuned) {numBasicYukong:d}N {numSkillYukong:d}E {numUltYukong:d}Q S{YukongCharacter.lightcone.superposition:d} {YukongCharacter.lightcone.name}', 
                                    YukongRotation, YukongCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([LunaeEstimate,TingyunEstimate,YukongEstimate,LuochaEstimate])