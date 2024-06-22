from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.hunt.Boothill import Boothill
from characters.harmony.RuanMei import RuanMei
from characters.harmony.ImaginaryTrailblazer import ImaginaryTrailblazer
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.IndeliblePromise import IndeliblePromise
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.hunt.Swordplay import Swordplay
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.planarSets.TaliaKingdomOfBanditry import TaliaKingdomOfBanditry
from relicSets.relicSets.IronCavalryAgainstTheScourge import IronCavalryAgainstTheScourge2pc, IronCavalryAgainstTheScourge4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc
from relicSets.relicSets.WatchmakerMasterOfDreamMachinations import Watchmaker2pc, Watchmaker4pc

def BoothillTrailblazerRuanMeiGallagher(config):
    #%% Boothill Trailblazer RuanMei Gallagher Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                                    substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                                    lightcone = MemoriesOfThePast(**config),
                                    relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                                    **config)
    
    BoothillCharacter = Boothill(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'BreakEffect'],
                                    substats = {'SPD.flat': 12, 'BreakEffect': 8, 'CR': 5, 'CD': 3}),
                                    lightcone = Swordplay(**config),
                                    relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = TaliaKingdomOfBanditry(),
                                    **config)

    TrailblazerCharacter = ImaginaryTrailblazer(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'BreakEffect'],
                                    substats = {'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5, 'DEF.percent': 3}),
                                    lightcone = DanceDanceDance(**config),
                                    relicsetone = Watchmaker2pc(), relicsettwo = Watchmaker4pc(uptime=0.0), planarset = TaliaKingdomOfBanditry(),
                                    **config)

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                                    substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                                    **config)
    
    team = [BoothillCharacter, TrailblazerCharacter, RuanMeiCharacter, GallagherCharacter]

    #%% Boothill Trailblazer RuanMei Gallagher Team Buffs
    for character in team:
        character.addStat('BreakEffect',description='Watchmaker 4pc', amount=0.30, uptime=0.66)

    # RuanMei Buffs, 3 turn RuanMei rotation
    RuanMeiCharacter.applyWeaknessModifiers(team=team)
    RuanMeiCharacter.applyPassiveBuffs(team=team)
    RuanMeiCharacter.applySkillBuff(team=team,uptime=3.0/3.0)
    RuanMeiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)

    # Trailblazer Vulnerability Buff
    TrailblazerCharacter.applyUltBuff(team=team)
    TrailblazerCharacter.applyE4Buff(team=team)
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)
    
    # assume that weakness broken uptime is increased by 1 ult, and an extra 1.5 because let's say boothill breaks fast
    for character in team:
        character.weaknessBrokenUptime = 1.0 - (1.0 - character.weaknessBrokenUptime) / 1.4

    #%% Print Statements
    for character in team:
        character.print()

    #%% Boothill Trailblazer RuanMei Gallagher Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long

    numEnhancedBasic = 3.0
    numSkill = 1.5
    numUlt = 1.0

    BoothillRotation = [BoothillCharacter.useSkill() * numSkill,
                        BoothillCharacter.useEnhancedBasic() * numEnhancedBasic,
                        BoothillCharacter.useUltimate() * numUlt, # 1 charge
                        ]
    TrailblazerRotationBoothill = [
            TrailblazerCharacter.useSuperBreak(character=BoothillCharacter, 
                                               baseGauge=BoothillCharacter.useEnhancedBasic().gauge,
                                               extraTypes=['skill']) * numEnhancedBasic,        
    ]
    TrailblazerRotationBoothill += [
            TrailblazerCharacter.useSuperBreak(character=BoothillCharacter, 
                                               baseGauge=BoothillCharacter.useUltimate().gauge,
                                               extraTypes=['skill']) * numUlt,   
    ]

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

    #%% Boothill Trailblazer RuanMei Gallagher Rotation Math

    totalBoothillEffect = sumEffects(BoothillRotation)
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    BoothillRotationDuration = totalBoothillEffect.actionvalue * 100.0 / BoothillCharacter.getTotalStat('SPD')
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

    DanceDanceDanceEffect.actionvalue = -0.24 * BoothillRotationDuration / TrailblazerRotationDuration
    BoothillCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    BoothillRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * RuanMeiRotationDuration / TrailblazerRotationDuration
    RuanMeiCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    RuanMeiRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * GallagherRotationDuration / TrailblazerRotationDuration
    GallagherCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    GallagherRotation.append(deepcopy(DanceDanceDanceEffect))
    
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalBoothillEffect = sumEffects(BoothillRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    BoothillRotationDuration = totalBoothillEffect.actionvalue * 100.0 / BoothillCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Boothill: ',BoothillRotationDuration)
    print('Trailblazer: ',TrailblazerRotationDuration)
    print('RuanMei: ',RuanMeiRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    TrailblazerRotation = [x * BoothillRotationDuration / TrailblazerRotationDuration for x in TrailblazerRotation]
    RuanMeiRotation = [x * BoothillRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    GallagherRotation = [x * BoothillRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    TrailblazerRotationRuanMei = [x * BoothillRotationDuration / RuanMeiRotationDuration for x in TrailblazerRotationRuanMei]
    TrailblazerRotationGallagher = [x * BoothillRotationDuration / GallagherRotationDuration for x in TrailblazerRotationGallagher]
    
    TrailblazerRotation += TrailblazerRotationBoothill
    TrailblazerRotation += TrailblazerRotationRuanMei
    TrailblazerRotation += TrailblazerRotationGallagher
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)

    BoothillEstimate = DefaultEstimator(f'Boothill: {numEnhancedBasic:.1f}Enh {numSkill}E {numUlt:.0f}Q',
                                    BoothillRotation, BoothillCharacter, config)
    TrailblazerEstimate = DefaultEstimator(f'Trailblazer: {numSkillTrailblazer:.0f}E {numBasicTrailblazer:.0f}N Q S{TrailblazerCharacter.lightcone.superposition:d} {TrailblazerCharacter.lightcone.name}', TrailblazerRotation, TrailblazerCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'Ruan Mei: {numBasicRuanMei:.0f}N {numSkillRuanMei:.0f}E 1Q, S{RuanMeiCharacter.lightcone.superposition:d} {RuanMeiCharacter.lightcone.name}', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    GallagherEstimate = DefaultEstimator(f'Gallagher: {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q, S{GallagherCharacter.lightcone.superposition:d} {GallagherCharacter.lightcone.name}', 
                                    GallagherRotation, GallagherCharacter, config)

    return([BoothillEstimate, TrailblazerEstimate, GallagherEstimate, RuanMeiEstimate])

