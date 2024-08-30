from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Aventurine import Aventurine
from characters.hunt.Topaz import Topaz
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
from lightCones.hunt.WorrisomeBlissful import WorrisomeBlissful
from lightCones.preservation.DestinysThreadsForewoven import DestinysThreadsForewoven
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.DuranDynastyOfRunningWolves import DuranDynastyOfRunningWolves
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.KnightOfPurityPalace import KnightOfPurityPalace2pc, KnightOfPurityPalace4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc, MusketeerOfWildWheat4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def FeixiaoTopazRobinAventurine(config, 
                                feixiaoEidolon:int=None, 
                                feixiaoLightCone:str='CruisingInTheStellarSea',
                                robinEidolon:int=None, 
                                robinLightCone:str ='PoisedToBloom',
                                topazEidolon:int=None,
                                topazSuperposition:int=0,):
    #%% Topaz Feixiao Robin Aventurine Characters
        
    FeixiaoSubstats = {'CR': 5, 'CD': 10, 'ATK.percent': 3, 'SPD.flat':10}
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

    topazLightcone = Swordplay(**config) if topazSuperposition == 0 else WorrisomeBlissful(superposition=topazSuperposition,**config)
    TopazSubstats = {'CR': 10, 'CD': 5, 'ATK.percent': 3, 'SPD.flat': 10}
    if robinEidolon is not None and robinEidolon >= 2:
        TopazSubstats['SPD.flat'] += 2
        TopazSubstats['CD'] -= 2
    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                                    substats = TopazSubstats),
                                    lightcone = topazLightcone, 
                                    relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = DuranDynastyOfRunningWolves(),
                                    eidolon=topazEidolon,
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
                                    substats = {'ATK.percent': 11, 'SPD.flat': 9, 'RES': 3, 'ATK.flat': 5}),
                                    lightcone = RobinLightCone,
                                    relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                                    eidolon=robinEidolon,
                                    **config)

    AventurineCharacter = Aventurine(RelicStats(mainstats = ['DEF.percent', 'SPD.flat', 'DEF.percent', 'DEF.percent'],
                                    substats = {'CR': 3, 'CD': 5, 'SPD.flat': 12, 'DEF.percent': 8}),
                                    lightcone = DestinysThreadsForewoven(defense=4000,**config),
                                    leverage_cr = 0.48,
                                    relicsetone = KnightOfPurityPalace2pc(), relicsettwo = KnightOfPurityPalace4pc(), planarset = BrokenKeel(),
                                    **config)
    
    team = [TopazCharacter, FeixiaoCharacter, RobinCharacter, AventurineCharacter]

    #%% Topaz Feixiao Robin Aventurine Team Buffs
    for character in [FeixiaoCharacter, TopazCharacter, RobinCharacter]:
        character.addStat('CD',description='Broken Keel from Aventurine',amount=0.1)
    if RobinCharacter.lightcone.name == 'Poised to Bloom':
        for character in [FeixiaoCharacter, TopazCharacter]:
            character.addStat('CD',description='Poised to Bloom',amount=0.12+0.04*RobinCharacter.lightcone.superposition)
    elif RobinCharacter.lightcone.name == 'Flowing Nightglow':
        RobinCharacter.addStat('DMG',description=RobinCharacter.lightcone.name,amount=0.2 + 0.04 * RobinCharacter.lightcone.superposition)
        for character in team:
            if character.name is not 'Robin':
                character.addStat('DMG',description=RobinCharacter.lightcone.name,amount=0.2 + 0.04 * RobinCharacter.lightcone.superposition, uptime=RobinUltUptime)
    elif RobinCharacter.lightcone.name == 'Carve the Moon, Weave the Clouds':
        for character in team:
            character.addStat('ATK.percent',description='Carve The Moon',amount=0.075 + 0.025 * RobinCharacter.lightcone.superposition, uptime=1.0/3.0)
            character.addStat('CD',description='Carve The Moon',amount=0.09 + 0.03 * RobinCharacter.lightcone.superposition, uptime=1.0/3.0)
            character.addStat('ER',description='Carve The Moon',amount=0.045 + 0.015 * RobinCharacter.lightcone.superposition, uptime=1.0/3.0)

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff(team,uptime=1.0)
    if topazSuperposition > 0:
        for character in [FeixiaoCharacter, RobinCharacter, AventurineCharacter]:
                character.addStat('CD',description='Worrisome, Blissful',
                                        amount=0.10 + 0.02 * TopazCharacter.lightcone.superposition,
                                        stacks=2.0)
    
    # Aventurine Buffs
    AventurineCharacter.applyUltDebuff(team=team,rotationDuration=4.0,targetingUptime=1.0)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)

    RobinCharacter.applyUltBuff([FeixiaoCharacter,TopazCharacter,AventurineCharacter],uptime=RobinUltUptime)
    # assume feixiao buff has 100% uptime
    if RobinUltUptime < 1.0:
        RobinCharacter.applyUltBuff([FeixiaoCharacter], uptime=1.0-RobinUltUptime)
    

    #%% Print Statements
    for character in team:
        character.print()

    #%% Topaz Feixiao Robin Aventurine Rotations
    # assume 154 ish spd Topaz and Feixiao, Topaz slower than Feixiao, and 134 ish spd robin
    
    numBasicRobin = 1.0 if RobinCharacter.eidolon < 2 else 0.0
    numSkillRobin = 1.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0, ignoreSpeed=True) # apply robin buff after we calculate damage for her basics

    numBasicTopaz = 2.0 if RobinCharacter.eidolon < 2 else 2.6
    numSkillTopaz = 2.0 if RobinCharacter.eidolon < 2 else 1.6
    numTalentTopaz = (numBasicTopaz + numSkillTopaz) * (2.0 if RobinCharacter.eidolon < 2 else 1.25) + 1.0 # rough estimate
    TopazRotation = []
    TopazRotation += [TopazCharacter.useBasic() * numBasicTopaz]
    TopazRotation += [TopazCharacter.useSkill() * numSkillTopaz]
    TopazRotation += [TopazCharacter.useUltimate()]
    TopazRotation += [TopazCharacter.useTalent(windfall=True) * 2.0] # two talents from windfall
    TopazRotation += [TopazCharacter.useTalent(windfall=False) * (numTalentTopaz - 1.0)] # deducted windfall advances
    
    RobinRotationTopaz = [RobinCharacter.useTalent() * (numBasicTopaz + numSkillTopaz + numTalentTopaz + 2.0)]
    RobinRotationTopaz += [RobinCharacter.useConcertoDamage(['basic','followup']) * numBasicTopaz * RobinUltUptime]
    RobinRotationTopaz += [RobinCharacter.useConcertoDamage(['skill','followup']) * numSkillTopaz * RobinUltUptime]
    RobinRotationTopaz += [RobinCharacter.useConcertoDamage(['followup']) * numTalentTopaz * RobinUltUptime]

    numBasicAventurine = 4.0
    numTalentAventurine = 4.0 # stacks from ultimate
    numEnemyAttacks = AventurineCharacter.numEnemies * AventurineCharacter.enemySpeed / AventurineCharacter.getTotalStat('SPD') # extra stacks from people getting hit per turn
    numEnemyAttacks += (1.0 + (6*1) / (6*1 + 4 + 3 + 3)) # extra stacks from when Aventurine is Targeted
    numTalentAventurine += numBasicAventurine * numEnemyAttacks
    
    numFollowups = 2.5 * FeixiaoCharacter.getTotalStat('SPD') # Feixiao gets about 2.5 followup per turn
    numFollowups += TopazCharacter.getTotalStat('SPD') * (numTalentTopaz + numBasicTopaz + numSkillTopaz) / (numBasicTopaz + numSkillTopaz)
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
    numAttacks += numTurns * (numBasicTopaz + numSkillTopaz + numTalentTopaz + 1.0) / (numBasicTopaz + numSkillTopaz)  # Topaz attacks
    numAttacks += numTurns * (1.0 + numTalentAventurine / 7.0) / numBasicAventurine # aventurine attacks
    
    numBasicFeixiao = 0.0
    numSkillFeixiao = 2.0
    numFollowupFeixiao = (numBasicFeixiao + 2.0 * numSkillFeixiao)
    numUltFeixiao = numAttacks * 0.5 + (3.0 if FeixiaoCharacter.eidolon >= 2 else 0.0)
    
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
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['ultimate','followup']) ] # assume we bank feixiao ults for robin uptime

    #%% Topaz Feixiao Robin Aventurine Rotation Math

    # four turn robin advance math
    totalRobinEffect = sumEffects(RobinRotation)
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    
    numTurnAV = 300.0 if RobinCharacter.eidolon >= 2 else 400.0

    TopazFourTurns = numTurnAV * TopazCharacter.useBasic().actionvalue / TopazCharacter.getTotalStat('SPD')
    FeixiaoFourTurns = numTurnAV * FeixiaoCharacter.useSkill().actionvalue / FeixiaoCharacter.getTotalStat('SPD')
    AventurineFourTurns = numTurnAV * AventurineCharacter.useBasic().actionvalue / AventurineCharacter.getTotalStat('SPD')
    
    TopazRotation += [RobinCharacter.useAdvanceForward() * (TopazFourTurns - RobinRotationDuration) * TopazCharacter.getTotalStat('SPD') * (numBasicTopaz + numSkillTopaz) / numTurnAV]
    FeixiaoRotation += [RobinCharacter.useAdvanceForward() * (FeixiaoFourTurns - RobinRotationDuration) * FeixiaoCharacter.getTotalStat('SPD') * (numBasicFeixiao + numSkillFeixiao) / numTurnAV]
    AventurineRotation += [RobinCharacter.useAdvanceForward() * (AventurineFourTurns - RobinRotationDuration) * AventurineCharacter.getTotalStat('SPD') * numBasicAventurine / numTurnAV]
        
    totalTopazEffect = sumEffects(TopazRotation)
    totalFeixiaoEffect = sumEffects(FeixiaoRotation)
    totalAventurineEffect = sumEffects(AventurineRotation)
    
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    FeixiaoRotationDuration = totalFeixiaoEffect.actionvalue * 100.0 / FeixiaoCharacter.getTotalStat('SPD')
    AventurineRotationDuration = totalAventurineEffect.actionvalue * 100.0 / AventurineCharacter.getTotalStat('SPD')
    
    print('##### Rotation Durations #####')
    print('Topaz: ',TopazRotationDuration * 4.0 / (numBasicTopaz + numSkillTopaz))
    print('Feixiao: ',FeixiaoRotationDuration * 4.0 / numFollowupFeixiao)
    print('Robin: ',RobinRotationDuration)
    print('Aventurine: ',AventurineRotationDuration * 4.0 / numBasicAventurine)

    # Scale other character's rotation
    FeixiaoRotation = [x * TopazRotationDuration / FeixiaoRotationDuration for x in FeixiaoRotation]
    RobinRotationFeixiao = [x * TopazRotationDuration / FeixiaoRotationDuration for x in RobinRotationFeixiao]
    RobinRotation = [x * TopazRotationDuration / RobinRotationDuration for x in RobinRotation]
    AventurineRotation = [x * TopazRotationDuration / AventurineRotationDuration for x in AventurineRotation]
    RobinRotationAventurine = [x * TopazRotationDuration / AventurineRotationDuration for x in RobinRotationAventurine]
    
    RobinRotation += RobinRotationTopaz
    RobinRotation += RobinRotationFeixiao
    RobinRotation += RobinRotationAventurine
    totalRobinEffect = sumEffects(RobinRotation)

    FeixiaoEstimate = DefaultEstimator(f'{FeixiaoCharacter.fullName()} {numSkillFeixiao:.2f}E {numFollowupFeixiao:.1f}T {numUltFeixiao:.1f}Q', FeixiaoRotation, FeixiaoCharacter, config)
    TopazEstimate = DefaultEstimator(f'{TopazCharacter.fullName()} {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numTalentTopaz:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    RobinEstimate = DefaultEstimator(f'{RobinCharacter.fullName()} {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q', 
                                    RobinRotation, RobinCharacter, config)
    AventurineEstimate = DefaultEstimator(f'E{AventurineCharacter.eidolon} S{AventurineCharacter.lightcone.superposition:.0f} {AventurineCharacter.lightcone.name} Aventurine: {numBasicAventurine:.0f}N {numTalentAventurine:.1f}T 1Q',
                                    AventurineRotation, AventurineCharacter, config)

    return([FeixiaoEstimate, TopazEstimate, RobinEstimate, AventurineEstimate])

