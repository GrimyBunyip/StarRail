from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.harmony.RuanMei import RuanMei
from characters.harmony.Tingyun import Tingyun
from characters.nihility.Kafka import Kafka
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def KafkaTingyunRuanMeiLuocha(config):
    #%% Kafka Tingyun RuanMei Luocha Characters
    
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

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                            benedictionTarget=KafkaCharacter,
                            **config)

    # I'm just going to assume 100% uptime on firmament frontline glamoth
    # Kafka and Tingyun are a few substats short of base 160 with a 12 substat cap
    # But I'll just generously assume you are able to get there

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                                    **config)
    
    team = [KafkaCharacter, TingyunCharacter, RuanMeiCharacter, LuochaCharacter]

    #%% Kafka Tingyun RuanMei Luocha Team Buffs
    # Fleet of the Ageless Buff
    for character in [KafkaCharacter, TingyunCharacter, RuanMeiCharacter]:
        character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)
    # Penacony Buff
    for character in [KafkaCharacter, RuanMeiCharacter, LuochaCharacter]:
        character.addStat('DMG.lightning',description='Penacony from Tingyun',amount=0.1)
        
    # Tingyun Messenger Buff
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)
    for character in [KafkaCharacter, RuanMeiCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(KafkaCharacter)
    TingyunCharacter.applyUltBuff(KafkaCharacter)

    # RuanMei Buffs, max skill uptime
    RuanMeiCharacter.applyWeaknessModifiers(team=team)
    RuanMeiCharacter.applyPassiveBuffs(team=team)
    RuanMeiCharacter.applySkillBuff(team=team,uptime=3.0/3.0)
    RuanMeiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Kafka Tingyun RuanMei Luocha Rotations
    numSkill = 2.0
    numTalent = 2.0
    numUlt = 1.0
    KafkaRotation = [
            KafkaCharacter.useSkill() * numSkill,
            KafkaCharacter.useTalent() * numTalent,
            KafkaCharacter.useUltimate() * numUlt,
            TingyunCharacter.useBenediction(['skill']) * numSkill, # apply benedictions with buffs
            TingyunCharacter.useBenediction(['talent','followup']) * numTalent, # apply benedictions with buffs
            TingyunCharacter.useBenediction(['ultimate']) * 1,
            TingyunCharacter.giveUltEnergy() * TingyunCharacter.getTotalStat('SPD') / KafkaCharacter.getTotalStat('SPD') / 1.5
    ]

    numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
    numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)

    TingyunRotation = [ 
            TingyunCharacter.useBasic() * 2, 
            TingyunCharacter.useSkill(),
            TingyunCharacter.useUltimate(),
    ]

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


    #%% Kafka Tingyun RuanMei Luocha Rotation Math
    totalKafkaEffect = sumEffects(KafkaRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's rotation
    TingyunRotation = [x * KafkaRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    RuanMeiRotation = [x * KafkaRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    LuochaRotation = [x * KafkaRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    
    # calculate total number of breaks for Ruan Mei Talent
    totalEffect = sumEffects(KafkaRotation + TingyunRotation + RuanMeiRotation + LuochaRotation)
    numBreaks = totalEffect.gauge * RuanMeiCharacter.weaknessBrokenUptime / RuanMeiCharacter.enemyToughness
    RuanMeiRotation.append(RuanMeiCharacter.useTalent() * numBreaks)

    KafkaEstimate = DefaultEstimator('Kafka {:.0f}E {:.0f}T {:.0f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDotKafka),
                                    KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats', 
                                    TingyunRotation, TingyunCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'RuanMei {numSkillRuanMei:.1f}E {numBasicRuanMei:.1f}N S{RuanMeiCharacter.lightcone.superposition:.0f} {RuanMeiCharacter.lightcone.name}, 12 Spd Substats', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([KafkaEstimate, TingyunEstimate, LuochaEstimate, RuanMeiEstimate])