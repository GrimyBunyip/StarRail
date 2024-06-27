from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Huohuo import Huohuo
from characters.harmony.Robin import Robin
from characters.nihility.Kafka import Kafka
from characters.nihility.BlackSwan import BlackSwan
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.abundance.PostOpConversation import PostOpConversation
from lightCones.harmony.ForTomorrowsJourney import ForTomorrowsJourney
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.nihility.EyesOfThePrey import EyesOfThePrey
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.PatienceIsAllYouNeed import PatienceIsAllYouNeed
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.PanCosmicCommercialEnterprise import PanCosmicCommercialEnterprise
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def KafkaRobinBlackSwanHuohuoPatience(config):
    #%% Kafka Robin BlackSwan Huohuo
    
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 11, 'SPD.flat': 9, 'RES': 3, 'ATK.flat': 5}),
                                    lightcone = ForTomorrowsJourney(**config),
                                    relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = SprightlyVonwacq(),
                                    **config)
    
    KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'BreakEffect': 5, 'ATK.flat': 3}),
                        lightcone = PatienceIsAllYouNeed(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

    # I'm just going to assume 100% uptime on firmament frontline glamoth
    # Kafka and Robin are a few substats short of base 160 with a 12 substat cap
    # But I'll just generously assume you are able to get there

    BlackSwanCharacter = BlackSwan(RelicStats(mainstats = ['EHR', 'ATK.percent', 'ATK.percent', 'DMG.wind'],
                        substats = {'ATK.percent': 12, 'SPD.flat': 5, 'EHR': 8, 'ATK.flat': 3}),
                        lightcone = EyesOfThePrey(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = PanCosmicCommercialEnterprise(),
                        **config)

    HuohuoCharacter = Huohuo(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'HP.flat': 3, 'RES': 6}),
                        lightcone = PostOpConversation(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                        **config)
    
    team = [KafkaCharacter, RobinCharacter, BlackSwanCharacter, HuohuoCharacter]

    #%% Kafka Robin BlackSwan Huohuo Team Buffs
    # Fleet of the Ageless Buff
    for character in [KafkaCharacter, RobinCharacter, BlackSwanCharacter]:
        character.addStat('ATK.percent',description='Fleet Huohuo',amount=0.08)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinUltUptime = 0.5 # assume better robin ult uptime because of shorter robin rotation
    RobinCharacter.applyUltBuff([KafkaCharacter,BlackSwanCharacter,HuohuoCharacter],uptime=RobinUltUptime)
        
    # Apply BlackSwan Vulnerability Debuff
    SwanUltRotation = 4.0
    BlackSwanCharacter.applySkillDebuff(team,rotationDuration=1.5)
    # BlackSwanCharacter.applyUltDebuff(team,rotationDuration=SwanUltRotation)
    # Epiphany does not apply to detonations, so bump this buff til after the rotation cone
    
    # Huohuo Buffs
    HuohuoCharacter.applyUltBuff(team,uptime=2.0/5.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Kafka Robin BlackSwan Huohuo Rotations
    # Napkin Math for stacks applied
    
    numDots = 3
    adjacentStackRate = 2 * (BlackSwanCharacter.numEnemies - 1) / BlackSwanCharacter.numEnemies
    dotStackRate = numDots * KafkaCharacter.numEnemies
    
    # 3 turn kafka ult rotation, 3 single target + 3 aoe every 3 turns
    KafkaStackRate = (3 + 3 * KafkaCharacter.numEnemies / 3)
    
    # Swan alternates applying basic and skill stacks
    swanBasicStacks = 1 + numDots
    swanSkillStacks = (1 + numDots) * min(3.0,BlackSwanCharacter.numEnemies)
    
    SwanStackRate = swanBasicStacks * 1.0 / 3.0 + swanSkillStacks * 2.0 / 3.0
    
    netStackRate = adjacentStackRate * KafkaCharacter.enemySpeed
    netStackRate += dotStackRate * KafkaCharacter.enemySpeed
    netStackRate += KafkaStackRate * KafkaCharacter.getTotalStat('SPD')
    netStackRate += SwanStackRate * BlackSwanCharacter.getTotalStat('SPD')
    netStackRate = netStackRate / KafkaCharacter.enemySpeed / KafkaCharacter.numEnemies
    netStackRate *= 1.0 + 1.0 / SwanUltRotation # swan ult effectively applies 1 extra rotation of dots every N turns
    print(f'net Stack Rate per Enemy {netStackRate}')
    
    BlackSwanCharacter.setSacramentStacks(netStackRate)
    
    numSkill = 2.6
    numTalent = numSkill
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
    KafkaRotation += [RobinCharacter.useAdvanceForward() * numSkill / 5.0]

    RobinRotationKafka = [RobinCharacter.useTalent() * (numSkill + numTalent + numUlt)]
    RobinRotationKafka += [RobinCharacter.useConcertoDamage(['skill']) * numSkill * RobinUltUptime]
    RobinRotationKafka += [RobinCharacter.useConcertoDamage(['followup']) * numTalent * RobinUltUptime]
    RobinRotationKafka += [RobinCharacter.useConcertoDamage(['ultimate']) * numUlt * RobinUltUptime]

    numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
    numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)

    numBasicRobin = 1.0
    numSkillRobin = 1.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                       RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate()]

    numBasicBlackSwan = SwanUltRotation * 1.0 / 2.0
    numSkillBlackSwan = SwanUltRotation * 1.0 / 2.0
    numUltBlackSwan = 1
    BlackSwanRotation = [
                    BlackSwanCharacter.useBasic() * numBasicBlackSwan,
                    BlackSwanCharacter.useSkill() * numSkillBlackSwan,
                    BlackSwanCharacter.useUltimate() * numUltBlackSwan]
    BlackSwanRotation += [RobinCharacter.useAdvanceForward() * SwanUltRotation / 5.0]

    RobinRotationBlackSwan = [RobinCharacter.useTalent() * (numBasicBlackSwan + numSkillBlackSwan + numUltBlackSwan)]
    RobinRotationBlackSwan += [RobinCharacter.useConcertoDamage(['basic']) * numBasicBlackSwan * RobinUltUptime]
    RobinRotationBlackSwan += [RobinCharacter.useConcertoDamage(['skill']) * numSkillBlackSwan * RobinUltUptime]
    RobinRotationBlackSwan += [RobinCharacter.useConcertoDamage(['ultimate']) * numUltBlackSwan * RobinUltUptime]
        
    numBasicHuohuo = 3.0
    numSkillHuohuo = 1.0
    HuohuoRotation = [HuohuoCharacter.useBasic() * numBasicHuohuo,
                    HuohuoCharacter.useUltimate() * 1,
                    HuohuoCharacter.useSkill() * numSkillHuohuo,]
    HuohuoRotation += [RobinCharacter.useAdvanceForward() * (numBasicHuohuo + numSkillHuohuo) / 5.0]

    RobinRotationHuohuo = [RobinCharacter.useTalent() * numBasicHuohuo]
    RobinRotationHuohuo += [RobinCharacter.useConcertoDamage(['basic']) * numBasicHuohuo * RobinUltUptime]
    
    BlackSwanCharacter.applyUltDebuff(team,rotationDuration=SwanUltRotation)
    # Epiphany does not apply to detonations, so bump this buff til after the rotation cone


    #%% Kafka Robin BlackSwan Huohuo Rotation Math
    numDotBlackSwan = DotEstimator(BlackSwanRotation, BlackSwanCharacter, config, dotMode='alwaysAll')
    numDotBlackSwan = min(numDotBlackSwan, 3.0 * (numSkillBlackSwan + numUltBlackSwan) * BlackSwanCharacter.numEnemies)

    totalKafkaEffect = sumEffects(KafkaRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalBlackSwanEffect = sumEffects(BlackSwanRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    BlackSwanRotationDuration = totalBlackSwanEffect.actionvalue * 100.0 / BlackSwanCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    KafkaRotation.append(HuohuoCharacter.giveUltEnergy(KafkaCharacter) * KafkaRotationDuration / HuohuoRotationDuration)
    BlackSwanRotation.append(HuohuoCharacter.giveUltEnergy(BlackSwanCharacter) * BlackSwanRotationDuration / HuohuoRotationDuration)
    RobinRotation.append(HuohuoCharacter.giveUltEnergy(RobinCharacter) * RobinRotationDuration / HuohuoRotationDuration)

    # scale other character's character's rotation
    RobinRotation = [x * KafkaRotationDuration / RobinRotationDuration for x in RobinRotation]
    BlackSwanRotation = [x * KafkaRotationDuration / BlackSwanRotationDuration for x in BlackSwanRotation]
    HuohuoRotation = [x * KafkaRotationDuration / HuohuoRotationDuration for x in HuohuoRotation]
    numDotBlackSwan *= KafkaRotationDuration / BlackSwanRotationDuration
    
    RobinRotation += RobinRotationKafka
    RobinRotation += RobinRotationBlackSwan
    RobinRotation += RobinRotationHuohuo
    totalRobinEffect = sumEffects(RobinRotation)

    KafkaEstimate = DefaultEstimator('Kafka {:.1f}E {:.1f}T {:.1f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDotKafka),
                                    KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
    RobinEstimate = DefaultEstimator(f'Robin: {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q, S{RobinCharacter.lightcone.superposition:d} {RobinCharacter.lightcone.name}', 
                                    RobinRotation, RobinCharacter, config)
    BlackSwanEstimate = DefaultEstimator(f'BlackSwan S{BlackSwanCharacter.lightcone.superposition:.0f} {BlackSwanCharacter.lightcone.name} {numBasicBlackSwan:.0f}N {numSkillBlackSwan:.0f}E {numUltBlackSwan:.0f}Q {numDotBlackSwan:.1f}Dot {BlackSwanCharacter.sacramentStacks:.1f}Sacrament', 
                                                                                                BlackSwanRotation, BlackSwanCharacter, config, numDot=numDotBlackSwan)
    HuohuoEstimate = DefaultEstimator(f'Huohuo: {numBasicHuohuo:.1f}N {numSkillHuohuo:.1f}E 1Q, S{HuohuoCharacter.lightcone.superposition:.0f} {HuohuoCharacter.lightcone.name}', 
                                    HuohuoRotation, HuohuoCharacter, config)

    return([KafkaEstimate, RobinEstimate, BlackSwanEstimate, HuohuoEstimate])