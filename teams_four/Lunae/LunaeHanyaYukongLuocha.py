from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Lunae import Lunae
from characters.harmony.Hanya import Hanya
from characters.harmony.Yukong import Yukong
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def LunaeHanyaYukongLuocha(config):
    #%% Lunae Hanya Yukong Luocha Characters
    LunaeCharacter = Lunae(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
                            substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                            lightcone = OnTheFallOfAnAeon(uptime=1.0,**config),
                            relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = WastelanderOfBanditryDesert4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                            substats = {'RES': 7, 'SPD.flat': 12, 'CD': 5, 'CR': 4}),
                            lightcone = DanceDanceDance(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                            **config)

    YukongCharacter = Yukong(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                            substats = {'CR': 7, 'CD': 12, 'SPD.flat': 6, 'RES': 3}),
                            lightcone = PlanetaryRendezvous(**config),
                            relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'RES': 3}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                                    **config)
    
    team = [LunaeCharacter, HanyaCharacter, YukongCharacter, LuochaCharacter]

    #%% Lunae Hanya Yukong Luocha Team Buffs
    # Broken Keel Buffs
    for character in [LunaeCharacter, YukongCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel from Hanya',amount=0.1)
    for character in [LunaeCharacter, HanyaCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel from Yukong',amount=0.1)
    for character in [LunaeCharacter, HanyaCharacter, YukongCharacter]:
        character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
        
    # Yukong imaginary damage trace
    for character in [LunaeCharacter, LuochaCharacter]:
        character.addStat('DMG',description='Yukong trace',amount=0.12,type=['imaginary'])

    # Yukong Planetary Rendezvous
    for character in [LunaeCharacter, LuochaCharacter]:
        character.addStat('DMG',description='Planetary Rendezvous',amount=0.09 + 0.03 * YukongCharacter.lightcone.superposition)

    # Hanya Messenger Buff
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)
    for character in [LunaeCharacter, YukongCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)

    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(LunaeCharacter,uptime=1.0)
    
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

    for character in [HanyaCharacter, LuochaCharacter]:
        character.addStat('ATK.percent',description='Roaring Bowstrings',
                        amount=0.88 if YukongCharacter.eidolon >= 3 else 0.80,
                        uptime=2.0 / 4.0 / 2.0) # 2 bowstrings, 2 characters, 4 turn rotation

    #%% Print Statements
    for character in team:
        character.print()

    #%% Lunae Hanya Yukong Luocha Rotations
    numHanyaSkill = 4
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]
        
    LunaeRotation = [  # 140 energy needed. EndTurn needed to factor in his buffs
                LunaeCharacter.useSkill()*3,
                LunaeCharacter.useEnhancedBasic3(), # -3 SP, 40 energy
                LunaeCharacter.endTurn(),
                LunaeCharacter.useSkill()*3,
                LunaeCharacter.useEnhancedBasic3(), # -3 SP, 40 energy
                LunaeCharacter.endTurn(),
                LunaeCharacter.useSkill()*3,
                LunaeCharacter.useEnhancedBasic3(), # -3 SP, 40 energy
                LunaeCharacter.useUltimate(), # +2 SP, 5 energy
                LunaeCharacter.endTurn(),
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

    #%% Lunae Hanya Yukong Luocha Rotation Math
    totalLunaeEffect = sumEffects(LunaeRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalYukongEffect = sumEffects(YukongRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    LunaeRotationDuration = totalLunaeEffect.actionvalue * 100.0 / LunaeCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    YukongRotationDuration = totalYukongEffect.actionvalue * 100.0 / YukongCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's rotation
    HanyaRotation = [x * LunaeRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    YukongRotation = [x * LunaeRotationDuration / YukongRotationDuration for x in YukongRotation]
    LuochaRotation = [x * LunaeRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()
    DanceDanceDanceEffect.actionvalue = -0.24 * LunaeRotationDuration / HanyaRotationDuration
    LunaeCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    LunaeRotation.append(DanceDanceDanceEffect)
    
    YukongCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    YukongRotation.append(DanceDanceDanceEffect)
    
    LuochaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    LuochaRotation.append(DanceDanceDanceEffect)
    
    HanyaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    HanyaRotation.append(DanceDanceDanceEffect)

    LunaeEstimate = DefaultEstimator('Lunae: 2N^3 1Q', LunaeRotation, LunaeCharacter, config)
    HanyaEstimate = DefaultEstimator('Hanya {:.0f}E {:.0f}Q S{:.0f} {}, 12 Spd Substats'.format(numHanyaSkill, numHanyaUlt,
                                    HanyaCharacter.lightcone.superposition, HanyaCharacter.lightcone.name), 
                                    HanyaRotation, HanyaCharacter, config)
    YukongEstimate = DefaultEstimator(f'Yukong (Speed Tuned) {numBasicYukong:d}N {numSkillYukong:d}E {numUltYukong:d}Q S{YukongCharacter.lightcone.superposition:d} {YukongCharacter.lightcone.name}', 
                                    YukongRotation, YukongCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([LunaeEstimate,HanyaEstimate,YukongEstimate,LuochaEstimate])