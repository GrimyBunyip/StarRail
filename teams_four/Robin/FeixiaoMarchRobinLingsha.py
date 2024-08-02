from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Lingsha import Lingsha
from characters.hunt.ImaginaryMarch import ImaginaryMarch
from characters.harmony.Robin import Robin
from characters.hunt.Feixiao import Feixiao
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.abundance.SharedFeeling import SharedFeeling
from lightCones.harmony.FlowingNightglow import FlowingNightglow
from lightCones.harmony.PoisedToBloom import PoisedToBloom
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.IVentureForthToHunt import IVentureForthToHunt
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.DestinysThreadsForewoven import DestinysThreadsForewoven
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.DuranDynastyOfRunningWolves import DuranDynastyOfRunningWolves
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.IronCavalryAgainstTheScourge import IronCavalryAgainstTheScourge2pc
from relicSets.relicSets.KnightOfPurityPalace import KnightOfPurityPalace2pc, KnightOfPurityPalace4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc, MusketeerOfWildWheat4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def FeixiaoMarchRobinLingsha(config, 
                                feixiaoEidolon:int=None, 
                                feixiaoSuperposition:int=0, 
                                robinEidolon:int=None, 
                                robinSuperposition:int=0):
    #%% March Feixiao Robin Lingsha Characters

    FeixiaoLightcone = CruisingInTheStellarSea(**config) if feixiaoSuperposition == 0 else IVentureForthToHunt(superposition=feixiaoSuperposition,**config)
    FeixiaoSubstats = {'CR': 7, 'CD': 10, 'ATK.percent': 3, 'SPD.flat':8} if feixiaoSuperposition == 0 else {'CR': 10, 'CD': 7, 'ATK.percent': 3, 'SPD.flat':8}
    FeixiaoCharacter = Feixiao(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.wind'],
                                    substats = FeixiaoSubstats),
                                    lightcone = FeixiaoLightcone,
                                    relicsetone = WindSoaringValorous2pc(),
                                    relicsettwo = WindSoaringValorous4pc(),
                                    planarset = DuranDynastyOfRunningWolves(),
                                    eidolon = feixiaoEidolon,
                                    **config)

    # give March swordplay if Feixiao uses Cruising
    MarchLightCone = Swordplay(**config) #if feixiaoSuperposition == 0 else CruisingInTheStellarSea(**config)
    MarchSubstats = {'CD': 7, 'CR': 12, 'ATK.percent': 3, 'SPD.flat': 6} #if feixiaoSuperposition == 0 else {'CD': 11, 'CR': 9, 'ATK.percent': 3, 'SPD.flat': 5}
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
                                    substats = {'ATK.percent': 11, 'SPD.flat': 9, 'RES': 3, 'ATK.flat': 5}),
                                    lightcone = RobinLightCone,
                                    relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                                    eidolon=robinEidolon,
                                    **config)

    LingshaCharacter = Lingsha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                    substats = {'SPD.flat': 13, 'BreakEffect': 7, 'ATK.percent': 5, 'ATK.flat': 3}),
                                    lightcone = SharedFeeling(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = IronCavalryAgainstTheScourge2pc(), planarset = ForgeOfTheKalpagniLantern(),
                                    **config)
    
    team = [MarchCharacter, FeixiaoCharacter, RobinCharacter, LingshaCharacter]

    #%% March Feixiao Robin Lingsha Team Buffs
    for character in [FeixiaoCharacter, MarchCharacter]:
        character.addStat('CD',description='Poised to Bloom',amount=0.12+0.04*RobinCharacter.lightcone.superposition)
    
    # March Buff
    MarchCharacter.applySkillBuff(FeixiaoCharacter)
    MarchCharacter.applyTalentBuff(FeixiaoCharacter,uptime=1.0)
    
    # Lingsha Buffs
    LingshaCharacter.applyUltDebuff(team=team,rotationDuration=4.0)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)

    RobinUltUptime = 1.0 if RobinCharacter.eidolon >= 2 else 0.5
    RobinUltUptimeFeixiao = 1.0 if RobinCharacter.eidolon >= 2 else 0.75 
    RobinCharacter.applyUltBuff([MarchCharacter,LingshaCharacter],uptime=RobinUltUptime)
    RobinCharacter.applyUltBuff([FeixiaoCharacter],uptime=RobinUltUptimeFeixiao)
    
    # apply Lingsha self buffs and MV calculations at the end
    LingshaCharacter.addAttackForTalent()

    #%% Print Statements
    for character in team:
        character.print()

    #%% March Feixiao Robin Lingsha Rotations
    # assume 154 ish spd March and Feixiao, March slower than Feixiao, and 134 ish spd robin
    
    numBasicRobin = 0.0
    numSkillRobin = 1.0 if RobinCharacter.eidolon >= 2 else 2.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0) # apply robin buff after we calculate damage for her basics
    
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

    numBasicLingsha = 0.0 if RobinCharacter.eidolon >= 2 else 2.0
    numSkillLingsha = 3.0 if RobinCharacter.eidolon >= 2 else 1.0
    # 1 from ultimate, 1.5 from autoheal, 1.5 from natural turns, but assume 1 and 1 if robin e2
    numTalentLingsha = 3.0 if RobinCharacter.eidolon >= 2 else 4.0 
    
    LingshaRotation = [LingshaCharacter.useBasic() * numBasicLingsha,
                       LingshaCharacter.useSkill() * numSkillLingsha,
                       LingshaCharacter.useTalent() * numTalentLingsha,
                       LingshaCharacter.useUltimate() * 1,]
    LingshaRotation[0].actionvalue *= 0.8 if LingshaCharacter.lightcone.name == 'Multiplication' else 1.0

    RobinRotationLingsha = [RobinCharacter.useTalent() * (numBasicLingsha + numSkillLingsha + numTalentLingsha + 1.0)]
    RobinRotationLingsha += [RobinCharacter.useConcertoDamage(['basic']) * numBasicLingsha * RobinUltUptime]
    RobinRotationLingsha += [RobinCharacter.useConcertoDamage(['skill']) * numSkillLingsha * RobinUltUptime]
    RobinRotationLingsha += [RobinCharacter.useConcertoDamage(['followup']) * numTalentLingsha * RobinUltUptime]
    RobinRotationLingsha += [RobinCharacter.useConcertoDamage(['ultimate']) * 1.0 * RobinUltUptime]
    
    # number of attacks in 2 feixiao turns
    numTurns = 2.0
    numAttacks = numTurns * 2.0 # feixiao attacks
    numAttacks += numTurns * (numBasicMarch + numFollowupMarch + numEnhancedMarch + 1.0) / numBasicMarch  # march attacks
    numAttacks += numTurns * (1.0 + numBasicLingsha + numSkillLingsha + numTalentLingsha) / (numBasicLingsha + numSkillLingsha) # Lingsha attacks
    
    numBasicFeixiao = 1.25 if RobinCharacter.eidolon >= 2 else 0.0
    numSkillFeixiao = 0.75 if RobinCharacter.eidolon >= 2 else 2.0
    numFollowupFeixiao = (numBasicFeixiao + numSkillFeixiao)
    numUltFeixiao = numAttacks * (1.0 if FeixiaoCharacter.eidolon >= 2 else 0.5)
    
    numBasicFeixiao *= 6.0 / numUltFeixiao
    numSkillFeixiao *= 6.0 / numUltFeixiao
    numFollowupFeixiao *= 6.0 / numUltFeixiao
    numUltFeixiao = 6.0
    
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

    #%% March Feixiao Robin Lingsha Rotation Math

    totalRobinEffect = sumEffects(RobinRotation)
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    
    numTurnAV = 300.0 if RobinCharacter.eidolon >= 2 else 400.0

    MarchNumTurns = numTurnAV * MarchCharacter.useBasic().actionvalue / MarchCharacter.getTotalStat('SPD')
    FeixiaoActionValue = FeixiaoCharacter.useSkill().actionvalue * numSkillFeixiao
    FeixiaoActionValue += FeixiaoCharacter.useBasic().actionvalue * numBasicFeixiao
    FeixiaoActionValue /= numSkillFeixiao + numBasicFeixiao
    FeixiaoNumTurns = numTurnAV * FeixiaoActionValue / FeixiaoCharacter.getTotalStat('SPD')
    LingshaNumTurns = numTurnAV * LingshaCharacter.useBasic().actionvalue / LingshaCharacter.getTotalStat('SPD')
    
    MarchRotation += [RobinCharacter.useAdvanceForward() * (MarchNumTurns - RobinRotationDuration) * MarchCharacter.getTotalStat('SPD') * numBasicMarch / numTurnAV]
    FeixiaoRotation += [RobinCharacter.useAdvanceForward() * (FeixiaoNumTurns - RobinRotationDuration) * FeixiaoCharacter.getTotalStat('SPD') * numFollowupFeixiao / numTurnAV]
    LingshaRotation += [RobinCharacter.useAdvanceForward() * (LingshaNumTurns - RobinRotationDuration) * LingshaCharacter.getTotalStat('SPD') * (numBasicLingsha + numSkillLingsha) / numTurnAV]
        
    totalMarchEffect = sumEffects(MarchRotation)
    totalFeixiaoEffect = sumEffects(FeixiaoRotation)
    totalLingshaEffect = sumEffects(LingshaRotation)
    
    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
    FeixiaoRotationDuration = totalFeixiaoEffect.actionvalue * 100.0 / FeixiaoCharacter.getTotalStat('SPD')
    LingshaRotationDuration = totalLingshaEffect.actionvalue * 100.0 / LingshaCharacter.getTotalStat('SPD')
    
    print('##### Rotation Durations #####')
    print('March: ',MarchRotationDuration * numTurnAV / 100.0 / numBasicMarch)
    print('Feixiao: ',FeixiaoRotationDuration * numTurnAV / 100.0 / numFollowupFeixiao)
    print('Robin: ',RobinRotationDuration)
    print('Lingsha: ',LingshaRotationDuration)

    # Scale other character's rotation
    FeixiaoRotation = [x * MarchRotationDuration / FeixiaoRotationDuration for x in FeixiaoRotation]
    RobinRotationFeixiao = [x * MarchRotationDuration / FeixiaoRotationDuration for x in RobinRotationFeixiao]
    RobinRotation = [x * MarchRotationDuration / RobinRotationDuration for x in RobinRotation]
    LingshaRotation = [x * MarchRotationDuration / LingshaRotationDuration for x in LingshaRotation]
    RobinRotationLingsha = [x * MarchRotationDuration / LingshaRotationDuration for x in RobinRotationLingsha]
    
    RobinRotation += RobinRotationMarch
    RobinRotation += RobinRotationFeixiao
    RobinRotation += RobinRotationLingsha
    totalRobinEffect = sumEffects(RobinRotation)

    FeixiaoEstimate = DefaultEstimator(f'{FeixiaoCharacter.fullName()} {numBasicFeixiao:.1f}N {numSkillFeixiao:.1f}E {numFollowupFeixiao:.1f}T {numUltFeixiao:.1f}Q', FeixiaoRotation, FeixiaoCharacter, config)
    MarchEstimate = DefaultEstimator(f'{MarchCharacter.fullName()} {numBasicMarch:.1f}N {numEnhancedMarch:.1f}Enh 1Q', MarchRotation, MarchCharacter, config)
    RobinEstimate = DefaultEstimator(f'{RobinCharacter.fullName()} {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q', 
                                    RobinRotation, RobinCharacter, config)
    LingshaEstimate = DefaultEstimator(f'{LingshaCharacter.fullName()} {numBasicLingsha:.0f}N {numSkillLingsha:.0f}E {numTalentLingsha:.1f}T 1Q',
                                    LingshaRotation, LingshaCharacter, config)

    return([FeixiaoEstimate, MarchEstimate, RobinEstimate, LingshaEstimate])

