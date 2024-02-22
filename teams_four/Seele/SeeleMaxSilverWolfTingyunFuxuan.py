from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Fuxuan import Fuxuan
from characters.harmony.Tingyun import Tingyun
from characters.hunt.Seele import Seele
from characters.nihility.SilverWolf import SilverWolf
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.GeniusOfBrilliantStars import GeniusOfBrilliantStars2pc, GeniusOfBrilliantStars4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def SeeleMaxSilverWolfTingyunFuxuan(config):
    #%% Seele MID Silver Wolf Tingyun Characters
    SeeleCharacter = Seele(relicstats = RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CD', 'DMG.quantum'],
                            substats = {'CR': 12, 'CD': 8, 'ATK.percent': 5, 'SPD.flat': 3}),
                            lightcone = CruisingInTheStellarSea(**config),
                            relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo=GeniusOfBrilliantStars4pc(), planarset = RutilantArena(),
                            **config)

    SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'BreakEffect'],
                            substats = {'SPD.flat':12,'BreakEffect':8, 'ATK.percent': 5, 'ATK.flat': 3}),
                            lightcone = BeforeTheTutorialMissionStarts(**config),
                            relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = PenaconyLandOfDreams(),
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                            benedictionTarget=SeeleCharacter,
                            **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                            substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                            lightcone = DayOneOfMyNewLife(**config),
                            relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                            **config)
    
    team = [SeeleCharacter, SilverWolfCharacter, TingyunCharacter, FuxuanCharacter]

    #%% Seele MID Silver Wolf Tingyun Team Buffs
        
    for character in [SilverWolfCharacter, SeeleCharacter, TingyunCharacter]:
        character.addStat('DMG.quantum',description='Penacony from Fuxuan',amount=0.1)
    for character in [SeeleCharacter, TingyunCharacter, FuxuanCharacter]:
        character.addStat('DMG.quantum',description='Penacony from Silver Wolf',amount=0.1)

    # Silver Wolf Debuffs
    # handle this separately for seele, assume it doesn't apply to her basics
    SilverWolfCharacter.applyDebuffs([SilverWolfCharacter, TingyunCharacter, FuxuanCharacter])

    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)

    # Tingyun Messenger Buff
    for character in [SeeleCharacter, SilverWolfCharacter, FuxuanCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(SeeleCharacter)
    TingyunCharacter.applyUltBuff(SeeleCharacter)
        
    #%% Print Statements
    for character in team:
        character.print()

    #%% Seele MAX Silver Wolf Bronya Luocha Rotations

    numBasic = 1.3
    numSkill = 1.3
    SeeleRotation = [ # endTurn needed to factor in resurgence buff
            SeeleCharacter.useBasic() * numBasic,
    ]

    SilverWolfCharacter.applyDebuffs([SeeleCharacter])
    SeeleRotation += [
            SeeleCharacter.useResurgence() * numSkill,
            SeeleCharacter.useSkill() * numSkill,
            SeeleCharacter.useUltimate(),
            SeeleCharacter.endTurn(),
            TingyunCharacter.useBenediction(['skill']) * numBasic, # apply benedictions with buffs
            TingyunCharacter.useBenediction(['skill']) * numSkill, # apply benedictions with buffs
            TingyunCharacter.useBenediction(['ultimate']) * 1,
            TingyunCharacter.giveUltEnergy() * TingyunCharacter.getTotalStat('SPD') / SeeleCharacter.getTotalStat('SPD') / 1.875

    ]

    numBasicSW = 0
    numSkillSW = 2
    numUltSW = 1
    SilverWolfRotation = [ # 
            SilverWolfCharacter.useBasic() * numBasicSW,
            SilverWolfCharacter.useSkill() * numSkillSW, #
            SilverWolfCharacter.useUltimate() * numUltSW, #
    ]

    TingyunRotation = [ 
            TingyunCharacter.useBasic() * 2, 
            TingyunCharacter.useSkill(),
            TingyunCharacter.useUltimate(),
    ]
    
    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% Seele MID Silver Wolf Tingyun Fuxuan Rotation Math

    totalSeeleEffect = sumEffects(SeeleRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalSilverWolfEffect = sumEffects(SilverWolfRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    SeeleRotationDuration = totalSeeleEffect.actionvalue * 100.0 / SeeleCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Seele: ',SeeleRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('SilverWolf: ',SilverWolfRotationDuration)
    print('Fuxuan: ',FuxuanRotationDuration)

    # Scale other character's rotation
    TingyunRotation = [x * SeeleRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    SilverWolfRotation = [x * SeeleRotationDuration / SilverWolfRotationDuration for x in SilverWolfRotation]
    FuxuanRotation = [x * SeeleRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    SeeleEstimate = DefaultEstimator(f'Seele Max Resurgence: {numBasic:.1f}N Resurgence({numSkill:.1f}E1Q)', SeeleRotation, SeeleCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats', 
                                    TingyunRotation, TingyunCharacter, config)
    SilverWolfEstimate = DefaultEstimator(f'SilverWolf {numBasicSW:.0f}N {numSkillSW:.0f}E {numUltSW:.0f}Q', SilverWolfRotation, SilverWolfCharacter, config)
    FuxuanEstimate = DefaultEstimator(f'Fuxuan: 2N 1E 1Q, S{FuxuanCharacter.lightcone.superposition:.0f} {FuxuanCharacter.lightcone.name}',
                                    FuxuanRotation, FuxuanCharacter, config)

    return([SeeleEstimate, SilverWolfEstimate, TingyunEstimate, FuxuanEstimate])