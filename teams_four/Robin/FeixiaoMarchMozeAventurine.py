from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Aventurine import Aventurine
from characters.hunt.ImaginaryMarch import ImaginaryMarch
from characters.hunt.Moze import Moze
from characters.hunt.Feixiao import Feixiao
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.IVentureForthToHunt import IVentureForthToHunt
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.DestinysThreadsForewoven import DestinysThreadsForewoven
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.DuranDynastyOfRunningWolves import DuranDynastyOfRunningWolves
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.KnightOfPurityPalace import KnightOfPurityPalace2pc, KnightOfPurityPalace4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc, MusketeerOfWildWheat4pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def FeixiaoMarchMozeAventurine(config, 
                                feixiaoEidolon:int=None, 
                                feixiaoSuperposition:int=0):
    #%% March Feixiao Moze Aventurine Characters

    FeixiaoLightcone = CruisingInTheStellarSea(**config) if feixiaoSuperposition == 0 else IVentureForthToHunt(superposition=feixiaoSuperposition,**config)
    FeixiaoSubstats = {'CR': 7, 'CD': 12, 'ATK.percent': 4, 'SPD.flat':5} if feixiaoSuperposition == 0 else {'CR': 10, 'CD': 12, 'ATK.percent': 3, 'SPD.flat':5}
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
    MarchSubstats = {'CD': 12, 'CR': 8, 'ATK.percent': 3, 'SPD.flat': 5} #if feixiaoSuperposition == 0 else {'CD': 11, 'CR': 9, 'ATK.percent': 3, 'SPD.flat': 5}
    MarchCharacter = ImaginaryMarch(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.imaginary'],
                                    substats = MarchSubstats),
                                    lightcone = MarchLightCone,
                                    relicsetone = MusketeerOfWildWheat2pc(),
                                    relicsettwo = MusketeerOfWildWheat4pc(),
                                    planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    master=FeixiaoCharacter,
                                    **config)
    
    MozeCharacter = Moze(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.lightning'],
                                    substats = {'CR': 12, 'CD': 5, 'SPD.flat': 8, 'ATK.percent': 3}),
                                    lightcone = Swordplay(**config),
                                    relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = DuranDynastyOfRunningWolves(),
                                    **config)

    AventurineCharacter = Aventurine(RelicStats(mainstats = ['DEF.percent', 'SPD.flat', 'DEF.percent', 'DEF.percent'],
                                    substats = {'CR': 3, 'CD': 5, 'SPD.flat': 12, 'DEF.percent': 8}),
                                    lightcone = DestinysThreadsForewoven(defense=4000,**config),
                                    leverage_cr = 0.48,
                                    relicsetone = KnightOfPurityPalace2pc(), relicsettwo = KnightOfPurityPalace4pc(), planarset = BrokenKeel(),
                                    **config)
    
    team = [MarchCharacter, FeixiaoCharacter, MozeCharacter, AventurineCharacter]

    #%% March Feixiao Moze Aventurine Team Buffs
    for character in [FeixiaoCharacter, MarchCharacter, MozeCharacter]:
        character.addStat('CD',description='Broken Keel from Aventurine',amount=0.1)
    
    # March Buff
    MarchCharacter.applySkillBuff(FeixiaoCharacter)
    MarchCharacter.applyTalentBuff(FeixiaoCharacter,uptime=1.0)
    
    # Aventurine Buffs
    AventurineCharacter.applyUltDebuff(team=team,rotationDuration=4.0,targetingUptime=1.0)

    # Moze Buffs
    MozeUptime=1.0
    MozeCharacter.applyDebuff(team, uptime=MozeUptime)

    #%% Print Statements
    for character in team:
        character.print()

    #%% March Feixiao Moze Aventurine Rotations

    numAdditionalMoze = 9.0
    numTalentMoze = 3.0
    numSkillMoze = 1.0
    numUltMoze = 0.75 # roughly 0.75 moze ults per rotation
    actionValueMoze = AventurineCharacter.useBasic().actionvalue / MozeUptime
    MozeRotation = [MozeCharacter.useSkill(actionvalue=actionValueMoze) * numSkillMoze,
                    MozeCharacter.useTalent() * (numTalentMoze + numUltMoze),
                    MozeCharacter.useAdditionalDamage() * numAdditionalMoze,
                    MozeCharacter.useUltimate()]
    
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
    
    numFollowups = 2.5 * FeixiaoCharacter.getTotalStat('SPD') # Feixiao gets about 2.5 followup per turn
    numFollowups += MarchCharacter.getTotalStat('SPD') # March gets about 1 followup per turn
    numFollowups += (numSkillMoze + numTalentMoze + 2.0 * numUltMoze) * MozeUptime
    numFollowups /= AventurineCharacter.getTotalStat('SPD')
    numTalentAventurine += numBasicAventurine * min(3.0,numFollowups)
    
    AventurineRotation = [AventurineCharacter.useBasic() * numBasicAventurine,
                          AventurineCharacter.useTalent() * numTalentAventurine,
                          AventurineCharacter.useUltimate() * 1,]
    
    # number of attacks in 2 feixiao turns
    numTurns = 2.0
    numAttacks = numTurns * 3.0 # feixiao attacks
    numAttacks += numTurns * (numBasicMarch + numFollowupMarch + numEnhancedMarch + 1.0) / numBasicMarch  # march attacks
    numAttacks += numTurns * (1.0 + numTalentAventurine / 7.0) / numBasicAventurine # aventurine attacks
    numAttacks += numTurns * (numSkillMoze + numTalentMoze + 2.0 * numUltMoze) * MozeUptime
    
    numBasicFeixiao = 0.0
    numSkillFeixiao = 2.0
    numFollowupFeixiao = (numBasicFeixiao + 2.0 * numSkillFeixiao)
    numUltFeixiao = numAttacks * 0.5 + (3.0 if FeixiaoCharacter.eidolon >= 2 else 0.0)
    
    numBasicFeixiao *= 6.0 / numUltFeixiao
    numSkillFeixiao *= 6.0 / numUltFeixiao
    numFollowupFeixiao *= 6.0 / numUltFeixiao
    numUltFeixiao = 1.0
    
    FeixiaoRotation = []
    FeixiaoRotation += [FeixiaoCharacter.useBasic() * numBasicFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useSkill() * numSkillFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useTalent() * numFollowupFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useUltimate() * numUltFeixiao] 

    #%% March Feixiao Moze Aventurine Rotation Math
    totalMozeEffect = sumEffects(MozeRotation)
    totalMarchEffect = sumEffects(MarchRotation)
    totalFeixiaoEffect = sumEffects(FeixiaoRotation)
    totalAventurineEffect = sumEffects(AventurineRotation)

    MozeRotationDuration = totalMozeEffect.actionvalue * 100.0 / MozeCharacter.getTotalStat('SPD')    
    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
    FeixiaoRotationDuration = totalFeixiaoEffect.actionvalue * 100.0 / FeixiaoCharacter.getTotalStat('SPD')
    AventurineRotationDuration = totalAventurineEffect.actionvalue * 100.0 / AventurineCharacter.getTotalStat('SPD')
    
    print('##### Rotation Durations #####')
    print('March: ',MarchRotationDuration * 2.0)
    print('Feixiao: ',FeixiaoRotationDuration * 2.0)
    print('Moze: ',MozeRotationDuration)
    print('Aventurine: ',AventurineRotationDuration)

    # Scale other character's rotation
    MarchRotation = [x * FeixiaoRotationDuration / MarchRotationDuration for x in MarchRotation]
    MozeRotation = [x * FeixiaoRotationDuration / MozeRotationDuration for x in MozeRotation]
    AventurineRotation = [x * FeixiaoRotationDuration / AventurineRotationDuration for x in AventurineRotation]

    FeixiaoEstimate = DefaultEstimator(f'{FeixiaoCharacter.fullName()} {numSkillFeixiao:.2f}E {numFollowupFeixiao:.1f}T {numUltFeixiao:.1f}Q', FeixiaoRotation, FeixiaoCharacter, config)
    MarchEstimate = DefaultEstimator(f'{MarchCharacter.fullName()} {numBasicMarch:.1f}N {numEnhancedMarch:.1f}Enh 1Q', MarchRotation, MarchCharacter, config)
    MozeEstimate = DefaultEstimator(f'{MozeCharacter.fullName()} {numSkillMoze:.1f}E {numTalentMoze:.2f}T {numUltMoze:.2f}Q', 
                                    MozeRotation, MozeCharacter, config)
    AventurineEstimate = DefaultEstimator(f'E{AventurineCharacter.eidolon} S{AventurineCharacter.lightcone.superposition:.0f} {AventurineCharacter.lightcone.name} Aventurine: {numBasicAventurine:.0f}N {numTalentAventurine:.1f}T 1Q',
                                    AventurineRotation, AventurineCharacter, config)

    return([FeixiaoEstimate, MarchEstimate, MozeEstimate, AventurineEstimate])

