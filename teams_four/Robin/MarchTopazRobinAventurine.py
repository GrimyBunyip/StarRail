from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Aventurine import Aventurine
from characters.hunt.ImaginaryMarch import ImaginaryMarch
from characters.harmony.Robin import Robin
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.harmony.CarveTheMoonWeaveTheClouds import CarveTheMoonWeaveTheClouds
from lightCones.harmony.FlowingNightglow import FlowingNightglow
from lightCones.harmony.ForTomorrowsJourney import ForTomorrowsJourney
from lightCones.harmony.PoisedToBloom import PoisedToBloom
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.DestinysThreadsForewoven import DestinysThreadsForewoven
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.KnightOfPurityPalace import KnightOfPurityPalace2pc, KnightOfPurityPalace4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def MarchTopazRobinAventurine(config,
                              robinEidolon:int=None,
                              robinLightCone:str='PoisedToBloom'):
    #%% March Topaz Robin Aventurine Characters
    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                                    substats = {'CR': 12, 'CD': 7, 'ATK.percent': 3, 'SPD.flat': 6}),
                                    lightcone = Swordplay(**config), 
                                    relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    **config)

    MarchCharacter = ImaginaryMarch(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.imaginary'],
                                    substats = {'CD': 6, 'CR': 12, 'ATK.percent': 3, 'SPD.flat': 7}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = WastelanderOfBanditryDesert2pc(),
                                    relicsettwo = WastelanderOfBanditryDesert4pc(uptimeCD=0.0),
                                    planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    master=TopazCharacter,
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
                                    **config)

    AventurineCharacter = Aventurine(RelicStats(mainstats = ['DEF.percent', 'SPD.flat', 'DEF.percent', 'DEF.percent'],
                                    substats = {'CR': 3, 'CD': 5, 'SPD.flat': 12, 'DEF.percent': 8}),
                                    lightcone = DestinysThreadsForewoven(defense=4000,**config),
                                    leverage_cr=0.48,
                                    relicsetone = KnightOfPurityPalace2pc(), relicsettwo = KnightOfPurityPalace4pc(), planarset = BrokenKeel(),
                                    **config)
    
    team = [MarchCharacter, TopazCharacter, RobinCharacter, AventurineCharacter]

    #%% March Topaz Robin Aventurine Team Buffs
    for character in [TopazCharacter, MarchCharacter, RobinCharacter]:
        character.addStat('CD',description='Broken Keel from Aventurine',amount=0.1)
    if RobinCharacter.lightcone.name == 'Poised to Bloom':
        for character in [TopazCharacter, MarchCharacter]:
            character.addStat('CD',description='Poised to Bloom',amount=0.12+0.04*RobinCharacter.lightcone.superposition)
    elif RobinCharacter.lightcone.name == 'Flowing Nightglow':
        for character in team:
            character.addStat('DMG',description=RobinCharacter.lightcone.name,amount=0.2 + 0.04 * RobinCharacter.lightcone.superposition, uptime=RobinUltUptime)
    elif RobinCharacter.lightcone.name == 'Carve the Moon, Weave the Clouds':
        for character in team:
            character.addStat('ATK.percent',description='Carve The Moon',amount=0.2, uptime=1.0/3.0)
            character.addStat('CD',description='Carve The Moon',amount=0.24, uptime=1.0/3.0)
            character.addStat('ER',description='Carve The Moon',amount=0.12, uptime=1.0/3.0)

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff(team,uptime=1.0)
    
    # March Buff
    MarchCharacter.applySkillBuff(TopazCharacter)
    MarchCharacter.applyTalentBuff(TopazCharacter,uptime=1.0)
    
    # Aventurine Buffs
    AventurineCharacter.applyUltDebuff(team=team,rotationDuration=4.0,targetingUptime=1.0)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinCharacter.applyUltBuff([MarchCharacter,TopazCharacter,AventurineCharacter],uptime=RobinUltUptime)

    #%% Print Statements
    for character in team:
        character.print()

    #%% March Topaz Robin Aventurine Rotations
    # assume 154 ish spd March and topaz, March slower than Topaz, and 134 ish spd robin
    
    numBasicRobin = 0.0
    numSkillRobin = 2.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0) # apply robin buff after we calculate damage for her basics

    numBasicTopaz = 0.0
    numSkillTopaz = 3.5
    numTalentTopaz = (numBasicTopaz + numSkillTopaz) * 1.25 + 1.0 # rough estimate
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
    TopazRotation += [RobinCharacter.useAdvanceForward() * (numSkillTopaz + numBasicTopaz) / 4.0]
    
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
    MarchRotation += [RobinCharacter.useAdvanceForward() * numBasicMarch / 4.0] 

    numBasicAventurine = 4.0
    numTalentAventurine = 4.0 # stacks from ultimate
    numEnemyAttacks = AventurineCharacter.numEnemies * AventurineCharacter.enemySpeed / AventurineCharacter.getTotalStat('SPD') # extra stacks from people getting hit per turn
    numEnemyAttacks += (1.0 + (6*1) / (6*1 + 4 + 3 + 3)) # extra stacks from when Aventurine is Targeted
    numTalentAventurine += numBasicAventurine * numEnemyAttacks
    
    numFollowups = (numTalentTopaz + 2.0) * TopazCharacter.getTotalStat('SPD') / 4.0 # Topaz gets about this many followup attacks per her turns, 4 turn rotation
    numFollowups += MarchCharacter.getTotalStat('SPD') # March gets about 1 followup per turn
    numFollowups /= AventurineCharacter.getTotalStat('SPD')
    numTalentAventurine += numBasicAventurine * min(3.0,numFollowups)
    
    AventurineRotation = [AventurineCharacter.useBasic() * numBasicAventurine,
                          AventurineCharacter.useTalent() * numTalentAventurine,
                          AventurineCharacter.useUltimate() * 1,
                          RobinCharacter.useAdvanceForward() * numBasicAventurine / 4.0,]

    RobinRotationAventurine = [RobinCharacter.useTalent() * (numBasicAventurine + numTalentAventurine / 7.0)]
    RobinRotationAventurine += [RobinCharacter.useConcertoDamage(['basic']) * numBasicAventurine * RobinUltUptime]
    RobinRotationAventurine += [RobinCharacter.useConcertoDamage(['followup']) * (numTalentAventurine / 7.0) * RobinUltUptime]

    #%% March Topaz Robin Aventurine Rotation Math

    totalMarchEffect = sumEffects(MarchRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalAventurineEffect = sumEffects(AventurineRotation)

    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    AventurineRotationDuration = totalAventurineEffect.actionvalue * 100.0 / AventurineCharacter.getTotalStat('SPD')    

    print('##### Rotation Durations #####')
    print('March: ',MarchRotationDuration)
    print('Topaz: ',TopazRotationDuration)
    print('Robin: ',RobinRotationDuration)
    print('Aventurine: ',AventurineRotationDuration)

    # Scale other character's rotation
    TopazRotation = [x * MarchRotationDuration / TopazRotationDuration for x in TopazRotation]
    RobinRotationTopaz = [x * MarchRotationDuration / TopazRotationDuration for x in RobinRotationTopaz]
    RobinRotation = [x * MarchRotationDuration / RobinRotationDuration for x in RobinRotation]
    AventurineRotation = [x * MarchRotationDuration / AventurineRotationDuration for x in AventurineRotation]
    RobinRotationAventurine = [x * MarchRotationDuration / AventurineRotationDuration for x in RobinRotationAventurine]
    
    RobinRotation += RobinRotationMarch
    RobinRotation += RobinRotationTopaz
    RobinRotation += RobinRotationAventurine
    totalRobinEffect = sumEffects(RobinRotation)

    MarchEstimate = DefaultEstimator(f'March: {numBasicMarch:.1f}N {numEnhancedMarch:.1f}Enh 1Q', MarchRotation, MarchCharacter, config)
    TopazEstimate = DefaultEstimator(f'Topaz: {TopazCharacter.lightcone.name} {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numTalentTopaz:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    RobinEstimate = DefaultEstimator(f'{RobinCharacter.fullName()} {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q', 
                                    RobinRotation, RobinCharacter, config)
    AventurineEstimate = DefaultEstimator(f'Aventurine: {numBasicAventurine:.0f}N {numTalentAventurine:.1f}T 1Q, S{AventurineCharacter.lightcone.superposition:.0f} {AventurineCharacter.lightcone.name}',
                                    AventurineRotation, AventurineCharacter, config)

    return([MarchEstimate, TopazEstimate, AventurineEstimate, RobinEstimate])

