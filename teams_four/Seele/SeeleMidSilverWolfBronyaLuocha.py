from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.harmony.Bronya import Bronya
from characters.hunt.Seele import Seele
from characters.nihility.SilverWolf import SilverWolf
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.GeniusOfBrilliantStars import GeniusOfBrilliantStars2pc, GeniusOfBrilliantStars4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def SeeleMidSilverWolfBronyaLuocha(config):
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

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                            **config)
    
    team = [SeeleCharacter, SilverWolfCharacter, BronyaCharacter, LuochaCharacter]

    #%% Seele MID Silver Wolf Bronya Team Buffs

    # Silver Wolf Debuffs
    # handle this separately for seele, assume it doesn't apply to her basics
    SilverWolfCharacter.applyDebuffs([SilverWolfCharacter, BronyaCharacter, LuochaCharacter])

    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    BronyaCharacter.applyUltBuff(SeeleCharacter,uptime=1.0/4.0) # estimate 1 bronya buff per 4 rotations
    BronyaCharacter.applySkillBuff(SeeleCharacter,uptime=1.0/2.0) # estimate 1 bronya skill buff per 2 attacks
    
    SeeleCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition, uptime=0.5)
        
    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
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

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Seele MID Silver Wolf Bronya Luocha Rotation Math

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
    totalLuochaEffect = sumEffects(LuochaRotation)

    SeeleRotationDuration = totalSeeleEffect.actionvalue * 100.0 / SeeleCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Seele: ',SeeleRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('SilverWolf: ',SilverWolfRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # Scale other character's rotation
    BronyaRotation = [x * SeeleRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    SilverWolfRotation = [x * SeeleRotationDuration / SilverWolfRotationDuration for x in SilverWolfRotation]
    LuochaRotation = [x * SeeleRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    SeeleEstimate = DefaultEstimator('Seele Ult Resurgence: 2N 1Resurgence(2E1Q)', SeeleRotation, SeeleCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    SilverWolfEstimate = DefaultEstimator(f'SilverWolf {numBasicSW:.0f}N {numSkillSW:.0f}E {numUltSW:.0f}Q', SilverWolfRotation, SilverWolfCharacter, config)
    LuochaEstimate = DefaultEstimator(f'Luocha: 3N 1E 1Q, S{LuochaCharacter.lightcone.superposition:d} {LuochaCharacter.lightcone.name}', 
                                    LuochaRotation, LuochaCharacter, config)

    return([SeeleEstimate, SilverWolfEstimate, BronyaEstimate, LuochaEstimate])