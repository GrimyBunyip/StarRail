from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.erudition.Qingque import Qingque
from characters.preservation.Fuxuan import Fuxuan
from characters.harmony.Hanya import Hanya
from characters.nihility.SilverWolf import SilverWolf
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.erudition.TheSeriousnessOfBreakfast import TheSeriousnessOfBreakfast
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.GeniusOfBrilliantStars import GeniusOfBrilliantStars2pc, GeniusOfBrilliantStars4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def QingqueHanyaSilverWolfFuxuan(config):
    #%% Qingque Hanya SilverWolf Fuxuan Characters
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

    SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'BreakEffect'],
                        substats = {'SPD.flat':12,'BreakEffect':8, 'ATK.percent': 5, 'ATK.flat': 3}),
                        lightcone = BeforeTheTutorialMissionStarts(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = PenaconyLandOfDreams(),
                        **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                        lightcone = DayOneOfMyNewLife(**config),
                        relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                        **config)
    
    team = [QingqueCharacter, HanyaCharacter, SilverWolfCharacter, FuxuanCharacter]

    #%% Qingque Hanya SilverWolf Fuxuan Team Buffs
    # Broken Keel Buff
    for character in [QingqueCharacter, FuxuanCharacter, SilverWolfCharacter]:
        character.addStat('CD',description='Broken Keel Hanya',amount=0.10)
    for character in [QingqueCharacter, HanyaCharacter, FuxuanCharacter]:
        character.addStat('DMG.quantum',description='Penacony SilverWolf',amount=0.10)
    for character in [QingqueCharacter, SilverWolfCharacter, HanyaCharacter]:
        character.addStat('DMG.quantum',description='Penacony Fuxuan',amount=0.10)

    # Messenger 4 pc
    for character in [QingqueCharacter, SilverWolfCharacter, FuxuanCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)

    # Silver Wolf Debuffs
    SilverWolfCharacter.applyDebuffs([SilverWolfCharacter, HanyaCharacter],targetingUptime=1.0) 
    SilverWolfCharacter.applyDebuffs([QingqueCharacter, FuxuanCharacter],targetingUptime=1.0/QingqueCharacter.numEnemies) 
        
    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(QingqueCharacter,uptime=1.0)
    
    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Qingque Hanya SilverWolf Fuxuan Rotations
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

    numBasicSW = 1
    numSkillSW = 1
    numUltSW = 1
    SilverWolfRotation = [ # 
            SilverWolfCharacter.useBasic() * numBasicSW,
            SilverWolfCharacter.useSkill() * numSkillSW, #
            SilverWolfCharacter.useUltimate() * numUltSW, #
    ]

    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% Qingque Hanya SilverWolf Fuxuan Rotation Math
    totalQingqueEffect = sumEffects(QingqueRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalSilverWolfEffect = sumEffects(SilverWolfRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    QingqueRotationDuration = totalQingqueEffect.actionvalue * 100.0 / QingqueCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Qingque: ',QingqueRotationDuration)
    print('Hanya: ',HanyaRotationDuration)
    print('SilverWolf: ',SilverWolfRotationDuration)
    print('Fuxuan: ',FuxuanRotationDuration)

    # scale other character's rotation
    HanyaRotation = [x * QingqueRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    SilverWolfRotation = [x * QingqueRotationDuration / SilverWolfRotationDuration for x in SilverWolfRotation]
    FuxuanRotation = [x * QingqueRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    QingqueEstimate = DefaultEstimator('Qingque 12E 4Enh 1N 1Q', QingqueRotation, QingqueCharacter, config)
    HanyaEstimate = DefaultEstimator(f'Hanya: {numHanyaSkill:.0f}E {numHanyaUlt:.0f}Q S{HanyaCharacter.lightcone.superposition:.0f} {HanyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanyaRotation, HanyaCharacter, config)
    SilverWolfEstimate = DefaultEstimator(f'SilverWolf {numBasicSW:.0f}N {numSkillSW:.0f}E {numUltSW:.0f}Q', SilverWolfRotation, SilverWolfCharacter, config)
    FuxuanEstimate = DefaultEstimator(f'Fuxuan: 2N 1E 1Q, S{FuxuanCharacter.lightcone.superposition:.0f} {FuxuanCharacter.lightcone.name}',
                                    FuxuanRotation, FuxuanCharacter, config)

    return([QingqueEstimate, HanyaEstimate, SilverWolfEstimate, FuxuanEstimate])

