from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.hunt.DrRatio import DrRatio
from characters.harmony.Tingyun import Tingyun
from characters.nihility.SilverWolf import SilverWolf
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def DrRatioTingyunSilverWolfLuocha(config):
    #%% DrRatio SilverWolf Tingyun Luocha Characters
    DrRatioCharacter = DrRatio(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CD', 'DMG.imaginary'],
                                    substats = {'CD': 8, 'CR': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = WastelanderOfBanditryDesert2pc(),
                                    relicsettwo = WastelanderOfBanditryDesert4pc(),
                                    planarset = FirmamentFrontlineGlamoth(stacks=2),
                                    debuffStacks=5.0,
                                    **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                                    substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                                    lightcone = MemoriesOfThePast(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                                    benedictionTarget=DrRatioCharacter,
                                    **config)

    SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'BreakEffect'],
                                    substats = {'SPD.flat':12,'BreakEffect':8, 'ATK.percent': 5, 'ATK.flat': 3}),
                                    lightcone = BeforeTheTutorialMissionStarts(**config),
                                    relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                                    **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 5, 'SPD.flat': 12, 'HP.percent': 4, 'RES': 7}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                                    **config)
    
    team = [DrRatioCharacter, SilverWolfCharacter, TingyunCharacter, LuochaCharacter]

    #%% DrRatio SilverWolf Tingyun Luocha Team Buffs
    for character in [SilverWolfCharacter, DrRatioCharacter, TingyunCharacter]:
        character.addStat('DMG.imaginary',description='Penacony from Luocha',amount=0.1)

    # messenger 4 pc buffs:
    DrRatioCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    SilverWolfCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5*3/4)

    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(DrRatioCharacter)
    TingyunCharacter.applyUltBuff(DrRatioCharacter)

    # Silver Wolf Debuffs
    SilverWolfCharacter.applyDebuffs(team=team,targetingUptime=1.0,numSkillUses=1) 
    
    # Dr Ratio Buff
    DrRatioCharacter.applyTalentBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% DrRatio SilverWolf Tingyun Luocha Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long

    numSkillRatio = 2.0
    numUltRatio = 1.0
    numTalentRatio = numSkillRatio + 2 * numUltRatio
    DrRatioRotation = [ # 110 max energy
            DrRatioCharacter.useSkill() * numSkillRatio,
            DrRatioCharacter.useUltimate() * numUltRatio,
            DrRatioCharacter.useTalent() * numTalentRatio,
            TingyunCharacter.useBenediction(['skill']) * numSkillRatio, # apply benedictions with buffs
            TingyunCharacter.useBenediction(['ultimate']) * numUltRatio,
            TingyunCharacter.useBenediction(['talent','followup']) * numUltRatio,
            TingyunCharacter.giveUltEnergy(),
    ]

    numBasicSW = 0
    numSkillSW = 2
    numUltSW = 1
    SilverWolfRotation = [ # 
            SilverWolfCharacter.useBasic() * numBasicSW,
            SilverWolfCharacter.useSkill() * numSkillSW, #
            SilverWolfCharacter.useUltimate() * numUltSW, #
    ]
    
    TingyunRotation = [ 
            TingyunCharacter.useBasic() * 2, 
            TingyunCharacter.useSkill(),
            TingyunCharacter.useUltimate(),
    ]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% DrRatio SilverWolf Tingyun Luocha Rotation Math

    totalDrRatioEffect = sumEffects(DrRatioRotation)
    totalSilverWolfEffect = sumEffects(SilverWolfRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    DrRatioRotationDuration = totalDrRatioEffect.actionvalue * 100.0 / DrRatioCharacter.getTotalStat('SPD')
    SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('DrRatio: ',DrRatioRotationDuration)
    print('SilverWolf: ',SilverWolfRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # Scale other character's rotation
    SilverWolfRotation = [x * DrRatioRotationDuration / SilverWolfRotationDuration for x in SilverWolfRotation]
    TingyunRotation = [x * DrRatioRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    LuochaRotation = [x * DrRatioRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    DrRatioEstimate = DefaultEstimator(f'DrRatio: {numSkillRatio:.0f}E {numTalentRatio:.1f}T {numUltRatio:.0f}Q, max debuffs on target', DrRatioRotation, DrRatioCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats',
                                    TingyunRotation, TingyunCharacter, config)
    SilverWolfEstimate = DefaultEstimator(f'SilverWolf {numBasicSW:.0f}N {numSkillSW:.0f}E {numUltSW:.0f}Q', SilverWolfRotation, SilverWolfCharacter, config)
    LuochaEstimate = DefaultEstimator(f'Luocha: 3N 1E 1Q, S{LuochaCharacter.lightcone.superposition:d} {LuochaCharacter.lightcone.name}', 
                                    LuochaRotation, LuochaCharacter, config)

    return([DrRatioEstimate, SilverWolfEstimate, TingyunEstimate, LuochaEstimate])

