from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.nihility.Guinaifen import Guinaifen
from characters.nihility.Kafka import Kafka
from characters.nihility.Luka import Luka
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc

def KafkaGuinaifenLukaLuocha(config):
    #%% Kafka Guinaifen Luka Luocha Characters
    KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'BreakEffect': 5, 'ATK.flat': 3}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=1),
                            **config)

    GuinaifenCharacter = Guinaifen(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'ATK.percent', 'DMG.fire'],
                            substats = {'ATK.percent': 12, 'SPD.flat': 8, 'EHR': 4, 'BreakEffect': 4}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = SpaceSealingStation(),
                            **config)

    # I'm just going to assume 100% uptime on firmament frontline glamoth
    # Kafka and Guinaifen are a few substats short of base 160 with a 12 substat cap
    # But I'll just generously assume you are able to get there

    LukaCharacter = Luka(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'ATK.percent', 'DMG.physical'],
                            substats = {'ATK.percent': 12, 'SPD.flat': 3, 'EHR': 8, 'BreakEffect': 5}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = SpaceSealingStation(),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                            **config)
    
    team = [KafkaCharacter, GuinaifenCharacter, LukaCharacter, LuochaCharacter]

    #%% Kafka Guinaifen Luka Luocha Team Buffs
    # Fleet of the Ageless Buff
    for character in [KafkaCharacter, GuinaifenCharacter, LukaCharacter]:
        character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)
        
    # Apply Guinaifen Debuff
    GuinaifenCharacter.applyFirekiss(team=team,uptime=1.0)

    # Give Luka Vulnerability to all other characters
    LukaCharacter.applyUltDebuff([LukaCharacter,LuochaCharacter],rotationDuration=5.0,targetingUptime=1.0) # single target characters aim for luka target
    LukaCharacter.applyUltDebuff([KafkaCharacter,GuinaifenCharacter],rotationDuration=5.0,targetingUptime=1.0/LukaCharacter.numEnemies)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Kafka Guinaifen Luka Luocha Rotations
    numSkill = 3.0
    numTalent = 3.0
    numUlt = 1.0
    GuinaifenDot = GuinaifenCharacter.useDot()
    GuinaifenDot.energy = 0.0 # kafka shouldn't be getting energy for Guinaifen Dot
    LukaDot = LukaCharacter.useDot()
    LukaDot.energy = 0.0
    extraDots = [ GuinaifenDot, LukaDot ]
    extraDotsUlt = [ GuinaifenDot * KafkaCharacter.numEnemies, LukaDot * min(2,KafkaCharacter.numEnemies) ]
    KafkaRotation = [
            KafkaCharacter.useSkill(extraDots=extraDots) * numSkill,
            KafkaCharacter.useTalent() * numTalent,
            KafkaCharacter.useUltimate(extraDots=extraDotsUlt) * numUlt,
    ]

    numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
    numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)

    numBasicGuinaifen = 2.0
    numSkillGuinaifen = 2.0
    numUltGuinaifen = 1.0
    GuinaifenRotation = [ # 
            GuinaifenCharacter.useBasic() * numBasicGuinaifen,
            GuinaifenCharacter.useSkill() * numSkillGuinaifen,
            GuinaifenCharacter.useUltimate() * numUlt,
    ]

    numEnhancedLuka = 3.0
    numSkillLuka = 2.0
    numUltLuka = 1.0

    LukaRotation = [ # 
            LukaCharacter.useEnhancedBasic() * numEnhancedLuka, # -6 Fighting Will
            LukaCharacter.useSkill() * numSkillLuka, # +4 Fighting Will
            LukaCharacter.useUltimate() * numUltLuka, # +2 Fighting Will
    ]
        
    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast


    #%% Kafka Guinaifen Luka Luocha Rotation Math
    numDotGuinaifen = DotEstimator(GuinaifenRotation, GuinaifenCharacter, config, dotMode='alwaysBlast')
    numDotGuinaifen = min(numDotGuinaifen, 2.0 * numSkillGuinaifen * min(3.0, GuinaifenCharacter.numEnemies))
    numDotLuka = DotEstimator(LukaRotation, LukaCharacter, config, dotMode='alwaysBlast')
    numDotLuka = min(numDotLuka, 3.0 * numSkillLuka)

    totalKafkaEffect = sumEffects(KafkaRotation)
    totalGuinaifenEffect = sumEffects(GuinaifenRotation)
    totalLukaEffect = sumEffects(LukaRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
    GuinaifenRotationDuration = totalGuinaifenEffect.actionvalue * 100.0 / GuinaifenCharacter.getTotalStat('SPD')
    LukaRotationDuration = totalLukaEffect.actionvalue * 100.0 / LukaCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's character's rotation
    GuinaifenRotation = [x * KafkaRotationDuration / GuinaifenRotationDuration for x in GuinaifenRotation]
    LukaRotation = [x * KafkaRotationDuration / LukaRotationDuration for x in LukaRotation]
    LuochaRotation = [x * KafkaRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    numDotGuinaifen *= KafkaRotationDuration / GuinaifenRotationDuration
    numDotLuka *= KafkaRotationDuration / LukaRotationDuration

    KafkaEstimate = DefaultEstimator('Kafka {:.0f}E {:.0f}T {:.0f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDotKafka),
                                    KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
    GuinaifenEstimate = DefaultEstimator('E6 Guinaifen S5 GNSW {:.0f}N {:.0f}E {:.0f}Q {:.1f}Dot'.format(numBasicGuinaifen, numSkillGuinaifen, numUltGuinaifen, numDotGuinaifen),
                                        GuinaifenRotation, GuinaifenCharacter, config, numDot=numDotGuinaifen)
    LukaEstimate = DefaultEstimator('E6 Luka S5 GNSW {:.0f}Enh {:.0f}S {:.0f}Q {:.1f}Dot'.format(numEnhancedLuka, numSkillLuka, numUltLuka, numDotLuka), 
                                    LukaRotation, LukaCharacter, config, numDot=numDotLuka)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([KafkaEstimate, GuinaifenEstimate, LukaEstimate, LuochaEstimate])