from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.nihility.Acheron import Acheron
from characters.nihility.Jiaoqiu import Jiaoqiu
from characters.nihility.Pela import Pela
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.nihility.AlongThePassingShore import AlongThePassingShore
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.nihility.EyesOfThePrey import EyesOfThePrey
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.PanCosmicCommercialEnterprise import PanCosmicCommercialEnterprise
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.FiresmithOfLavaForging import FiresmithOfLavaForging2pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def AcheronPelaJiaoqiuGallagher(config, acheronEidolon:int=None, acheronSuperposition:int=0):
    #%% Acheron Silver Wolf Jiaoqiu Gallagher Characters
    acheronLightCone = GoodNightAndSleepWell(**config) if acheronSuperposition == 0 else AlongThePassingShore(superposition=acheronSuperposition,**config)
    AcheronCharacter = Acheron(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'ATK.percent'],
                            substats = {'CR': 10, 'CD': 10, 'ATK.percent': 5, 'SPD.flat': 4}),
                            lightcone = acheronLightCone,
                            relicsetone = Pioneer2pc(), relicsettwo = Pioneer4pc(),
                            planarset = IzumoGenseiAndTakamaDivineRealm(),
                            eidolon = acheronEidolon,
                            **config)

    PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                            substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
                            lightcone = ResolutionShinesAsPearlsOfSweat(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
                            **config)

    JiaoqiuCharacter = Jiaoqiu(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'EHR', 'ER'],
                            substats = {'CD': 3, 'CR': 5, 'EHR': 12, 'SPD.flat': 8}),
                            lightcone = BeforeTheTutorialMissionStarts(**config),
                            relicsetone = Pioneer2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PanCosmicCommercialEnterprise(),
                            **config)

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                            substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                            lightcone = Multiplication(**config),
                            relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = PenaconyLandOfDreams(),
                            **config)
    
    team = [AcheronCharacter, PelaCharacter, JiaoqiuCharacter, GallagherCharacter]

    #%% Acheron Silver Wolf Jiaoqiu Gallagher Team Buffs
    for character in [JiaoqiuCharacter, AcheronCharacter, GallagherCharacter]:
        character.addStat('CD',description='Broken Keel from Pela',amount=0.1)
    for character in [JiaoqiuCharacter, AcheronCharacter, PelaCharacter]:
        character.addStat('DMG.fire',description='Penacony from Gallagher',amount=0.1)

    # Jiaoqiu Debuffs, 3 turn Jiaoqiu rotation
    JiaoqiuCharacter.applyTalentDebuff(team)
    JiaoqiuCharacter.applyUltDebuff(team)

    # Pela Debuffs, 3 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotationDuration=2)
        
    # Resolution Shines as Pearls of Sweat uptime
    sweatUptime = (1.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
    sweatUptime += (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
    sweatUptime = min(1.0, sweatUptime)
    for character in [AcheronCharacter, JiaoqiuCharacter, PelaCharacter, GallagherCharacter]:
        character.addStat('DefShred',description='Resolution Sweat',
                        amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                        uptime=sweatUptime)
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)
        
    #%% Print Statements
    for character in team:
        character.print()

    #%% Acheron Silver Wolf Jiaoqiu Gallagher Rotations
    
    numStacks =  (3.0 / 2.0) * PelaCharacter.getTotalStat('SPD') # 3 pela attacks per 2 turn rotation
    numStacks +=  (4.0 / 3.0) * JiaoqiuCharacter.getTotalStat('SPD') # 4 Jiaoqiu attacks per 3 turn rotation
    numStacks += 1.25 * (2/4) * GallagherCharacter.getTotalStat('SPD') # 1.25 from multiplication, 2 debuffs per 4 turn rotation
    jiaoqiuUltChance = 1.0 * 0.6 * (0.62 if JiaoqiuCharacter.eidolon >= 5 else 0.60)
    jiaoqiuUltChance *= 1.0 + JiaoqiuCharacter.getTotalStat('EHR')
    jiaoqiuUltChance = min(1.0, jiaoqiuUltChance)
    enemyActionRate = JiaoqiuCharacter.numEnemies * JiaoqiuCharacter.enemySpeed
    jiaoqiuUltRate = 6.0 * JiaoqiuCharacter.getTotalStat('SPD') / 3.0
    jiaoqiuStackRate = min(jiaoqiuUltRate, enemyActionRate)
    numStacks += jiaoqiuUltChance * jiaoqiuStackRate # stacks from trend, assume each enemy does a single target per turn
    numStacks /= AcheronCharacter.getTotalStat('SPD')
    numStacks += 1 # Assume Acheron generates 1 stack when she skills
    numStacks += 1 if acheronEidolon is not None and acheronEidolon >= 2 else 0
    numStacks += 1 if AcheronCharacter.lightcone.name == 'Along the Passing Shore' else 0
    
    numSkillAcheron = 9.0 / numStacks

    AcheronRotation = [ 
            AcheronCharacter.useSkill() * numSkillAcheron,
            AcheronCharacter.useUltimate_st() * 3,
            AcheronCharacter.useUltimate_aoe(num_stacks=3.0) * 3.0,
            AcheronCharacter.useUltimate_end(),
    ]

    numSkillPela = 2.0
    PelaRotation = [PelaCharacter.useSkill() * numSkillPela,
                    PelaCharacter.useUltimate(),]

    numBasicJiaoqiu = 3.0
    numSkillJiaoqiu = 0.0
    JiaoqiuRotation = [JiaoqiuCharacter.useBasic() * numBasicJiaoqiu,
                       JiaoqiuCharacter.useSkill() * numSkillJiaoqiu,
                        JiaoqiuCharacter.useUltimate(),]

    numBasicGallagher = 4.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1,]
    if GallagherCharacter.lightcone.name == 'Multiplication':
        GallagherRotation[-1].actionvalue += 0.20 # advance foward cannot exceed a certain amount

    #%% Acheron Silver Wolf Jiaoqiu Gallagher Rotation Math
    numDotJiaoqiu = DotEstimator(JiaoqiuRotation, JiaoqiuCharacter, config, dotMode='alwaysAll')

    totalAcheronEffect = sumEffects(AcheronRotation)
    totalJiaoqiuEffect = sumEffects(JiaoqiuRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    AcheronRotationDuration = totalAcheronEffect.actionvalue * 100.0 / AcheronCharacter.getTotalStat('SPD')
    JiaoqiuRotationDuration = totalJiaoqiuEffect.actionvalue * 100.0 / JiaoqiuCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Acheron: ',AcheronRotationDuration)
    print('Jiaoqiu: ',JiaoqiuRotationDuration)
    print('Pela: ',PelaRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    JiaoqiuRotation = [x * AcheronRotationDuration / JiaoqiuRotationDuration for x in JiaoqiuRotation]
    PelaRotation = [x * AcheronRotationDuration / PelaRotationDuration for x in PelaRotation]
    GallagherRotation = [x * AcheronRotationDuration / GallagherRotationDuration for x in GallagherRotation]

    AcheronEstimate = DefaultEstimator(f'Acheron E{AcheronCharacter.eidolon:d} S{AcheronCharacter.lightcone.superposition:d} {AcheronCharacter.lightcone.name}: {numSkillAcheron:.1f}E 1Q', AcheronRotation, AcheronCharacter, config)
    JiaoqiuEstimate = DefaultEstimator(f'Jiaoqiu: {numBasicJiaoqiu:.0f}N {numSkillJiaoqiu:.0f}E 1Q {JiaoqiuCharacter.talentStacks:.0f} Roasts, S{JiaoqiuCharacter.lightcone.superposition:d} {JiaoqiuCharacter.lightcone.name}', 
                                    JiaoqiuRotation, JiaoqiuCharacter, config, numDot=numDotJiaoqiu)
    PelaEstimate = DefaultEstimator(f'Pela: 2E 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    GallagherEstimate = DefaultEstimator(f'Gallagher: {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q, S{GallagherCharacter.lightcone.superposition:d} {GallagherCharacter.lightcone.name}', 
                                    GallagherRotation, GallagherCharacter, config)

    return([AcheronEstimate, PelaEstimate, JiaoqiuEstimate, GallagherEstimate])