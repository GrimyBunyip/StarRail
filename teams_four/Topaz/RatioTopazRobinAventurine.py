from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Aventurine import Aventurine
from characters.hunt.DrRatio import DrRatio
from characters.harmony.Robin import Robin
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.harmony.ForTomorrowsJourney import ForTomorrowsJourney
from lightCones.harmony.PoisedToBloom import PoisedToBloom
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.DestinysThreadsForewoven import DestinysThreadsForewoven
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.KnightOfPurityPalace import KnightOfPurityPalace2pc, KnightOfPurityPalace4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc

def DrRatioTopazRobinAventurine(config):
    #%% DrRatio Topaz Robin Aventurine Characters
    DrRatioCharacter = DrRatio(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.imaginary'],
                                    substats = {'CD': 5, 'CR': 8, 'ATK.percent': 3, 'SPD.flat': 12}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = Pioneer2pc(),
                                    relicsettwo = Pioneer4pc(stacks=2),
                                    planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    debuffStacks=3.0, # assume a bit more than 2 average with no third consistent 3rd debuff
                                    **config)

    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                                    substats = {'CR': 7, 'CD': 9, 'ATK.percent': 3, 'SPD.flat': 9}),
                                    lightcone = Swordplay(**config),
                                    relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = IzumoGenseiAndTakamaDivineRealm(),
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
    
    team = [DrRatioCharacter, TopazCharacter, RobinCharacter, AventurineCharacter]

    #%% DrRatio Topaz Robin Aventurine Team Buffs
    for character in [TopazCharacter, DrRatioCharacter, RobinCharacter]:
        character.addStat('CD',description='Broken Keel from Aventurine',amount=0.1)
    for character in [TopazCharacter, DrRatioCharacter, AventurineCharacter]:
        character.addStat('CD',description='Broken Keel from Robin',amount=0.1)
    for character in [TopazCharacter, DrRatioCharacter]:
        character.addStat('CD',description='Poised to Bloom',amount=0.12+0.04*RobinCharacter.lightcone.superposition)

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff(team,uptime=1.0)
    
    # Dr Ratio Buff
    DrRatioCharacter.applyTalentBuff(team)
    
    # Aventurine Buffs
    AventurineCharacter.applyUltDebuff(team=team,rotationDuration=4.0,targetingUptime=1.0)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinUltUptime = 0.5 # assume about half of our attacks get robin buff
    RobinCharacter.applyUltBuff([DrRatioCharacter,TopazCharacter,AventurineCharacter],uptime=RobinUltUptime)

    #%% Print Statements
    for character in team:
        character.print()

    #%% DrRatio Topaz Robin Aventurine Rotations
    # assume 154 ish spd ratio and topaz, ratio slower than Topaz, and 134 ish spd robin
    # this optimizes use of robin's advance forward, while keeping numby math good-ish
    # we'll look at what a 4 turn rotation looks like for ratio and topaz here

    # Turn 1 (based on the 154 spd characters)
    # Robin Ult
    # Topaz Ult -> Ratio Ult -> Aventurine Ult -> Ratio Followup -> Numby attack
    # Topaz Skill -> Numby Attack
    # Ratio Skill -> Ratio followup -> Numby half turn
    # Aventurine Basic
    
    # Turn 2 
    # Numby Attack -> Topaz Skill -> Numby half turn
    # Ratio Skill -> Ratio followup -> Numby attack
    # Aventurine Basic
    
    # Turn 3 - Concerto Expired
    # Topaz Basic -> Numby Attack
    # Ratio Skill -> Ratio followup -> Numby half turn
    # Aventurine Basic
    
    # Turn 4
    # Numby Attack -> Topaz Basic -> Numby half turn
    # Ratio Skill -> Ratio followup -> Numby attack
    # Aventurine Basic
    
    numBasicRobin = 2.0
    numSkillRobin = 1.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0) # apply robin buff after we calculate damage for her basics
    
    numSkillRatio = 3.5
    numUltRatio = 1.0
    numTalentRatio = numSkillRatio * 0.8 + 2 * numUltRatio # multiply 0.8 for no extra debuff teams
    
    DrRatioRotation = []
    DrRatioRotation += [DrRatioCharacter.useSkill() * numSkillRatio]
    DrRatioRotation += [DrRatioCharacter.useTalent() * numTalentRatio] 
    DrRatioRotation += [DrRatioCharacter.useUltimate()] 

    RobinRotationRatio = [RobinCharacter.useTalent() * (numSkillRatio + numTalentRatio + 1.0)]
    RobinRotationRatio += [RobinCharacter.useConcertoDamage(['skill']) * numSkillRatio * RobinUltUptime]
    RobinRotationRatio += [RobinCharacter.useConcertoDamage(['ultimate']) * RobinUltUptime]
    RobinRotationRatio += [RobinCharacter.useConcertoDamage(['followup']) * (numTalentRatio - 2.0) * RobinUltUptime]
    DrRatioRotation += [RobinCharacter.useAdvanceForward() * numSkillRatio / 5.0] 

    numBasicTopaz = 2.0
    numSkillTopaz = 2.0
    numTalentTopaz = (numBasicTopaz + numSkillTopaz) * 1.5 + 1.0 # rough estimate
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
    TopazRotation += [RobinCharacter.useAdvanceForward() * (numBasicTopaz + numSkillTopaz) / 5.0] 

    numBasicAventurine = 4.0
    numTalentAventurine = 4.0 # stacks from ultimate
    numEnemyAttacks = AventurineCharacter.numEnemies * AventurineCharacter.enemySpeed / AventurineCharacter.getTotalStat('SPD') # extra stacks from people getting hit per turn
    numEnemyAttacks += (1.0 + (6*1) / (6*1 + 4 + 3 + 3)) # extra stacks from when Aventurine is Targeted
    numTalentAventurine += numBasicAventurine * numEnemyAttacks
    
    numFollowups = (numTalentTopaz + 2.0) * TopazCharacter.getTotalStat('SPD') / 4.0 # Topaz gets about this many followup attacks per her turns, 4 turn rotation
    numFollowups += (numTalentRatio) * DrRatioCharacter.getTotalStat('SPD') / 4.0 # Ratio gets about this many followup attacks per his turns, 4 turn rotation
    numFollowups /= AventurineCharacter.getTotalStat('SPD')
    numTalentAventurine += numBasicAventurine * numFollowups
    
    AventurineRotation = [AventurineCharacter.useBasic() * numBasicAventurine,
                          AventurineCharacter.useTalent() * numTalentAventurine,
                          AventurineCharacter.useUltimate() * 1,
                          RobinCharacter.useAdvanceForward() * numBasicAventurine / 5.0,]

    RobinRotationAventurine = [RobinCharacter.useTalent() * (numBasicAventurine + numTalentAventurine / 7.0)]
    RobinRotationAventurine += [RobinCharacter.useConcertoDamage(['basic']) * numBasicAventurine * RobinUltUptime]
    RobinRotationAventurine += [RobinCharacter.useConcertoDamage(['followup']) * (numTalentAventurine / 7.0) * RobinUltUptime]

    #%% DrRatio Topaz Robin Aventurine Rotation Math

    totalDrRatioEffect = sumEffects(DrRatioRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalAventurineEffect = sumEffects(AventurineRotation)

    DrRatioRotationDuration = totalDrRatioEffect.actionvalue * 100.0 / DrRatioCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    AventurineRotationDuration = totalAventurineEffect.actionvalue * 100.0 / AventurineCharacter.getTotalStat('SPD')
    

    print('##### Rotation Durations #####')
    print('DrRatio: ',DrRatioRotationDuration)
    print('Topaz: ',TopazRotationDuration)
    print('Robin: ',RobinRotationDuration)
    print('Aventurine: ',AventurineRotationDuration)

    # Scale other character's rotation
    TopazRotation = [x * DrRatioRotationDuration / TopazRotationDuration for x in TopazRotation]
    RobinRotationTopaz = [x * DrRatioRotationDuration / TopazRotationDuration for x in RobinRotationTopaz]
    RobinRotation = [x * DrRatioRotationDuration / RobinRotationDuration for x in RobinRotation]
    AventurineRotation = [x * DrRatioRotationDuration / AventurineRotationDuration for x in AventurineRotation]
    RobinRotationAventurine = [x * DrRatioRotationDuration / AventurineRotationDuration for x in RobinRotationAventurine]
    
    RobinRotation += RobinRotationRatio
    RobinRotation += RobinRotationTopaz
    RobinRotation += RobinRotationAventurine
    totalRobinEffect = sumEffects(RobinRotation)

    DrRatioEstimate = DefaultEstimator(f'DrRatio: {numSkillRatio:.1f}E {numTalentRatio:.1f}T {numUltRatio:.0f}Q, max debuffs on target', DrRatioRotation, DrRatioCharacter, config)
    TopazEstimate = DefaultEstimator(f'Topaz: {TopazCharacter.lightcone.name} {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numTalentTopaz:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    RobinEstimate = DefaultEstimator(f'Robin: {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q, S{RobinCharacter.lightcone.superposition:d} {RobinCharacter.lightcone.name}', 
                                    RobinRotation, RobinCharacter, config)
    AventurineEstimate = DefaultEstimator(f'Aventurine: {numBasicAventurine:.0f}N {numTalentAventurine:.1f}T 1Q, S{AventurineCharacter.lightcone.superposition:.0f} {AventurineCharacter.lightcone.name}',
                                    AventurineRotation, AventurineCharacter, config)

    return([DrRatioEstimate, TopazEstimate, AventurineEstimate, RobinEstimate])

