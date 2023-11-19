from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Lunae import Lunae
from characters.harmony.Yukong import Yukong
from characters.nihility.Pela import Pela
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def LunaePelaYukongLuocha(config):
    #%% Lunae Pela Yukong Luocha Characters
    LunaeCharacter = Lunae(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.imaginary'],
                            substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                            lightcone = OnTheFallOfAnAeon(**config),
                            relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = WastelanderOfBanditryDesert4pc(), planarset = RutilantArena(),
                            **config)

    PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                            substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
                            lightcone = ResolutionShinesAsPearlsOfSweat(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
                            **config)

    YukongCharacter = Yukong(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                            substats = {'CR': 7, 'CD': 12, 'SPD.flat': 6, 'RES': 3}),
                            lightcone = PlanetaryRendezvous(**config),
                            relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'RES': 3}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                                    **config)
    
    team = [LunaeCharacter, PelaCharacter, YukongCharacter, LuochaCharacter]

    #%% Lunae Pela Yukong Luocha Team Buffs
    # Broken Keel Buffs
    for character in [LunaeCharacter, YukongCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel from Pela',amount=0.1)
        
    # Penacony Buff
    for character in [LunaeCharacter, PelaCharacter, LuochaCharacter]:
        character.addStat('DMG.imaginary',description='Penacony from Yukong',amount=0.1)
    for character in [LunaeCharacter, PelaCharacter, YukongCharacter]:
        character.addStat('DMG.imaginary',description='Penacony from Luocha',amount=0.1)
        
    # Pela Debuffs, 3 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotationDuration=3)
        
    # Resolution Shines as Pearls of Sweat uptime
    sweatUptime = (1.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
    sweatUptime += (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
    sweatUptime = min(1.0, sweatUptime)
    for character in [LunaeCharacter,YukongCharacter,PelaCharacter,LuochaCharacter]:
        character.addStat('DefShred',description='Resolution Sweat',
                        amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                        uptime=sweatUptime)
        
    # Yukong imaginary damage trace
    for character in [LunaeCharacter, LuochaCharacter]:
        character.addStat('DMG',description='Yukong trace',amount=0.12,type=['imaginary'])

    # Yukong Planetary Rendezvous
    for character in [LunaeCharacter, LuochaCharacter]:
        character.addStat('DMG',description='Planetary Rendezvous',amount=0.09 + 0.03 * YukongCharacter.lightcone.superposition)

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

    for character in [PelaCharacter, LuochaCharacter]:
        character.addStat('ATK.percent',description='Roaring Bowstrings',
                        amount=0.88 if YukongCharacter.eidolon >= 3 else 0.80,
                        uptime=2.0 / 4.0 / 2.0) # 2 bowstrings, 2 characters, 4 turn rotation

    #%% Print Statements
    for character in team:
        character.print()

    #%% Lunae Pela Yukong Luocha Rotations
    numBasicPela = 3.0
    PelaRotation = [PelaCharacter.useBasic() * numBasicPela,
                    PelaCharacter.useUltimate(),]

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

    #%% Lunae Pela Yukong Luocha Rotation Math
    totalLunaeEffect = sumEffects(LunaeRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalYukongEffect = sumEffects(YukongRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    LunaeRotationDuration = totalLunaeEffect.actionvalue * 100.0 / LunaeCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    YukongRotationDuration = totalYukongEffect.actionvalue * 100.0 / YukongCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's rotation
    PelaRotation = [x * LunaeRotationDuration / PelaRotationDuration for x in PelaRotation]
    YukongRotation = [x * LunaeRotationDuration / YukongRotationDuration for x in YukongRotation]
    LuochaRotation = [x * LunaeRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    LunaeEstimate = DefaultEstimator('Lunae: 2N^3 1Q', LunaeRotation, LunaeCharacter, config)
    PelaEstimate = DefaultEstimator(f'Pela: {numBasicPela:.0f}N 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    YukongEstimate = DefaultEstimator(f'Yukong (Speed Tuned) {numBasicYukong:d}N {numSkillYukong:d}E {numUltYukong:d}Q S{YukongCharacter.lightcone.superposition:d} {YukongCharacter.lightcone.name}', 
                                    YukongRotation, YukongCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([LunaeEstimate,PelaEstimate,YukongEstimate,LuochaEstimate])