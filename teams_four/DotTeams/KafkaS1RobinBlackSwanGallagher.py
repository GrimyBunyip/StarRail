from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.harmony.Robin import Robin
from characters.nihility.Kafka import Kafka
from characters.nihility.BlackSwan import BlackSwan
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.abundance.PostOpConversation import PostOpConversation
from lightCones.abundance.QuidProQuo import QuidProQuo
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
from relicSets.relicSets.SacerdosRelivedOrdeal import SacerdosRelivedOrdeal2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def KafkaS1RobinBlackSwanGallagher(config):
    #%% Kafka Robin BlackSwan Gallagher
    
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

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                            substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                            lightcone = QuidProQuo(**config),
                            relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = SprightlyVonwacq(),
                            **config)
    
    team = [KafkaCharacter, RobinCharacter, BlackSwanCharacter, GallagherCharacter]

    #%% Kafka Robin BlackSwan Gallagher Team Buffs
    # Fleet of the Ageless Buff
    for character in [KafkaCharacter, RobinCharacter, BlackSwanCharacter]:
        character.addStat('ATK.percent',description='Fleet Gallagher',amount=0.08)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinUltUptime = 0.5 # assume better robin ult uptime because of shorter robin rotation
    RobinCharacter.applyUltBuff([KafkaCharacter,BlackSwanCharacter,GallagherCharacter],uptime=RobinUltUptime)
        
    # Apply BlackSwan Vulnerability Debuff
    SwanUltRotation = 4.0
    BlackSwanCharacter.applySkillDebuff(team,rotationDuration=1.5)
    # BlackSwanCharacter.applyUltDebuff(team,rotationDuration=SwanUltRotation)
    # Epiphany does not apply to detonations, so bump this buff til after the rotation cone
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Kafka Robin BlackSwan Gallagher Rotations
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
        

    numBasicGallagher = 4.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1,]
    if GallagherCharacter.lightcone.name == 'Multiplication':
        GallagherRotation[-1].actionvalue += 0.20 # advance foward cannot exceed a certain amount

    RobinRotationGallagher = [RobinCharacter.useTalent() * (numBasicGallagher + numEnhancedGallagher + 1.0)]
    RobinRotationGallagher += [RobinCharacter.useConcertoDamage(['basic']) * numBasicGallagher * RobinUltUptime]
    RobinRotationGallagher += [RobinCharacter.useConcertoDamage(['basic','enhancedBasic']) * numEnhancedGallagher * RobinUltUptime]
    RobinRotationGallagher += [RobinCharacter.useConcertoDamage(['ultimate']) * 1.0 * RobinUltUptime]
    
    BlackSwanCharacter.applyUltDebuff(team,rotationDuration=SwanUltRotation)
    # Epiphany does not apply to detonations, so bump this buff til after the rotation cone


    #%% Kafka Robin BlackSwan Gallagher Rotation Math
    numDotBlackSwan = DotEstimator(BlackSwanRotation, BlackSwanCharacter, config, dotMode='alwaysAll')
    numDotBlackSwan = min(numDotBlackSwan, 3.0 * (numSkillBlackSwan + numUltBlackSwan) * BlackSwanCharacter.numEnemies)

    totalKafkaEffect = sumEffects(KafkaRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalBlackSwanEffect = sumEffects(BlackSwanRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    BlackSwanRotationDuration = totalBlackSwanEffect.actionvalue * 100.0 / BlackSwanCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    QPQEffect = BaseEffect()
    
    QPQEffect.energy = 16.0 
    QPQEffect.energy *= 0.25 # assume quarter uptime
    QPQEffect.energy *= (numBasicGallagher + numEnhancedGallagher)
    QPQEffect.energy *= KafkaRotationDuration / GallagherRotationDuration
    KafkaCharacter.addDebugInfo(QPQEffect,['buff'],'Quid Pro Quo Energy')
    KafkaRotation.append(deepcopy(QPQEffect))
    
    QPQEffect.energy = 16.0 
    QPQEffect.energy *= 0.25 # assume quarter uptime
    QPQEffect.energy *= (numBasicGallagher + numEnhancedGallagher)
    QPQEffect.energy *= RobinRotationDuration / RobinRotationDuration
    RobinCharacter.addDebugInfo(QPQEffect,['buff'],'Quid Pro Quo Energy')
    RobinRotation.append(deepcopy(QPQEffect))
    
    QPQEffect.energy = 16.0 
    QPQEffect.energy *= 0.25 # assume quarter uptime
    QPQEffect.energy *= (numBasicGallagher + numEnhancedGallagher)
    QPQEffect.energy *= BlackSwanRotationDuration / BlackSwanRotationDuration
    BlackSwanCharacter.addDebugInfo(QPQEffect,['buff'],'Quid Pro Quo Energy')
    BlackSwanRotation.append(deepcopy(QPQEffect))

    # scale other character's character's rotation
    RobinRotation = [x * KafkaRotationDuration / RobinRotationDuration for x in RobinRotation]
    BlackSwanRotation = [x * KafkaRotationDuration / BlackSwanRotationDuration for x in BlackSwanRotation]
    GallagherRotation = [x * KafkaRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    numDotBlackSwan *= KafkaRotationDuration / BlackSwanRotationDuration
    
    RobinRotation += RobinRotationKafka
    RobinRotation += RobinRotationBlackSwan
    RobinRotation += RobinRotationGallagher
    totalRobinEffect = sumEffects(RobinRotation)

    KafkaEstimate = DefaultEstimator('Kafka {:.1f}E {:.1f}T {:.1f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDotKafka),
                                    KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
    RobinEstimate = DefaultEstimator(f'Robin: {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q, S{RobinCharacter.lightcone.superposition:d} {RobinCharacter.lightcone.name}', 
                                    RobinRotation, RobinCharacter, config)
    BlackSwanEstimate = DefaultEstimator(f'BlackSwan S{BlackSwanCharacter.lightcone.superposition:.0f} {BlackSwanCharacter.lightcone.name} {numBasicBlackSwan:.0f}N {numSkillBlackSwan:.0f}E {numUltBlackSwan:.0f}Q {numDotBlackSwan:.1f}Dot {BlackSwanCharacter.sacramentStacks:.1f}Sacrament', 
                                                                                                BlackSwanRotation, BlackSwanCharacter, config, numDot=numDotBlackSwan)
    GallagherEstimate = DefaultEstimator(f'{GallagherCharacter.fullName()} {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q', 
                                    GallagherRotation, GallagherCharacter, config)

    return([KafkaEstimate, RobinEstimate, BlackSwanEstimate, GallagherEstimate])