from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Fuxuan import Fuxuan
from characters.harmony.RuanMei import RuanMei
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

def SeeleMaxSilverWolfRuanMeiFuxuan(config):
    #%% Seele MID Silver Wolf RuanMei Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                        substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                        **config)
    
    SeeleCharacter = Seele(relicstats = RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CD', 'DMG.quantum'],
                            substats = {'CR': 12, 'CD': 8, 'ATK.percent': 5, 'SPD.flat': 3}),
                            lightcone = CruisingInTheStellarSea(**config),
                            relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo=GeniusOfBrilliantStars4pc(), planarset = RutilantArena(),
                            **config)

    SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'DMG.quantum'],
                            substats = {'SPD.flat':12,'BreakEffect':8, 'ATK.percent': 5, 'ATK.flat': 3}),
                            lightcone = BeforeTheTutorialMissionStarts(**config),
                            relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = PenaconyLandOfDreams(),
                            **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                            substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                            lightcone = DayOneOfMyNewLife(**config),
                            relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                            **config)
    
    team = [SeeleCharacter, SilverWolfCharacter, RuanMeiCharacter, FuxuanCharacter]

    #%% Seele MID Silver Wolf RuanMei Team Buffs
        
    for character in [SilverWolfCharacter, SeeleCharacter, RuanMeiCharacter]:
        character.addStat('DMG.quantum',description='Penacony from Fuxuan',amount=0.1)
    for character in [SeeleCharacter, RuanMeiCharacter, FuxuanCharacter]:
        character.addStat('DMG.quantum',description='Penacony from Silver Wolf',amount=0.1)

    # Silver Wolf Debuffs
    # handle this separately for seele, assume it doesn't apply to her basics
    SilverWolfCharacter.applyDebuffs([SilverWolfCharacter, RuanMeiCharacter, FuxuanCharacter])

    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)

    # RuanMei Buffs, max skill uptime
    RuanMeiCharacter.applyWeaknessModifiers(team=team)
    RuanMeiCharacter.applyPassiveBuffs(team=team)
    RuanMeiCharacter.applySkillBuff(team=team,uptime=3.0/3.0)
    RuanMeiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)
        
    #%% Print Statements
    for character in team:
        character.print()

    #%% Seele MAX Silver Wolf Bronya Luocha Rotations

    numBasic = 2.0
    numSkill = 2.0
    SeeleRotation = [ # endTurn needed to factor in resurgence buff
            SeeleCharacter.useBasic() * numBasic,
    ]

    SilverWolfCharacter.applyDebuffs([SeeleCharacter])
    SeeleRotation += [
            SeeleCharacter.useResurgence() * numSkill,
            SeeleCharacter.useSkill() * numSkill,
            SeeleCharacter.useUltimate(),
            SeeleCharacter.endTurn(),
    ]

    numBasicSW = 0
    numSkillSW = 2
    numUltSW = 1
    SilverWolfRotation = [ # 
            SilverWolfCharacter.useBasic() * numBasicSW,
            SilverWolfCharacter.useSkill() * numSkillSW, #
            SilverWolfCharacter.useUltimate() * numUltSW, #
    ]

    numBasicRuanMei = 2.0
    numSkillRuanMei = 1.0
    RuanMeiRotation = [RuanMeiCharacter.useBasic() * numBasicRuanMei,
                       RuanMeiCharacter.useSkill() * numSkillRuanMei,
                    RuanMeiCharacter.useUltimate()]
    
    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% Seele MID Silver Wolf RuanMei Fuxuan Rotation Math
    totalSeeleEffect = sumEffects(SeeleRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalSilverWolfEffect = sumEffects(SilverWolfRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    SeeleRotationDuration = totalSeeleEffect.actionvalue * 100.0 / SeeleCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Seele: ',SeeleRotationDuration)
    print('RuanMei: ',RuanMeiRotationDuration)
    print('SilverWolf: ',SilverWolfRotationDuration)
    print('Fuxuan: ',FuxuanRotationDuration)

    # Scale other character's rotation
    RuanMeiRotation = [x * SeeleRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    SilverWolfRotation = [x * SeeleRotationDuration / SilverWolfRotationDuration for x in SilverWolfRotation]
    FuxuanRotation = [x * SeeleRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    SeeleEstimate = DefaultEstimator(f'Seele Max Resurgence: {numBasic:.1f}N Resurgence({numSkill:.1f}E1Q)', SeeleRotation, SeeleCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'RuanMei {numSkillRuanMei:.1f}E {numBasicRuanMei:.1f}N S{RuanMeiCharacter.lightcone.superposition:.0f} {RuanMeiCharacter.lightcone.name}, 12 Spd Substats', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    SilverWolfEstimate = DefaultEstimator(f'SilverWolf {numBasicSW:.0f}N {numSkillSW:.0f}E {numUltSW:.0f}Q', SilverWolfRotation, SilverWolfCharacter, config)
    FuxuanEstimate = DefaultEstimator(f'Fuxuan: 2N 1E 1Q, S{FuxuanCharacter.lightcone.superposition:.0f} {FuxuanCharacter.lightcone.name}',
                                    FuxuanRotation, FuxuanCharacter, config)

    return([SeeleEstimate, SilverWolfEstimate, RuanMeiEstimate, FuxuanEstimate])