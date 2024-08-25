from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Lynx import Lynx
from characters.hunt.ImaginaryMarch import ImaginaryMarch
from characters.harmony.Robin import Robin
from characters.hunt.Feixiao import Feixiao
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.QuidProQuo import QuidProQuo
from lightCones.harmony.FlowingNightglow import FlowingNightglow
from lightCones.harmony.PoisedToBloom import PoisedToBloom
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.IVentureForthToHunt import IVentureForthToHunt
from lightCones.hunt.Swordplay import Swordplay
from relicSets.planarSets.DuranDynastyOfRunningWolves import DuranDynastyOfRunningWolves
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc, MusketeerOfWildWheat4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def FeixiaoMarchRobinLynx(config, 
                                feixiaoEidolon:int=None, 
                                feixiaoSuperposition:int=0, 
                                robinEidolon:int=None, 
                                robinSuperposition:int=0,):
    #%% March Feixiao Robin Lynx Characters

    FeixiaoLightcone = CruisingInTheStellarSea(**config) if feixiaoSuperposition == 0 else IVentureForthToHunt(superposition=feixiaoSuperposition,**config)
    FeixiaoSubstats = {'CR': 7, 'CD': 12, 'ATK.percent': 4, 'SPD.flat':5} if feixiaoSuperposition == 0 else {'CR': 10, 'CD': 11, 'ATK.percent': 3, 'SPD.flat':4}
    if robinEidolon is not None and robinEidolon >= 2:
        FeixiaoSubstats['SPD.flat'] += 1
        FeixiaoSubstats['CD'] -= 1
    FeixiaoCharacter = Feixiao(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.wind'],
                                    substats = FeixiaoSubstats),
                                    lightcone = FeixiaoLightcone,
                                    relicsetone = WindSoaringValorous2pc(),
                                    relicsettwo = WindSoaringValorous4pc(),
                                    planarset = DuranDynastyOfRunningWolves(),
                                    eidolon = feixiaoEidolon,
                                    **config)

    # give March swordplay if Feixiao uses Cruising
    MarchLightCone = Swordplay(**config) #if feixiaoSuperposition == 0 else CruisingInTheStellarSea(**config)
    MarchSubstats = {'CD': 8, 'CR': 12, 'ATK.percent': 4, 'SPD.flat': 4} #if feixiaoSuperposition == 0 else {'CD': 11, 'CR': 9, 'ATK.percent': 3, 'SPD.flat': 5}
    if robinEidolon is not None and robinEidolon >= 2:
        MarchSubstats['SPD.flat'] += 2
        MarchSubstats['CD'] -= 2
    MarchCharacter = ImaginaryMarch(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.imaginary'],
                                    substats = MarchSubstats),
                                    lightcone = MarchLightCone,
                                    relicsetone = MusketeerOfWildWheat2pc(),
                                    relicsettwo = MusketeerOfWildWheat4pc(),
                                    planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    master=FeixiaoCharacter,
                                    **config)
    
    RobinLightCone = PoisedToBloom(**config) if robinSuperposition == 0 else FlowingNightglow(superposition=robinSuperposition,**config)
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 11, 'SPD.flat': 9, 'RES': 3, 'ATK.flat': 6}),
                                    lightcone = RobinLightCone,
                                    relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                                    eidolon=robinEidolon,
                                    **config)

    LynxCharacter = Lynx(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                                    substats = {'HP.percent': 8, 'SPD.flat': 12, 'HP.flat': 3, 'RES': 5}),
                                    lightcone = QuidProQuo(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = ForgeOfTheKalpagniLantern(),
                                    **config)
    
    team = [MarchCharacter, FeixiaoCharacter, RobinCharacter, LynxCharacter]

    #%% March Feixiao Robin Lynx Team Buffs
    for character in [FeixiaoCharacter, MarchCharacter, RobinCharacter]:
        character.addStat('CD',description='Broken Keel from Lynx',amount=0.1)
    if RobinCharacter.lightcone.name == 'Poised to Bloom':
        for character in [FeixiaoCharacter, MarchCharacter]:
            character.addStat('CD',description='Poised to Bloom',amount=0.12+0.04*RobinCharacter.lightcone.superposition)
    
    # March Buff
    MarchCharacter.applySkillBuff(FeixiaoCharacter)
    MarchCharacter.applyTalentBuff(FeixiaoCharacter,uptime=1.0)
    
    # Lynx Buffs
    LynxCharacter.applySkillBuff(RobinCharacter,uptime=1.0)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)

    RobinUltUptime = 0.5 if RobinCharacter.eidolon < 2 else 1.0
    RobinCharacter.applyUltBuff([FeixiaoCharacter, MarchCharacter,LynxCharacter],uptime=RobinUltUptime)

    #%% Print Statements
    for character in team:
        character.print()

    #%% March Feixiao Robin Lynx Rotations
    # assume 154 ish spd March and Feixiao, March slower than Feixiao, and 134 ish spd robin
    
    numBasicRobin = 0.0
    numSkillRobin = 2.0 if RobinCharacter.eidolon < 2 else 1.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0) # apply robin buff after we calculate damage for her basics
    
    # 4 charges from march basics and followups. 
    # 6 charges from fei skills and followups. 1 ish more from ult
    numBasicMarch = 2.0
    numFollowupMarch = numBasicMarch
    numEnhancedMarch = 1.5
    
    MarchRotation = []
    MarchRotation += [MarchCharacter.useBasic() * numBasicMarch]
    MarchRotation += [MarchCharacter.useFollowup() * numFollowupMarch]
    MarchRotation += [MarchCharacter.useEnhancedBasic(actionValue=0.0, numHits=5.0, chance=0.8) ]
    MarchRotation += [MarchCharacter.useEnhancedBasic(actionValue=0.0, numHits=3.0, chance=0.6) * (numEnhancedMarch - 1.0)]
    MarchRotation += [MarchCharacter.useUltimate()] 

    RobinRotationMarch = [RobinCharacter.useTalent() * (2.0 * numBasicMarch + numEnhancedMarch + 1.0)]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['basic']) * numBasicMarch * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['basic','enhancedBasic']) * numEnhancedMarch * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['ultimate']) * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['followup']) * numFollowupMarch * RobinUltUptime]

    numBasicLynx = 2.0
    numSkillLynx = 1.0
    LynxRotation = [LynxCharacter.useBasic() * numBasicLynx,
                    LynxCharacter.useSkill() * numSkillLynx,
                    LynxCharacter.useUltimate(),]

    RobinRotationLynx = [RobinCharacter.useTalent() * numBasicLynx]
    RobinRotationLynx += [RobinCharacter.useConcertoDamage(['basic']) * numBasicLynx * RobinUltUptime]
    
    # assume 2 procs go to robin, then other 2 split between the rest
    QPQEffect = BaseEffect()
    QPQEffect.energy = 16.0
    LynxCharacter.addDebugInfo(QPQEffect,['buff'],'Quid Pro Quo Energy')
    MarchRotation.append(deepcopy(QPQEffect) * MarchCharacter.getER() )
    RobinRotation.append(deepcopy(QPQEffect) * 2 * RobinCharacter.getER() )
    
    # number of attacks in 2 feixiao turns
    numTurns = 2.0
    numAttacks = numTurns * 3.0 # feixiao attacks
    numAttacks += numTurns * (numBasicMarch + numFollowupMarch + numEnhancedMarch + 1.0) / numBasicMarch  # march attacks
    numAttacks += numTurns * (numBasicLynx) / (numBasicLynx + numSkillLynx) # Lynx attacks
    
    numBasicFeixiao = 0.0
    numSkillFeixiao = 2.0
    numFollowupFeixiao = (numBasicFeixiao + 2.0 * numSkillFeixiao)
    numUltFeixiao = numAttacks * 0.5 + (1.75 * (numBasicFeixiao + numSkillFeixiao) if FeixiaoCharacter.eidolon >= 2 else 0.0)
    
    numBasicFeixiao *= 6.0 / numUltFeixiao
    numSkillFeixiao *= 6.0 / numUltFeixiao
    numFollowupFeixiao *= 6.0 / numUltFeixiao
    numUltFeixiao = 1.0
    
    FeixiaoRotation = []
    FeixiaoRotation += [FeixiaoCharacter.useBasic() * numBasicFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useSkill() * numSkillFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useTalent() * numFollowupFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useUltimate() * numUltFeixiao] 

    RobinRotationFeixiao = [RobinCharacter.useTalent() * (numBasicFeixiao + numSkillFeixiao + numFollowupFeixiao + 1.0)]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['basic']) * numBasicFeixiao * RobinUltUptime]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['skill']) * numSkillFeixiao * RobinUltUptime]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['followup']) * numFollowupFeixiao * RobinUltUptime]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['ultimate','followup']) * RobinUltUptime]

    #%% March Feixiao Robin Lynx Rotation Math

    # four turn robin advance math
    totalRobinEffect = sumEffects(RobinRotation)
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    
    numTurnAV = 300.0 if RobinCharacter.eidolon >= 2 else 400.0

    MarchFourTurns = numTurnAV * MarchCharacter.useBasic().actionvalue / MarchCharacter.getTotalStat('SPD')
    FeixiaoFourTurns = numTurnAV * FeixiaoCharacter.useSkill().actionvalue / FeixiaoCharacter.getTotalStat('SPD')
    LynxFourTurns = numTurnAV * LynxCharacter.useBasic().actionvalue / LynxCharacter.getTotalStat('SPD')
    
    MarchRotation += [RobinCharacter.useAdvanceForward() * (MarchFourTurns - RobinRotationDuration) * MarchCharacter.getTotalStat('SPD') * numBasicMarch / numTurnAV]
    FeixiaoRotation += [RobinCharacter.useAdvanceForward() * (FeixiaoFourTurns - RobinRotationDuration) * FeixiaoCharacter.getTotalStat('SPD') * (numBasicFeixiao + numSkillFeixiao) / numTurnAV]
    LynxRotation += [RobinCharacter.useAdvanceForward() * (LynxFourTurns - RobinRotationDuration) * LynxCharacter.getTotalStat('SPD') * numBasicLynx / numTurnAV]
        
    totalMarchEffect = sumEffects(MarchRotation)
    totalFeixiaoEffect = sumEffects(FeixiaoRotation)
    totalLynxEffect = sumEffects(LynxRotation)
    
    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
    FeixiaoRotationDuration = totalFeixiaoEffect.actionvalue * 100.0 / FeixiaoCharacter.getTotalStat('SPD')
    LynxRotationDuration = totalLynxEffect.actionvalue * 100.0 / LynxCharacter.getTotalStat('SPD')
    
    print('##### Rotation Durations #####')
    print('March: ',MarchRotationDuration * 2.0)
    print('Feixiao: ',FeixiaoRotationDuration * 2.0)
    print('Robin: ',RobinRotationDuration)
    print('Lynx: ',LynxRotationDuration)

    # Scale other character's rotation
    FeixiaoRotation = [x * MarchRotationDuration / FeixiaoRotationDuration for x in FeixiaoRotation]
    RobinRotationFeixiao = [x * MarchRotationDuration / FeixiaoRotationDuration for x in RobinRotationFeixiao]
    RobinRotation = [x * MarchRotationDuration / RobinRotationDuration for x in RobinRotation]
    LynxRotation = [x * MarchRotationDuration / LynxRotationDuration for x in LynxRotation]
    RobinRotationLynx = [x * MarchRotationDuration / LynxRotationDuration for x in RobinRotationLynx]
    
    RobinRotation += RobinRotationMarch
    RobinRotation += RobinRotationFeixiao
    RobinRotation += RobinRotationLynx
    totalRobinEffect = sumEffects(RobinRotation)

    FeixiaoEstimate = DefaultEstimator(f'{FeixiaoCharacter.fullName()} {numSkillFeixiao:.2f}E {numFollowupFeixiao:.1f}T {numUltFeixiao:.1f}Q', FeixiaoRotation, FeixiaoCharacter, config)
    MarchEstimate = DefaultEstimator(f'{MarchCharacter.fullName()} {numBasicMarch:.1f}N {numEnhancedMarch:.1f}Enh 1Q', MarchRotation, MarchCharacter, config)
    RobinEstimate = DefaultEstimator(f'{RobinCharacter.fullName()} {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q', 
                                    RobinRotation, RobinCharacter, config)
    LynxEstimate = DefaultEstimator(f'Lynx: {numBasicLynx:.1f}N {numSkillLynx:.1f}E 1Q, S{LynxCharacter.lightcone.superposition:.0f} {LynxCharacter.lightcone.name}',
                                    LynxRotation, LynxCharacter, config)

    return([FeixiaoEstimate, MarchEstimate, RobinEstimate, LynxEstimate])

