from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.harmony.RuanMei import RuanMei
from characters.nihility.BlackSwan import BlackSwan
from characters.nihility.Kafka import Kafka
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.nihility.EyesOfThePrey import EyesOfThePrey
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.PatienceIsAllYouNeed import PatienceIsAllYouNeed
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.PanCosmicCommercialEnterprise import PanCosmicCommercialEnterprise
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def KafkaBlackSwanRuanMeiLuocha(config):
    #%% Kafka BlackSwan RuanMei Luocha Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                        substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                        **config)
    
    KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'BreakEffect': 5, 'ATK.flat': 3}),
                            lightcone = PatienceIsAllYouNeed(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    BlackSwanCharacter = BlackSwan(RelicStats(mainstats = ['EHR', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'EHR': 5, 'BreakEffect': 3}),
                            lightcone = EyesOfThePrey(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = PanCosmicCommercialEnterprise(),
                            sacramentStacks=15.0, # Estimate low uptime because it's a kafka mei team
                            **config)

    # I'm just going to assume 100% uptime on firmament frontline glamoth
    # Kafka and BlackSwan are a few substats short of base 160 with a 12 substat cap
    # But I'll just generously assume you are able to get there

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                                    **config)
    
    team = [KafkaCharacter, BlackSwanCharacter, RuanMeiCharacter, LuochaCharacter]

    #%% Kafka BlackSwan RuanMei Luocha Team Buffs
    # Fleet of the Ageless Buff
    for character in [KafkaCharacter, BlackSwanCharacter, RuanMeiCharacter]:
        character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)
        
    # Apply BlackSwan Vulnerability Debuff
    BlackSwanCharacter.applySkillDebuff(team,rotationDuration=2.0)
    BlackSwanCharacter.applyUltDebuff(team,rotationDuration=4.0)

    # RuanMei Buffs, max skill uptime
    RuanMeiCharacter.applyWeaknessModifiers(team=team)
    RuanMeiCharacter.applyPassiveBuffs(team=team)
    RuanMeiCharacter.applySkillBuff(team=team,uptime=3.0/3.0)
    RuanMeiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Kafka BlackSwan RuanMei Luocha Rotations
    
    KafkaStacks = 3 + 3 + 3 + 3 * KafkaCharacter.numEnemies
    KafkaStackRate = KafkaStacks * KafkaCharacter.getTotalStat('SPD') / 3
        
    SwanStacks = 2*3 + 2*3*min(3,BlackSwanCharacter.numEnemies) + 3 * BlackSwanCharacter.numEnemies
    SwanStackRate = SwanStacks * BlackSwanCharacter.getTotalStat('SPD') / 4
    
    netStackRate = (KafkaStackRate + SwanStackRate) / KafkaCharacter.enemyDotSpeed / KafkaCharacter.numEnemies + 3
    print(f'net Stack Rate per Enemy {netStackRate}')
    
    numSkill = 3.0
    numTalent = 3.0
    numUlt = 1.0
    BlackSwanDot = BlackSwanCharacter.useDotDetonation()
    BlackSwanDot.energy = 0.0 # kafka shouldn't be getting energy for BlackSwan Dot
    extraDots = [ BlackSwanDot]
    extraDotsUlt = [ BlackSwanDot * KafkaCharacter.numEnemies, ]
    KafkaRotation = [
            KafkaCharacter.useSkill(extraDots=extraDots) * numSkill,
            KafkaCharacter.useTalent() * numTalent,
            KafkaCharacter.useUltimate(extraDots=extraDotsUlt) * numUlt,
    ]

    numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
    numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)

    numBasicBlackSwan = 2
    numSkillBlackSwan = 2
    numUltBlackSwan = 1
    BlackSwanRotation = [
                    BlackSwanCharacter.useBasic() * numBasicBlackSwan,
                    BlackSwanCharacter.useSkill() * numSkillBlackSwan,
                    BlackSwanCharacter.useUltimate() * numUltBlackSwan]

    numBasicRuanMei = 2.0
    numSkillRuanMei = 1.0
    RuanMeiRotation = [RuanMeiCharacter.useBasic() * numBasicRuanMei,
                       RuanMeiCharacter.useSkill() * numSkillRuanMei,
                    RuanMeiCharacter.useUltimate()]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast


    #%% Kafka BlackSwan RuanMei Luocha Rotation Math
    numDotBlackSwan = DotEstimator(BlackSwanRotation, BlackSwanCharacter, config, dotMode='alwaysBlast')
    numDotBlackSwan = min(numDotBlackSwan, 2.0 * numSkillBlackSwan * min(3.0, BlackSwanCharacter.numEnemies))

    totalKafkaEffect = sumEffects(KafkaRotation)
    totalBlackSwanEffect = sumEffects(BlackSwanRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
    BlackSwanRotationDuration = totalBlackSwanEffect.actionvalue * 100.0 / BlackSwanCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's rotation
    BlackSwanRotation = [x * KafkaRotationDuration / BlackSwanRotationDuration for x in BlackSwanRotation]
    RuanMeiRotation = [x * KafkaRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    LuochaRotation = [x * KafkaRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    numDotBlackSwan *= KafkaRotationDuration / BlackSwanRotationDuration
    
    # calculate total number of breaks for Ruan Mei Talent
    totalEffect = sumEffects(KafkaRotation + BlackSwanRotation + RuanMeiRotation + LuochaRotation)
    numBreaks = totalEffect.gauge * RuanMeiCharacter.weaknessBrokenUptime / RuanMeiCharacter.enemyToughness
    RuanMeiRotation.append(RuanMeiCharacter.useTalent() * numBreaks)

    KafkaEstimate = DefaultEstimator('Kafka {:.0f}E {:.0f}T {:.0f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDotKafka),
                                    KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
    BlackSwanEstimate = DefaultEstimator('E6 BlackSwan S5 GNSW {:.1f}N {:.1f}E {:.0f}Q {:.1f}Dot'.format(numBasicBlackSwan, numSkillBlackSwan, numUltBlackSwan, numDotBlackSwan),
                                        BlackSwanRotation, BlackSwanCharacter, config, numDot=numDotBlackSwan)
    RuanMeiEstimate = DefaultEstimator(f'RuanMei {numSkillRuanMei:.1f}E {numBasicRuanMei:.1f}N S{RuanMeiCharacter.lightcone.superposition:.0f} {RuanMeiCharacter.lightcone.name}, 12 Spd Substats', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([KafkaEstimate, BlackSwanEstimate, LuochaEstimate, RuanMeiEstimate])