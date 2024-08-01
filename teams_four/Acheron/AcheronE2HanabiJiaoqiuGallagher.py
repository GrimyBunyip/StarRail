from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.nihility.Acheron import Acheron
from characters.nihility.Jiaoqiu import Jiaoqiu
from characters.harmony.Hanabi import Hanabi
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.nihility.AlongThePassingShore import AlongThePassingShore
from lightCones.nihility.EyesOfThePrey import EyesOfThePrey
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.FiresmithOfLavaForging import FiresmithOfLavaForging2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def AcheronE2HanabiJiaoqiuGallagher(config, acheronSuperposition:int=0, jiaoqiuEidolon:int=None):
    #%% Acheron Hanabi Jiaoqiu Gallagher Characters
    acheronLightCone = GoodNightAndSleepWell(**config) if acheronSuperposition == 0 else AlongThePassingShore(superposition=acheronSuperposition,**config)
    AcheronCharacter = Acheron(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'ATK.percent'],
                            substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'ATK.flat': 3}),
                            lightcone = acheronLightCone,
                            relicsetone = Pioneer2pc(), relicsettwo = Pioneer4pc(),
                            planarset = IzumoGenseiAndTakamaDivineRealm(),
                            eidolon=2,
                            **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'SPD.flat', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'RES': 5, 'DEF.percent': 3}),
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
    
    team = [AcheronCharacter, HanabiCharacter, JiaoqiuCharacter, GallagherCharacter]

    #%% Acheron Hanabi Jiaoqiu Gallagher Team Buffs
    for character in [JiaoqiuCharacter, AcheronCharacter, GallagherCharacter]:
        character.addStat('CD',description='Broken Keel from Hanabi',amount=0.1)
        
    # Hanabi Messenger 4 pc
    for character in [AcheronCharacter, JiaoqiuCharacter, GallagherCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)

    # Jiaoqiu Debuffs, 3 turn Jiaoqiu rotation
    JiaoqiuCharacter.applyTalentDebuff(team)
    JiaoqiuCharacter.applyUltDebuff(team)

    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=AcheronCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=3.0/3.0)
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)  
    #%% Print Statements
    for character in team:
        character.print()

    #%% Acheron Hanabi Jiaoqiu Gallagher Rotations
    
    numStacks =  (4.0 / 3.0) * JiaoqiuCharacter.getTotalStat('SPD') # 4 Jiaoqiu attacks per 3 turn rotation
    numStacks += 1.25 * (2/4) * GallagherCharacter.getTotalStat('SPD') # 1.25 from multiplication, 2 debuffs per 4 turn rotation
    jiaoqiuUltChance = 1.0 * 0.6 * (0.62 if JiaoqiuCharacter.eidolon >= 5 else 0.60)
    jiaoqiuUltChance *= 1.0 + JiaoqiuCharacter.getTotalStat('EHR')
    jiaoqiuUltChance = min(1.0, jiaoqiuUltChance)
    numStacks += jiaoqiuUltChance * JiaoqiuCharacter.numEnemies * JiaoqiuCharacter.enemySpeed # stacks from trend, assume each enemy does a single target per turn
    numStacks /= HanabiCharacter.getTotalStat('SPD')
    numStacks += 1 + 1
    numStacks += 1 if AcheronCharacter.lightcone.name == 'Along the Passing Shore' else 0
        
    numSkillAcheron = 9.0 / numStacks
    print(f"{numStacks * AcheronCharacter.getTotalStat('SPD'):.2f} stack rate")

    AcheronRotation = [ 
            AcheronCharacter.useSkill() * numSkillAcheron,
            AcheronCharacter.useUltimate_st() * 3,
            AcheronCharacter.useUltimate_aoe(num_stacks=3.0) * 3.0,
            AcheronCharacter.useUltimate_end(),
            HanabiCharacter.useAdvanceForward(advanceAmount=1.0 - AcheronCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')) * numSkillAcheron,
    ]
    
    numBasicJiaoqiu = 1.0
    numSkillJiaoqiu = 2.0
    JiaoqiuRotation = [JiaoqiuCharacter.useBasic() * numBasicJiaoqiu,
                       JiaoqiuCharacter.useSkill() * numSkillJiaoqiu,
                       JiaoqiuCharacter.useUltimate(),]

    numBasicHanabi = 0.0
    numSkillHanabi = 3.0 # let's say half the time, huohuo can shave off a turn
    HanabiRotation = [HanabiCharacter.useBasic() * numBasicHanabi,
                       HanabiCharacter.useSkill() * numSkillHanabi,
                    HanabiCharacter.useUltimate()]

    numBasicGallagher = 4.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1,]
    if GallagherCharacter.lightcone.name == 'Multiplication':
        GallagherRotation[-1].actionvalue += 0.20 # advance foward cannot exceed a certain amount

    #%% Acheron Hanabi Jiaoqiu Gallagher Rotation Math
    numDotJiaoqiu = DotEstimator(JiaoqiuRotation, JiaoqiuCharacter, config, dotMode='alwaysAll')

    totalAcheronEffect = sumEffects(AcheronRotation)
    totalJiaoqiuEffect = sumEffects(JiaoqiuRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    AcheronRotationDuration = totalAcheronEffect.actionvalue * 100.0 / AcheronCharacter.getTotalStat('SPD')
    JiaoqiuRotationDuration = totalJiaoqiuEffect.actionvalue * 100.0 / JiaoqiuCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Acheron: ',AcheronRotationDuration)
    print('Jiaoqiu: ',JiaoqiuRotationDuration)
    print('Hanabi: ',HanabiRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    JiaoqiuRotation = [x * AcheronRotationDuration / JiaoqiuRotationDuration for x in JiaoqiuRotation]
    HanabiRotation = [x * AcheronRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    GallagherRotation = [x * AcheronRotationDuration / GallagherRotationDuration for x in GallagherRotation]

    AcheronEstimate = DefaultEstimator(f'Acheron E{AcheronCharacter.eidolon:d} S{AcheronCharacter.lightcone.superposition:d} {AcheronCharacter.lightcone.shortname}: {numSkillAcheron:.1f}E 1Q', AcheronRotation, AcheronCharacter, config)
    JiaoqiuEstimate = DefaultEstimator(f'Jiaoqiu E{numSkillJiaoqiu:.0f}: {numBasicJiaoqiu:.0f}N {numSkillJiaoqiu:.0f}E 1Q {JiaoqiuCharacter.talentStacks:.0f} Roasts, S{JiaoqiuCharacter.lightcone.superposition:d} {JiaoqiuCharacter.lightcone.name}', 
                                    JiaoqiuRotation, JiaoqiuCharacter, config, numDot=numDotJiaoqiu)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    GallagherEstimate = DefaultEstimator(f'{GallagherCharacter.fullName()} {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q', 
                                    GallagherRotation, GallagherCharacter, config)

    return([AcheronEstimate, HanabiEstimate, JiaoqiuEstimate, GallagherEstimate])