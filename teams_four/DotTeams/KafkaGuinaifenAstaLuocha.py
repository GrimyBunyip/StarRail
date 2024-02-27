from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.harmony.Asta import Asta
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

def KafkaGuinaifenAstaLuocha(config):
    #%% Kafka Guinaifen Asta Luocha Characters
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

    AstaCharacter = Asta(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'ATK.percent'],
                                    substats = {'EHR': 8, 'SPD.flat': 12, 'BreakEffect': 3, 'ATK.percent': 5}),
                                    lightcone = MemoriesOfThePast(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(uptime=0.5), planarset = FleetOfTheAgeless(),
                                    **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                                    **config)
    
    team = [KafkaCharacter, GuinaifenCharacter, AstaCharacter, LuochaCharacter]

    #%% Kafka Guinaifen Asta Luocha Team Buffs
    # Fleet of the Ageless Buff
    for character in [KafkaCharacter, GuinaifenCharacter, AstaCharacter]:
        character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)
    for character in [KafkaCharacter, GuinaifenCharacter, LuochaCharacter]:
        character.addStat('ATK.percent',description='Fleet Asta',amount=0.08)
        
    # Apply Guinaifen Debuff
    GuinaifenCharacter.applyFirekiss(team=team,uptime=1.0)
        
    # messenger 4 pc buffs:
    KafkaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0 / 3.0)
    GuinaifenCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0 / 3.0)
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0 / 4.0)

    # Asta Buffs
    AstaCharacter.applyChargingBuff(team)
    AstaCharacter.applyTraceBuff(team)
    AstaCharacter.applyUltBuff(team,rotation=3.0)

    # Asta Ignite Buff
    GuinaifenCharacter.addStat('DMG.fire',description='Kafka Trace',amount=0.18)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Kafka Guinaifen Asta Luocha Rotations
    numSkill = 3.0
    numTalent = 3.0
    numUlt = 1.0
    GuinaifenDot = GuinaifenCharacter.useDot()
    GuinaifenDot.energy = 0.0 # kafka shouldn't be getting energy for Guinaifen Dot
    AstaDot = AstaCharacter.useDot()
    AstaDot.energy = 0.0 # kafka shouldn't be getting energy for Guinaifen Dot
    extraDots = [ GuinaifenDot, AstaDot]
    extraDotsUlt = [ GuinaifenDot * KafkaCharacter.numEnemies, AstaDot * KafkaCharacter.numEnemies ]
    KafkaRotation = [
            KafkaCharacter.useSkill(extraDots=extraDots) * numSkill,
            KafkaCharacter.useTalent() * numTalent,
            KafkaCharacter.useUltimate(extraDots=extraDotsUlt) * numUlt,
    ]

    numSkillGuinaifen = 2.0
    numBasicGuinaifen = 2.0
    numUltGuinaifen = 1.0

    numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
    numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)

    GuinaifenRotation = [ # 
            GuinaifenCharacter.useSkill() * numSkillGuinaifen,
            GuinaifenCharacter.useBasic() * numBasicGuinaifen,
            GuinaifenCharacter.useUltimate() * numUltGuinaifen,
    ]

    numBasicAsta = 1.5
    numSkillAsta = 1.5
    AstaRotation = [AstaCharacter.useBasic() * numBasicAsta,
                    AstaCharacter.useSkill() * numSkillAsta,
                    AstaCharacter.useUltimate() * 1,]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast


    #%% Kafka Guinaifen Asta Luocha Rotation Math
    numDotGuinaifen = DotEstimator(GuinaifenRotation, GuinaifenCharacter, config, dotMode='alwaysBlast')
    numDotGuinaifen = min(numDotGuinaifen, 2.0 * numSkillGuinaifen * min(3.0, GuinaifenCharacter.numEnemies))

    totalKafkaEffect = sumEffects(KafkaRotation)
    totalGuinaifenEffect = sumEffects(GuinaifenRotation)
    totalAstaEffect = sumEffects(AstaRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
    GuinaifenRotationDuration = totalGuinaifenEffect.actionvalue * 100.0 / GuinaifenCharacter.getTotalStat('SPD')
    AstaRotationDuration = totalAstaEffect.actionvalue * 100.0 / AstaCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's rotation
    GuinaifenRotation = [x * KafkaRotationDuration / GuinaifenRotationDuration for x in GuinaifenRotation]
    AstaRotation = [x * KafkaRotationDuration / AstaRotationDuration for x in AstaRotation]
    LuochaRotation = [x * KafkaRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    numDotGuinaifen *= KafkaRotationDuration / GuinaifenRotationDuration

    KafkaEstimate = DefaultEstimator('Kafka {:.0f}E {:.0f}T {:.0f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDotKafka),
                                    KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
    GuinaifenEstimate = DefaultEstimator(f'E6 Guinaifen S{GuinaifenCharacter.lightcone.superposition:d} {GuinaifenCharacter.lightcone.name} {GuinaifenCharacter.firekissStacks:.0f}Firekiss {numBasicGuinaifen:.0f}N {numSkillGuinaifen:.0f}E {numUltGuinaifen:.0f}Q {numDotGuinaifen:.1f}Dot',
                                                                                                            GuinaifenRotation, GuinaifenCharacter, config, numDot=numDotGuinaifen)
    AstaEstimate = DefaultEstimator(f'Asta: {numBasicAsta:.1f}N {numSkillAsta:.1f}E 1Q, S{AstaCharacter.lightcone.superposition:d} {AstaCharacter.lightcone.name}', 
                                    AstaRotation, AstaCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([KafkaEstimate, GuinaifenEstimate, LuochaEstimate, AstaEstimate])