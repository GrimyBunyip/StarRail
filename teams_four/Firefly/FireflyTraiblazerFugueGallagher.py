from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.destruction.Firefly import Firefly
from characters.nihility.Fugue import Fugue
from characters.harmony.ImaginaryTrailblazer import ImaginaryTrailblazer
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.destruction.WhereaboutsShouldDreamsRest import WhereaboutsShouldDreamsRest
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.nihility.LongRoadLeadsHome import LongRoadLeadsHome
from lightCones.nihility.SolitaryHealing import SolitaryHealing
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.IronCavalryAgainstTheScourge import IronCavalryAgainstTheScourge2pc, IronCavalryAgainstTheScourge4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc
from relicSets.relicSets.WatchmakerMasterOfDreamMachinations import Watchmaker2pc, Watchmaker4pc

def FireflyTrailblazerFugueGallagher(config,
                                       fireflyEidolon:int=None,
                                       fireflySuperposition:int=0,
                                       fugueEidolon:int=None,
                                       fugueCone:str='SolitaryHealing'):
    #%% Firefly Trailblazer Fugue Gallagher Characters
    
    fireflyLightcone = OnTheFallOfAnAeon(**config,uptime=1.0) if fireflySuperposition == 0 else WhereaboutsShouldDreamsRest(superposition=fireflySuperposition, **config)
    FireflyCharacter = Firefly(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'SPD.flat', 'BreakEffect'],
                                    substats = {'SPD.flat': 12, 'ATK.flat': 3, 'BreakEffect': 8, 'ATK.percent': 5}),
                                    lightcone = fireflyLightcone,
                                    eidolon = fireflyEidolon,
                                    relicsetone = IronCavalryAgainstTheScourge2pc(), relicsettwo = IronCavalryAgainstTheScourge4pc(), planarset = ForgeOfTheKalpagniLantern(),
                                    **config)

    TrailblazerCharacter = ImaginaryTrailblazer(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'BreakEffect'],
                                    substats = {'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5, 'DEF.percent': 3}),
                                    lightcone = DanceDanceDance(**config),
                                    relicsetone = Watchmaker2pc(), relicsettwo = Watchmaker4pc(uptime=0.0), planarset = ForgeOfTheKalpagniLantern(),
                                    **config)

    if fugueCone == 'SolitaryHealing':
        FugueLightCone = SolitaryHealing(**config)
    elif fugueCone == 'LongRoadLeadsHome':
        FugueLightCone = LongRoadLeadsHome(**config)
    FugueCharacter = Fugue(RelicStats(mainstats = ['EHR', 'SPD.flat', 'DEF.percent', 'ER'],
                                    substats = {'EHR': 5, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 3}),
                                    lightcone = FugueLightCone,
                                    eidolon = fugueEidolon,
                                    relicsetone = IronCavalryAgainstTheScourge2pc(), relicsettwo = IronCavalryAgainstTheScourge4pc(), planarset = ForgeOfTheKalpagniLantern(),
                                    **config)
    
    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                                    substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = IronCavalryAgainstTheScourge2pc(), relicsettwo = IronCavalryAgainstTheScourge4pc(), planarset = SprightlyVonwacq(),
                                    **config)
    
    team = [FireflyCharacter, TrailblazerCharacter, FugueCharacter, GallagherCharacter]

    #%% Firefly Trailblazer Fugue Gallagher Team Buffs
    for character in team:
        watchmakerUptime = 0.66 if FireflyCharacter.eidolon == 0 else 1.0
        character.addStat('BreakEffect',description='Watchmaker 4pc', amount=0.30, uptime=watchmakerUptime)

    # Trailblazer Vulnerability Buff
    TrailblazerCharacter.applyUltBuff(team=team)
    TrailblazerCharacter.applyE4Buff(team=team)
    
    # Fugue Skill Buff
    FugueCharacter.applySkillBuff(FireflyCharacter)
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)

    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
    for character in team:
        character.print()

    #%% Firefly Trailblazer Fugue Gallagher Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long

    numSkillFirefly = 2.0
    numEnhancedFirefly = 4.0
    numUltFirefly = 1.0
    fireflySpd = FireflyCharacter.getTotalStat('SPD')
    fireflySpdMod = 1.0 - fireflySpd / (fireflySpd + (65.0 if FireflyCharacter.eidolon >= 5 else 60.0))
    fireflySpdMod *= numEnhancedFirefly
    FireflyRotation = [ 
            FireflyCharacter.useSkill() * numSkillFirefly,
            FireflyCharacter.useUltimate() * numUltFirefly,
            FireflyCharacter.extraTurn(), # advance from ult
            FireflyCharacter.extraTurn() * 0.25 * (numSkillFirefly - 1.0), # advance from skill
            FireflyCharacter.extraTurn() * fireflySpdMod # advance from speed boost
    ]
    TrailblazerRotationFirefly = [
            TrailblazerCharacter.useSuperBreak(character=FireflyCharacter, 
                                               baseGauge=FireflyCharacter.useSkill().gauge,
                                               extraTypes=['skill']) * numSkillFirefly,        
    ]
    FugueRotationFirefly = [
            FugueCharacter.useSuperBreak(character=FireflyCharacter, 
                                               baseGauge=FireflyCharacter.useSkill().gauge,
                                               extraTypes=['skill']) * numSkillFirefly,    
    ]

    FireflyCharacter.applyUltVulnerability()
    numEnhancedFirefly *= 1.5 if FireflyCharacter.eidolon >= 2.0 else 1.0
    FireflyRotation += [FireflyCharacter.useEnhancedSkill() * numEnhancedFirefly]
    FireflyRotation[-1].actionvalue *= 2.0 / 3.0 if FireflyCharacter.eidolon >= 2 else 1.0
    FireflyRotation += [FireflyCharacter.useSuperBreak(baseGauge=FireflyCharacter.useEnhancedSkill().gauge,
                                                       extraTypes=['skill','enhancedSkill']) * numEnhancedFirefly]
    TrailblazerRotationFirefly += [TrailblazerCharacter.useSuperBreak(character=FireflyCharacter, 
                                                                      baseGauge=FireflyCharacter.useEnhancedSkill().gauge,
                                                                      extraTypes=['skill','enhancedSkill']) * numEnhancedFirefly]
    FugueRotationFirefly += [FugueCharacter.useSuperBreak(character=FireflyCharacter, 
                                                                      baseGauge=FireflyCharacter.useEnhancedSkill().gauge,
                                                                      extraTypes=['skill','enhancedSkill']) * numEnhancedFirefly]

    numBasicTrailblazer = 1.0 if FireflyCharacter.eidolon == 0 else 0.0
    numSkillTrailblazer = 2.0
    TrailblazerRotation = [ # 130 max energy
            TrailblazerCharacter.useBasic() * numBasicTrailblazer,
            TrailblazerCharacter.useSkill() * numSkillTrailblazer,
            TrailblazerCharacter.useUltimate(),
            TrailblazerCharacter.useSuperBreak(character=TrailblazerCharacter, 
                                               baseGauge=TrailblazerCharacter.useBasic().gauge,
                                               extraTypes=['basic']) * numBasicTrailblazer,
            TrailblazerCharacter.useSuperBreak(character=TrailblazerCharacter,
                                               baseGauge=TrailblazerCharacter.useSkill().gauge,
                                               extraTypes=['skill']) * numSkillTrailblazer,
    ]
    FugueRotationTrailblazer = [
            FugueCharacter.useSuperBreak(character=TrailblazerCharacter, 
                                               baseGauge=TrailblazerCharacter.useBasic().gauge,
                                               extraTypes=['basic']) * numBasicTrailblazer,
            FugueCharacter.useSuperBreak(character=TrailblazerCharacter,
                                               baseGauge=TrailblazerCharacter.useSkill().gauge,
                                               extraTypes=['skill']) * numSkillTrailblazer,
    ]

    numBasicFugue = 4.0
    numSkillFugue = 2.0
    FugueRotation = [FugueCharacter.useEnhancedBasic() * numBasicFugue,
                     FugueCharacter.useSkill() * numSkillFugue,
                     FugueCharacter.useUltimate(),
                     FugueCharacter.useSuperBreak(character=FugueCharacter,
                                                        baseGauge=FugueCharacter.useEnhancedBasic().gauge,
                                                        extraTypes=['basic','enhancedBasic']) * numBasicFugue]
    TrailblazerRotationFugue = [
                       TrailblazerCharacter.useSuperBreak(character=FugueCharacter,
                                                          baseGauge=FugueCharacter.useEnhancedBasic().gauge,
                                                          extraTypes=['basic','enhancedBasic']) * numBasicFugue
    ]

    numBasicGallagher = 4.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1,]
    if GallagherCharacter.lightcone.name == 'Multiplication':
        GallagherRotation[-1].actionvalue += 0.20 # advance foward cannot exceed a certain amount
        
    TrailblazerRotationGallagher = [
        TrailblazerCharacter.useSuperBreak(character=GallagherCharacter,
                                                             baseGauge=GallagherCharacter.useBasic().gauge,
                                                             extraTypes=['basic']) * numBasicGallagher,
        TrailblazerCharacter.useSuperBreak(character=GallagherCharacter,
                                                             baseGauge=GallagherCharacter.useEnhancedBasic().gauge,
                                                             extraTypes=['basic','enhancedBasic']) * numEnhancedGallagher,
        TrailblazerCharacter.useSuperBreak(character=GallagherCharacter,
                                                             baseGauge=GallagherCharacter.useUltimate().gauge,
                                                             extraTypes=['ultimate']),
    ]
    FugueRotationGallagher = [
        FugueCharacter.useSuperBreak(character=GallagherCharacter,
                                     baseGauge=GallagherCharacter.useBasic().gauge,
                                     extraTypes=['basic']) * numBasicGallagher,
        FugueCharacter.useSuperBreak(character=GallagherCharacter,
                                     baseGauge=GallagherCharacter.useEnhancedBasic().gauge,
                                     extraTypes=['basic','enhancedBasic']) * numEnhancedGallagher,
        FugueCharacter.useSuperBreak(character=GallagherCharacter,
                                     baseGauge=GallagherCharacter.useUltimate().gauge,
                                     extraTypes=['ultimate']),
    ]

    #%% Firefly Trailblazer Fugue Gallagher Rotation Math

    totalFireflyEffect = sumEffects(FireflyRotation)
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)
    totalFugueEffect = sumEffects(FugueRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    FireflyRotationDuration = totalFireflyEffect.actionvalue * 100.0 / FireflyCharacter.getTotalStat('SPD')
    TrailblazerRotationDuration = totalTrailblazerEffect.actionvalue * 100.0 / TrailblazerCharacter.getTotalStat('SPD')
    FugueRotationDuration = totalFugueEffect.actionvalue * 100.0 / FugueCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()

    DanceDanceDanceEffect.actionvalue = -0.24
    TrailblazerCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    TrailblazerRotation.append(deepcopy(DanceDanceDanceEffect))
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)
    TrailblazerRotationDuration = totalTrailblazerEffect.actionvalue * 100.0 / TrailblazerCharacter.getTotalStat('SPD')

    DanceDanceDanceEffect.actionvalue = -0.24 * FireflyRotationDuration / TrailblazerRotationDuration
    FireflyCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    FireflyRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * FugueRotationDuration / TrailblazerRotationDuration
    FugueCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    FugueRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * GallagherRotationDuration / TrailblazerRotationDuration
    GallagherCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    GallagherRotation.append(deepcopy(DanceDanceDanceEffect))
    
    totalFugueEffect = sumEffects(FugueRotation)
    totalFireflyEffect = sumEffects(FireflyRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    FireflyRotationDuration = totalFireflyEffect.actionvalue * 100.0 / FireflyCharacter.getTotalStat('SPD')
    FugueRotationDuration = totalFugueEffect.actionvalue * 100.0 / FugueCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    if FugueCharacter.eidolon >= 2:
        # Apply Fugue E2 Effect
        FugueE2Effect = BaseEffect()

        FugueE2Effect.actionvalue = -0.24
        FugueCharacter.addDebugInfo(FugueE2Effect,['buff'],'Dance Dance Dance Effect')
        FugueRotation.append(deepcopy(FugueE2Effect))
        totalFugueEffect = sumEffects(FugueRotation)
        FugueRotationDuration = totalFugueEffect.actionvalue * 100.0 / FugueCharacter.getTotalStat('SPD')

        FugueE2Effect.actionvalue = -0.24 * FireflyRotationDuration / FugueRotationDuration
        FireflyCharacter.addDebugInfo(FugueE2Effect,['buff'],'Dance Dance Dance Effect')
        FireflyRotation.append(deepcopy(FugueE2Effect))
        
        FugueE2Effect.actionvalue = -0.24 * FugueRotationDuration / FugueRotationDuration
        TrailblazerCharacter.addDebugInfo(FugueE2Effect,['buff'],'Dance Dance Dance Effect')
        TrailblazerRotation.append(deepcopy(FugueE2Effect))
        
        FugueE2Effect.actionvalue = -0.24 * GallagherRotationDuration / FugueRotationDuration
        GallagherCharacter.addDebugInfo(FugueE2Effect,['buff'],'Dance Dance Dance Effect')
        GallagherRotation.append(deepcopy(FugueE2Effect))
        
        totalTrailblazerEffect = sumEffects(TrailblazerRotation)
        totalFireflyEffect = sumEffects(FireflyRotation)
        totalGallagherEffect = sumEffects(GallagherRotation)

        FireflyRotationDuration = totalFireflyEffect.actionvalue * 100.0 / FireflyCharacter.getTotalStat('SPD')
        TrailblazerRotationDuration = totalTrailblazerEffect.actionvalue * 100.0 / FugueCharacter.getTotalStat('SPD')
        GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Firefly: ',FireflyRotationDuration)
    print('Trailblazer: ',TrailblazerRotationDuration)
    print('Fugue: ',FugueRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    TrailblazerRotation = [x * FireflyRotationDuration / TrailblazerRotationDuration for x in TrailblazerRotation]
    FugueRotation = [x * FireflyRotationDuration / FugueRotationDuration for x in FugueRotation]
    GallagherRotation = [x * FireflyRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    TrailblazerRotationFugue = [x * FireflyRotationDuration / FugueRotationDuration for x in TrailblazerRotationFugue]
    TrailblazerRotationGallagher = [x * FireflyRotationDuration / GallagherRotationDuration for x in TrailblazerRotationGallagher]
    FugueRotationTrailblazer = [x * FireflyRotationDuration / TrailblazerRotationDuration for x in FugueRotationTrailblazer]
    FugueRotationGallagher = [x * FireflyRotationDuration / GallagherRotationDuration for x in FugueRotationGallagher]
    
    TrailblazerRotation += TrailblazerRotationFirefly
    TrailblazerRotation += TrailblazerRotationFugue
    TrailblazerRotation += TrailblazerRotationGallagher
    FugueRotation += FugueRotationFirefly
    FugueRotation += FugueRotationTrailblazer
    FugueRotation += FugueRotationGallagher
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)
    totalFugueEffect = sumEffects(FugueRotation)

    FireflyEstimate = DefaultEstimator(f'{FireflyCharacter.fullName()} {FireflyCharacter.weaknessBrokenUptime:.2f} Weakness Uptime: {numSkillFirefly:.1f}E {2*numEnhancedFirefly:.1f}Enh {numUltFirefly:.0f}Q', 
                                       FireflyRotation, FireflyCharacter, config, exoToughness=True)
    TrailblazerEstimate = DefaultEstimator(f'{TrailblazerCharacter.fullName()} {numSkillTrailblazer:.0f}E {numBasicTrailblazer:.0f}N Q', 
                                           TrailblazerRotation, TrailblazerCharacter, config, exoToughness=True)
    FugueEstimate = DefaultEstimator(f'{FugueCharacter.fullName()} {numBasicFugue:.0f}Enh {numSkillFugue:.0f}E 1Q', 
                                    FugueRotation, FugueCharacter, config, exoToughness=True)
    GallagherEstimate = DefaultEstimator(f'{GallagherCharacter.fullName()} {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q', 
                                    GallagherRotation, GallagherCharacter, config, exoToughness=True)

    return([FireflyEstimate, TrailblazerEstimate, GallagherEstimate, FugueEstimate])

