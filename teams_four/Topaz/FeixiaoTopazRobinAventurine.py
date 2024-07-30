from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Aventurine import Aventurine
from characters.hunt.Feixiao import Feixiao
from characters.harmony.Robin import Robin
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.harmony.PoisedToBloom import PoisedToBloom
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.DestinysThreadsForewoven import DestinysThreadsForewoven
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.DuranDynastyOfRunningWolves import DuranDynastyOfRunningWolves
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.KnightOfPurityPalace import KnightOfPurityPalace2pc, KnightOfPurityPalace4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def FeixiaoTopazRobinAventurine(config):
    #%% Feixiao Topaz Robin Aventurine Characters
    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                                    substats = {'CR': 10, 'CD': 5, 'ATK.percent': 3, 'SPD.flat': 10}),
                                    lightcone = Swordplay(**config), 
                                    relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = DuranDynastyOfRunningWolves(),
                                    **config)

    FeixiaoCharacter = Feixiao(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.wind'],
                                    substats = {'CR': 7, 'CD': 12, 'ATK.percent': 8, 'SPD.flat': 1}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = WindSoaringValorous2pc(),
                                    relicsettwo = WindSoaringValorous4pc(),
                                    planarset = DuranDynastyOfRunningWolves(),
                                    **config)
    
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 11, 'SPD.flat': 9, 'RES': 3, 'ATK.flat': 5}),
                                    lightcone = PoisedToBloom(**config),
                                    relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                                    **config)

    AventurineCharacter = Aventurine(RelicStats(mainstats = ['DEF.percent', 'SPD.flat', 'DEF.percent', 'DEF.percent'],
                                    substats = {'CR': 3, 'CD': 5, 'SPD.flat': 12, 'DEF.percent': 8}),
                                    lightcone = DestinysThreadsForewoven(defense=4000,**config),
                                    leverage_cr=0.48,
                                    relicsetone = KnightOfPurityPalace2pc(), relicsettwo = KnightOfPurityPalace4pc(), planarset = BrokenKeel(),
                                    **config)
    
    team = [FeixiaoCharacter, TopazCharacter, RobinCharacter, AventurineCharacter]

    #%% Feixiao Topaz Robin Aventurine Team Buffs
    for character in [TopazCharacter, FeixiaoCharacter, RobinCharacter]:
        character.addStat('CD',description='Broken Keel from Aventurine',amount=0.1)
    for character in [TopazCharacter, FeixiaoCharacter]:
        character.addStat('CD',description='Poised to Bloom',amount=0.12+0.04*RobinCharacter.lightcone.superposition)

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff(team,uptime=1.0)
    
    # Aventurine Buffs
    AventurineCharacter.applyUltDebuff(team=team,rotationDuration=4.0,targetingUptime=1.0)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinUltUptime = 0.5 # assume better robin ult uptime because of shorter robin rotation
    RobinCharacter.applyUltBuff([FeixiaoCharacter,TopazCharacter,AventurineCharacter],uptime=RobinUltUptime)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Feixiao Topaz Robin Aventurine Rotations
    # assume 154 ish spd Feixiao and topaz, Feixiao slower than Topaz, and 134 ish spd robin
    
    numBasicRobin = 0.0
    numSkillRobin = 2.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0) # apply robin buff after we calculate damage for her basics

    numBasicTopaz = 2.0
    numSkillTopaz = 2.0
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

    numBasicAventurine = 4.0
    numTalentAventurine = 4.0 # stacks from ultimate
    numEnemyAttacks = AventurineCharacter.numEnemies * AventurineCharacter.enemySpeed / AventurineCharacter.getTotalStat('SPD') # extra stacks from people getting hit per turn
    numEnemyAttacks += (1.0 + (6*1) / (6*1 + 4 + 3 + 3)) # extra stacks from when Aventurine is Targeted
    numTalentAventurine += numBasicAventurine * numEnemyAttacks
    
    numFollowups = (numTalentTopaz + 2.0) * TopazCharacter.getTotalStat('SPD') / 4.0 # Topaz gets about this many followup attacks per her turns, 4 turn rotation
    numFollowups += FeixiaoCharacter.getTotalStat('SPD') # Feixiao gets about 1 followup per turn
    numFollowups /= AventurineCharacter.getTotalStat('SPD')
    numTalentAventurine += numBasicAventurine * numFollowups
    
    AventurineRotation = [AventurineCharacter.useBasic() * numBasicAventurine,
                          AventurineCharacter.useTalent() * numTalentAventurine,
                          AventurineCharacter.useUltimate() * 1,
                          RobinCharacter.useAdvanceForward() * numBasicAventurine / 4.0,]

    RobinRotationAventurine = [RobinCharacter.useTalent() * (numBasicAventurine + numTalentAventurine / 7.0)]
    RobinRotationAventurine += [RobinCharacter.useConcertoDamage(['basic']) * numBasicAventurine * RobinUltUptime]
    RobinRotationAventurine += [RobinCharacter.useConcertoDamage(['followup']) * (numTalentAventurine / 7.0) * RobinUltUptime]
    
    # number of attacks in 2 feixiao turns
    numTurns = 2.0
    numAttacks = numTurns * 2.0 # feixiao attacks
    numAttacks += numTurns * (1.0 + numTalentTopaz / (numBasicTopaz + numSkillTopaz))  # topaz attacks
    numAttacks += numTurns * (1.0 + numTalentAventurine / numBasicAventurine / 6.0) # aventurine attacks
    
    numBasicFeixiao = 1.0 * 2.0 / 3.0
    numSkillFeixiao = 2.0 * 2.0 / 3.0
    numFollowupFeixiao = (numBasicFeixiao + numSkillFeixiao)
    numUltFeixiao = numAttacks / 2.0
    
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
    FeixiaoRotation += [RobinCharacter.useAdvanceForward() * (numBasicFeixiao + numSkillFeixiao) / 4.0]

    #%% Feixiao Topaz Robin Aventurine Rotation Math

    totalFeixiaoEffect = sumEffects(FeixiaoRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalAventurineEffect = sumEffects(AventurineRotation)

    FeixiaoRotationDuration = totalFeixiaoEffect.actionvalue * 100.0 / FeixiaoCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    AventurineRotationDuration = totalAventurineEffect.actionvalue * 100.0 / AventurineCharacter.getTotalStat('SPD')    

    print('##### Rotation Durations #####')
    print('Feixiao: ',FeixiaoRotationDuration)
    print('Topaz: ',TopazRotationDuration)
    print('Robin: ',RobinRotationDuration)
    print('Aventurine: ',AventurineRotationDuration)

    # Scale other character's rotation
    TopazRotation = [x * FeixiaoRotationDuration / TopazRotationDuration for x in TopazRotation]
    RobinRotationTopaz = [x * FeixiaoRotationDuration / TopazRotationDuration for x in RobinRotationTopaz]
    RobinRotation = [x * FeixiaoRotationDuration / RobinRotationDuration for x in RobinRotation]
    AventurineRotation = [x * FeixiaoRotationDuration / AventurineRotationDuration for x in AventurineRotation]
    RobinRotationAventurine = [x * FeixiaoRotationDuration / AventurineRotationDuration for x in RobinRotationAventurine]
    
    RobinRotation += RobinRotationFeixiao
    RobinRotation += RobinRotationTopaz
    RobinRotation += RobinRotationAventurine
    totalRobinEffect = sumEffects(RobinRotation)

    FeixiaoEstimate = DefaultEstimator(f'Feixiao: {numBasicFeixiao:.1f}N {numSkillFeixiao:.1f}E {numFollowupFeixiao:.1f}T {numUltFeixiao:.1f}Q, S{FeixiaoCharacter.lightcone.superposition:d} {FeixiaoCharacter.lightcone.name}', FeixiaoRotation, FeixiaoCharacter, config)
    TopazEstimate = DefaultEstimator(f'Topaz: {TopazCharacter.lightcone.name} {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numTalentTopaz:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    RobinEstimate = DefaultEstimator(f'Robin: {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q, S{RobinCharacter.lightcone.superposition:d} {RobinCharacter.lightcone.name}', 
                                    RobinRotation, RobinCharacter, config)
    AventurineEstimate = DefaultEstimator(f'Aventurine: {numBasicAventurine:.0f}N {numTalentAventurine:.1f}T 1Q, S{AventurineCharacter.lightcone.superposition:.0f} {AventurineCharacter.lightcone.name}',
                                    AventurineRotation, AventurineCharacter, config)

    return([FeixiaoEstimate, TopazEstimate, AventurineEstimate, RobinEstimate])

