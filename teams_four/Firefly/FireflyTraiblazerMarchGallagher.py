from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.destruction.Firefly import Firefly
from characters.harmony.ImaginaryTrailblazer import ImaginaryTrailblazer
from characters.hunt.ImaginaryMarch import ImaginaryMarch
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.relicSets.IronCavalryAgainstTheScourge import IronCavalryAgainstTheScourge2pc, IronCavalryAgainstTheScourge4pc
from relicSets.relicSets.WatchmakerMasterOfDreamMachinations import Watchmaker2pc, Watchmaker4pc

def FireflyTrailblazerMarchGallagher(config):
    #%% Firefly Trailblazer March Gallagher Characters
    FireflyCharacter = Firefly(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'SPD.flat', 'BreakEffect'],
                                    substats = {'SPD.flat': 12, 'ATK.flat': 3, 'BreakEffect': 8, 'ATK.percent': 5}),
                                    attackForTalent=3250,
                                    lightcone = OnTheFallOfAnAeon(**config,uptime=1.0),
                                    relicsetone = IronCavalryAgainstTheScourge2pc(), relicsettwo = IronCavalryAgainstTheScourge4pc(), planarset = ForgeOfTheKalpagniLantern(),
                                    **config)

    TrailblazerCharacter = ImaginaryTrailblazer(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'BreakEffect'],
                                    substats = {'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5, 'DEF.percent': 3}),
                                    lightcone = DanceDanceDance(**config),
                                    relicsetone = Watchmaker2pc(), relicsettwo = Watchmaker4pc(uptime=0.0), planarset = ForgeOfTheKalpagniLantern(),
                                    **config)

    MarchCharacter = ImaginaryMarch(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'CR', 'DMG.imaginary'],
                                    substats = {'CD': 5, 'CR': 3, 'BreakEffect': 8, 'SPD.flat': 12}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = IronCavalryAgainstTheScourge2pc(),
                                    relicsettwo = IronCavalryAgainstTheScourge4pc(),
                                    planarset = ForgeOfTheKalpagniLantern(),
                                    master=TrailblazerCharacter,
                                    **config)

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                                    substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = IronCavalryAgainstTheScourge2pc(), relicsettwo = IronCavalryAgainstTheScourge4pc(), planarset = PenaconyLandOfDreams(),
                                    **config)
    
    team = [FireflyCharacter, TrailblazerCharacter, MarchCharacter, GallagherCharacter]

    #%% Firefly Trailblazer March Gallagher Team Buffs
    for character in team:
        character.addStat('DMG.fire',description='Penacony from Gallagher',amount=0.1)
    for character in team:
        character.addStat('BreakEffect',description='Watchmaker 4pc', amount=0.30, uptime=0.66)

    # Trailblazer Vulnerability Buff
    TrailblazerCharacter.applyUltBuff(team=team)
    TrailblazerCharacter.applyE4Buff(team=team)
    
    # Handle firefly's ult vulnerability separately
    FireflyCharacter.applyUltVulnerability(team=[TrailblazerCharacter, GallagherCharacter, MarchCharacter])
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)
    
    # March Buff
    MarchCharacter.applySkillBuff(FireflyCharacter)
    MarchCharacter.applyE6Buff(FireflyCharacter,uptime=MarchCharacter.getTotalStat('SPD') / (FireflyCharacter.getTotalStat('SPD') + 60.0))

    #%% Print Statements
    for character in team:
        character.print()

    #%% Firefly Trailblazer March Gallagher Rotations
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
            FireflyCharacter.useSuperBreak(extraTypes=['skill']) * numSkillFirefly,
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

    FireflyCharacter.applyUltVulnerability([FireflyCharacter],uptime=1.0)
    FireflyRotation += [FireflyCharacter.useEnhancedSkill() * numEnhancedFirefly]
    FireflyRotation += [FireflyCharacter.useSuperBreak(extraTypes=['skill','enhancedSkill']) * numEnhancedFirefly]
    TrailblazerRotationFirefly += [TrailblazerCharacter.useSuperBreak(character=FireflyCharacter, 
                                                                      baseGauge=FireflyCharacter.useEnhancedSkill().gauge,
                                                                      extraTypes=['skill','enhancedSkill']) * numEnhancedFirefly]

    numBasicTrailblazer = 1.0
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
    numBasicMarch = 2.0
    numEnhancedMarch = 1.0
    
    MarchRotation = []
    MarchRotation += [MarchCharacter.useBasic() * numBasicMarch]
    MarchRotation += [MarchCharacter.useFollowup() * numBasicMarch]
    MarchRotation += [MarchCharacter.useEnhancedBasic(actionValue=0.0, numHits=5.0, chance=0.8) * numEnhancedMarch]
    MarchRotation += [MarchCharacter.useUltimate()] 
    TrailblazerRotationMarch = [TrailblazerCharacter.useSuperBreak(character=MarchCharacter, 
                                baseGauge=MarchCharacter.useBasic().gauge,
                                extraTypes=['basic']) * numBasicMarch,]
    TrailblazerRotationMarch += [TrailblazerCharacter.useSuperBreak(character=MarchCharacter, 
                                baseGauge=MarchCharacter.useFollowup().gauge,
                                extraTypes=['followup']) * numBasicMarch]
    TrailblazerRotationMarch += [TrailblazerCharacter.useSuperBreak(character=MarchCharacter, 
                                baseGauge=MarchCharacter.useEnhancedBasic(actionValue=0.0, numHits=5.0, chance=0.8).gauge,
                                extraTypes=['basic','enhancedBasic']) * numEnhancedMarch]
    TrailblazerRotationMarch += [TrailblazerCharacter.useSuperBreak(character=MarchCharacter, 
                                baseGauge=MarchCharacter.useUltimate().gauge,
                                extraTypes=['ultimate'])]

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

    #%% Firefly Trailblazer March Gallagher Rotation Math

    totalFireflyEffect = sumEffects(FireflyRotation)
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)
    totalMarchEffect = sumEffects(MarchRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    FireflyRotationDuration = totalFireflyEffect.actionvalue * 100.0 / FireflyCharacter.getTotalStat('SPD')
    TrailblazerRotationDuration = totalTrailblazerEffect.actionvalue * 100.0 / TrailblazerCharacter.getTotalStat('SPD')
    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
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
    
    DanceDanceDanceEffect.actionvalue = -0.24 * MarchRotationDuration / TrailblazerRotationDuration
    MarchCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    MarchRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * GallagherRotationDuration / TrailblazerRotationDuration
    GallagherCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    GallagherRotation.append(deepcopy(DanceDanceDanceEffect))
    
    totalMarchEffect = sumEffects(MarchRotation)
    totalFireflyEffect = sumEffects(FireflyRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    FireflyRotationDuration = totalFireflyEffect.actionvalue * 100.0 / FireflyCharacter.getTotalStat('SPD')
    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Firefly: ',FireflyRotationDuration)
    print('Trailblazer: ',TrailblazerRotationDuration)
    print('March: ',MarchRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    TrailblazerRotation = [x * FireflyRotationDuration / TrailblazerRotationDuration for x in TrailblazerRotation]
    MarchRotation = [x * FireflyRotationDuration / MarchRotationDuration for x in MarchRotation]
    GallagherRotation = [x * FireflyRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    TrailblazerRotationMarch = [x * FireflyRotationDuration / MarchRotationDuration for x in TrailblazerRotationMarch]
    TrailblazerRotationGallagher = [x * FireflyRotationDuration / GallagherRotationDuration for x in TrailblazerRotationGallagher]
    
    TrailblazerRotation += TrailblazerRotationFirefly
    TrailblazerRotation += TrailblazerRotationMarch
    TrailblazerRotation += TrailblazerRotationGallagher
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)

    FireflyEstimate = DefaultEstimator(f'E{FireflyCharacter.eidolon} Firefly {FireflyCharacter.weaknessBrokenUptime:.2f} Weakness Uptime: {numSkillFirefly:.1f}E {2*numEnhancedFirefly:.1f}Enh {numUltFirefly:.0f}Q S{FireflyCharacter.lightcone.superposition:d} {FireflyCharacter.lightcone.shortname}', FireflyRotation, FireflyCharacter, config)
    TrailblazerEstimate = DefaultEstimator(f'Trailblazer: {numSkillTrailblazer:.0f}E {numBasicTrailblazer:.0f}N Q S{TrailblazerCharacter.lightcone.superposition:d} {TrailblazerCharacter.lightcone.name}', TrailblazerRotation, TrailblazerCharacter, config)
    MarchEstimate = DefaultEstimator(f'March: {numBasicMarch:.1f}N {numEnhancedMarch:.1f}Enh 1Q', MarchRotation, MarchCharacter, config)
    GallagherEstimate = DefaultEstimator(f'Gallagher: {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q, S{GallagherCharacter.lightcone.superposition:d} {GallagherCharacter.lightcone.name}', 
                                    GallagherRotation, GallagherCharacter, config)

    return([FireflyEstimate, TrailblazerEstimate, MarchEstimate, GallagherEstimate])

