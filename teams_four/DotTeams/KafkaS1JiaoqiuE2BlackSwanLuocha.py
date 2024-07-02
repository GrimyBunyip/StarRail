from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.nihility.Jiaoqiu import Jiaoqiu
from characters.nihility.Kafka import Kafka
from characters.nihility.BlackSwan import BlackSwan
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.nihility.EyesOfThePrey import EyesOfThePrey
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.PatienceIsAllYouNeed import PatienceIsAllYouNeed
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.PanCosmicCommercialEnterprise import PanCosmicCommercialEnterprise
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc

def KafkaS1JiaoqiuE2BlackSwanLuocha(config):
    #%% Kafka Jiaoqiu BlackSwan Luocha
    KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'BreakEffect': 5, 'ATK.flat': 3}),
                            lightcone = PatienceIsAllYouNeed(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=1),
                            **config)

    originalFivestarEidolons = config['fivestarEidolons']
    config['fivestarEidolons'] = 2
    JiaoqiuCharacter = Jiaoqiu(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.flat': 3, 'EHR': 5, 'ATK.percent': 12, 'SPD.flat': 8}),
                            lightcone = BeforeTheTutorialMissionStarts(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = PanCosmicCommercialEnterprise(),
                            talentStacks=3,
                            **config)
    config['fivestarEidolons'] = originalFivestarEidolons

    # I'm just going to assume 100% uptime on firmament frontline glamoth
    # Kafka and Jiaoqiu are a few substats short of base 160 with a 12 substat cap
    # But I'll just generously assume you are able to get there

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
    
    team = [KafkaCharacter, JiaoqiuCharacter, BlackSwanCharacter, LuochaCharacter]

    #%% Kafka Jiaoqiu BlackSwan Luocha Team Buffs
    # Fleet of the Ageless Buff
    for character in [KafkaCharacter, JiaoqiuCharacter, BlackSwanCharacter]:
        character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)

    # Jiaoqiu Debuffs, 3 turn Jiaoqiu rotation
    JiaoqiuCharacter.applyTalentDebuff(team)
    jiaoqiuUltUptime = 1.0
    JiaoqiuCharacter.applyUltDebuff(team)
        
    # Apply BlackSwan Vulnerability Debuff
    SwanUltRotation = 4.0
    BlackSwanCharacter.applySkillDebuff(team,rotationDuration=1.0)
    # BlackSwanCharacter.applyUltDebuff(team,rotationDuration=SwanUltRotation)
    # Epiphany does not apply to detonations, so bump this buff til after the rotation cone

    #%% Print Statements
    for character in team:
        character.print()

    #%% Kafka Jiaoqiu BlackSwan Luocha Rotations
    # Napkin Math for stacks applied
    
    numDots = 4
    adjacentStackRate = 2 * (BlackSwanCharacter.numEnemies - 1) / BlackSwanCharacter.numEnemies
    dotStackRate = numDots * KafkaCharacter.numEnemies
    
    # 3 turn kafka ult rotation, 3 single target + 3 aoe every 3 turns
    KafkaStackRate = (3 + 3 * KafkaCharacter.numEnemies / 3)
    
    # Swan spams skill
    SwanStackRate = (1 + numDots) * min(3.0,BlackSwanCharacter.numEnemies)
    
    netStackRate = adjacentStackRate * KafkaCharacter.enemySpeed
    netStackRate += dotStackRate * KafkaCharacter.enemySpeed
    netStackRate += KafkaStackRate * KafkaCharacter.getTotalStat('SPD')
    netStackRate += SwanStackRate * BlackSwanCharacter.getTotalStat('SPD')
    netStackRate = netStackRate / KafkaCharacter.enemySpeed / KafkaCharacter.numEnemies
    netStackRate *= 1.0 + 1.0 / SwanUltRotation # swan ult effectively applies 1 extra rotation of dots every N turns
    print(f'net Stack Rate per Enemy {netStackRate}')
    
    BlackSwanCharacter.setSacramentStacks(netStackRate)
    
    numSkill = 3.0
    numTalent = 3.0
    numUlt = 1.0
    JiaoqiuDot = JiaoqiuCharacter.useDot()
    JiaoqiuDot.energy = 0.0 # kafka shouldn't be getting energy for Jiaoqiu Dot
    BlackSwanDot = BlackSwanCharacter.useDotDetonation()
    BlackSwanDot.energy = 0.0
    extraDots = [ JiaoqiuDot, BlackSwanDot ]
    extraDotsUlt = [ JiaoqiuDot * KafkaCharacter.numEnemies, BlackSwanDot * KafkaCharacter.numEnemies ]
    KafkaRotation = [
            KafkaCharacter.useSkill(extraDots=extraDots) * numSkill,
            KafkaCharacter.useTalent() * numTalent,
            KafkaCharacter.useUltimate(extraDots=extraDotsUlt) * numUlt,
    ]

    numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
    numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)

    numBasicJiaoqiu = 3.0
    numSkillJiaoqiu = 0.0
    JiaoqiuRotation = [JiaoqiuCharacter.useBasic() * numBasicJiaoqiu,
                       JiaoqiuCharacter.useSkill() * numSkillJiaoqiu,
                        JiaoqiuCharacter.useUltimate(),]

    numBasicBlackSwan = 0.0
    numSkillBlackSwan = SwanUltRotation
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
    
    BlackSwanCharacter.applyUltDebuff(team,rotationDuration=SwanUltRotation)
    # Epiphany does not apply to detonations, so bump this buff til after the rotation cone


    #%% Kafka Jiaoqiu BlackSwan Luocha Rotation Math
    numDotJiaoqiu = DotEstimator(JiaoqiuRotation, JiaoqiuCharacter, config, dotMode='alwaysAll') * jiaoqiuUltUptime
    numDotBlackSwan = DotEstimator(BlackSwanRotation, BlackSwanCharacter, config, dotMode='alwaysAll')
    
    totalKafkaEffect = sumEffects(KafkaRotation)
    totalJiaoqiuEffect = sumEffects(JiaoqiuRotation)
    totalBlackSwanEffect = sumEffects(BlackSwanRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
    JiaoqiuRotationDuration = totalJiaoqiuEffect.actionvalue * 100.0 / JiaoqiuCharacter.getTotalStat('SPD')
    BlackSwanRotationDuration = totalBlackSwanEffect.actionvalue * 100.0 / BlackSwanCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's character's rotation
    JiaoqiuRotation = [x * KafkaRotationDuration / JiaoqiuRotationDuration for x in JiaoqiuRotation]
    BlackSwanRotation = [x * KafkaRotationDuration / BlackSwanRotationDuration for x in BlackSwanRotation]
    LuochaRotation = [x * KafkaRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    numDotJiaoqiu *= KafkaRotationDuration / JiaoqiuRotationDuration
    numDotBlackSwan *= KafkaRotationDuration / BlackSwanRotationDuration

    KafkaEstimate = DefaultEstimator('Kafka {:.0f}E {:.0f}T {:.0f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDotKafka),
                                    KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
    JiaoqiuEstimate = DefaultEstimator(f'Jiaoqiu E{JiaoqiuCharacter.eidolon:d}: {numBasicJiaoqiu:.0f}N {numSkillJiaoqiu:.0f}E 1Q {JiaoqiuCharacter.talentStacks:.0f} Roasts, S{JiaoqiuCharacter.lightcone.superposition:d} {JiaoqiuCharacter.lightcone.name}', 
                                    JiaoqiuRotation, JiaoqiuCharacter, config, numDot=numDotJiaoqiu)
    BlackSwanEstimate = DefaultEstimator(f'BlackSwan S{BlackSwanCharacter.lightcone.superposition:.0f} {BlackSwanCharacter.lightcone.name} {numBasicBlackSwan:.0f}N {numSkillBlackSwan:.0f}E {numUltBlackSwan:.0f}Q {numDotBlackSwan:.1f}Dot {BlackSwanCharacter.sacramentStacks:.1f}Sacrament', 
                                                                                                BlackSwanRotation, BlackSwanCharacter, config, numDot=numDotBlackSwan)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([KafkaEstimate, JiaoqiuEstimate, BlackSwanEstimate, LuochaEstimate])