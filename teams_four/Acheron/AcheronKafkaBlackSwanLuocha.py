from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.nihility.Acheron import Acheron
from characters.nihility.BlackSwan import BlackSwan
from characters.nihility.Kafka import Kafka
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.nihility.EyesOfThePrey import EyesOfThePrey
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.PatienceIsAllYouNeed import PatienceIsAllYouNeed
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.PanCosmicCommercialEnterprise import PanCosmicCommercialEnterprise
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc

def AcheronKafkaBlackSwanLuocha(config):
    #%% Acheron Kafka BlackSwan Luocha Characters
    AcheronCharacter = Acheron(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'ATK.percent'],
                            substats = {'CR': 10, 'CD': 10, 'ATK.percent': 5, 'SPD.flat': 3}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Pioneer2pc(), relicsettwo = Pioneer4pc(),
                            planarset = IzumoGenseiAndTakamaDivineRealm(),
                            **config)
    
    KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'BreakEffect': 5, 'ATK.flat': 3}),
                            lightcone = PatienceIsAllYouNeed(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    BlackSwanCharacter = BlackSwan(RelicStats(mainstats = ['EHR', 'SPD.flat', 'ATK.percent', 'DMG.wind'],
                            substats = {'ATK.percent': 12, 'SPD.flat': 8, 'EHR': 5, 'ATK.flat': 3}),
                            lightcone = EyesOfThePrey(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = PanCosmicCommercialEnterprise(),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                            **config)
    
    team = [AcheronCharacter, KafkaCharacter, BlackSwanCharacter, LuochaCharacter]

    #%% Acheron Kafka BlackSwan Luocha Team Buffs
    for character in [KafkaCharacter, AcheronCharacter, BlackSwanCharacter]:
        character.addStat('ATK.percent',description='Fleet from Luocha',amount=0.08)
    for character in [KafkaCharacter, AcheronCharacter, LuochaCharacter]:
        character.addStat('ATK.percent',description='Fleet from BlackSwan',amount=0.08)
        
    # Apply BlackSwan Vulnerability Debuff
    SwanUltRotation = 5.0
    BlackSwanCharacter.applySkillDebuff(team,rotationDuration=2.0)
    # BlackSwanCharacter.applyUltDebuff(team,rotationDuration=SwanUltRotation)
    # Epiphany does not apply to detonations, so bump this buff til after the rotation cone
        
    #%% Print Statements
    for character in team:
        character.print()

    #%% Acheron Kafka BlackSwan Luocha Rotations
    
    #
    percent_basics = 0.5
    numStacks = 1.0 * percent_basics # Assume Acheron generates 1 stack when she skills
    numStacks += (7/3) * KafkaCharacter.getTotalStat('SPD') / AcheronCharacter.getTotalStat('SPD') # 7 Kafka attacks per 3 turn rotation
    numStacks +=  (6/5) * BlackSwanCharacter.getTotalStat('SPD') / AcheronCharacter.getTotalStat('SPD') # 6 BlackSwan attacks per 5 turn rotation
    
    numSkillAcheron = 9.0 / numStacks
    numBasicAcheron = numSkillAcheron * percent_basics
    numSkillAcheron = numSkillAcheron * ( 1 - percent_basics )

    AcheronRotation = [ 
            AcheronCharacter.useBasic() * numBasicAcheron,
            AcheronCharacter.useSkill() * numSkillAcheron,
            AcheronCharacter.useUltimate_st() * 3,
            AcheronCharacter.useUltimate_aoe(num_stacks=3.0) * 3.0,
            AcheronCharacter.useUltimate_end(),
    ]
    
    numSkill = 3.0
    numTalent = 3.0
    numUlt = 1.0
    BlackSwanDot = BlackSwanCharacter.useDotDetonation()
    BlackSwanDot.energy = 0.0
    extraDots = []
    extraDotsUlt = [ BlackSwanDot * KafkaCharacter.numEnemies ]
    KafkaRotation = [
            KafkaCharacter.useSkill(extraDots=extraDots) * numSkill,
            KafkaCharacter.useTalent() * numTalent,
            KafkaCharacter.useUltimate(extraDots=extraDotsUlt) * numUlt,
    ]
    # Napkin Math for stacks applied
    
    numDots = 3
    adjacentStackRate = 2 * (BlackSwanCharacter.numEnemies - 1) / BlackSwanCharacter.numEnemies
    dotStackRate = numDots * KafkaCharacter.numEnemies
    
    # 3 turn kafka ult rotation, 3 single target + 3 aoe every 3 turns
    KafkaStackRate = (3 + 3 * KafkaCharacter.numEnemies / 3)
    
    # Swan alternates applying basic and skill stacks
    swanBasicStacks = 1 + numDots
    swanSkillStacks = (1 + numDots) * min(3.0,BlackSwanCharacter.numEnemies)
    
    SwanStackRate = (swanBasicStacks + swanSkillStacks) / 2
    
    netStackRate = adjacentStackRate * KafkaCharacter.enemySpeed
    netStackRate += dotStackRate * KafkaCharacter.enemySpeed
    netStackRate += KafkaStackRate * KafkaCharacter.getTotalStat('SPD')
    netStackRate += SwanStackRate * BlackSwanCharacter.getTotalStat('SPD')
    netStackRate = netStackRate / KafkaCharacter.enemySpeed / KafkaCharacter.numEnemies
    netStackRate *= 1.0 + 1.0 / SwanUltRotation # swan ult effectively applies 1 extra rotation of dots every N turns
    print(f'net Stack Rate per Enemy {netStackRate}')
    
    BlackSwanCharacter.setSacramentStacks(netStackRate)

    numBasicBlackSwan = SwanUltRotation / 2.0
    numSkillBlackSwan = SwanUltRotation / 2.0
    numUltBlackSwan = 1
    BlackSwanRotation = [
                    BlackSwanCharacter.useBasic() * numBasicBlackSwan,
                    BlackSwanCharacter.useSkill() * numSkillBlackSwan,
                    BlackSwanCharacter.useUltimate() * numUltBlackSwan]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Acheron Kafka BlackSwan Luocha Rotation Math
    numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
    numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)
    numDotBlackSwan = DotEstimator(BlackSwanRotation, BlackSwanCharacter, config, dotMode='alwaysAll')

    totalAcheronEffect = sumEffects(AcheronRotation)
    totalBlackSwanEffect = sumEffects(BlackSwanRotation)
    totalKafkaEffect = sumEffects(KafkaRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    AcheronRotationDuration = totalAcheronEffect.actionvalue * 100.0 / AcheronCharacter.getTotalStat('SPD')
    BlackSwanRotationDuration = totalBlackSwanEffect.actionvalue * 100.0 / BlackSwanCharacter.getTotalStat('SPD')
    KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Acheron: ',AcheronRotationDuration)
    print('BlackSwan: ',BlackSwanRotationDuration)
    print('Kafka: ',KafkaRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # Scale other character's rotation
    BlackSwanRotation = [x * AcheronRotationDuration / BlackSwanRotationDuration for x in BlackSwanRotation]
    KafkaRotation = [x * AcheronRotationDuration / KafkaRotationDuration for x in KafkaRotation]
    LuochaRotation = [x * AcheronRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    numDotBlackSwan *= KafkaRotationDuration / BlackSwanRotationDuration

    AcheronEstimate = DefaultEstimator(f'Acheron E{AcheronCharacter.eidolon:d} S{AcheronCharacter.lightcone.superposition:d} {AcheronCharacter.lightcone.name}: {numBasicAcheron:.1f}N {numSkillAcheron:.1f}E 1Q', AcheronRotation, AcheronCharacter, config)
    BlackSwanEstimate = DefaultEstimator(f'BlackSwan S{BlackSwanCharacter.lightcone.superposition:.0f} {BlackSwanCharacter.lightcone.name} {numBasicBlackSwan:.0f}N {numSkillBlackSwan:.0f}E {numUltBlackSwan:.0f}Q {numDotBlackSwan:.1f}Dot {BlackSwanCharacter.sacramentStacks:.1f}Sacrament', 
                                                                                                BlackSwanRotation, BlackSwanCharacter, config, numDot=numDotBlackSwan)
    KafkaEstimate = DefaultEstimator(f'Kafka {numSkill:.0f}E {numTalent:.0f}T {numUlt:.0f}Q {numDotKafka:.1f}Dot, {KafkaCharacter.lightcone.name} S{KafkaCharacter.lightcone.superposition}',
                                    KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
    LuochaEstimate = DefaultEstimator(f'Luocha: 3N 1E 1Q, S{LuochaCharacter.lightcone.superposition:d} {LuochaCharacter.lightcone.name}', 
                                    LuochaRotation, LuochaCharacter, config)

    return([AcheronEstimate, BlackSwanEstimate, KafkaEstimate, LuochaEstimate])