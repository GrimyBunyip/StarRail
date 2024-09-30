from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.destruction.Firefly import Firefly
from characters.harmony.RuanMei import RuanMei
from characters.harmony.ImaginaryTrailblazer import ImaginaryTrailblazer
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.destruction.WhereaboutsShouldDreamsRest import WhereaboutsShouldDreamsRest
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.IronCavalryAgainstTheScourge import IronCavalryAgainstTheScourge2pc, IronCavalryAgainstTheScourge4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc
from relicSets.relicSets.WatchmakerMasterOfDreamMachinations import Watchmaker2pc, Watchmaker4pc

def FireflyTrailblazerRuanMeiGallagher(config,
                                       fireflyEidolon:int=None,
                                       fireflySuperposition:int=0):
    #%% Firefly Trailblazer RuanMei Gallagher Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                                    substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                                    lightcone = MemoriesOfThePast(**config),
                                    relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                                    **config)
    
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

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                                    substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = IronCavalryAgainstTheScourge2pc(), relicsettwo = IronCavalryAgainstTheScourge4pc(), planarset = SprightlyVonwacq(),
                                    **config)
    
    team = [FireflyCharacter, TrailblazerCharacter, RuanMeiCharacter, GallagherCharacter]

    #%% Firefly Trailblazer RuanMei Gallagher Team Buffs
    for character in team:
        character.addStat('BreakEffect',description='Watchmaker 4pc', amount=0.30, uptime=0.66)

    # Trailblazer Vulnerability Buff
    TrailblazerCharacter.applyUltBuff(team=team)
    TrailblazerCharacter.applyE4Buff(team=team)
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)

    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
    for character in team:
        character.print()

    #%% Firefly Trailblazer RuanMei Gallagher Rotations
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

    FireflyCharacter.applyUltVulnerability()
    numEnhancedFirefly *= 1.5 if FireflyCharacter.eidolon >= 2.0 else 1.0
    FireflyRotation += [FireflyCharacter.useEnhancedSkill() * numEnhancedFirefly]
    FireflyRotation[-1].actionvalue *= 2.0 / 3.0 if FireflyCharacter.eidolon >= 2 else 1.0
    FireflyRotation += [FireflyCharacter.useSuperBreak(extraTypes=['skill','enhancedSkill']) * numEnhancedFirefly]
    TrailblazerRotationFirefly += [TrailblazerCharacter.useSuperBreak(character=FireflyCharacter, 
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

    numBasicRuanMei = 2.0
    numSkillRuanMei = 1.0
    RuanMeiRotation = [RuanMeiCharacter.useBasic() * numBasicRuanMei,
                       RuanMeiCharacter.useSkill() * numSkillRuanMei,
                       RuanMeiCharacter.useUltimate(),]
    TrailblazerRotationRuanMei = [
                       TrailblazerCharacter.useSuperBreak(character=RuanMeiCharacter,
                                                          baseGauge=RuanMeiCharacter.useBasic().gauge,
                                                          extraTypes=['basic']) * numBasicRuanMei
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

    #%% Firefly Trailblazer RuanMei Gallagher Rotation Math

    totalFireflyEffect = sumEffects(FireflyRotation)
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    FireflyRotationDuration = totalFireflyEffect.actionvalue * 100.0 / FireflyCharacter.getTotalStat('SPD')
    TrailblazerRotationDuration = totalTrailblazerEffect.actionvalue * 100.0 / TrailblazerCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
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
    
    DanceDanceDanceEffect.actionvalue = -0.24 * RuanMeiRotationDuration / TrailblazerRotationDuration
    RuanMeiCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    RuanMeiRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * GallagherRotationDuration / TrailblazerRotationDuration
    GallagherCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    GallagherRotation.append(deepcopy(DanceDanceDanceEffect))
    
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalFireflyEffect = sumEffects(FireflyRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    FireflyRotationDuration = totalFireflyEffect.actionvalue * 100.0 / FireflyCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Firefly: ',FireflyRotationDuration)
    print('Trailblazer: ',TrailblazerRotationDuration)
    print('RuanMei: ',RuanMeiRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    TrailblazerRotation = [x * FireflyRotationDuration / TrailblazerRotationDuration for x in TrailblazerRotation]
    RuanMeiRotation = [x * FireflyRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    GallagherRotation = [x * FireflyRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    TrailblazerRotationRuanMei = [x * FireflyRotationDuration / RuanMeiRotationDuration for x in TrailblazerRotationRuanMei]
    TrailblazerRotationGallagher = [x * FireflyRotationDuration / GallagherRotationDuration for x in TrailblazerRotationGallagher]
    
    TrailblazerRotation += TrailblazerRotationFirefly
    TrailblazerRotation += TrailblazerRotationRuanMei
    TrailblazerRotation += TrailblazerRotationGallagher
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)

    FireflyEstimate = DefaultEstimator(f'{FireflyCharacter.fullName()} {FireflyCharacter.weaknessBrokenUptime:.2f} Weakness Uptime: {numSkillFirefly:.1f}E {2*numEnhancedFirefly:.1f}Enh {numUltFirefly:.0f}Q', 
                                       FireflyRotation, FireflyCharacter, config)
    TrailblazerEstimate = DefaultEstimator(f'{TrailblazerCharacter.fullName()} {numSkillTrailblazer:.0f}E {numBasicTrailblazer:.0f}N Q', 
                                           TrailblazerRotation, TrailblazerCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'{RuanMeiCharacter.fullName()} {numBasicRuanMei:.0f}N {numSkillRuanMei:.0f}E 1Q', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    GallagherEstimate = DefaultEstimator(f'{GallagherCharacter.fullName()} {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q', 
                                    GallagherRotation, GallagherCharacter, config)

    return([FireflyEstimate, TrailblazerEstimate, GallagherEstimate, RuanMeiEstimate])

