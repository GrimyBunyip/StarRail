from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Aventurine import Aventurine
from characters.hunt.ImaginaryMarch import ImaginaryMarch
from characters.harmony.Robin import Robin
from characters.hunt.Feixiao import Feixiao
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.harmony.CarveTheMoonWeaveTheClouds import CarveTheMoonWeaveTheClouds
from lightCones.harmony.FlowingNightglow import FlowingNightglow
from lightCones.harmony.ForTomorrowsJourney import ForTomorrowsJourney
from lightCones.harmony.PoisedToBloom import PoisedToBloom
from lightCones.hunt.BaptismOfPureThought import BaptismOfPureThought
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.IVentureForthToHunt import IVentureForthToHunt
from lightCones.hunt.InTheNight import InTheNight
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.DestinysThreadsForewoven import DestinysThreadsForewoven
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.DuranDynastyOfRunningWolves import DuranDynastyOfRunningWolves
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.KnightOfPurityPalace import KnightOfPurityPalace2pc, KnightOfPurityPalace4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc, MusketeerOfWildWheat4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def FeixiaoMarchRobinAventurine(config, 
                                feixiaoEidolon:int=None, 
                                feixiaoSuperposition:int=0, 
                                feixiaoLightCone:str='CruisingInTheStellarSea',
                                robinEidolon:int=None, 
                                robinLightCone:str='PoisedToBloom'):
    #%% March Feixiao Robin Aventurine Characters

    FeixiaoSubstats = {'CR': 7, 'CD': 12, 'ATK.percent': 4, 'SPD.flat':5} if feixiaoSuperposition == 0 else {'CR': 10, 'CD': 11, 'ATK.percent': 3, 'SPD.flat':4}
    if robinEidolon is not None and robinEidolon >= 2:
        FeixiaoSubstats['SPD.flat'] += 1
        FeixiaoSubstats['CD'] -= 1
        
    if feixiaoLightCone == 'CruisingInTheStellarSea':
        FeixiaoLightcone = CruisingInTheStellarSea(**config)
    elif feixiaoLightCone == 'IVentureForthToHunt':
        FeixiaoLightcone = IVentureForthToHunt(**config)
        FeixiaoSubstats['CR'] += 5
        FeixiaoSubstats['CD'] -= 5
    elif feixiaoLightCone == 'InTheNight':
        FeixiaoLightcone = InTheNight(**config)
        FeixiaoSubstats['CR'] += 4
        FeixiaoSubstats['CD'] -= 4
    elif feixiaoLightCone == 'BaptismOfPureThought':
        FeixiaoLightcone = BaptismOfPureThought(**config)
        FeixiaoSubstats['CR'] += 5
        FeixiaoSubstats['CD'] -= 5
    FeixiaoCharacter = Feixiao(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.wind'],
                                    substats = FeixiaoSubstats),
                                    lightcone = FeixiaoLightcone,
                                    relicsetone = WindSoaringValorous2pc(),
                                    relicsettwo = WindSoaringValorous4pc(),
                                    planarset = DuranDynastyOfRunningWolves(),
                                    eidolon = feixiaoEidolon,
                                    **config)

    # give March swordplay if Feixiao uses Cruising
    MarchLightCone = Swordplay(**config)
    MarchSubstats = {'CD': 5, 'CR': 12, 'ATK.percent': 3, 'SPD.flat': 8}
    if robinEidolon is not None and robinEidolon >= 2:
        MarchSubstats['SPD.flat'] += 2
        MarchSubstats['CD'] -= 2
    MarchCharacter = ImaginaryMarch(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ATK.percent'],
                                    substats = MarchSubstats),
                                    lightcone = MarchLightCone,
                                    relicsetone = MusketeerOfWildWheat2pc(),
                                    relicsettwo = MusketeerOfWildWheat4pc(),
                                    planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    master=FeixiaoCharacter,
                                    **config)
    

    RobinUltUptime = 0.5 if robinEidolon is None or robinEidolon < 2 else 1.0
    if robinLightCone == 'PoisedToBloom':
        RobinLightCone = PoisedToBloom(**config)
    elif robinLightCone == 'FlowingNightglow':
        RobinLightCone = FlowingNightglow(**config, uptime=RobinUltUptime)
    elif robinLightCone == 'ForTomorrowsJourney':
        RobinLightCone = ForTomorrowsJourney(**config)
    elif robinLightCone == 'CarveTheMoonWeaveTheClouds':
        RobinLightCone = CarveTheMoonWeaveTheClouds(**config)
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 11, 'SPD.flat': 9, 'RES': 3, 'ATK.flat': 6}),
                                    lightcone = RobinLightCone,
                                    relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                                    eidolon=robinEidolon,
                                    ultUptime=RobinUltUptime,
                                    **config)

    AventurineCharacter = Aventurine(RelicStats(mainstats = ['DEF.percent', 'SPD.flat', 'DEF.percent', 'DEF.percent'],
                                    substats = {'CR': 3, 'CD': 5, 'SPD.flat': 12, 'DEF.percent': 8}),
                                    lightcone = DestinysThreadsForewoven(defense=4000,**config),
                                    leverage_cr = 0.48,
                                    relicsetone = KnightOfPurityPalace2pc(), relicsettwo = KnightOfPurityPalace4pc(), planarset = BrokenKeel(),
                                    **config)
    
    team = [MarchCharacter, FeixiaoCharacter, RobinCharacter, AventurineCharacter]

    #%% March Feixiao Robin Aventurine Team Buffs

    # March Buff
    MarchCharacter.applySkillBuff(FeixiaoCharacter)
    MarchCharacter.applyTalentBuff(FeixiaoCharacter,uptime=1.0)
    
    # Aventurine Buffs
    AventurineCharacter.applyUltDebuff(team=team,rotationDuration=4.0,targetingUptime=1.0)

    # Robin Buffs
    RobinCharacter.applyUltBuff([FeixiaoCharacter, MarchCharacter,AventurineCharacter],uptime=RobinUltUptime)
    # assume feixiao buff has 100% uptime
    if RobinUltUptime < 1.0:
        RobinCharacter.applyUltBuff([FeixiaoCharacter], uptime=1.0-RobinUltUptime)

    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
    for character in team:
        character.print()

    #%% March Feixiao Robin Aventurine Rotations
    # assume 154 ish spd March and Feixiao, March slower than Feixiao, and 134 ish spd robin
    
    numBasicRobin = 0.0
    numSkillRobin = 2.0 if RobinCharacter.eidolon < 2 else 1.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0, ignoreSpeed=True) # apply robin buff after we calculate damage for her basics
    
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
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['followup']) * numFollowupMarch * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['ultimate']) * RobinUltUptime]

    numBasicAventurine = 4.0
    numTalentAventurine = 4.0 # stacks from ultimate
    numEnemyAttacks = AventurineCharacter.numEnemies * AventurineCharacter.enemySpeed / AventurineCharacter.getTotalStat('SPD') # extra stacks from people getting hit per turn
    numEnemyAttacks += (1.0 + (6*1) / (6*1 + 4 + 3 + 3)) # extra stacks from when Aventurine is Targeted
    numTalentAventurine += numBasicAventurine * numEnemyAttacks
    
    numFollowups = 2.5 * FeixiaoCharacter.getTotalStat('SPD') # Feixiao gets followup per turn
    numFollowups += MarchCharacter.getTotalStat('SPD') # March gets about 1 followup per turn
    numFollowups /= AventurineCharacter.getTotalStat('SPD')
    numTalentAventurine += numBasicAventurine * min(3.0,numFollowups)
    
    AventurineRotation = [AventurineCharacter.useBasic() * numBasicAventurine,
                          AventurineCharacter.useTalent() * numTalentAventurine,
                          AventurineCharacter.useUltimate() * 1,]

    RobinRotationAventurine = [RobinCharacter.useTalent() * (numBasicAventurine + numTalentAventurine / 7.0)]
    RobinRotationAventurine += [RobinCharacter.useConcertoDamage(['basic']) * numBasicAventurine * RobinUltUptime]
    RobinRotationAventurine += [RobinCharacter.useConcertoDamage(['followup']) * (numTalentAventurine / 7.0) * RobinUltUptime]
    
    # number of attacks in 2 feixiao turns
    numTurns = 2.0
    numAttacks = numTurns * 3.0 # feixiao attacks
    numAttacks += numTurns * (numBasicMarch + numFollowupMarch + numEnhancedMarch + 1.0) / numBasicMarch  # march attacks
    numAttacks += numTurns * (1.0 + numTalentAventurine / 7.0) / numBasicAventurine # aventurine attacks
    
    numBasicFeixiao = 0.0
    numSkillFeixiao = 2.0
    numFollowupFeixiao = (numBasicFeixiao + 2.0 * numSkillFeixiao)
    numUltFeixiao = numAttacks * 0.5 + (2.34 * (numBasicFeixiao + numSkillFeixiao) if FeixiaoCharacter.eidolon >= 2 else 0.0)
    
    numUltFeixiao = numUltFeixiao / 6.0
    
    FeixiaoRotation = []
    FeixiaoRotation += [FeixiaoCharacter.useBasic() * numBasicFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useSkill() * numSkillFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useTalent() * numFollowupFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useUltimate() * numUltFeixiao] 

    RobinRotationFeixiao = [RobinCharacter.useTalent() * (numBasicFeixiao + numSkillFeixiao + numFollowupFeixiao + 1.0)]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['basic']) * numBasicFeixiao * RobinUltUptime]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['skill']) * numSkillFeixiao * RobinUltUptime]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['followup']) * numFollowupFeixiao * RobinUltUptime]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['ultimate','followup'])] # assume we bank feixiao ults for robin uptime

    #%% March Feixiao Robin Aventurine Rotation Math

    # four turn robin advance math
    totalRobinEffect = sumEffects(RobinRotation)
    print(RobinCharacter.getTotalStat('SPD'))
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    
    numTurnAV = 300.0 if RobinCharacter.eidolon >= 2 else 400.0

    MarchFourTurns = numTurnAV * MarchCharacter.useBasic().actionvalue / MarchCharacter.getTotalStat('SPD')
    FeixiaoFourTurns = numTurnAV * FeixiaoCharacter.useSkill().actionvalue / FeixiaoCharacter.getTotalStat('SPD')
    AventurineFourTurns = numTurnAV * AventurineCharacter.useBasic().actionvalue / AventurineCharacter.getTotalStat('SPD')
    
    MarchRotation += [RobinCharacter.useAdvanceForward() * (MarchFourTurns - RobinRotationDuration) * MarchCharacter.getTotalStat('SPD') * numBasicMarch / numTurnAV]
    FeixiaoRotation += [RobinCharacter.useAdvanceForward() * (FeixiaoFourTurns - RobinRotationDuration) * FeixiaoCharacter.getTotalStat('SPD') * (numBasicFeixiao + numSkillFeixiao) / numTurnAV]
    AventurineRotation += [RobinCharacter.useAdvanceForward() * (AventurineFourTurns - RobinRotationDuration) * AventurineCharacter.getTotalStat('SPD') * numBasicAventurine / numTurnAV]
        
    totalMarchEffect = sumEffects(MarchRotation)
    totalFeixiaoEffect = sumEffects(FeixiaoRotation)
    totalAventurineEffect = sumEffects(AventurineRotation)
    
    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
    FeixiaoRotationDuration = totalFeixiaoEffect.actionvalue * 100.0 / FeixiaoCharacter.getTotalStat('SPD')
    AventurineRotationDuration = totalAventurineEffect.actionvalue * 100.0 / AventurineCharacter.getTotalStat('SPD')
    
    print('##### Rotation Durations #####')
    print('March: ',MarchRotationDuration * 2.0)
    print('Feixiao: ',FeixiaoRotationDuration * 2.0)
    print('Robin: ',RobinRotationDuration)
    print('Aventurine: ',AventurineRotationDuration)

    # Scale other character's rotation
    FeixiaoRotation = [x * MarchRotationDuration / FeixiaoRotationDuration for x in FeixiaoRotation]
    RobinRotationFeixiao = [x * MarchRotationDuration / FeixiaoRotationDuration for x in RobinRotationFeixiao]
    RobinRotation = [x * MarchRotationDuration / RobinRotationDuration for x in RobinRotation]
    AventurineRotation = [x * MarchRotationDuration / AventurineRotationDuration for x in AventurineRotation]
    RobinRotationAventurine = [x * MarchRotationDuration / AventurineRotationDuration for x in RobinRotationAventurine]
    
    RobinRotation += RobinRotationMarch
    RobinRotation += RobinRotationFeixiao
    RobinRotation += RobinRotationAventurine
    totalRobinEffect = sumEffects(RobinRotation)

    FeixiaoEstimate = DefaultEstimator(f'{FeixiaoCharacter.fullName()} {numSkillFeixiao:.2f}E {numFollowupFeixiao:.1f}T {numUltFeixiao:.1f}Q', FeixiaoRotation, FeixiaoCharacter, config)
    MarchEstimate = DefaultEstimator(f'{MarchCharacter.fullName()} {numBasicMarch:.1f}N {numEnhancedMarch:.1f}Enh 1Q', MarchRotation, MarchCharacter, config)
    RobinEstimate = DefaultEstimator(f'{RobinCharacter.fullName()} {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q', 
                                    RobinRotation, RobinCharacter, config)
    AventurineEstimate = DefaultEstimator(f'E{AventurineCharacter.eidolon} S{AventurineCharacter.lightcone.superposition:.0f} {AventurineCharacter.lightcone.name} Aventurine: {numBasicAventurine:.0f}N {numTalentAventurine:.1f}T 1Q',
                                    AventurineRotation, AventurineCharacter, config)

    return([FeixiaoEstimate, MarchEstimate, RobinEstimate, AventurineEstimate])

