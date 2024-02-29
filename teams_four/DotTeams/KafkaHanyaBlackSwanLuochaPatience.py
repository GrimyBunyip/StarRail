from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.harmony.Hanya import Hanya
from characters.nihility.Kafka import Kafka
from characters.nihility.BlackSwan import BlackSwan
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.nihility.EyesOfThePrey import EyesOfThePrey
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.PatienceIsAllYouNeed import PatienceIsAllYouNeed
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.PanCosmicCommercialEnterprise import PanCosmicCommercialEnterprise
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def KafkaHanyaBlackSwanLuochaPatience(config):
    #%% Kafka Hanya BlackSwan Luocha
    KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'BreakEffect': 5, 'ATK.flat': 3}),
                        lightcone = PatienceIsAllYouNeed(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

    # I'm just going to assume 100% uptime on firmament frontline glamoth
    # Kafka and Hanya are a few substats short of base 160 with a 12 substat cap
    # But I'll just generously assume you are able to get there

    BlackSwanCharacter = BlackSwan(RelicStats(mainstats = ['EHR', 'ATK.percent', 'ATK.percent', 'DMG.wind'],
                        substats = {'ATK.percent': 12, 'SPD.flat': 5, 'EHR': 8, 'ATK.flat': 3}),
                        lightcone = EyesOfThePrey(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = PanCosmicCommercialEnterprise(),
                        **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                        substats = {'CR': 8, 'SPD.flat': 12, 'CD': 5, 'ATK.percent': 3}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = FleetOfTheAgeless(),
                        **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                        **config)
    
    team = [KafkaCharacter, HanyaCharacter, BlackSwanCharacter, LuochaCharacter]

    #%% Kafka Hanya BlackSwan Luocha Team Buffs
    # Fleet of the Ageless Buff
    for character in [KafkaCharacter, HanyaCharacter, BlackSwanCharacter]:
        character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)
    for character in [KafkaCharacter, LuochaCharacter, BlackSwanCharacter]:
        character.addStat('ATK.percent',description='Fleet Hanya',amount=0.08)
        
    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(KafkaCharacter,uptime=1.0)

    # Messenger 4 pc
    for character in [KafkaCharacter, BlackSwanCharacter, LuochaCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Apply BlackSwan Vulnerability Debuff
    SwanUltRotation = 4.0
    BlackSwanCharacter.applySkillDebuff(team,rotationDuration=1.0)
    # BlackSwanCharacter.applyUltDebuff(team,rotationDuration=SwanUltRotation)
    # Epiphany does not apply to detonations, so bump this buff til after the rotation cone

    #%% Print Statements
    for character in team:
        character.print()

    #%% Kafka Hanya BlackSwan Luocha Rotations
    # Napkin Math for stacks applied
    
    numDots = 3
    adjacentStackRate = 2 * (BlackSwanCharacter.numEnemies - 1) / BlackSwanCharacter.numEnemies
    dotStackRate = numDots * KafkaCharacter.numEnemies
    
    # 3 turn kafka ult rotation, 3 single target + 3 aoe every 3 turns
    KafkaStackRate = (3 + 3 * KafkaCharacter.numEnemies / 3)
    
    # Swan alternates applying basic and skill stacks
    swanBasicStacks = 1 + numDots
    swanSkillStacks = (1 + numDots) * min(3.0,BlackSwanCharacter.numEnemies)
    
    SwanStackRate = swanBasicStacks * 0.0 + swanSkillStacks * 1.0
    
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
    BlackSwanDot = BlackSwanCharacter.useDotDetonation()
    BlackSwanDot.energy = 0.0
    extraDots = [ BlackSwanDot ]
    extraDotsUlt = [ BlackSwanDot * KafkaCharacter.numEnemies ]
    KafkaRotation = [
            KafkaCharacter.useSkill(extraDots=extraDots) * numSkill,
            KafkaCharacter.useTalent() * numTalent,
            KafkaCharacter.useUltimate(extraDots=extraDotsUlt) * numUlt,
    ]

    numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
    numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)

    numHanyaSkill = 3
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]

    numBasicBlackSwan = SwanUltRotation * 0.0
    numSkillBlackSwan = SwanUltRotation * 1.0
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


    #%% Kafka Hanya BlackSwan Luocha Rotation Math
    numDotBlackSwan = DotEstimator(BlackSwanRotation, BlackSwanCharacter, config, dotMode='alwaysAll')
    numDotBlackSwan = min(numDotBlackSwan, 3.0 * (numSkillBlackSwan + numUltBlackSwan) * BlackSwanCharacter.numEnemies)

    totalKafkaEffect = sumEffects(KafkaRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalBlackSwanEffect = sumEffects(BlackSwanRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    BlackSwanRotationDuration = totalBlackSwanEffect.actionvalue * 100.0 / BlackSwanCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's character's rotation
    HanyaRotation = [x * KafkaRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    BlackSwanRotation = [x * KafkaRotationDuration / BlackSwanRotationDuration for x in BlackSwanRotation]
    LuochaRotation = [x * KafkaRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    numDotBlackSwan *= KafkaRotationDuration / BlackSwanRotationDuration
    
    # calculate total number of breaks for Ruan Mei Talent
    totalEffect = sumEffects(KafkaRotation + BlackSwanRotation + HanyaRotation + LuochaRotation)
    numBreaks = totalEffect.gauge * HanyaCharacter.weaknessBrokenUptime / HanyaCharacter.enemyToughness
    HanyaRotation.append(HanyaCharacter.useTalent() * numBreaks)

    KafkaEstimate = DefaultEstimator('Kafka {:.0f}E {:.0f}T {:.0f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDotKafka),
                                    KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
    HanyaEstimate = DefaultEstimator(f'Hanya: {numHanyaSkill:.0f}E {numHanyaUlt:.0f}Q S{HanyaCharacter.lightcone.superposition:.0f} {HanyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanyaRotation, HanyaCharacter, config)
    BlackSwanEstimate = DefaultEstimator(f'BlackSwan S{BlackSwanCharacter.lightcone.superposition:.0f} {BlackSwanCharacter.lightcone.name} {numBasicBlackSwan:.0f}N {numSkillBlackSwan:.0f}E {numUltBlackSwan:.0f}Q {numDotBlackSwan:.1f}Dot {BlackSwanCharacter.sacramentStacks:.1f}Sacrament', 
                                                                                                BlackSwanRotation, BlackSwanCharacter, config, numDot=numDotBlackSwan)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([KafkaEstimate, HanyaEstimate, BlackSwanEstimate, LuochaEstimate])