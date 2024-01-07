from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.harmony.RuanMei import RuanMei
from characters.nihility.Sampo import Sampo
from characters.nihility.Kafka import Kafka
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def KafkaSampoRuanMeiLuocha(config):
    #%% Kafka Sampo RuanMei Luocha Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                        substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                        **config)
    
    KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'BreakEffect': 5, 'ATK.flat': 3}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    SampoCharacter = Sampo(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.wind'],
                                    substats = {'ATK.percent': 5, 'SPD.flat': 12, 'EHR': 8, 'BreakEffect': 3}),
                                    lightcone = GoodNightAndSleepWell(**config),
                                    relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                                    **config)

    # I'm just going to assume 100% uptime on firmament frontline glamoth
    # Kafka and Sampo are a few substats short of base 160 with a 12 substat cap
    # But I'll just generously assume you are able to get there

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                                    **config)
    
    team = [KafkaCharacter, SampoCharacter, RuanMeiCharacter, LuochaCharacter]

    #%% Kafka Sampo RuanMei Luocha Team Buffs
    # Fleet of the Ageless Buff
    for character in [KafkaCharacter, SampoCharacter, RuanMeiCharacter]:
        character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)
        
    # Apply Sampo Vulnerability Debuff
    SampoCharacter.applyUltDebuff(team,rotationDuration=3.5)

    # RuanMei Buffs, max skill uptime
    RuanMeiCharacter.applyWeaknessModifiers(team=team)
    RuanMeiCharacter.applyPassiveBuffs(team=team)
    RuanMeiCharacter.applySkillBuff(team=team,uptime=3.0/3.0)
    RuanMeiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Kafka Sampo RuanMei Luocha Rotations
    numSkill = 3.0
    numTalent = 3.0
    numUlt = 1.0
    SampoDot = SampoCharacter.useDot()
    SampoDot.energy = 0.0 # kafka shouldn't be getting energy for Sampo Dot
    extraDots = [ SampoDot]
    extraDotsUlt = [ SampoDot * KafkaCharacter.numEnemies, ]
    KafkaRotation = [
            KafkaCharacter.useSkill(extraDots=extraDots) * numSkill,
            KafkaCharacter.useTalent() * numTalent,
            KafkaCharacter.useUltimate(extraDots=extraDotsUlt) * numUlt,
    ]

    numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
    numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)

    numBasicSampo = 1
    numSkillSampo = 2.5
    numUltSampo = 1
    SampoRotation = [
                    SampoCharacter.useBasic() * numBasicSampo,
                    SampoCharacter.useSkill() * numSkillSampo,
                    SampoCharacter.useUltimate() * numUltSampo]

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


    #%% Kafka Sampo RuanMei Luocha Rotation Math
    numDotSampo = DotEstimator(SampoRotation, SampoCharacter, config, dotMode='alwaysBlast')
    numDotSampo = min(numDotSampo, 3.0 * (numSkillSampo + numUltSampo) * SampoCharacter.numEnemies)

    totalKafkaEffect = sumEffects(KafkaRotation)
    totalSampoEffect = sumEffects(SampoRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
    SampoRotationDuration = totalSampoEffect.actionvalue * 100.0 / SampoCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's rotation
    SampoRotation = [x * KafkaRotationDuration / SampoRotationDuration for x in SampoRotation]
    RuanMeiRotation = [x * KafkaRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    LuochaRotation = [x * KafkaRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    numDotSampo *= KafkaRotationDuration / SampoRotationDuration
    
    # calculate total number of breaks for Ruan Mei Talent
    totalEffect = sumEffects(KafkaRotation + SampoRotation + RuanMeiRotation + LuochaRotation)
    numBreaks = totalEffect.gauge * RuanMeiCharacter.weaknessBrokenUptime / RuanMeiCharacter.enemyToughness
    RuanMeiRotation.append(RuanMeiCharacter.useTalent() * numBreaks)

    KafkaEstimate = DefaultEstimator('Kafka {:.0f}E {:.0f}T {:.0f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDotKafka),
                                    KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
    SampoEstimate = DefaultEstimator('Sampo S{:.0f} {} {:.1f}N {:.1f}E {:.0f}Q {:.1f}Dot'.format(SampoCharacter.lightcone.superposition, SampoCharacter.lightcone.name, 
                                                                                                numBasicSampo, numSkillSampo, numUltSampo, numDotSampo), 
                                                                                                SampoRotation, SampoCharacter, config, numDot=numDotSampo)
    RuanMeiEstimate = DefaultEstimator(f'RuanMei {numSkillRuanMei:.1f}E {numBasicRuanMei:.1f}N S{RuanMeiCharacter.lightcone.superposition:.0f} {RuanMeiCharacter.lightcone.name}, 12 Spd Substats', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([KafkaEstimate, SampoEstimate, LuochaEstimate, RuanMeiEstimate])