from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.nihility.Guinaifen import Guinaifen
from characters.nihility.Kafka import Kafka
from characters.nihility.Sampo import Sampo
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc

def KafkaGuinaifenSampoLuocha(config):
    #%% Kafka Guinaifen Sampo Luocha
    KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'BreakEffect': 5, 'ATK.flat': 3}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=1),
                            **config)

    GuinaifenCharacter = Guinaifen(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.fire'],
                            substats = {'ATK.percent': 7, 'SPD.flat': 13, 'EHR': 4, 'BreakEffect': 4}),
                            lightcone = ResolutionShinesAsPearlsOfSweat(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    # I'm just going to assume 100% uptime on firmament frontline glamoth
    # Kafka and Guinaifen are a few substats short of base 160 with a 12 substat cap
    # But I'll just generously assume you are able to get there

    SampoCharacter = Sampo(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.wind'],
                                    substats = {'ATK.percent': 5, 'SPD.flat': 12, 'EHR': 8, 'BreakEffect': 3}),
                                    lightcone = GoodNightAndSleepWell(**config),
                                    relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                                    **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                                    **config)
    
    team = [KafkaCharacter, GuinaifenCharacter, SampoCharacter, LuochaCharacter]

    #%% Kafka Guinaifen Sampo Luocha Team Buffs
    # Fleet of the Ageless Buff
    for character in [KafkaCharacter, GuinaifenCharacter, SampoCharacter]:
        character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)
        
    # Apply Guinaifen Debuff
    GuinaifenCharacter.applyFirekiss(team=team,uptime=1.0)

    # Resolution Shines as Pearls of Sweat uptime
    sweatUptime = (3.0 / 4.0) * GuinaifenCharacter.getTotalStat('SPD') / GuinaifenCharacter.enemySpeed # 2 skills and an ult
    sweatUptime += (1.0 / 4.0) * GuinaifenCharacter.getTotalStat('SPD') / GuinaifenCharacter.enemySpeed / GuinaifenCharacter.numEnemies # 1 basic (ignore the other basic)
    sweatUptime = min(1.0, sweatUptime)
    for character in team:
        character.addStat('DefShred',description='Resolution Sweat',
                        amount=0.11 + 0.01 * GuinaifenCharacter.lightcone.superposition,
                        uptime=sweatUptime)
        
    # Apply Sampo Vulnerability Debuff
    SampoCharacter.applyUltDebuff(team,rotationDuration=4.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Kafka Guinaifen Sampo Luocha Rotations
    numSkill = 3.0
    numTalent = 3.0
    numUlt = 1.0
    GuinaifenDot = GuinaifenCharacter.useDot()
    GuinaifenDot.energy = 0.0 # kafka shouldn't be getting energy for Guinaifen Dot
    SampoDot = SampoCharacter.useDot()
    SampoDot.energy = 0.0
    extraDots = [ GuinaifenDot, SampoDot ]
    extraDotsUlt = [ GuinaifenDot * KafkaCharacter.numEnemies, SampoDot * KafkaCharacter.numEnemies ]
    KafkaRotation = [
            KafkaCharacter.useSkill(extraDots=extraDots) * numSkill,
            KafkaCharacter.useTalent() * numTalent,
            KafkaCharacter.useUltimate(extraDots=extraDotsUlt) * numUlt,
    ]

    numBasicGuinaifen = 2.0
    numSkillGuinaifen = 2.0
    numUltGuinaifen = 1.0
    GuinaifenRotation = [ # 
            GuinaifenCharacter.useBasic() * numBasicGuinaifen,
            GuinaifenCharacter.useSkill() * numSkillGuinaifen,
            GuinaifenCharacter.useUltimate() * numUlt,
    ]

    numBasicSampo = 2
    numSkillSampo = 2
    numUltSampo = 1
    SampoRotation = [
                    SampoCharacter.useBasic() * numBasicSampo,
                    SampoCharacter.useSkill() * numSkillSampo,
                    SampoCharacter.useUltimate() * numUltSampo]
        
    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast


    #%% Kafka Guinaifen Sampo Luocha Rotation Math
    numDotGuinaifen = DotEstimator(GuinaifenRotation, GuinaifenCharacter, config, dotMode='alwaysBlast')
    numDotGuinaifen = min(numDotGuinaifen, 2.0 * numSkillGuinaifen * min(3.0, GuinaifenCharacter.numEnemies))
    numDotSampo = DotEstimator(SampoRotation, SampoCharacter, config, dotMode='alwaysBlast')
    numDotSampo = min(numDotSampo, 3.0 * (numSkillSampo + numUltSampo) * SampoCharacter.numEnemies)
    numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
    numDotKafka = min(numDotKafka, 2 * numUlt * KafkaCharacter.numEnemies + 2 * numTalent)

    totalKafkaEffect = sumEffects(KafkaRotation)
    totalGuinaifenEffect = sumEffects(GuinaifenRotation)
    totalSampoEffect = sumEffects(SampoRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
    GuinaifenRotationDuration = totalGuinaifenEffect.actionvalue * 100.0 / GuinaifenCharacter.getTotalStat('SPD')
    SampoRotationDuration = totalSampoEffect.actionvalue * 100.0 / SampoCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's character's rotation
    GuinaifenRotation = [x * KafkaRotationDuration / GuinaifenRotationDuration for x in GuinaifenRotation]
    SampoRotation = [x * KafkaRotationDuration / SampoRotationDuration for x in SampoRotation]
    LuochaRotation = [x * KafkaRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    numDotGuinaifen *= KafkaRotationDuration / GuinaifenRotationDuration
    numDotSampo *= KafkaRotationDuration / SampoRotationDuration

    KafkaEstimate = DefaultEstimator('Kafka {:.0f}E {:.0f}T {:.0f}Q {:.1f}Dot'.format(numSkill, numTalent, numUlt, numDotKafka),
                                    KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
    GuinaifenEstimate = DefaultEstimator(f'E6 Guinaifen S{GuinaifenCharacter.lightcone.superposition:d} {GuinaifenCharacter.lightcone.name} {GuinaifenCharacter.firekissStacks:.0f}Firekiss {numBasicGuinaifen:.0f}N {numSkillGuinaifen:.0f}E {numUltGuinaifen:.0f}Q {numDotGuinaifen:.1f}Dot',
                                                                                                            GuinaifenRotation, GuinaifenCharacter, config, numDot=numDotGuinaifen)
    SampoEstimate = DefaultEstimator('Sampo S{:.0f} {} {:.0f}N {:.0f}E {:.0f}Q {:.1f}Dot'.format(SampoCharacter.lightcone.superposition, SampoCharacter.lightcone.name, 
                                                                                                numBasicSampo, numSkillSampo, numUltSampo, numDotSampo), 
                                                                                                SampoRotation, SampoCharacter, config, numDot=numDotSampo)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([KafkaEstimate, GuinaifenEstimate, SampoEstimate, LuochaEstimate])