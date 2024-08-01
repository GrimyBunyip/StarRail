from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.hunt.ImaginaryMarch import ImaginaryMarch
from characters.harmony.Robin import Robin
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.QuidProQuo import QuidProQuo
from lightCones.harmony.FlowingNightglow import FlowingNightglow
from lightCones.harmony.PoisedToBloom import PoisedToBloom
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.DestinysThreadsForewoven import DestinysThreadsForewoven
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.KnightOfPurityPalace import KnightOfPurityPalace2pc, KnightOfPurityPalace4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def MarchTopazRobinGallagher(config,
                             robinEidolon:int=None,
                             robinSuperposition:int=0):
    #%% March Topaz Robin Gallagher Characters
    topazSubstats = {'CR': 12, 'CD': 8, 'ATK.percent': 3, 'SPD.flat': 5} if robinEidolon is None or robinEidolon < 2 else {'CR': 12, 'CD': 6, 'ATK.percent': 3, 'SPD.flat': 7}
    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                                    substats = topazSubstats),
                                    lightcone = Swordplay(**config), 
                                    relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    **config)

    marchSubstats = {'CD': 7, 'CR': 12, 'ATK.percent': 3, 'SPD.flat': 6} if robinEidolon is None or robinEidolon < 2 else {'CD': 6, 'CR': 10, 'ATK.percent': 3, 'SPD.flat': 9}
    MarchCharacter = ImaginaryMarch(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.imaginary'],
                                    substats = marchSubstats),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = WastelanderOfBanditryDesert2pc(),
                                    relicsettwo = WastelanderOfBanditryDesert4pc(uptimeCD=0.0),
                                    planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    master=TopazCharacter,
                                    **config)
    
    RobinLightCone = PoisedToBloom(**config) if robinSuperposition == 0 else FlowingNightglow(superposition=robinSuperposition,**config)
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 11, 'SPD.flat': 9, 'RES': 3, 'ATK.flat': 5}),
                                    lightcone = RobinLightCone,
                                    relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                                    eidolon=robinEidolon,
                                    **config)

    gallagherSubstats = {'BreakEffect': 10, 'SPD.flat': 9, 'HP.percent': 3, 'RES': 6} if robinEidolon is None or robinEidolon < 2 else {'BreakEffect': 7, 'SPD.flat': 13, 'HP.percent': 3, 'RES': 6}
    GallagherCharacter = Gallagher(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                                    substats = gallagherSubstats),
                                    lightcone = QuidProQuo(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = ThiefOfShootingMeteor2pc(), planarset = ForgeOfTheKalpagniLantern(),
                                    **config)
    
    team = [MarchCharacter, TopazCharacter, RobinCharacter, GallagherCharacter]

    #%% March Topaz Robin Gallagher Team Buffs
    for character in [TopazCharacter, MarchCharacter]:
        character.addStat('CD',description='Poised to Bloom',amount=0.12+0.04*RobinCharacter.lightcone.superposition)

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff(team,uptime=1.0)
    
    # March Buff
    MarchCharacter.applySkillBuff(TopazCharacter)
    MarchCharacter.applyTalentBuff(TopazCharacter,uptime=1.0)
    
    # Gallagher Buffs
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=3.0)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinUltUptime = 1.0 if RobinCharacter.eidolon >= 2 else 0.5
    RobinCharacter.applyUltBuff([MarchCharacter,TopazCharacter,GallagherCharacter],uptime=RobinUltUptime)

    #%% Print Statements
    for character in team:
        character.print()

    #%% March Topaz Robin Gallagher Rotations
    # assume 154 ish spd March and topaz, March slower than Topaz, and 134 ish spd robin
    
    numBasicRobin = 0.0
    numSkillRobin = 1.0 if RobinCharacter.eidolon >= 2 else 2.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0) # apply robin buff after we calculate damage for her basics

    numBasicTopaz = 0.0
    numSkillTopaz = 3.5
    numTalentTopaz = (numBasicTopaz + numSkillTopaz) * 1.0 + 1.0 # rough estimate
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
    
    numBasicMarch = 2.0
    numFollowupMarch = numBasicMarch
    numEnhancedMarch = 1.0
    
    MarchRotation = []
    MarchRotation += [MarchCharacter.useBasic() * numBasicMarch]
    MarchRotation += [MarchCharacter.useFollowup() * numFollowupMarch]
    MarchRotation += [MarchCharacter.useEnhancedBasic(actionValue=0.0, numHits=5.0, chance=0.8) * numEnhancedMarch]
    MarchRotation += [MarchCharacter.useUltimate()] 

    RobinRotationMarch = [RobinCharacter.useTalent() * (2.0 * numBasicMarch + numEnhancedMarch + 1.0)]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['basic']) * numBasicMarch * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['basic','enhancedBasic']) * numEnhancedMarch * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['ultimate']) * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['followup']) * numFollowupMarch * RobinUltUptime]

    numBasicGallagher = 2.0 if RobinCharacter.eidolon >= 2 else 4.0
    numSkillGallagher = 1.0 if RobinCharacter.eidolon >= 2 else 0.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useSkill() * numSkillGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1,]

    RobinRotationGallagher = [RobinCharacter.useTalent() * (numBasicGallagher + numEnhancedGallagher + 1.0)]
    RobinRotationGallagher += [RobinCharacter.useConcertoDamage(['basic']) * (numBasicGallagher + numEnhancedGallagher) * RobinUltUptime]
    RobinRotationGallagher += [RobinCharacter.useConcertoDamage(['ultimate']) * 1.0 * RobinUltUptime]
    
    # assume 2 procs go to robin, then other 2 split between the rest
    QPQEffect = BaseEffect()
    QPQEffect.energy = 16.0
    GallagherCharacter.addDebugInfo(QPQEffect,['buff'],'Quid Pro Quo Energy')
    RobinRotation.append(deepcopy(QPQEffect) * 2 * RobinCharacter.getER() )
    MarchRotation.append(deepcopy(QPQEffect) * MarchCharacter.getER() )

    #%% March Topaz Robin Gallagher Rotation Math

    totalRobinEffect = sumEffects(RobinRotation)
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    
    numTurnAV = 300.0 if RobinCharacter.eidolon >= 2 else 400.0

    MarchNumTurns = numTurnAV * MarchCharacter.useBasic().actionvalue / MarchCharacter.getTotalStat('SPD')
    TopazNumTurns = numTurnAV * TopazCharacter.useSkill().actionvalue / TopazCharacter.getTotalStat('SPD')
    GallagherNumTurns = numTurnAV * GallagherCharacter.useBasic().actionvalue / GallagherCharacter.getTotalStat('SPD')
    
    MarchRotation += [RobinCharacter.useAdvanceForward() * (MarchNumTurns - RobinRotationDuration) * MarchCharacter.getTotalStat('SPD') * numBasicMarch / numTurnAV]
    TopazRotation += [RobinCharacter.useAdvanceForward() * (TopazNumTurns - RobinRotationDuration) * TopazCharacter.getTotalStat('SPD') * (numBasicTopaz + numSkillTopaz) / numTurnAV]
    GallagherRotation += [RobinCharacter.useAdvanceForward() * (GallagherNumTurns - RobinRotationDuration) * GallagherCharacter.getTotalStat('SPD') * (numBasicGallagher + numSkillGallagher) / numTurnAV]
        
    totalMarchEffect = sumEffects(MarchRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)
    
    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('March: ',MarchRotationDuration)
    print('Topaz: ',TopazRotationDuration)
    print('Robin: ',RobinRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    TopazRotation = [x * MarchRotationDuration / TopazRotationDuration for x in TopazRotation]
    RobinRotationTopaz = [x * MarchRotationDuration / TopazRotationDuration for x in RobinRotationTopaz]
    RobinRotation = [x * MarchRotationDuration / RobinRotationDuration for x in RobinRotation]
    GallagherRotation = [x * MarchRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    RobinRotationGallagher = [x * MarchRotationDuration / GallagherRotationDuration for x in RobinRotationGallagher]
    
    RobinRotation += RobinRotationMarch
    RobinRotation += RobinRotationTopaz
    RobinRotation += RobinRotationGallagher
    totalRobinEffect = sumEffects(RobinRotation)

    MarchEstimate = DefaultEstimator(f'March: {numBasicMarch:.1f}N {numEnhancedMarch:.1f}Enh 1Q', MarchRotation, MarchCharacter, config)
    TopazEstimate = DefaultEstimator(f'{TopazCharacter.rotationPrefix} {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numTalentTopaz:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    GallagherEstimate = DefaultEstimator(f'{GallagherCharacter.rotationPrefix} {numBasicGallagher:.0f}N {numSkillGallagher:.0f}E {numEnhancedGallagher:.0f}Enh 1Q', 
                                    GallagherRotation, GallagherCharacter, config)
    RobinEstimate = DefaultEstimator(f'{RobinCharacter.rotationPrefix} {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q', 
                                    RobinRotation, RobinCharacter, config)

    return([MarchEstimate, TopazEstimate, RobinEstimate, GallagherEstimate])

