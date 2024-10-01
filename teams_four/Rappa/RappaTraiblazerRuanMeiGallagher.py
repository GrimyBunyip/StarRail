from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.erudition.Rappa import Rappa
from characters.harmony.RuanMei import RuanMei
from characters.harmony.ImaginaryTrailblazer import ImaginaryTrailblazer
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.QuidProQuo import QuidProQuo
from lightCones.erudition.AfterTheCharmonyFall import AfterTheCharmonyFall
from lightCones.erudition.NinjutsuInscription import NinjutsuInscription
from lightCones.erudition.Passkey import Passkey
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.planarSets.TaliaKingdomOfBanditry import TaliaKingdomOfBanditry
from relicSets.relicSets.IronCavalryAgainstTheScourge import IronCavalryAgainstTheScourge2pc, IronCavalryAgainstTheScourge4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc
from relicSets.relicSets.WatchmakerMasterOfDreamMachinations import Watchmaker2pc, Watchmaker4pc

def RappaTrailblazerRuanMeiGallagher(config,
                                     rappaEidolon:int=None,
                                     rappaLightcone:str='Passkey',
                                     numChargesRappa:float = 5.0,
                                     rappaNumSkillOverride:float=None,):
    #%% Rappa Trailblazer RuanMei Gallagher Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                                    substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                                    lightcone = MemoriesOfThePast(**config),
                                    relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                                    **config)
    
    if rappaLightcone == 'Passkey':
        RappaLightcone = Passkey(**config)
    elif rappaLightcone == 'AfterTheCharmonyFall':
        RappaLightcone = AfterTheCharmonyFall(**config)
    elif rappaLightcone == 'NinjutsuInscription':
        RappaLightcone = NinjutsuInscription(**config)
    RappaCharacter = Rappa(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'SPD.flat', 'BreakEffect'],
                                    substats = {'SPD.flat': 12, 'ATK.flat': 3, 'BreakEffect': 8, 'ATK.percent': 5}),
                                    lightcone = RappaLightcone,
                                    eidolon = rappaEidolon,
                                    relicsetone = IronCavalryAgainstTheScourge2pc(), relicsettwo = IronCavalryAgainstTheScourge4pc(), planarset = TaliaKingdomOfBanditry(),
                                    **config)

    TrailblazerCharacter = ImaginaryTrailblazer(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'BreakEffect'],
                                    substats = {'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5, 'DEF.percent': 3}),
                                    lightcone = DanceDanceDance(**config),
                                    relicsetone = Watchmaker2pc(), relicsettwo = Watchmaker4pc(uptime=0.0), planarset = ForgeOfTheKalpagniLantern(),
                                    **config)

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                                    substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = QuidProQuo(**config),
                                    relicsetone = IronCavalryAgainstTheScourge2pc(), relicsettwo = IronCavalryAgainstTheScourge4pc(), planarset = SprightlyVonwacq(),
                                    **config)
    
    team = [RappaCharacter, TrailblazerCharacter, RuanMeiCharacter, GallagherCharacter]

    #%% Rappa Trailblazer RuanMei Gallagher Team Buffs
    for character in team:
        character.addStat('BreakEffect',description='Watchmaker 4pc', amount=0.30, uptime=1.0)

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

    #%% Rappa Trailblazer RuanMei Gallagher Rotations

    numSkillRappa = 1.7
    numSkillRappa -= RappaCharacter.numEnemies * 0.1 if config['enemyType'] == 'elite' else 0.0
    numSkillRappa -= (2.0 / 3.0) if RappaCharacter.eidolon >= 1 else 0.0
    numSkillRappa -= (2.0 * 12.0 / 30.0) if rappaLightcone == 'Passkey' else 0.0
    numSkillRappa = rappaNumSkillOverride if rappaNumSkillOverride is not None else numSkillRappa
    numEnhancedRappa = 3.0
    RappaRotation = [ 
            RappaCharacter.useSkill() * numSkillRappa,
            RappaCharacter.useEnhancedBasic() * numEnhancedRappa,
            RappaCharacter.useTalent(numCharges=numChargesRappa) * numEnhancedRappa,
            RappaCharacter.useSuperBreak() * numEnhancedRappa,
            RappaCharacter.useUltimate(),
    ]
    TrailblazerRotationRappa = [
            TrailblazerCharacter.useSuperBreak(character=RappaCharacter, 
                                               baseGauge=RappaCharacter.useSkill().gauge,
                                               extraTypes=['skill']) * numSkillRappa,
            TrailblazerCharacter.useSuperBreak(character=RappaCharacter, 
                                               baseGauge=RappaCharacter.useEnhancedBasic().gauge,
                                               extraTypes=['basic','enhancedBasic']) * numEnhancedRappa,
            TrailblazerCharacter.useSuperBreak(character=RappaCharacter, 
                                               baseGauge=RappaCharacter.useTalent(numCharges=numChargesRappa).gauge,
                                               extraTypes=['basic','enhancedBasic']) * numEnhancedRappa,
    ]

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

    #%% Rappa Trailblazer RuanMei Gallagher Rotation Math

    totalRappaEffect = sumEffects(RappaRotation)
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    RappaRotationDuration = totalRappaEffect.actionvalue * 100.0 / RappaCharacter.getTotalStat('SPD')
    TrailblazerRotationDuration = totalTrailblazerEffect.actionvalue * 100.0 / TrailblazerCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')
    
    if GallagherCharacter.lightcone.name == 'Quid Pro Quo':
        QPQEffect = BaseEffect()
        QPQEffect.energy = 16.0 
        QPQEffect.energy *= numBasicGallagher + numEnhancedGallagher
        QPQEffect.energy *= 1.0 / 3.0
        
        RappaRotation.append(QPQEffect * RappaRotationDuration / GallagherRotationDuration)

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()

    DanceDanceDanceEffect.actionvalue = -0.24
    TrailblazerCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    TrailblazerRotation.append(deepcopy(DanceDanceDanceEffect))
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)
    TrailblazerRotationDuration = totalTrailblazerEffect.actionvalue * 100.0 / TrailblazerCharacter.getTotalStat('SPD')

    DanceDanceDanceEffect.actionvalue = -0.24 * RappaRotationDuration / TrailblazerRotationDuration
    RappaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    RappaRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * RuanMeiRotationDuration / TrailblazerRotationDuration
    RuanMeiCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    RuanMeiRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * GallagherRotationDuration / TrailblazerRotationDuration
    GallagherCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    GallagherRotation.append(deepcopy(DanceDanceDanceEffect))
    
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalRappaEffect = sumEffects(RappaRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    RappaRotationDuration = totalRappaEffect.actionvalue * 100.0 / RappaCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Rappa: ',RappaRotationDuration)
    print('Trailblazer: ',TrailblazerRotationDuration)
    print('RuanMei: ',RuanMeiRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    TrailblazerRotation = [x * RappaRotationDuration / TrailblazerRotationDuration for x in TrailblazerRotation]
    RuanMeiRotation = [x * RappaRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    GallagherRotation = [x * RappaRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    TrailblazerRotationRuanMei = [x * RappaRotationDuration / RuanMeiRotationDuration for x in TrailblazerRotationRuanMei]
    TrailblazerRotationGallagher = [x * RappaRotationDuration / GallagherRotationDuration for x in TrailblazerRotationGallagher]
    
    TrailblazerRotation += TrailblazerRotationRappa
    TrailblazerRotation += TrailblazerRotationRuanMei
    TrailblazerRotation += TrailblazerRotationGallagher
    totalTrailblazerEffect = sumEffects(TrailblazerRotation)

    RappaEstimate = DefaultEstimator(f'{RappaCharacter.fullName()} {numSkillRappa:.1f}E {numEnhancedRappa:.0f}Enh {numChargesRappa:.1f}Avg Charges', 
                                       RappaRotation, RappaCharacter, config)
    TrailblazerEstimate = DefaultEstimator(f'{TrailblazerCharacter.fullName()} {numSkillTrailblazer:.0f}E {numBasicTrailblazer:.0f}N Q', 
                                           TrailblazerRotation, TrailblazerCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'{RuanMeiCharacter.fullName()} {numBasicRuanMei:.0f}N {numSkillRuanMei:.0f}E 1Q', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    GallagherEstimate = DefaultEstimator(f'{GallagherCharacter.fullName()} {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q', 
                                    GallagherRotation, GallagherCharacter, config)

    return([RappaEstimate, TrailblazerEstimate, GallagherEstimate, RuanMeiEstimate])

