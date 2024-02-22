from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.nihility.Acheron import Acheron
from characters.nihility.Pela import Pela
from characters.nihility.Kafka import Kafka
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.PatienceIsAllYouNeed import PatienceIsAllYouNeed
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.BandOfSizzlingThunder import BandOfSizzlingThunder2pc, BandOfSizzlingThunder4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def AcheronKafkaPelaLuocha(config):
    #%% Acheron Kafka Pela Luocha Characters
    AcheronCharacter = Acheron(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'ATK.percent'],
                            substats = {'CR': 10, 'CD': 10, 'ATK.percent': 5, 'SPD.flat': 3}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Pioneer2pc(), relicsettwo = Pioneer4pc(),
                            planarset = IzumoGenseiAndTakamaDivineRealm(),
                            **config)
    
    KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'BreakEffect': 5, 'ATK.flat': 3}),
                            lightcone = PatienceIsAllYouNeed(**config),
                            relicsetone = BandOfSizzlingThunder2pc(), relicsettwo = BandOfSizzlingThunder4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                            substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
                            lightcone = ResolutionShinesAsPearlsOfSweat(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = FleetOfTheAgeless(),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                            **config)
    
    team = [AcheronCharacter, KafkaCharacter, PelaCharacter, LuochaCharacter]

    #%% Acheron Kafka Pela Luocha Team Buffs
    for character in [KafkaCharacter, AcheronCharacter, PelaCharacter]:
        character.addStat('ATK.percent',description='Fleet from Luocha',amount=0.08)
    for character in [KafkaCharacter, AcheronCharacter, LuochaCharacter]:
        character.addStat('ATK.percent',description='Fleet from Pela',amount=0.08)

    # Pela Debuffs, 3 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotationDuration=3)
        
    # Resolution Shines as Pearls of Sweat uptime
    sweatUptime = (1.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
    sweatUptime += (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
    sweatUptime = min(1.0, sweatUptime)
    for character in [AcheronCharacter, KafkaCharacter, PelaCharacter, LuochaCharacter]:
        character.addStat('DefShred',description='Resolution Sweat',
                        amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                        uptime=sweatUptime)
        
    #%% Print Statements
    for character in team:
        character.print()

    #%% Acheron Kafka Pela Luocha Rotations
    
    numStacks = 1 # Assume Acheron generates 1 stack when she skills
    numStacks += (7 / 3) * KafkaCharacter.getTotalStat('SPD') / AcheronCharacter.getTotalStat('SPD') # 7 Kafka attacks per 3 turn wolf rotation
    numStacks +=  (4 / 3) * PelaCharacter.getTotalStat('SPD') / AcheronCharacter.getTotalStat('SPD') # 4 pela attacks per 3 turn wolf rotation
    
    numSkillAcheron = 9.0 / numStacks

    AcheronRotation = [ 
            AcheronCharacter.useSkill() * numSkillAcheron,
            AcheronCharacter.useUltimate_st() * 3,
            AcheronCharacter.useUltimate_aoe(num_stacks=3.0) * 3.0,
            AcheronCharacter.useUltimate_end(),
    ]
    
    numSkill = 3.0
    numTalent = 3.0
    numUlt = 1.0
    extraDots = []
    extraDotsUlt = []
    KafkaRotation = [
            KafkaCharacter.useSkill(extraDots=extraDots) * numSkill,
            KafkaCharacter.useTalent() * numTalent,
            KafkaCharacter.useUltimate(extraDots=extraDotsUlt) * numUlt,
    ]

    numBasicPela = 3.0
    PelaRotation = [PelaCharacter.useBasic() * numBasicPela,
                    PelaCharacter.useUltimate(),]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Acheron Kafka Pela Luocha Rotation Math
    numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
    numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)

    totalAcheronEffect = sumEffects(AcheronRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalKafkaEffect = sumEffects(KafkaRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    AcheronRotationDuration = totalAcheronEffect.actionvalue * 100.0 / AcheronCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Acheron: ',AcheronRotationDuration)
    print('Pela: ',PelaRotationDuration)
    print('Kafka: ',KafkaRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # Scale other character's rotation
    PelaRotation = [x * AcheronRotationDuration / PelaRotationDuration for x in PelaRotation]
    KafkaRotation = [x * AcheronRotationDuration / KafkaRotationDuration for x in KafkaRotation]
    LuochaRotation = [x * AcheronRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    AcheronEstimate = DefaultEstimator(f'Acheron E{AcheronCharacter.eidolon:d} S{AcheronCharacter.lightcone.superposition:d} {AcheronCharacter.lightcone.name}: {numSkillAcheron:.1f}E 1Q', AcheronRotation, AcheronCharacter, config)
    PelaEstimate = DefaultEstimator(f'Pela: 3N 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    KafkaEstimate = DefaultEstimator(f'Kafka {numSkill:.0f}E {numTalent:.0f}T {numUlt:.0f}Q {numDotKafka:.1f}Dot, {KafkaCharacter.lightcone.name} S{KafkaCharacter.lightcone.superposition}',
                                    KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
    LuochaEstimate = DefaultEstimator(f'Luocha: 3N 1E 1Q, S{LuochaCharacter.lightcone.superposition:d} {LuochaCharacter.lightcone.name}', 
                                    LuochaRotation, LuochaCharacter, config)

    return([AcheronEstimate, PelaEstimate, KafkaEstimate, LuochaEstimate])