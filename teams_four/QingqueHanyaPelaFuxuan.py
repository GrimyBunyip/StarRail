from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.erudition.Qingque import Qingque
from characters.preservation.Fuxuan import Fuxuan
from characters.harmony.Hanya import Hanya
from characters.nihility.Pela import Pela
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.erudition.TheSeriousnessOfBreakfast import TheSeriousnessOfBreakfast
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.GeniusOfBrilliantStars import GeniusOfBrilliantStars2pc, GeniusOfBrilliantStars4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc

def QingqueHanyaPelaFuxuan(config):
    #%% Qingque Hanya Pela Fuxuan Characters
    QingqueCharacter = Qingque(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.quantum'],
                        substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                        lightcone = TheSeriousnessOfBreakfast(**config),
                        relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo = GeniusOfBrilliantStars4pc(), planarset = RutilantArena(),
                        **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                        substats = {'CR': 8, 'SPD.flat': 12, 'CD': 5, 'ATK.percent': 3}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

    PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                        substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
                        lightcone = ResolutionShinesAsPearlsOfSweat(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
                        **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                        lightcone = DayOneOfMyNewLife(**config),
                        relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                        **config)
    
    team = [QingqueCharacter, HanyaCharacter, PelaCharacter, FuxuanCharacter]

    #%% Qingque Hanya Pela Fuxuan Team Buffs
    # Broken Keel Buff
    for character in [QingqueCharacter, FuxuanCharacter, PelaCharacter]:
        character.addStat('CD',description='Broken Keel Hanya',amount=0.10)
    for character in [QingqueCharacter, HanyaCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel Pela',amount=0.10)
    for character in [QingqueCharacter, PelaCharacter, HanyaCharacter]:
        character.addStat('DMG.quantum',description='Penacony Fuxuan',amount=0.10)

    # Messenger 4 pc
    for character in [QingqueCharacter, PelaCharacter, FuxuanCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)

    # Pela Debuffs, 2 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotationDuration=3)
        
    # Resolution Shines as Pearls of Sweat uptime
    sweatUptime = (1.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
    sweatUptime += (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
    sweatUptime = min(1.0, sweatUptime)
    for character in [QingqueCharacter,HanyaCharacter,PelaCharacter,FuxuanCharacter]:
        character.addStat('DefShred',description='Resolution Sweat',
                        amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                        uptime=sweatUptime)
        
    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(QingqueCharacter,uptime=1.0)
    
    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Qingque Hanya Pela Fuxuan Rotations
    numHanyaSkill = 3
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]

    QingqueRotation = [ # expect 2.3 SP used per basic, estimating with 1 2 2 3 4 split. Assume 1 whiff
        QingqueCharacter.useSkill(),
        QingqueCharacter.useSkill(),
        QingqueCharacter.useSkill(),
        QingqueCharacter.useSkill(),
        QingqueCharacter.useEnhancedBasic(),
        QingqueCharacter.drawTileFromAlly(),
        QingqueCharacter.useSkill(),
        QingqueCharacter.useSkill(),
        QingqueCharacter.useSkill(),
        QingqueCharacter.useEnhancedBasic(),
        QingqueCharacter.drawTileFromAlly(),
        QingqueCharacter.useSkill(), 
        QingqueCharacter.useSkill(),
        QingqueCharacter.useEnhancedBasic(),
        QingqueCharacter.useSkill(),
        QingqueCharacter.useSkill(),
        QingqueCharacter.useBasic(),
        QingqueCharacter.drawTileFromAlly(),
        QingqueCharacter.useSkill(),
        QingqueCharacter.useUltimate(),
        QingqueCharacter.useEnhancedBasic(),
        QingqueCharacter.drawTileFromAlly(),
    ]

    numBasicPela = 3.0
    PelaRotation = [PelaCharacter.useBasic() * numBasicPela,
                    PelaCharacter.useUltimate(),]

    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% Qingque Hanya Pela Fuxuan Rotation Math
    totalQingqueEffect = sumEffects(QingqueRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    QingqueRotationDuration = totalQingqueEffect.actionvalue * 100.0 / QingqueCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Qingque: ',QingqueRotationDuration)
    print('Hanya: ',HanyaRotationDuration)
    print('Pela: ',PelaRotationDuration)
    print('Fuxuan: ',FuxuanRotationDuration)

    # scale other character's rotation
    HanyaRotation = [x * QingqueRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    PelaRotation = [x * QingqueRotationDuration / PelaRotationDuration for x in PelaRotation]
    FuxuanRotation = [x * QingqueRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    QingqueEstimate = DefaultEstimator('Qingque 12E 4Enh 1N 1Q', QingqueRotation, QingqueCharacter, config)
    HanyaEstimate = DefaultEstimator(f'Hanya: {numHanyaSkill:.0f}E {numHanyaUlt:.0f}Q S{HanyaCharacter.lightcone.superposition:.0f} {HanyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanyaRotation, HanyaCharacter, config)
    PelaEstimate = DefaultEstimator(f'Pela: {numBasicPela:.0f}N 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    FuxuanEstimate = DefaultEstimator('Fuxuan: 2N 1E 1Q, S{:.0f} {}'.format(FuxuanCharacter.lightcone.superposition, FuxuanCharacter.lightcone.name),
                                    FuxuanRotation, FuxuanCharacter, config)

    return([QingqueEstimate, HanyaEstimate, PelaEstimate, FuxuanEstimate])

