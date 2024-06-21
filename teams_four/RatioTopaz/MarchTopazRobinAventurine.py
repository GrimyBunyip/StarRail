from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Aventurine import Aventurine
from characters.hunt.ImaginaryMarch import ImaginaryMarch
from characters.harmony.Robin import Robin
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.harmony.PoisedToBloom import PoisedToBloom
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.DestinysThreadsForewoven import DestinysThreadsForewoven
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.KnightOfPurityPalace import KnightOfPurityPalace2pc, KnightOfPurityPalace4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def MarchTopazRobinAventurine(config):
    #%% ImaginaryMarch Topaz Robin Aventurine Characters
    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                                    substats = {'CR': 12, 'CD': 8, 'ATK.percent': 4, 'SPD.flat': 4}),
                                    lightcone = Swordplay(**config), 
                                    relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    **config)

    ImaginaryMarchCharacter = ImaginaryMarch(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.imaginary'],
                                    substats = {'CD': 8, 'CR': 12, 'ATK.percent': 3, 'SPD.flat': 5}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = WastelanderOfBanditryDesert2pc(),
                                    relicsettwo = WastelanderOfBanditryDesert4pc(uptimeCD=0.0),
                                    planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    master=TopazCharacter,
                                    **config)
    
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 8, 'SPD.flat': 12, 'RES': 3, 'ATK.flat': 5}),
                                    lightcone = PoisedToBloom(**config),
                                    relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = BrokenKeel(),
                                    **config)

    AventurineCharacter = Aventurine(RelicStats(mainstats = ['DEF.percent', 'SPD.flat', 'DEF.percent', 'DEF.percent'],
                                    substats = {'CR': 3, 'CD': 5, 'SPD.flat': 10, 'DEF.percent': 10}),
                                    lightcone = DestinysThreadsForewoven(defense=4000,**config),
                                    leverage_cr=0.48,
                                    relicsetone = KnightOfPurityPalace2pc(), relicsettwo = KnightOfPurityPalace4pc(), planarset = BrokenKeel(),
                                    **config)
    
    team = [ImaginaryMarchCharacter, TopazCharacter, RobinCharacter, AventurineCharacter]

    #%% ImaginaryMarch Topaz Robin Aventurine Team Buffs
    for character in [TopazCharacter, ImaginaryMarchCharacter, RobinCharacter]:
        character.addStat('CD',description='Broken Keel from Aventurine',amount=0.1)
    for character in [TopazCharacter, ImaginaryMarchCharacter, AventurineCharacter]:
        character.addStat('CD',description='Broken Keel from Robin',amount=0.1)
    for character in [TopazCharacter, ImaginaryMarchCharacter]:
        character.addStat('CD',description='Poised to Bloom',amount=0.12+0.04*RobinCharacter.lightcone.superposition)

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff(team,uptime=1.0)
    
    # March Buff
    ImaginaryMarchCharacter.applySkillBuff(TopazCharacter)
    ImaginaryMarchCharacter.applyE6Buff(TopazCharacter,uptime=1.0)
    
    # Aventurine Buffs
    AventurineCharacter.applyUltDebuff(team=team,rotationDuration=4.0,targetingUptime=1.0)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinUltUptime = 0.5 # assume better robin ult uptime because of shorter robin rotation
    RobinCharacter.applyUltBuff([ImaginaryMarchCharacter,TopazCharacter,AventurineCharacter],uptime=RobinUltUptime)

    #%% Print Statements
    for character in team:
        character.print()

    #%% ImaginaryMarch Topaz Robin Aventurine Rotations
    # assume 154 ish spd March and topaz, March slower than Topaz, and 134 ish spd robin
    
    numBasicRobin = 2.0
    numSkillRobin = 1.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0) # apply robin buff after we calculate damage for her basics
    
    numBasicMarch = 2.0
    numEnhancedMarch = 1.2
    
    ImaginaryMarchRotation = []
    ImaginaryMarchRotation += [ImaginaryMarchCharacter.useBasic() * numBasicMarch]
    ImaginaryMarchRotation += [ImaginaryMarchCharacter.useFollowup() * numBasicMarch]
    ImaginaryMarchRotation += [ImaginaryMarchCharacter.useEnhancedBasic(actionValue=0.0, numHits=5.0, chance=0.8) * numEnhancedMarch]
    ImaginaryMarchRotation += [ImaginaryMarchCharacter.useUltimate()] 

    RobinRotationMarch = [RobinCharacter.useTalent() * (2.0 * numBasicMarch + numEnhancedMarch + 1.0)]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['basic']) * numBasicMarch * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['basic','enhancedBasic']) * numEnhancedMarch * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['ultimate']) * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['followup']) * numBasicMarch * RobinUltUptime]
    ImaginaryMarchRotation += [RobinCharacter.useAdvanceForward() * numBasicMarch / 4.0] 

    numBasicTopaz = 0.0
    numSkillTopaz = 3.5
    numTalentTopaz = (numBasicTopaz + numSkillTopaz) * 1.25 # rough estimate
    TopazRotation = []
    TopazRotation += [TopazCharacter.useBasic() * numBasicTopaz]
    TopazRotation += [TopazCharacter.useSkill() * numSkillTopaz]
    TopazRotation += [TopazCharacter.useUltimate()]
    TopazRotation += [TopazCharacter.useTalent(windfall=True) * 2.0] # two talents from windfall
    TopazRotation += [TopazCharacter.useTalent(windfall=False) * numTalentTopaz]
    
    RobinRotationTopaz = [RobinCharacter.useTalent() * (numBasicTopaz + numSkillTopaz + numTalentTopaz + 2.0)]
    RobinRotationTopaz += [RobinCharacter.useConcertoDamage(['basic','followup']) * numBasicTopaz * RobinUltUptime]
    RobinRotationTopaz += [RobinCharacter.useConcertoDamage(['skill','followup']) * numSkillTopaz * RobinUltUptime]
    RobinRotationTopaz += [RobinCharacter.useConcertoDamage(['followup']) * numTalentTopaz * RobinUltUptime]
    TopazRotation += [RobinCharacter.useAdvanceForward() * (numSkillTopaz + numBasicTopaz) / 4.0]

    numBasicAventurine = 4.0
    numTalentAventurine = 4.0 # stacks from ultimate
    numEnemyAttacks = AventurineCharacter.numEnemies * AventurineCharacter.enemySpeed / AventurineCharacter.getTotalStat('SPD') # extra stacks from people getting hit per turn
    numEnemyAttacks += (1.0 + (6*1) / (6*1 + 4 + 3 + 3)) # extra stacks from when Aventurine is Targeted
    numTalentAventurine += numBasicAventurine * numEnemyAttacks
    
    numFollowups = (numTalentTopaz + 2.0) * TopazCharacter.getTotalStat('SPD') / 4.0 # Topaz gets about this many followup attacks per her turns, 4 turn rotation
    numFollowups += ImaginaryMarchCharacter.getTotalStat('SPD') # March gets about 1 followup per turn
    numFollowups /= AventurineCharacter.getTotalStat('SPD')
    numTalentAventurine += numBasicAventurine * numFollowups
    
    AventurineRotation = [AventurineCharacter.useBasic() * numBasicAventurine,
                          AventurineCharacter.useTalent() * numTalentAventurine,
                          AventurineCharacter.useUltimate() * 1,
                          RobinCharacter.useAdvanceForward() * numBasicAventurine / 4.0,]

    RobinRotationAventurine = [RobinCharacter.useTalent() * (numBasicAventurine + numTalentAventurine / 7.0)]
    RobinRotationAventurine += [RobinCharacter.useConcertoDamage(['basic']) * numBasicAventurine * RobinUltUptime]
    RobinRotationAventurine += [RobinCharacter.useConcertoDamage(['followup']) * (numTalentAventurine / 7.0) * RobinUltUptime]

    #%% ImaginaryMarch Topaz Robin Aventurine Rotation Math

    totalImaginaryMarchEffect = sumEffects(ImaginaryMarchRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalAventurineEffect = sumEffects(AventurineRotation)

    ImaginaryMarchRotationDuration = totalImaginaryMarchEffect.actionvalue * 100.0 / ImaginaryMarchCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    AventurineRotationDuration = totalAventurineEffect.actionvalue * 100.0 / AventurineCharacter.getTotalStat('SPD')    

    print('##### Rotation Durations #####')
    print('ImaginaryMarch: ',ImaginaryMarchRotationDuration)
    print('Topaz: ',TopazRotationDuration)
    print('Robin: ',RobinRotationDuration)
    print('Aventurine: ',AventurineRotationDuration)

    # Scale other character's rotation
    TopazRotation = [x * ImaginaryMarchRotationDuration / TopazRotationDuration for x in TopazRotation]
    RobinRotationTopaz = [x * ImaginaryMarchRotationDuration / TopazRotationDuration for x in RobinRotationTopaz]
    RobinRotation = [x * ImaginaryMarchRotationDuration / RobinRotationDuration for x in RobinRotation]
    AventurineRotation = [x * ImaginaryMarchRotationDuration / AventurineRotationDuration for x in AventurineRotation]
    RobinRotationAventurine = [x * ImaginaryMarchRotationDuration / AventurineRotationDuration for x in RobinRotationAventurine]
    
    RobinRotation += RobinRotationMarch
    RobinRotation += RobinRotationTopaz
    RobinRotation += RobinRotationAventurine
    totalRobinEffect = sumEffects(RobinRotation)

    ImaginaryMarchEstimate = DefaultEstimator(f'ImaginaryMarch: {numBasicMarch:.1f}N {numEnhancedMarch:.1f}Enh 1Q', ImaginaryMarchRotation, ImaginaryMarchCharacter, config)
    TopazEstimate = DefaultEstimator(f'Topaz: {TopazCharacter.lightcone.name} {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numTalentTopaz:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    RobinEstimate = DefaultEstimator(f'Robin: {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q, S{RobinCharacter.lightcone.superposition:d} {RobinCharacter.lightcone.name}', 
                                    RobinRotation, RobinCharacter, config)
    AventurineEstimate = DefaultEstimator(f'Aventurine: {numBasicAventurine:.0f}N {numTalentAventurine:.1f}T 1Q, S{AventurineCharacter.lightcone.superposition:.0f} {AventurineCharacter.lightcone.name}',
                                    AventurineRotation, AventurineCharacter, config)

    return([ImaginaryMarchEstimate, TopazEstimate, AventurineEstimate, RobinEstimate])

