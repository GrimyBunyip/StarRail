from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.nihility.Acheron import Acheron
from characters.nihility.Jiaoqiu import Jiaoqiu
from characters.harmony.Bronya import Bronya
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.nihility.AlongThePassingShore import AlongThePassingShore
from lightCones.nihility.EyesOfThePrey import EyesOfThePrey
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.PatienceIsAllYouNeed import PatienceIsAllYouNeed
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.PanCosmicCommercialEnterprise import PanCosmicCommercialEnterprise
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.FiresmithOfLavaForging import FiresmithOfLavaForging2pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def AcheronE2BronyaJiaoqiuGallagher(config, acheronSuperposition:int=0, jiaoqiuEidolon:int=None):
    #%% Acheron Bronya Jiaoqiu Gallagher Characters
    acheronLightCone = AlongThePassingShore(**config) if acheronSuperposition >= 1 else GoodNightAndSleepWell(**config)
    AcheronCharacter = Acheron(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'ATK.percent'],
                        substats = {'CR': 8, 'CD': 6, 'ATK.percent': 3, 'SPD.flat': 11}),
                        lightcone = acheronLightCone,
                        relicsetone = Pioneer2pc(), relicsettwo = Pioneer4pc(),
                        planarset = IzumoGenseiAndTakamaDivineRealm(),
                        eidolon=2,
                        **config)
    
    BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'HP.percent', 'CD', 'ER'],
                        substats = {'CD': 12, 'SPD.flat': 8, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = PastAndFuture(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

    JiaoqiuCharacter = Jiaoqiu(RelicStats(mainstats = ['DMG.fire', 'ATK.percent', 'EHR', 'ER'],
                        substats = {'ATK.flat': 3, 'SPD.flat': 5, 'EHR': 12, 'ATK.percent': 8}),
                        lightcone = EyesOfThePrey(**config),
                        relicsetone = Pioneer2pc(), relicsettwo = FiresmithOfLavaForging2pc(), planarset = SprightlyVonwacq(),
                        talentStacks=3 if jiaoqiuEidolon is not None and jiaoqiuEidolon >= 1 else 2,
                        eidolon=jiaoqiuEidolon,
                        **config)

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                        substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                        **config)
    
    team = [AcheronCharacter, BronyaCharacter, JiaoqiuCharacter, GallagherCharacter]

    #%% Acheron Bronya Jiaoqiu Gallagher Team Buffs
    for character in [JiaoqiuCharacter, AcheronCharacter, GallagherCharacter]:
        character.addStat('CD',description='Broken Keel from Bronya',amount=0.1)
        
    # Bronya Messenger 4 pc
    for character in [AcheronCharacter, JiaoqiuCharacter, GallagherCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)

    # Jiaoqiu Debuffs, 3 turn Jiaoqiu rotation
    JiaoqiuCharacter.applyTalentDebuff(team)
    jiaoqiuUltUptime = 0.75
    JiaoqiuCharacter.applyUltDebuff(team, uptime=jiaoqiuUltUptime)
        
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    BronyaCharacter.applyUltBuff(AcheronCharacter,uptime=0.25) # only get Bronya ult buff every 4 bronya turns
    BronyaCharacter.applyUltBuff(JiaoqiuCharacter,uptime=0.5) # only get Bronya ult buff every 4 bronya turns
    BronyaCharacter.applyUltBuff(GallagherCharacter,uptime=0.5) # only get Bronya ult buff every 4 bronya turns
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)
      
    #%% Print Statements
    for character in team:
        character.print()

    #%% Acheron Bronya Jiaoqiu Gallagher Rotations
    
    numStacks =  (4.0 / 3.0) * JiaoqiuCharacter.getTotalStat('SPD') # 4 Jiaoqiu attacks per 3 turn rotation
    numStacks += 1.25 * (2/4) * GallagherCharacter.getTotalStat('SPD') # 1.25 from multiplication, 2 debuffs per 4 turn rotation
    jiaoqiuUltChance = 1.0 * 0.6 * (0.62 if JiaoqiuCharacter.eidolon >= 5 else 0.60)
    jiaoqiuUltChance *= 1.0 + JiaoqiuCharacter.getTotalStat('EHR')
    jiaoqiuUltChance = min(1.0, jiaoqiuUltChance)
    numStacks += jiaoqiuUltUptime * jiaoqiuUltChance * JiaoqiuCharacter.numEnemies * JiaoqiuCharacter.enemySpeed # stacks from trend, assume each enemy does a single target per turn
    numStacks *= 0.5 # halve the stacks from outside of Acheron because of Bronya
    numStacks /= BronyaCharacter.getTotalStat('SPD')
    numStacks += 1 + 1
    numStacks += 1 if AcheronCharacter.lightcone.name == 'Along the Passing Shore' else 0
    
    numStacksSkill = 9.0
    numSkillAcheron = numStacksSkill / numStacks
    numBasicAcheron = (9.0 - numStacksSkill) / (numStacks - 1.0)
    print(f"{numStacks * AcheronCharacter.getTotalStat('SPD'):.2f} stack rate")

    AcheronRotation = []

    AcheronRotation += [AcheronCharacter.useSkill() * numSkillAcheron * 0.5,
                        AcheronCharacter.useBasic() * numBasicAcheron * 0.5,] # half of acheron skills will not be bronya buffed
    
    BronyaCharacter.applySkillBuff(AcheronCharacter,uptime=1.0)
    AcheronCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition)
    AcheronRotation += [AcheronCharacter.useSkill() * numSkillAcheron * 0.5]
    AcheronRotation += [AcheronCharacter.useBasic() * numBasicAcheron * 0.5]
    AcheronRotation += [AcheronCharacter.useUltimate_st() * 3]
    AcheronRotation += [AcheronCharacter.useUltimate_aoe(num_stacks=3.0) * 3.0]
    AcheronRotation += [AcheronCharacter.useUltimate_end()]
    AcheronRotation += [BronyaCharacter.useAdvanceForward() * numSkillAcheron * 0.5] # Half of the turns

    numBasicJiaoqiu = 4.0
    numSkillJiaoqiu = 0.0
    JiaoqiuRotation = [JiaoqiuCharacter.useBasic() * numBasicJiaoqiu,
                       JiaoqiuCharacter.useSkill() * numSkillJiaoqiu,
                        JiaoqiuCharacter.useUltimate(),]

    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    numBasicGallagher = 4.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1,]
    if GallagherCharacter.lightcone.name == 'Multiplication':
        GallagherRotation[-1].actionvalue += 0.20 # advance foward cannot exceed a certain amount

    #%% Acheron Bronya Jiaoqiu Gallagher Rotation Math
    numDotJiaoqiu = DotEstimator(JiaoqiuRotation, JiaoqiuCharacter, config, dotMode='alwaysAll') * jiaoqiuUltUptime

    totalAcheronEffect = sumEffects(AcheronRotation)
    totalJiaoqiuEffect = sumEffects(JiaoqiuRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    AcheronRotationDuration = totalAcheronEffect.actionvalue * 100.0 / AcheronCharacter.getTotalStat('SPD')
    JiaoqiuRotationDuration = totalJiaoqiuEffect.actionvalue * 100.0 / JiaoqiuCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Acheron: ',AcheronRotationDuration)
    print('Jiaoqiu: ',JiaoqiuRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    JiaoqiuRotation = [x * AcheronRotationDuration / JiaoqiuRotationDuration for x in JiaoqiuRotation]
    BronyaRotation = [x * AcheronRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    GallagherRotation = [x * AcheronRotationDuration / GallagherRotationDuration for x in GallagherRotation]

    AcheronEstimate = DefaultEstimator(f'Acheron E{AcheronCharacter.eidolon:d} S{AcheronCharacter.lightcone.superposition:d} {AcheronCharacter.lightcone.shortname}: {numBasicAcheron:.1f}N {numSkillAcheron:.1f}E{numSkillAcheron:.1f}E 1Q', AcheronRotation, AcheronCharacter, config)
    JiaoqiuEstimate = DefaultEstimator(f'Jiaoqiu E{JiaoqiuCharacter.eidolon:d}: {numBasicJiaoqiu:.0f}N {numSkillJiaoqiu:.0f}E 1Q {JiaoqiuCharacter.talentStacks:.0f} Roasts, S{JiaoqiuCharacter.lightcone.superposition:d} {JiaoqiuCharacter.lightcone.name}', 
                                    JiaoqiuRotation, JiaoqiuCharacter, config, numDot=numDotJiaoqiu)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    GallagherEstimate = DefaultEstimator(f'Gallagher: {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q, S{GallagherCharacter.lightcone.superposition:d} {GallagherCharacter.lightcone.name}', 
                                    GallagherRotation, GallagherCharacter, config)

    return([AcheronEstimate, BronyaEstimate, JiaoqiuEstimate, GallagherEstimate])