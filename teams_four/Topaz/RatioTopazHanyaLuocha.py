from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.hunt.DrRatio import DrRatio
from characters.harmony.Hanya import Hanya
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.Swordplay import Swordplay
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc

def DrRatioTopazHanyaLuocha(config):
    #%% DrRatio Topaz Hanya Luocha Characters
    DrRatioCharacter = DrRatio(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.imaginary'],
                                    substats = {'CD': 12, 'CR': 8, 'ATK.percent': 3, 'SPD.flat': 5}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = Pioneer2pc(),
                                    relicsettwo = Pioneer4pc(),
                                    planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    **config)

    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'ATK.percent', 'CR', 'ATK.percent'],
                                    substats = {'CR': 8, 'CD': 12, 'ATK.percent': 3, 'SPD.flat': 5}),
                                    lightcone = Swordplay(**config),
                                    relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                                    substats = {'CR': 8, 'SPD.flat': 12, 'CD': 5, 'ATK.percent': 3}),
                                    lightcone = DanceDanceDance(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                                    **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 5, 'SPD.flat': 12, 'HP.percent': 4, 'RES': 7}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                                    **config)
    
    team = [DrRatioCharacter, TopazCharacter, HanyaCharacter, LuochaCharacter]

    #%% DrRatio Topaz Hanya Luocha Team Buffs
    for character in [TopazCharacter, DrRatioCharacter, HanyaCharacter]:
        character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
    for character in [TopazCharacter, DrRatioCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel from Hanya',amount=0.1)

    # messenger 4 pc buffs:
    DrRatioCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    TopazCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5*3/4)

    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(DrRatioCharacter,uptime=2.0/3.0)
    HanyaCharacter.applyUltBuff(TopazCharacter,uptime=2.0/3.0)

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff([TopazCharacter,DrRatioCharacter],uptime=1.0)
    
    # Dr Ratio Buff
    DrRatioCharacter.applyTalentBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% DrRatio Topaz Hanya Luocha Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long

    numSkillRatio = 3.5
    numUltRatio = 1.0
    numTalentRatio = numSkillRatio + 2 * numUltRatio
    DrRatioRotation = [ # 110 max energy
            DrRatioCharacter.useSkill() * numSkillRatio,
            DrRatioCharacter.useUltimate() * numUltRatio,
            DrRatioCharacter.useTalent() * numTalentRatio,
    ]

    numBasicTopaz = 0.0
    numSkillTopaz = 3.83
    TopazRotation = [ # 130 max energy
            TopazCharacter.useBasic() * numBasicTopaz,
            TopazCharacter.useSkill() * numSkillTopaz,
            TopazCharacter.useUltimate(),
            TopazCharacter.useTalent(windfall=True) * 2, # two talents from windfall
    ]

    topazTurns = sum([x.actionvalue for x in TopazRotation])
    numbyTurns = topazTurns * 80 / TopazCharacter.getTotalStat('SPD')
    numbyAdvanceForwards = topazTurns / 2 + numTalentRatio    
    TopazRotation.append(TopazCharacter.useTalent(windfall=False) * (numbyTurns + numbyAdvanceForwards*0.8)) # about 1 talent per basic/skill, 0.8 on advances because I want to assume some desync with Hanya in the mix

    numHanyaSkill = 4
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% DrRatio Topaz Hanya Luocha Rotation Math

    totalDrRatioEffect = sumEffects(DrRatioRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    DrRatioRotationDuration = totalDrRatioEffect.actionvalue * 100.0 / DrRatioCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()

    DanceDanceDanceEffect.actionvalue = -0.24
    HanyaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    HanyaRotation.append(deepcopy(DanceDanceDanceEffect))
    totalHanyaEffect = sumEffects(HanyaRotation)
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')

    DanceDanceDanceEffect.actionvalue = -0.24 * TopazRotationDuration / HanyaRotationDuration
    TopazCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    TopazRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * DrRatioRotationDuration / HanyaRotationDuration
    DrRatioCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    DrRatioRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * LuochaRotationDuration / HanyaRotationDuration
    LuochaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    LuochaRotation.append(deepcopy(DanceDanceDanceEffect))
    
    totalDrRatioEffect = sumEffects(DrRatioRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    DrRatioRotationDuration = totalDrRatioEffect.actionvalue * 100.0 / DrRatioCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('DrRatio: ',DrRatioRotationDuration)
    print('Topaz: ',TopazRotationDuration)
    print('Hanya: ',HanyaRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # Scale other character's rotation
    TopazRotation = [x * DrRatioRotationDuration / TopazRotationDuration for x in TopazRotation]
    HanyaRotation = [x * DrRatioRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    LuochaRotation = [x * DrRatioRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    DrRatioEstimate = DefaultEstimator(f'DrRatio: {numSkillRatio:.1f}E {numTalentRatio:.1f}T {numUltRatio:.0f}Q, max debuffs on target', DrRatioRotation, DrRatioCharacter, config)
    TopazEstimate = DefaultEstimator(f'Topaz: {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numbyTurns + numbyAdvanceForwards:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    HanyaEstimate = DefaultEstimator(f'Hanya: {numHanyaSkill:.0f}E {numHanyaUlt:.0f}Q S{HanyaCharacter.lightcone.superposition:.0f} {HanyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanyaRotation, HanyaCharacter, config)
    LuochaEstimate = DefaultEstimator(f'Luocha: 3N 1E 1Q, S{LuochaCharacter.lightcone.superposition:d} {LuochaCharacter.lightcone.name}', 
                                    LuochaRotation, LuochaCharacter, config)

    return([DrRatioEstimate, TopazEstimate, LuochaEstimate, HanyaEstimate])

