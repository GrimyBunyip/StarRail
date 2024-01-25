from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.hunt.DrRatio import DrRatio
from characters.nihility.SilverWolf import SilverWolf
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.Swordplay import Swordplay
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def DrRatioTopazSilverWolfLuocha(config):
    #%% DrRatio Topaz SilverWolf Luocha Characters
    
    DrRatioCharacter = DrRatio(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.imaginary'],
                                    substats = {'CD': 5, 'CR': 6, 'ATK.percent': 3, 'SPD.flat': 14}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = Pioneer2pc(),
                                    relicsettwo = Pioneer4pc(),
                                    planarset = FirmamentFrontlineGlamoth(stacks=2),
                                    debuffStacks=5,
                                    **config)

    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                                    substats = {'CR': 5, 'CD': 8, 'ATK.percent': 3, 'SPD.flat': 12}),
                                    lightcone = Swordplay(**config),
                                    relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                                    **config)

    SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'BreakEffect'],
                                    substats = {'SPD.flat':12,'BreakEffect':8, 'ATK.percent': 5, 'ATK.flat': 3}),
                                    lightcone = BeforeTheTutorialMissionStarts(**config),
                                    relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                                    **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 5, 'SPD.flat': 12, 'HP.percent': 4, 'RES': 7}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                                    **config)
    
    team = [DrRatioCharacter, TopazCharacter, SilverWolfCharacter, LuochaCharacter]

    #%% DrRatio Topaz SilverWolf Luocha Team Buffs
    for character in [TopazCharacter, DrRatioCharacter, SilverWolfCharacter]:
        character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)

    # Silver Wolf Debuffs
    SilverWolfCharacter.applyDebuffs(team=team,targetingUptime=1.0,rotationDuration=2.2,numSkillUses=1.8) 

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff([TopazCharacter,DrRatioCharacter],uptime=1.0)
    
    # Dr Ratio Buff
    DrRatioCharacter.applyTalentBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% DrRatio Topaz SilverWolf Luocha Rotations
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

    numBasicTopaz = 4.0
    numSkillTopaz = 1.0
    TopazRotation = [ # 130 max energy
            TopazCharacter.useBasic() * numBasicTopaz,
            TopazCharacter.useSkill() * numSkillTopaz,
            TopazCharacter.useUltimate(),
            TopazCharacter.useTalent(windfall=True) * 2, # two talents from windfall
    ]

    topazTurns = sum([x.actionvalue for x in TopazRotation])
    numbyTurns = topazTurns * 80 / TopazCharacter.getTotalStat('SPD')
    numbyAdvanceForwards = topazTurns / 2 + numTalentRatio    
    TopazRotation.append(TopazCharacter.useTalent(windfall=False) * (numbyTurns + numbyAdvanceForwards)) # about 1 talent per basic/skill

    numBasicSW = 0.4
    numSkillSW = 1.8
    numUltSW = 1
    SilverWolfRotation = [ # 
            SilverWolfCharacter.useBasic() * numBasicSW,
            SilverWolfCharacter.useSkill() * numSkillSW, #
            SilverWolfCharacter.useUltimate() * numUltSW, #
    ]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% DrRatio Topaz SilverWolf Luocha Rotation Math

    totalDrRatioEffect = sumEffects(DrRatioRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalSilverWolfEffect = sumEffects(SilverWolfRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    DrRatioRotationDuration = totalDrRatioEffect.actionvalue * 100.0 / DrRatioCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('DrRatio: ',DrRatioRotationDuration)
    print('Topaz: ',TopazRotationDuration)
    print('SilverWolf: ',SilverWolfRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # Scale other character's rotation
    TopazRotation = [x * DrRatioRotationDuration / TopazRotationDuration for x in TopazRotation]
    SilverWolfRotation = [x * DrRatioRotationDuration / SilverWolfRotationDuration for x in SilverWolfRotation]
    LuochaRotation = [x * DrRatioRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    DrRatioEstimate = DefaultEstimator(f'DrRatio: {numSkillRatio:.1f}E {numTalentRatio:.1f}T {numUltRatio:.0f}Q, max debuffs on target', DrRatioRotation, DrRatioCharacter, config)
    TopazEstimate = DefaultEstimator(f'Topaz: {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numbyTurns + numbyAdvanceForwards:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    SilverWolfEstimate = DefaultEstimator(f'SilverWolf {numBasicSW:.1f}N {numSkillSW:.1f}E {numUltSW:.0f}Q', SilverWolfRotation, SilverWolfCharacter, config)
    LuochaEstimate = DefaultEstimator(f'Luocha: 3N 1E 1Q, S{LuochaCharacter.lightcone.superposition:d} {LuochaCharacter.lightcone.name}', 
                                    LuochaRotation, LuochaCharacter, config)

    return([DrRatioEstimate, TopazEstimate, LuochaEstimate, SilverWolfEstimate])

