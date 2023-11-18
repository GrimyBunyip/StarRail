from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Jingliu import Jingliu
from characters.harmony.Bronya import Bronya
from characters.nihility.Pela import Pela
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc, HunterOfGlacialForest4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def JingliuBronyaPelaLuocha(config):
    #%% Jingliu Bronya Pela Luocha Characters
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

    PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                            substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
                            lightcone = ResolutionShinesAsPearlsOfSweat(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [JingliuCharacter, BronyaCharacter, PelaCharacter, LuochaCharacter]

    #%% Jingliu Bronya Pela Luocha Team Buffs
    # only enhanced skills have rutilant arena buff
    JingliuCharacter.addStat('DMG',description='Rutilant Arena', amount=0.20, type=['enhancedSkill']) # take care of rutilant arena manually

    # Broken Keel and Penacony Buff
    for character in [JingliuCharacter, BronyaCharacter, PelaCharacter]:
        character.addStat('CD',description='Broken Keel Luocha',amount=0.10)
    for character in [JingliuCharacter, PelaCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel Bronya',amount=0.10)
        
    for character in [JingliuCharacter, BronyaCharacter, LuochaCharacter]:
        character.addStat('DMG.ice',description='Penacony Pela',amount=0.10)

    # Messenger 4 pc
    for character in [JingliuCharacter, PelaCharacter, LuochaCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/5.0)

    # Pela Debuffs, 3 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotationDuration=3)
        
    # Resolution Shines as Pearls of Sweat uptime
    sweatUptime = (1.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
    sweatUptime += (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
    sweatUptime = min(1.0, sweatUptime)
    for character in team:
        character.addStat('DefShred',description='Resolution Sweat',
                        amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                        uptime=sweatUptime)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Jingliu Bronya Pela Luocha Rotations
    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    # Assume Bronya skill buff applies to skills, and only applies a fraction of the time to the remaining abilities
    numSkill = 2.0
    numEnhanced = 3.0
    numUlt = 1.0

    JingliuRotation = []

    # 1 skill should have bronya buff, 1 should not.
    JingliuRotation += [JingliuCharacter.useSkill()]
    BronyaCharacter.applySkillBuff(JingliuCharacter,uptime=1.0)
    JingliuCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition)
    JingliuRotation += [JingliuCharacter.useSkill()]
    JingliuCharacter.stats['DMG'].pop() # remove bronya skill buff
    JingliuCharacter.stats['DMG'].pop() # remove past and future

    # 2 enhanced skills will not have bronya buff
    JingliuRotation += [JingliuCharacter.useEnhancedSkill() * 2]

    # 1 enhanced skill and the ultimate will both have bronya buff
    BronyaCharacter.applySkillBuff(JingliuCharacter,uptime=1.0)
    BronyaCharacter.applyUltBuff(JingliuCharacter,uptime=0.5) # only get Bronya ult buff every other rotation
    JingliuCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition)
    JingliuRotation += [JingliuCharacter.useEnhancedSkill()]
    JingliuRotation += [JingliuCharacter.useUltimate()]
    JingliuRotation += [JingliuCharacter.extraTurn() * 0.9] # multiply by 0.9 because it tends to overlap with skill advances
    JingliuRotation += [BronyaCharacter.useAdvanceForward() * 2] #Jingliu rotation is basically 4 turns

    numBasicPela = 3.0
    PelaRotation = [PelaCharacter.useBasic() * numBasicPela,
                    PelaCharacter.useUltimate(),]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast

    #%% Jingliu Bronya Pela Luocha Rotation Math
    totalJingliuEffect = sumEffects(JingliuRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    JingliuRotationDuration = totalJingliuEffect.actionvalue * 100.0 / JingliuCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Jingliu: ',JingliuRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Pela: ',PelaRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # scale other character's rotation
    BronyaRotation = [x * JingliuRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    PelaRotation = [x * JingliuRotationDuration / PelaRotationDuration for x in PelaRotation]
    LuochaRotation = [x * JingliuRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    JingliuEstimate = DefaultEstimator('Jingliu {:.0f}E {:.0f}Moon {:.0f}Q'.format(numSkill, numEnhanced, numUlt),
                                                    JingliuRotation, JingliuCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    PelaEstimate = DefaultEstimator(f'Pela: {numBasicPela:.0f}N 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name),
                                    LuochaRotation, LuochaCharacter, config)

    return([JingliuEstimate, BronyaEstimate, PelaEstimate, LuochaEstimate])