from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Aventurine import Aventurine
from characters.hunt.Topaz import Topaz
from characters.hunt.Moze import Moze
from characters.hunt.Feixiao import Feixiao
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.IVentureForthToHunt import IVentureForthToHunt
from lightCones.hunt.Swordplay import Swordplay
from lightCones.hunt.WorrisomeBlissful import WorrisomeBlissful
from lightCones.preservation.DestinysThreadsForewoven import DestinysThreadsForewoven
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.DuranDynastyOfRunningWolves import DuranDynastyOfRunningWolves
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.KnightOfPurityPalace import KnightOfPurityPalace2pc, KnightOfPurityPalace4pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def FeixiaoTopazMozeAventurine(config, 
                                feixiaoEidolon:int=None, 
                                feixiaoSuperposition:int=0,
                                topazEidolon:int=None,
                                topazSuperposition:int=0,):
    #%% Topaz Feixiao Moze Aventurine Characters

    FeixiaoLightcone = CruisingInTheStellarSea(**config) if feixiaoSuperposition == 0 else IVentureForthToHunt(superposition=feixiaoSuperposition,**config)
    FeixiaoSubstats = {'CR': 7, 'CD': 8, 'ATK.percent': 3, 'SPD.flat':10} if feixiaoSuperposition == 0 else {'CR': 10, 'CD': 5, 'ATK.percent': 3, 'SPD.flat':10}
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
    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                                    substats = TopazSubstats),
                                    lightcone = topazLightcone, 
                                    relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = DuranDynastyOfRunningWolves(),
                                    eidolon=topazEidolon,
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
    
    team = [TopazCharacter, FeixiaoCharacter, MozeCharacter, AventurineCharacter]

    #%% Topaz Feixiao Moze Aventurine Team Buffs
    for character in [FeixiaoCharacter, TopazCharacter, MozeCharacter]:
        character.addStat('CD',description='Broken Keel from Aventurine',amount=0.1)
    if MozeCharacter.lightcone.name == 'Poised to Bloom':
        for character in [FeixiaoCharacter, TopazCharacter]:
            character.addStat('CD',description='Poised to Bloom',amount=0.12+0.04*MozeCharacter.lightcone.superposition)

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff(team,uptime=1.0)
    if topazSuperposition > 0:
        for character in [FeixiaoCharacter, MozeCharacter, AventurineCharacter]:
                character.addStat('CD',description='Worrisome, Blissful',
                                        amount=0.10 + 0.02 * TopazCharacter.lightcone.superposition,
                                        stacks=2.0)
    
    # Aventurine Buffs
    AventurineCharacter.applyUltDebuff(team=team,rotationDuration=4.0,targetingUptime=1.0)

    # Moze Buffs
    MozeUptime=1.0
    MozeCharacter.applyDebuff(team, uptime=MozeUptime)    

    #%% Print Statements
    for character in team:
        character.print()

    #%% Topaz Feixiao Moze Aventurine Rotations
    
    numAdditionalMoze = 9.0
    numTalentMoze = 3.0
    numSkillMoze = 1.0
    numUltMoze = 0.75 # roughly 0.75 moze ults per rotation
    actionValueMoze = AventurineCharacter.useBasic().actionvalue / MozeUptime
    MozeRotation = [MozeCharacter.useSkill(actionvalue=actionValueMoze) * numSkillMoze,
                    MozeCharacter.useTalent() * (numTalentMoze + numUltMoze),
                    MozeCharacter.useAdditionalDamage() * numAdditionalMoze,
                    MozeCharacter.useUltimate()]

    numBasicTopaz = 2.0
    numSkillTopaz = 2.0
    numTalentTopaz = (numBasicTopaz + numSkillTopaz) * 2.0 + 1.0 # rough estimate
    TopazRotation = []
    TopazRotation += [TopazCharacter.useBasic() * numBasicTopaz]
    TopazRotation += [TopazCharacter.useSkill() * numSkillTopaz]
    TopazRotation += [TopazCharacter.useUltimate()]
    TopazRotation += [TopazCharacter.useTalent(windfall=True) * 2.0] # two talents from windfall
    TopazRotation += [TopazCharacter.useTalent(windfall=False) * (numTalentTopaz - 1.0)] # deducted windfall advances

    numBasicAventurine = 4.0
    numTalentAventurine = 4.0 # stacks from ultimate
    numEnemyAttacks = AventurineCharacter.numEnemies * AventurineCharacter.enemySpeed / AventurineCharacter.getTotalStat('SPD') # extra stacks from people getting hit per turn
    numEnemyAttacks += (1.0 + (6*1) / (6*1 + 4 + 3 + 3)) # extra stacks from when Aventurine is Targeted
    numTalentAventurine += numBasicAventurine * numEnemyAttacks
    
    numFollowups = 2.5 * FeixiaoCharacter.getTotalStat('SPD') # Feixiao gets about 2.5 followup per turn
    numFollowups += (numSkillMoze + numTalentMoze + 2.0 * numUltMoze) * MozeUptime
    numFollowups += TopazCharacter.getTotalStat('SPD') * (numTalentTopaz + numBasicTopaz + numSkillTopaz) / (numBasicTopaz + numSkillTopaz)
    numFollowups /= AventurineCharacter.getTotalStat('SPD')
    numTalentAventurine += numBasicAventurine * min(3.0,numFollowups)
    
    AventurineRotation = [AventurineCharacter.useBasic() * numBasicAventurine,
                          AventurineCharacter.useTalent() * numTalentAventurine,
                          AventurineCharacter.useUltimate() * 1,]
    
    # number of attacks in 2 feixiao turns
    numTurns = 2.0
    numAttacks = numTurns * 3.0 # feixiao attacks
    numAttacks += numTurns * (numSkillMoze + numTalentMoze + 2.0 * numUltMoze) * MozeUptime
    numAttacks += numTurns * (numBasicTopaz + numSkillTopaz + numTalentTopaz + 1.0) / (numBasicTopaz + numSkillTopaz)  # Topaz attacks
    numAttacks += numTurns * (1.0 + numTalentAventurine / 7.0) / numBasicAventurine # aventurine attacks
    
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

    #%% Topaz Feixiao Moze Aventurine Rotation Math

    # four turn Moze advance math
    totalMozeEffect = sumEffects(MozeRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalFeixiaoEffect = sumEffects(FeixiaoRotation)
    totalAventurineEffect = sumEffects(AventurineRotation)

    MozeRotationDuration = totalMozeEffect.actionvalue * 100.0 / MozeCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    FeixiaoRotationDuration = totalFeixiaoEffect.actionvalue * 100.0 / FeixiaoCharacter.getTotalStat('SPD')
    AventurineRotationDuration = totalAventurineEffect.actionvalue * 100.0 / AventurineCharacter.getTotalStat('SPD')
    
    print('##### Rotation Durations #####')
    print('Topaz: ',TopazRotationDuration)
    print('Feixiao: ',FeixiaoRotationDuration)
    print('Moze: ',MozeRotationDuration)
    print('Aventurine: ',AventurineRotationDuration)

    # Scale other character's rotation
    MozeRotation = [x * FeixiaoRotationDuration / MozeRotationDuration for x in MozeRotation]
    TopazRotation = [x * FeixiaoRotationDuration / TopazRotationDuration for x in TopazRotation]
    AventurineRotation = [x * FeixiaoRotationDuration / AventurineRotationDuration for x in AventurineRotation]

    FeixiaoEstimate = DefaultEstimator(f'{FeixiaoCharacter.fullName()} {numSkillFeixiao:.2f}E {numFollowupFeixiao:.1f}T {numUltFeixiao:.1f}Q', FeixiaoRotation, FeixiaoCharacter, config)
    TopazEstimate = DefaultEstimator(f'{TopazCharacter.fullName()} {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numTalentTopaz:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    MozeEstimate = DefaultEstimator(f'{MozeCharacter.fullName()} {numSkillMoze:.1f}E {numTalentMoze:.2f}T {numUltMoze:.2f}Q', 
                                    MozeRotation, MozeCharacter, config)
    AventurineEstimate = DefaultEstimator(f'E{AventurineCharacter.eidolon} S{AventurineCharacter.lightcone.superposition:.0f} {AventurineCharacter.lightcone.name} Aventurine: {numBasicAventurine:.0f}N {numTalentAventurine:.1f}T 1Q',
                                    AventurineRotation, AventurineCharacter, config)

    return([FeixiaoEstimate, TopazEstimate, MozeEstimate, AventurineEstimate])

