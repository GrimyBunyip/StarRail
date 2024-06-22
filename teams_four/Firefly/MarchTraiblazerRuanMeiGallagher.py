from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.hunt.ImaginaryMarch import ImaginaryMarch
from characters.harmony.RuanMei import RuanMei
from characters.harmony.ImaginaryTrailblazer import ImaginaryTrailblazer
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.IndeliblePromise import IndeliblePromise
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.planarSets.TaliaKingdomOfBanditry import TaliaKingdomOfBanditry
from relicSets.relicSets.IronCavalryAgainstTheScourge import IronCavalryAgainstTheScourge2pc, IronCavalryAgainstTheScourge4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc
from relicSets.relicSets.WatchmakerMasterOfDreamMachinations import Watchmaker2pc, Watchmaker4pc

def MarchTrailblazerRuanMeiGallagher(config):
    #%% March Trailblazer RuanMei Gallagher Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                                    substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                                    lightcone = MemoriesOfThePast(**config),
                                    relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                                    **config)

    TrailblazerCharacter = ImaginaryTrailblazer(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                                    substats = {'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5, 'DEF.percent': 3}),
                                    lightcone = DanceDanceDance(**config),
                                    relicsetone = Watchmaker2pc(), relicsettwo = Watchmaker4pc(uptime=0.0), planarset = TaliaKingdomOfBanditry(),
                                    **config)

    MarchCharacter = ImaginaryMarch(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'CR', 'DMG.imaginary'],
                                    substats = {'CD': 5, 'CR': 3, 'BreakEffect': 12, 'SPD.flat': 8}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = ThiefOfShootingMeteor2pc(),
                                    relicsettwo = ThiefOfShootingMeteor4pc(),
                                    planarset = TaliaKingdomOfBanditry(),
                                    master=TrailblazerCharacter,
                                    **config)
    
    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                                    substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = IronCavalryAgainstTheScourge2pc(), relicsettwo = IronCavalryAgainstTheScourge4pc(), planarset = PenaconyLandOfDreams(),
                                    **config)
    
    team = [MarchCharacter, TrailblazerCharacter, RuanMeiCharacter, GallagherCharacter]

    #%% March Trailblazer RuanMei Gallagher Team Buffs
    for character in team:
        character.addStat('DMG.fire',description='Penacony from Gallagher',amount=0.1)
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
    
    # March Buff
    MarchCharacter.applySkillBuff(TrailblazerCharacter)
    MarchCharacter.applyE6Buff(TrailblazerCharacter,uptime=1.0)
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% March Trailblazer RuanMei Gallagher Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long

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

    numBasicTrailblazer = 0.0
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

    #%% March Trailblazer RuanMei Gallagher Rotation Math

    totalMarchEffect = sumEffects(MarchRotation)
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
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

    DanceDanceDanceEffect.actionvalue = -0.24 * MarchRotationDuration / TrailblazerRotationDuration
    MarchCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    MarchRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * RuanMeiRotationDuration / TrailblazerRotationDuration
    RuanMeiCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    RuanMeiRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * GallagherRotationDuration / TrailblazerRotationDuration
    GallagherCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    GallagherRotation.append(deepcopy(DanceDanceDanceEffect))
    
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalMarchEffect = sumEffects(MarchRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('March: ',MarchRotationDuration)
    print('Trailblazer: ',TrailblazerRotationDuration)
    print('RuanMei: ',RuanMeiRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    TrailblazerRotation = [x * MarchRotationDuration / TrailblazerRotationDuration for x in TrailblazerRotation]
    RuanMeiRotation = [x * MarchRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    GallagherRotation = [x * MarchRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    TrailblazerRotationRuanMei = [x * MarchRotationDuration / RuanMeiRotationDuration for x in TrailblazerRotationRuanMei]
    TrailblazerRotationGallagher = [x * MarchRotationDuration / GallagherRotationDuration for x in TrailblazerRotationGallagher]
    
    TrailblazerRotation += TrailblazerRotationMarch
    TrailblazerRotation += TrailblazerRotationRuanMei
    TrailblazerRotation += TrailblazerRotationGallagher
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)

    MarchEstimate = DefaultEstimator(f'March: {numBasicMarch:.1f}N {numEnhancedMarch:.1f}Enh 1Q', MarchRotation, MarchCharacter, config)
    TrailblazerEstimate = DefaultEstimator(f'Trailblazer: {numSkillTrailblazer:.0f}E {numBasicTrailblazer:.0f}N Q S{TrailblazerCharacter.lightcone.superposition:d} {TrailblazerCharacter.lightcone.name}', TrailblazerRotation, TrailblazerCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'Ruan Mei: {numBasicRuanMei:.0f}N {numSkillRuanMei:.0f}E 1Q, S{RuanMeiCharacter.lightcone.superposition:d} {RuanMeiCharacter.lightcone.name}', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    GallagherEstimate = DefaultEstimator(f'Gallagher: {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q, S{GallagherCharacter.lightcone.superposition:d} {GallagherCharacter.lightcone.name}', 
                                    GallagherRotation, GallagherCharacter, config)

    return([MarchEstimate, TrailblazerEstimate, GallagherEstimate, RuanMeiEstimate])

