from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Fuxuan import Fuxuan
from characters.harmony.Bronya import Bronya
from characters.hunt.Seele import Seele
from characters.nihility.SilverWolf import SilverWolf
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
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

def SeeleMidSilverWolfBronyaFuxuan(config):
    #%% Seele MID Silver Wolf Bronya Characters
    SeeleCharacter = Seele(relicstats = RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.quantum'],
                            substats = {'CD': 12, 'CR': 8, 'ATK.percent': 5, 'SPD.flat': 3}),
                            lightcone = CruisingInTheStellarSea(**config),
                            relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo=GeniusOfBrilliantStars4pc(), planarset = RutilantArena(),
                            **config)

    SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'DMG.quantum'],
                            substats = {'SPD.flat':12,'BreakEffect':8, 'ATK.percent': 5, 'ATK.flat': 3}),
                            lightcone = BeforeTheTutorialMissionStarts(**config),
                            relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = PenaconyLandOfDreams(),
                            **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'ER'],
                            substats = {'CD': 12, 'SPD.flat': 8, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = PastAndFuture(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                            **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                            substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                            lightcone = DayOneOfMyNewLife(**config),
                            relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                            **config)
    
    team = [SeeleCharacter, SilverWolfCharacter, BronyaCharacter, FuxuanCharacter]

    #%% Seele MID Silver Wolf Bronya Team Buffs
        
    for character in [SilverWolfCharacter, SeeleCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel from Bronya',amount=0.1)

    for character in [SilverWolfCharacter, SeeleCharacter, BronyaCharacter]:
        character.addStat('DMG.quantum',description='Penacony from Fuxuan',amount=0.1)
    for character in [SeeleCharacter, BronyaCharacter, FuxuanCharacter]:
        character.addStat('DMG.quantum',description='Penacony from Silver Wolf',amount=0.1)

    # Silver Wolf Debuffs
    # handle this separately for seele, assume it doesn't apply to her basics
    SilverWolfCharacter.applyDebuffs([SilverWolfCharacter, BronyaCharacter, FuxuanCharacter])

    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)

    # Bronya Messenger Buff
    for character in [SeeleCharacter, SilverWolfCharacter, FuxuanCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)

    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    BronyaCharacter.applyUltBuff(SeeleCharacter,uptime=1.0/4.0) # estimate 1 bronya buff per 4 rotations
    BronyaCharacter.applySkillBuff(SeeleCharacter,uptime=1.0/2.0) # estimate 1 bronya skill buff per 2 attacks
    
    SeeleCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition, uptime=0.5)
        
    #%% Print Statements
    for character in team:
        character.print()

    #%% Seele MID Silver Wolf Bronya Rotations

    SeeleRotation = [ # endTurn needed to factor in resurgence buff
            SeeleCharacter.useBasic(),
            SeeleCharacter.useUltimate(), # use ult to trigger resurgence, on an enemy that isn't debuffed yet
    ]

    SilverWolfCharacter.applyDebuffs([SeeleCharacter])
    SeeleRotation += [ # endTurn needed to factor in resurgence buff
        SeeleCharacter.useBasic() * 1,
        SeeleCharacter.useResurgence(),
        SeeleCharacter.useSkill() * 2,
        SeeleCharacter.endTurn(),
        BronyaCharacter.useAdvanceForward() * 1.1, # minus 0.4, to ignore the two advance forwards from basics
    ]

    numBasicSW = 2
    numSkillSW = 1
    numUltSW = 1
    SilverWolfRotation = [ # 
            SilverWolfCharacter.useBasic() * numBasicSW,
            SilverWolfCharacter.useSkill() * numSkillSW, #
            SilverWolfCharacter.useUltimate() * numUltSW, #
    ]

    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]
    
    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% Seele MID Silver Wolf Bronya Fuxuan Rotation Math

    #Seele is too fast for slow bronya. And we don't have enough SP to go faster
    totalSeeleEffect = sumEffects(SeeleRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    SeeleRotationDuration = totalSeeleEffect.actionvalue * 100.0 / SeeleCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    for effect in SeeleRotation:
        effect.actionvalue *= (BronyaRotationDuration / 4) / (SeeleRotationDuration / 1.5 )

    totalSeeleEffect = sumEffects(SeeleRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalSilverWolfEffect = sumEffects(SilverWolfRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    SeeleRotationDuration = totalSeeleEffect.actionvalue * 100.0 / SeeleCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Seele: ',SeeleRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('SilverWolf: ',SilverWolfRotationDuration)
    print('Fuxuan: ',FuxuanRotationDuration)

    # Scale other character's rotation
    BronyaRotation = [x * SeeleRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    SilverWolfRotation = [x * SeeleRotationDuration / SilverWolfRotationDuration for x in SilverWolfRotation]
    FuxuanRotation = [x * SeeleRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    SeeleEstimate = DefaultEstimator('Seele Ult Resurgence: 2N 1Resurgence(2E1Q)', SeeleRotation, SeeleCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    SilverWolfEstimate = DefaultEstimator(f'SilverWolf {numBasicSW:.0f}N {numSkillSW:.0f}E {numUltSW:.0f}Q', SilverWolfRotation, SilverWolfCharacter, config)
    FuxuanEstimate = DefaultEstimator(f'Fuxuan: 2N 1E 1Q, S{FuxuanCharacter.lightcone.superposition:.0f} {FuxuanCharacter.lightcone.name}',
                                    FuxuanRotation, FuxuanCharacter, config)

    return([SeeleEstimate, SilverWolfEstimate, BronyaEstimate, FuxuanEstimate])