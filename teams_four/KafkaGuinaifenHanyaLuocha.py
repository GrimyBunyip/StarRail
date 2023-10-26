from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.harmony.Hanya import Hanya
from characters.nihility.Guinaifen import Guinaifen
from characters.nihility.Kafka import Kafka
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc

def KafkaGuinaifenHanyaLuocha(config):
    #%% Kafka Guinaifen Hanya Luocha Characters
    KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'BreakEffect': 5, 'ATK.flat': 3}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    GuinaifenCharacter = Guinaifen(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.fire'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'EHR': 4, 'BreakEffect': 4}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    # I'm just going to assume 100% uptime on firmament frontline glamoth
    # Kafka and Guinaifen are a few substats short of base 160 with a 12 substat cap
    # But I'll just generously assume you are able to get there

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                            substats = {'CD': 8, 'SPD.flat': 12, 'CR': 5, 'BreakEffect': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = FleetOfTheAgeless(),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                                    **config)
    
    team = [KafkaCharacter, GuinaifenCharacter, HanyaCharacter, LuochaCharacter]

    #%% Kafka Guinaifen Hanya Luocha Team Buffs
    # Fleet of the Ageless Buff
    for character in [KafkaCharacter, GuinaifenCharacter, HanyaCharacter]:
        character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)
    for character in [KafkaCharacter, GuinaifenCharacter, LuochaCharacter]:
        character.addStat('ATK.percent',description='Fleet Asta',amount=0.08)
        
    # Give Guinaifen Vulnerability to all other characters
    for character in [KafkaCharacter, HanyaCharacter, LuochaCharacter]:
        character.addStat('Vulnerability',description='Guinaifen Vulnerability',
                            amount=0.076 if GuinaifenCharacter.eidolon >= 5 else 0.07,
                            stacks=min(GuinaifenCharacter.firekissStacks,4.0 if GuinaifenCharacter.eidolon >= 6 else 3.0))
        
    # messenger 4 pc buffs:
    KafkaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0 / 3.0)
    GuinaifenCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0 / 3.0)
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0 / 4.0)
    
    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(KafkaCharacter,uptime=1.0)
    
    #%% Print Statements
    for character in team:
        character.print()

    #%% Kafka Guinaifen Hanya Luocha Rotations
    numSkill = 3.0
    numTalent = 3.0
    numUlt = 1.0
    GuinaifenDot = GuinaifenCharacter.useDot()
    GuinaifenDot.energy = 0.0 # kafka shouldn't be getting energy for Guinaifen Dot
    extraDots = [ GuinaifenDot ]
    extraDotsUlt = [ GuinaifenDot * KafkaCharacter.numEnemies ]
    KafkaRotation = [
            KafkaCharacter.useSkill(extraDots=extraDots) * numSkill,
            KafkaCharacter.useTalent() * numTalent,
            KafkaCharacter.useUltimate(extraDots=extraDotsUlt) * numUlt,
    ]

    numSkillGuinaifen = 3.0
    numUltGuinaifen = 1.0

    numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
    numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)

    GuinaifenRotation = [ # 
            GuinaifenCharacter.useSkill() * numSkillGuinaifen,
            GuinaifenCharacter.useUltimate() * numUlt,
    ]

    numHanyaSkill = 3
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]
        
    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast


    #%% Kafka Guinaifen Hanya Luocha Rotation Math
    numDotGuinaifen = DotEstimator(GuinaifenRotation, GuinaifenCharacter, config, dotMode='alwaysBlast')
    numDotGuinaifen = min(numDotGuinaifen, 2.0 * numSkillGuinaifen * min(3.0, GuinaifenCharacter.numEnemies))

    totalKafkaEffect = sumEffects(KafkaRotation)
    totalGuinaifenEffect = sumEffects(GuinaifenRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
    GuinaifenRotationDuration = totalGuinaifenEffect.actionvalue * 100.0 / GuinaifenCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's character's rotation
    GuinaifenRotation = [x * KafkaRotationDuration / GuinaifenRotationDuration for x in GuinaifenRotation]
    HanyaRotation = [x * KafkaRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    LuochaRotation = [x * KafkaRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    numDotGuinaifen *= KafkaRotationDuration / GuinaifenRotationDuration

    KafkaEstimate = DefaultEstimator('Kafka {:.0f}E {:.0f}T {:.0f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDotKafka),
                                    KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
    GuinaifenEstimate = DefaultEstimator('E6 Guinaifen S5 GNSW {:.0f}E {:.0f}Q {:.1f}Dot'.format(numSkillGuinaifen, numUltGuinaifen, numDotGuinaifen),
                                        GuinaifenRotation, GuinaifenCharacter, config, numDot=numDotGuinaifen)
    HanyaEstimate = DefaultEstimator('Hanya 2.5 SP per E {:.0f}E {:.0f}Q S{:.0f} {}, 12 Spd Substats'.format(numHanyaSkill, numHanyaUlt,
                                    HanyaCharacter.lightcone.superposition, HanyaCharacter.lightcone.name), 
                                    HanyaRotation, HanyaCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([KafkaEstimate, GuinaifenEstimate, HanyaEstimate, LuochaEstimate])