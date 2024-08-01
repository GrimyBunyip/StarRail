from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Aventurine import Aventurine
from characters.hunt.ImaginaryMarch import ImaginaryMarch
from characters.hunt.Topaz import Topaz
from characters.hunt.Feixiao import Feixiao
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.harmony.FlowingNightglow import FlowingNightglow
from lightCones.harmony.PoisedToBloom import PoisedToBloom
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.IVentureForthToHunt import IVentureForthToHunt
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

def FeixiaoMarchTopazAventurine(config, 
                                feixiaoEidolon:int=None, 
                                feixiaoSuperposition:int=0, 
                                topazEidolon:int=None, 
                                topazSuperposition:int=0):
    #%% March Feixiao Topaz Aventurine Characters

    FeixiaoLightcone = CruisingInTheStellarSea(**config) if feixiaoSuperposition == 0 else IVentureForthToHunt(superposition=feixiaoSuperposition,**config)
    FeixiaoSubstats = {'CR': 7, 'CD': 12, 'ATK.percent': 6, 'ATK.flat':3} if feixiaoSuperposition == 0 else {'CR': 10, 'CD': 12, 'ATK.percent': 5, 'ATK.flat':3}
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
    MarchSubstats = {'CD': 12, 'CR': 8, 'ATK.percent': 3, 'SPD.flat': 5} #if feixiaoSuperposition == 0 else {'CD': 11, 'CR': 9, 'ATK.percent': 3, 'SPD.flat': 5}
    MarchCharacter = ImaginaryMarch(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.imaginary'],
                                    substats = MarchSubstats),
                                    lightcone = MarchLightCone,
                                    relicsetone = MusketeerOfWildWheat2pc(),
                                    relicsettwo = MusketeerOfWildWheat4pc(),
                                    planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    master=FeixiaoCharacter,
                                    **config)

    topazLightcone = Swordplay(**config) if topazSuperposition == 0 else WorrisomeBlissful(superposition=topazSuperposition,**config)
    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                                    substats = {'CR': 10, 'CD': 5, 'ATK.percent': 3, 'SPD.flat': 10}),
                                    lightcone = topazLightcone, 
                                    relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = DuranDynastyOfRunningWolves(),
                                    eidolon=topazEidolon,
                                    **config)

    AventurineCharacter = Aventurine(RelicStats(mainstats = ['DEF.percent', 'SPD.flat', 'DEF.percent', 'DEF.percent'],
                                    substats = {'CR': 3, 'CD': 5, 'SPD.flat': 12, 'DEF.percent': 8}),
                                    lightcone = DestinysThreadsForewoven(defense=4000,**config),
                                    leverage_cr = 0.48,
                                    relicsetone = KnightOfPurityPalace2pc(), relicsettwo = KnightOfPurityPalace4pc(), planarset = BrokenKeel(),
                                    **config)
    
    team = [MarchCharacter, FeixiaoCharacter, TopazCharacter, AventurineCharacter]

    #%% March Feixiao Topaz Aventurine Team Buffs
    for character in [FeixiaoCharacter, MarchCharacter, TopazCharacter]:
        character.addStat('CD',description='Broken Keel from Aventurine',amount=0.1)
    
    # March Buff
    MarchCharacter.applySkillBuff(FeixiaoCharacter)
    MarchCharacter.applyTalentBuff(FeixiaoCharacter,uptime=1.0)
    
    # Aventurine Buffs
    AventurineCharacter.applyUltDebuff(team=team,rotationDuration=4.0,targetingUptime=1.0)

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff(team,uptime=1.0)
    if topazSuperposition > 0:
        for character in [FeixiaoCharacter, MarchCharacter, AventurineCharacter]:
                character.addStat('CD',description='Worrisome, Blissful',
                                        amount=0.10 + 0.02 * TopazCharacter.lightcone.superposition,
                                        stacks=2.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% March Feixiao Topaz Aventurine Rotations
    # assume 154 ish spd March and Feixiao, March slower than Feixiao, and 134 ish spd Topaz

    numBasicTopaz = 0.0
    numSkillTopaz = 3.5
    numTalentTopaz = (numBasicTopaz + numSkillTopaz) * 2.0 + 1.0 # rough estimate
    TopazRotation = []
    TopazRotation += [TopazCharacter.useBasic() * numBasicTopaz]
    TopazRotation += [TopazCharacter.useSkill() * numSkillTopaz]
    TopazRotation += [TopazCharacter.useUltimate()]
    TopazRotation += [TopazCharacter.useTalent(windfall=True) * 2.0] # two talents from windfall
    TopazRotation += [TopazCharacter.useTalent(windfall=False) * (numTalentTopaz - 1.0)] # deducted windfall advances
    
    numBasicMarch = 2.0
    numFollowupMarch = numBasicMarch
    numEnhancedMarch = 1.0
    
    MarchRotation = []
    MarchRotation += [MarchCharacter.useBasic() * numBasicMarch]
    MarchRotation += [MarchCharacter.useFollowup() * numFollowupMarch]
    MarchRotation += [MarchCharacter.useEnhancedBasic(actionValue=0.0, numHits=5.0, chance=0.8) * numEnhancedMarch]
    MarchRotation += [MarchCharacter.useUltimate()] 

    numBasicAventurine = 4.0
    numTalentAventurine = 4.0 # stacks from ultimate
    numEnemyAttacks = AventurineCharacter.numEnemies * AventurineCharacter.enemySpeed / AventurineCharacter.getTotalStat('SPD') # extra stacks from people getting hit per turn
    numEnemyAttacks += (1.0 + (6*1) / (6*1 + 4 + 3 + 3)) # extra stacks from when Aventurine is Targeted
    numTalentAventurine += numBasicAventurine * numEnemyAttacks
    
    numFollowups = FeixiaoCharacter.getTotalStat('SPD') # Feixiao gets followup per turn
    numFollowups += MarchCharacter.getTotalStat('SPD') # March gets about 1 followup per turn
    numFollowups += 3.25 * TopazCharacter.getTotalStat('SPD') # March gets about 3.25 followup per turn
    numFollowups /= AventurineCharacter.getTotalStat('SPD')
    numTalentAventurine += numBasicAventurine * numFollowups
    
    AventurineRotation = [AventurineCharacter.useBasic() * numBasicAventurine,
                          AventurineCharacter.useTalent() * numTalentAventurine,
                          AventurineCharacter.useUltimate() * 1,]
    
    # number of attacks in 2 feixiao turns
    numTurns = 2.0
    numAttacks = numTurns * 2.0 # feixiao attacks
    numAttacks += numTurns * (numBasicMarch + numFollowupMarch + numEnhancedMarch + 1.0) / numBasicMarch  # march attacks
    numAttacks += numTurns * (1.0 + numTalentAventurine / numBasicAventurine / 6.0) # aventurine attacks
    numAttacks += numTurns * (numBasicTopaz + numSkillTopaz + numTalentTopaz) / (numBasicTopaz + numSkillTopaz)
    
    numBasicFeixiao = 0.0
    numSkillFeixiao = 2.0
    numFollowupFeixiao = (numBasicFeixiao + numSkillFeixiao)
    numUltFeixiao = numAttacks * (1.0 if FeixiaoCharacter.eidolon >= 2 else 0.5)
    
    FeixiaoRotation = []
    FeixiaoRotation += [FeixiaoCharacter.useBasic() * numBasicFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useSkill() * numSkillFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useTalent() * numFollowupFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useUltimate() * numUltFeixiao] 

    #%% March Feixiao Topaz Aventurine Rotation Math
    totalTopazEffect = sumEffects(TopazRotation)
    totalMarchEffect = sumEffects(MarchRotation)
    totalFeixiaoEffect = sumEffects(FeixiaoRotation)
    totalAventurineEffect = sumEffects(AventurineRotation)

    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')    
    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
    FeixiaoRotationDuration = totalFeixiaoEffect.actionvalue * 100.0 / FeixiaoCharacter.getTotalStat('SPD')
    AventurineRotationDuration = totalAventurineEffect.actionvalue * 100.0 / AventurineCharacter.getTotalStat('SPD')
    
    print('##### Rotation Durations #####')
    print('March: ',MarchRotationDuration * 2.0)
    print('Feixiao: ',FeixiaoRotationDuration * 2.0)
    print('Topaz: ',TopazRotationDuration)
    print('Aventurine: ',AventurineRotationDuration)

    # Scale other character's rotation
    MarchRotation = [x * FeixiaoRotationDuration / MarchRotationDuration for x in MarchRotation]
    TopazRotation = [x * FeixiaoRotationDuration / TopazRotationDuration for x in TopazRotation]
    AventurineRotation = [x * FeixiaoRotationDuration / AventurineRotationDuration for x in AventurineRotation]

    FeixiaoEstimate = DefaultEstimator(f'{FeixiaoCharacter.fullName()} {numBasicFeixiao:.1f}N {numSkillFeixiao:.1f}E {numFollowupFeixiao:.1f}T {numUltFeixiao:.1f}Q', FeixiaoRotation, FeixiaoCharacter, config)
    MarchEstimate = DefaultEstimator(f'{MarchCharacter.fullName()} {numBasicMarch:.1f}N {numEnhancedMarch:.1f}Enh 1Q', MarchRotation, MarchCharacter, config)
    TopazEstimate = DefaultEstimator(f'{TopazCharacter.fullName()} {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numTalentTopaz:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    AventurineEstimate = DefaultEstimator(f'E{AventurineCharacter.eidolon} S{AventurineCharacter.lightcone.superposition:.0f} {AventurineCharacter.lightcone.name} Aventurine: {numBasicAventurine:.0f}N {numTalentAventurine:.1f}T 1Q',
                                    AventurineRotation, AventurineCharacter, config)

    return([FeixiaoEstimate, MarchEstimate, TopazEstimate, AventurineEstimate])

