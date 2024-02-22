from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.erudition.Qingque import Qingque
from characters.preservation.Fuxuan import Fuxuan
from characters.harmony.Hanabi import Hanabi
from characters.nihility.Pela import Pela
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.erudition.GeniusesRepose import GeniusesRepose
from lightCones.erudition.TheSeriousnessOfBreakfast import TheSeriousnessOfBreakfast
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.GeniusOfBrilliantStars import GeniusOfBrilliantStars2pc, GeniusOfBrilliantStars4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def QingqueHanabiPelaFuxuan(config):
    #%% Qingque Hanabi Pela Fuxuan Characters
    QingqueCharacter = Qingque(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.quantum'],
                        substats = {'CR': 12, 'CD': 8, 'ATK.percent': 5, 'BreakEffect': 3}),
                        lightcone = GeniusesRepose(**config),
                        relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo = GeniusOfBrilliantStars4pc(), planarset = RutilantArena(),
                        **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'SPD.flat', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'RES': 5, 'DEF.percent': 3}),
                        lightcone = PastAndFuture(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                        **config)

    PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                        substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
                        lightcone = BeforeTheTutorialMissionStarts(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
                        **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                        lightcone = DayOneOfMyNewLife(**config),
                        relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                        **config)
    
    team = [QingqueCharacter, HanabiCharacter, PelaCharacter, FuxuanCharacter]

    #%% Qingque Hanabi Pela Fuxuan Team Buffs
    # Broken Keel Buff
    for character in [QingqueCharacter, FuxuanCharacter, PelaCharacter]:
        character.addStat('DMG.quantum',description='Penacony Hanabi',amount=0.10)
    for character in [QingqueCharacter, HanabiCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel Pela',amount=0.10)
    for character in [QingqueCharacter, PelaCharacter, HanabiCharacter]:
        character.addStat('DMG.quantum',description='Penacony Fuxuan',amount=0.10)

    # Past and Future
    QingqueCharacter.addStat('DMG',description='Past and Future',amount=0.32)

    # Messenger 4 pc
    for character in [QingqueCharacter, PelaCharacter, FuxuanCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc Hanabi',amount=0.12,uptime=1.0/3.0)

    # Pela Debuffs, 2 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotationDuration=2)
        
    # Hanabi Buffs
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=QingqueCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)
    
    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Qingque Hanabi Pela Fuxuan Rotations
    numBasicHanabi = 0.0
    numSkillHanabi = 3.0
    HanabiRotation = [HanabiCharacter.useBasic() * numBasicHanabi,
                       HanabiCharacter.useSkill() * numSkillHanabi,
                    HanabiCharacter.useUltimate()]

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
        QingqueCharacter.useSkill(),
        QingqueCharacter.useSkill(),
        QingqueCharacter.useEnhancedBasic(), #except pela gives SP so no whiff, -2 and add more skll usages, this is usually skill usages here
        QingqueCharacter.drawTileFromAlly(),
        QingqueCharacter.useSkill(),
        QingqueCharacter.useUltimate(),
        QingqueCharacter.useEnhancedBasic(),
        QingqueCharacter.drawTileFromAlly(),
        HanabiCharacter.useAdvanceForward(advanceAmount=1.0 - QingqueCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')) * 5,
    ]

    numBasicPela = 2.0
    PelaRotation = [PelaCharacter.useBasic() * numBasicPela,
                    PelaCharacter.useUltimate(),]

    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% Qingque Hanabi Pela Fuxuan Rotation Math
    totalQingqueEffect = sumEffects(QingqueRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    QingqueRotationDuration = totalQingqueEffect.actionvalue * 100.0 / QingqueCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Qingque: ',QingqueRotationDuration)
    print('Hanabi: ',HanabiRotationDuration)
    print('Pela: ',PelaRotationDuration)
    print('Fuxuan: ',FuxuanRotationDuration)

    # scale other character's rotation
    HanabiRotation = [x * QingqueRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    PelaRotation = [x * QingqueRotationDuration / PelaRotationDuration for x in PelaRotation]
    FuxuanRotation = [x * QingqueRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    QingqueEstimate = DefaultEstimator('Qingque 14E 5Enh 1Q', QingqueRotation, QingqueCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    PelaEstimate = DefaultEstimator(f'Pela: {numBasicPela:.0f}N 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    FuxuanEstimate = DefaultEstimator('Fuxuan: 2N 1E 1Q, S{:.0f} {}'.format(FuxuanCharacter.lightcone.superposition, FuxuanCharacter.lightcone.name),
                                    FuxuanRotation, FuxuanCharacter, config)

    return([QingqueEstimate, HanabiEstimate, PelaEstimate, FuxuanEstimate])

