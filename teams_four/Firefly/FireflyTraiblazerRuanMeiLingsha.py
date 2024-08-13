from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Lingsha import Lingsha
from characters.destruction.Firefly import Firefly
from characters.harmony.RuanMei import RuanMei
from characters.harmony.ImaginaryTrailblazer import ImaginaryTrailblazer
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.EchoesOfTheCoffin import EchoesOfTheCoffin
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.destruction.WhereaboutsShouldDreamsRest import WhereaboutsShouldDreamsRest
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.IronCavalryAgainstTheScourge import IronCavalryAgainstTheScourge2pc, IronCavalryAgainstTheScourge4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc
from relicSets.relicSets.WatchmakerMasterOfDreamMachinations import Watchmaker2pc, Watchmaker4pc

def FireflyTrailblazerRuanMeiLingsha(config,
                                       fireflyEidolon:int=None,
                                       fireflySuperposition:int=0,
                                       lingshaEidolon:int=None,
                                       lingshaSuperposition:int=0,):
    #%% Firefly Trailblazer RuanMei Lingsha Characters
    
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

    trailblazerLightcone = MemoriesOfThePast(**config) if FireflyCharacter.eidolon == 0 else DanceDanceDance(**config)
    TrailblazerCharacter = ImaginaryTrailblazer(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'BreakEffect'],
                                    substats = {'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5, 'DEF.percent': 3}),
                                    lightcone = trailblazerLightcone,
                                    relicsetone = Watchmaker2pc(), relicsettwo = Watchmaker4pc(uptime=0.0), planarset = ForgeOfTheKalpagniLantern(),
                                    **config)

    lingshaLightcone = EchoesOfTheCoffin(**config) if lingshaSuperposition == 0 else Multiplication(**config)
    LingshaCharacter = Lingsha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                    substats = {'SPD.flat': 12, 'BreakEffect': 8, 'ATK.percent': 5, 'ATK.flat': 3}),
                                    lightcone = lingshaLightcone,
                                    eidolon = lingshaEidolon,
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = IronCavalryAgainstTheScourge2pc(), planarset = ForgeOfTheKalpagniLantern(),
                                    **config)
    
    team = [FireflyCharacter, TrailblazerCharacter, RuanMeiCharacter, LingshaCharacter]

    #%% Firefly Trailblazer RuanMei Lingsha Team Buffs
    for character in team:
        character.addStat('DMG.fire',description='Penacony from Lingsha',amount=0.1)
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
    
    # Handle firefly's ult vulnerability separately
    FireflyCharacter.applyUltVulnerability(team=[TrailblazerCharacter, LingshaCharacter, RuanMeiCharacter])
    
    # Apply Lingsha Debuff
    lingshaUltRotation = 2.0 if LingshaCharacter.lightcone.name == 'Echoes of the Coffin' else 3.0
    LingshaCharacter.applyUltDebuff(team=team,rotationDuration=lingshaUltRotation)
    if LingshaCharacter.eidolon >= 2:
        for character in team:
            character.addStat('BreakEffect',description='Lingsha E2',amount=0.4)
    if LingshaCharacter.lightcone.name == 'Echoes of the Coffin':
        for character in team:
            character.addStat('SPD.flat',description='Echoes of the Coffin', 
                              amount=10 + 2 * LingshaCharacter.lightcone.superposition,
                              uptime=min(1.0, 1.0 / lingshaUltRotation))
    
    # apply Firefly and Lingsha self buffs and MV calculations at the end
    FireflyCharacter.addBreakEffectTalent()
    LingshaCharacter.addAttackForTalent()

    #%% Print Statements
    for character in team:
        character.print()

    #%% Firefly Trailblazer RuanMei Lingsha Rotations
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
    numEnhancedFirefly *= 1.5 if FireflyCharacter.eidolon >= 2.0 else 1.0
    FireflyRotation += [FireflyCharacter.useEnhancedSkill() * numEnhancedFirefly]
    FireflyRotation[-1].actionvalue *= 2.0 / 3.0 if FireflyCharacter.eidolon >= 2 else 1.0
    FireflyRotation += [FireflyCharacter.useSuperBreak(extraTypes=['skill','enhancedSkill']) * numEnhancedFirefly]
    TrailblazerRotationFirefly += [TrailblazerCharacter.useSuperBreak(character=FireflyCharacter, 
                                                                      baseGauge=FireflyCharacter.useEnhancedSkill().gauge,
                                                                      extraTypes=['skill','enhancedSkill']) * numEnhancedFirefly]

    numBasicTrailblazer = 3.0 if FireflyCharacter.eidolon == 0 else 1.0
    numSkillTrailblazer = 0.0 if FireflyCharacter.eidolon == 0 else 2.0
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

    numBasicLingsha = 1.0 if LingshaCharacter.lightcone.name == 'Echoes of the Coffin' else 2.0
    numSkillLingsha = 1.0
    # 1 from ultimate, 1.5 from autoheal, 1.5 from natural turns
    # 1 from ultimate, 1 from autoheal, 1 from natural turns if S1
    numTalentLingsha = 3.0 if LingshaCharacter.lightcone.name == 'Echoes of the Coffin' else 4.0
    
    LingshaRotation = [LingshaCharacter.useBasic() * numBasicLingsha,
                       LingshaCharacter.useSkill() * numSkillLingsha,
                       LingshaCharacter.useTalent() * numTalentLingsha,
                       LingshaCharacter.useUltimate() * 1,]
    LingshaRotation[0].actionvalue *= 0.8 if LingshaCharacter.lightcone.name == 'Multiplication' else 1.0
        
    TrailblazerRotationLingsha = [
        TrailblazerCharacter.useSuperBreak(character=LingshaCharacter,
                                           baseGauge=LingshaCharacter.useBasic().gauge,
                                           extraTypes=['basic']) * numBasicLingsha,
        TrailblazerCharacter.useSuperBreak(character=LingshaCharacter,
                                           baseGauge=LingshaCharacter.useSkill().gauge,
                                           extraTypes=['skill']) * numSkillLingsha,
        TrailblazerCharacter.useSuperBreak(character=LingshaCharacter,
                                           baseGauge=LingshaCharacter.useTalent().gauge,
                                           extraTypes=['talent']) * numTalentLingsha,
        TrailblazerCharacter.useSuperBreak(character=LingshaCharacter,
                                           baseGauge=LingshaCharacter.useUltimate().gauge,
                                           extraTypes=['ultimate']),
    ]

    #%% Firefly Trailblazer RuanMei Lingsha Rotation Math

    totalFireflyEffect = sumEffects(FireflyRotation)
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalLingshaEffect = sumEffects(LingshaRotation)

    FireflyRotationDuration = totalFireflyEffect.actionvalue * 100.0 / FireflyCharacter.getTotalStat('SPD')
    TrailblazerRotationDuration = totalTrailblazerEffect.actionvalue * 100.0 / TrailblazerCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    LingshaRotationDuration = totalLingshaEffect.actionvalue * 100.0 / LingshaCharacter.getTotalStat('SPD')

    # Apply Dance Dance Dance Effect
    if TrailblazerCharacter.lightcone.name == 'Dance! Dance! Dance!':
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
        
        DanceDanceDanceEffect.actionvalue = -0.24 * LingshaRotationDuration / TrailblazerRotationDuration
        LingshaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
        LingshaRotation.append(deepcopy(DanceDanceDanceEffect))
        
        totalRuanMeiEffect = sumEffects(RuanMeiRotation)
        totalFireflyEffect = sumEffects(FireflyRotation)
        totalLingshaEffect = sumEffects(LingshaRotation)

        FireflyRotationDuration = totalFireflyEffect.actionvalue * 100.0 / FireflyCharacter.getTotalStat('SPD')
        RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
        LingshaRotationDuration = totalLingshaEffect.actionvalue * 100.0 / LingshaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Firefly: ',FireflyRotationDuration)
    print('Trailblazer: ',TrailblazerRotationDuration)
    print('RuanMei: ',RuanMeiRotationDuration)
    print('Lingsha: ',LingshaRotationDuration)

    # Scale other character's rotation
    TrailblazerRotation = [x * FireflyRotationDuration / TrailblazerRotationDuration for x in TrailblazerRotation]
    RuanMeiRotation = [x * FireflyRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    LingshaRotation = [x * FireflyRotationDuration / LingshaRotationDuration for x in LingshaRotation]
    TrailblazerRotationRuanMei = [x * FireflyRotationDuration / RuanMeiRotationDuration for x in TrailblazerRotationRuanMei]
    TrailblazerRotationLingsha = [x * FireflyRotationDuration / LingshaRotationDuration for x in TrailblazerRotationLingsha]
    
    TrailblazerRotation += TrailblazerRotationFirefly
    TrailblazerRotation += TrailblazerRotationRuanMei
    TrailblazerRotation += TrailblazerRotationLingsha
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)

    FireflyEstimate = DefaultEstimator(f'{FireflyCharacter.fullName()} {FireflyCharacter.weaknessBrokenUptime:.2f} Weakness Uptime: {numSkillFirefly:.1f}E {2*numEnhancedFirefly:.1f}Enh {numUltFirefly:.0f}Q', 
                                       FireflyRotation, FireflyCharacter, config)
    TrailblazerEstimate = DefaultEstimator(f'{TrailblazerCharacter.fullName()} {numSkillTrailblazer:.0f}E {numBasicTrailblazer:.0f}N Q', 
                                           TrailblazerRotation, TrailblazerCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'{RuanMeiCharacter.fullName()} {numBasicRuanMei:.0f}N {numSkillRuanMei:.0f}E 1Q', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    LingshaEstimate = DefaultEstimator(f'{LingshaCharacter.fullName()} {numBasicLingsha:.0f}N {numSkillLingsha:.0f}E {numTalentLingsha:.1f}T 1Q',
                                    LingshaRotation, LingshaCharacter, config)

    return([FireflyEstimate, TrailblazerEstimate, LingshaEstimate, RuanMeiEstimate])

