from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.erudition.Qingque import Qingque
from characters.abundance.Luocha import Luocha
from characters.harmony.Hanabi import Hanabi
from characters.nihility.SilverWolf import SilverWolf
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.erudition.TheSeriousnessOfBreakfast import TheSeriousnessOfBreakfast
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
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

def QingqueHanabiSilverWolfLuocha(config):
    #%% Qingque Hanabi SilverWolf Luocha Characters
    QingqueCharacter = Qingque(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.quantum'],
                        substats = {'CR': 12, 'CD': 8, 'ATK.percent': 5, 'SPD.flat': 3}),
                        lightcone = TheSeriousnessOfBreakfast(**config),
                        relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo = GeniusOfBrilliantStars4pc(), planarset = RutilantArena(),
                        **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'DEF.percent', 'ER'],
                        substats = {'RES': 8, 'CD': 12, 'HP.percent': 5, 'SPD.flat': 3}),
                        lightcone = PlanetaryRendezvous(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                        **config)

    SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'BreakEffect'],
                        substats = {'SPD.flat':12,'BreakEffect':8, 'ATK.percent': 5, 'ATK.flat': 3}),
                        lightcone = BeforeTheTutorialMissionStarts(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = PenaconyLandOfDreams(),
                        **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [QingqueCharacter, HanabiCharacter, SilverWolfCharacter, LuochaCharacter]

    #%% Qingque Hanabi SilverWolf Luocha Team Buffs
    # Broken Keel Buff
    for character in [QingqueCharacter, LuochaCharacter, SilverWolfCharacter]:
        character.addStat('DMG.quantum',description='Penacony Hanabi',amount=0.10)
    for character in [QingqueCharacter, HanabiCharacter, LuochaCharacter]:
        character.addStat('DMG.quantum',description='Penacony SilverWolf',amount=0.10)
    for character in [QingqueCharacter, SilverWolfCharacter, HanabiCharacter]:
        character.addStat('CD',description='Broken Keel Luocha',amount=0.10)
    for character in team:
        character.addStat('DMG.quantum',description='Planetary Rendezvous',amount=0.24)

    # Messenger 4 pc
    for character in [QingqueCharacter, SilverWolfCharacter, LuochaCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc Hanabi',amount=0.12,uptime=1.0/3.0)

    # Silver Wolf Debuffs
    SilverWolfCharacter.applyDebuffs([SilverWolfCharacter, HanabiCharacter],targetingUptime=1.0) 
    SilverWolfCharacter.applyDebuffs([QingqueCharacter, LuochaCharacter],targetingUptime=1.0/QingqueCharacter.numEnemies) 
        
    # Hanabi Buffs
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=QingqueCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Qingque Hanabi SilverWolf Luocha Rotations
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
        QingqueCharacter.useBasic(),
        QingqueCharacter.drawTileFromAlly(),
        QingqueCharacter.useSkill(),
        QingqueCharacter.useUltimate(),
        QingqueCharacter.useEnhancedBasic(),
        QingqueCharacter.drawTileFromAlly(),
        HanabiCharacter.useAdvanceForward() * 5 * 2 / 3,
    ]

    numBasicSW = 1
    numSkillSW = 1
    numUltSW = 1
    SilverWolfRotation = [ # 
            SilverWolfCharacter.useBasic() * numBasicSW,
            SilverWolfCharacter.useSkill() * numSkillSW, #
            SilverWolfCharacter.useUltimate() * numUltSW, #
    ]
        
    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Qingque Hanabi SilverWolf Luocha Rotation Math
    totalQingqueEffect = sumEffects(QingqueRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalSilverWolfEffect = sumEffects(SilverWolfRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    QingqueRotationDuration = totalQingqueEffect.actionvalue * 100.0 / QingqueCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Qingque: ',QingqueRotationDuration)
    print('Hanabi: ',HanabiRotationDuration)
    print('SilverWolf: ',SilverWolfRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # scale other character's rotation
    HanabiRotation = [x * QingqueRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    SilverWolfRotation = [x * QingqueRotationDuration / SilverWolfRotationDuration for x in SilverWolfRotation]
    LuochaRotation = [x * QingqueRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    QingqueEstimate = DefaultEstimator('Qingque 12E 4Enh 1N 1Q', QingqueRotation, QingqueCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    SilverWolfEstimate = DefaultEstimator(f'SilverWolf {numBasicSW:.0f}N {numSkillSW:.0f}E {numUltSW:.0f}Q', SilverWolfRotation, SilverWolfCharacter, config)
    LuochaEstimate = DefaultEstimator(f'Luocha: 2N 1E 1Q, S{LuochaCharacter.lightcone.superposition:.0f} {LuochaCharacter.lightcone.name}',
                                    LuochaRotation, LuochaCharacter, config)

    return([QingqueEstimate, HanabiEstimate, SilverWolfEstimate, LuochaEstimate])

