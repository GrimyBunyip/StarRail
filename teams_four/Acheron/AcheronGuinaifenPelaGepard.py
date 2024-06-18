from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Gepard import Gepard
from characters.nihility.Acheron import Acheron
from characters.nihility.Pela import Pela
from characters.nihility.Guinaifen import Guinaifen
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from lightCones.preservation.LandausChoice import LandausChoice
from lightCones.preservation.TrendOfTheUniversalMarket import TrendOfTheUniversalMarket
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.KnightOfPurityPalace import KnightOfPurityPalace2pc, KnightOfPurityPalace4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def AcheronGuinaifenPelaGepard(config):
    #%% Acheron Silver Wolf Pela Gepard Characters
    AcheronCharacter = Acheron(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'ATK.percent'],
                            substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Pioneer2pc(), relicsettwo = Pioneer4pc(),
                            planarset = IzumoGenseiAndTakamaDivineRealm(),
                            **config)

    GuinaifenCharacter = Guinaifen(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ER', 'DMG.fire'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'EHR': 4, 'BreakEffect': 4}),
                            lightcone = BeforeTheTutorialMissionStarts(**config),
                            relicsetone = Pioneer2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                            firekissStacks=2.0,
                            **config)

    PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                            substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
                            lightcone = ResolutionShinesAsPearlsOfSweat(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
                            **config)

    GepardCharacter = Gepard(RelicStats(mainstats = ['ER', 'SPD.flat', 'DEF.percent', 'DEF.percent'],
                            substats = {'DEF.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                            lightcone = TrendOfTheUniversalMarket(**config),
                            relicsetone = KnightOfPurityPalace2pc(), relicsettwo = KnightOfPurityPalace4pc(), planarset = BrokenKeel(),
                            **config)
    
    team = [AcheronCharacter, GuinaifenCharacter, PelaCharacter, GepardCharacter]

    #%% Acheron Silver Wolf Pela Gepard Team Buffs
    for character in [GuinaifenCharacter, AcheronCharacter, PelaCharacter]:
        character.addStat('CD',description='Broken Keel from Gepard',amount=0.1)
    for character in [GuinaifenCharacter, AcheronCharacter, GepardCharacter]:
        character.addStat('CD',description='Broken Keel from Pela',amount=0.1)

    # Pela Debuffs, 3 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotationDuration=3)
        
    # Resolution Shines as Pearls of Sweat uptime
    sweatUptime = (1.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
    sweatUptime += (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
    sweatUptime = min(1.0, sweatUptime)
    for character in [AcheronCharacter, GuinaifenCharacter, PelaCharacter, GepardCharacter]:
        character.addStat('DefShred',description='Resolution Sweat',
                        amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                        uptime=sweatUptime)
        
    # Apply Guinaifen Debuff
    GuinaifenCharacter.applyFirekiss(team=team,uptime=1.0)
    #%% Print Statements
    for character in team:
        character.print()

    #%% Acheron Silver Wolf Pela Gepard Rotations
    
    numStacks = (3.0/2.0) * GuinaifenCharacter.getTotalStat('SPD') # 3 guinaifen attacks per 2 turn rotation
    numStacks +=  1.0 * PelaCharacter.getTotalStat('SPD') # 3 pela attacks per 3 turn rotation
    numStacks += (1/7) * GepardCharacter.getTotalStat('SPD') # gepard occasionally skills, wolf skill is typically more valuable despite not giving +1 stack
    if GepardCharacter.lightcone.name == 'Trend of the Universal Market':
        enemyChanceToHitGepard = (6*4) / (6*4+4+4+4)
        numStacks += enemyChanceToHitGepard * GepardCharacter.numEnemies * GepardCharacter.enemySpeed # stacks from trend, assume each enemy does a single target per turn
    numStacks /= AcheronCharacter.getTotalStat('SPD')
    numStacks += 1 # Assume Acheron generates 1 stack when she skills
    
    numSkillAcheron = 9.0 / numStacks
    print(f"{numStacks * AcheronCharacter.getTotalStat('SPD'):.2f} stack rate")

    AcheronRotation = [ 
            AcheronCharacter.useSkill() * numSkillAcheron,
            AcheronCharacter.useUltimate_st() * 3,
            AcheronCharacter.useUltimate_aoe(num_stacks=3.0) * 3.0,
            AcheronCharacter.useUltimate_end(),
    ]

    numSkillGuinaifen = 2.0
    numBasicGuinaifen = 0.0
    numUltGuinaifen = 1.0

    GuinaifenRotation = [ # 
            GuinaifenCharacter.useSkill() * numSkillGuinaifen,
            GuinaifenCharacter.useBasic() * numBasicGuinaifen,
            GuinaifenCharacter.useUltimate() * numUltGuinaifen,
    ]

    numBasicPela = 3.0
    PelaRotation = [PelaCharacter.useBasic() * numBasicPela,
                    PelaCharacter.useUltimate(),]

    numBasicGepard = 3.0 * 6.0 / 7.0
    numSkillGepard = 3.0 * 1.0 / 7.0
    GepardRotation = [GepardCharacter.useBasic() * numBasicGepard,
                      GepardCharacter.useSkill() * numSkillGepard,
                      GepardCharacter.useUltimate() * 1,]

    #%% Acheron Silver Wolf Pela Gepard Rotation Math
    numDotGuinaifen = DotEstimator(GuinaifenRotation, GuinaifenCharacter, config, dotMode='alwaysBlast')

    totalAcheronEffect = sumEffects(AcheronRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalGuinaifenEffect = sumEffects(GuinaifenRotation)
    totalGepardEffect = sumEffects(GepardRotation)

    AcheronRotationDuration = totalAcheronEffect.actionvalue * 100.0 / AcheronCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    GuinaifenRotationDuration = totalGuinaifenEffect.actionvalue * 100.0 / GuinaifenCharacter.getTotalStat('SPD')
    GepardRotationDuration = totalGepardEffect.actionvalue * 100.0 / GepardCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Acheron: ',AcheronRotationDuration)
    print('Pela: ',PelaRotationDuration)
    print('Guinaifen: ',GuinaifenRotationDuration)
    print('Gepard: ',GepardRotationDuration)

    # Scale other character's rotation
    PelaRotation = [x * AcheronRotationDuration / PelaRotationDuration for x in PelaRotation]
    GuinaifenRotation = [x * AcheronRotationDuration / GuinaifenRotationDuration for x in GuinaifenRotation]
    GepardRotation = [x * AcheronRotationDuration / GepardRotationDuration for x in GepardRotation]

    AcheronEstimate = DefaultEstimator(f'Acheron E{AcheronCharacter.eidolon:d} S{AcheronCharacter.lightcone.superposition:d} {AcheronCharacter.lightcone.shortname}: {numSkillAcheron:.1f}E 1Q', AcheronRotation, AcheronCharacter, config)
    PelaEstimate = DefaultEstimator(f'Pela: 3N 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    GuinaifenEstimate = DefaultEstimator(f'E6 Guinaifen S{GuinaifenCharacter.lightcone.superposition:d} {GuinaifenCharacter.lightcone.name} {GuinaifenCharacter.firekissStacks:.0f} Firekiss {numBasicGuinaifen:.0f}N {numSkillGuinaifen:.0f}E {numUltGuinaifen:.0f}Q {numDotGuinaifen:.1f}Dot',
                                                                                                            GuinaifenRotation, GuinaifenCharacter, config, numDot=numDotGuinaifen)
    GepardEstimate = DefaultEstimator(f'Gepard: {numBasicGepard:.1f}N {numSkillGepard:.1f}E 1Q, S{GepardCharacter.lightcone.superposition:.0f} {GepardCharacter.lightcone.name}',
                                    GepardRotation, GepardCharacter, config)

    return([AcheronEstimate, GuinaifenEstimate, PelaEstimate, GepardEstimate])