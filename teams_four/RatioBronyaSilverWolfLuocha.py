from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.hunt.DrRatio import DrRatio
from characters.harmony.Bronya import Bronya
from characters.nihility.SilverWolf import SilverWolf
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def DrRatioBronyaSilverWolfLuocha(config):
    #%% DrRatio SilverWolf Bronya Luocha Characters
    DrRatioCharacter = DrRatio(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
                                    substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'ATK.flat': 3}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = WastelanderOfBanditryDesert2pc(),
                                    relicsettwo = WastelanderOfBanditryDesert4pc(),
                                    planarset = FirmamentFrontlineGlamoth(stacks=2),
                                    **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'HP.percent', 'CD', 'ER'],
                                    substats = {'CD': 12, 'SPD.flat': 7, 'HP.percent': 5, 'DEF.percent': 3}),
                                    lightcone = PastAndFuture(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
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
    
    team = [DrRatioCharacter, SilverWolfCharacter, BronyaCharacter, LuochaCharacter]

    #%% DrRatio SilverWolf Bronya Luocha Team Buffs
    for character in [SilverWolfCharacter, DrRatioCharacter, BronyaCharacter]:
        character.addStat('DMG.imaginary',description='Penacony from Luocha',amount=0.1)
    for character in [SilverWolfCharacter, DrRatioCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel from Bronya',amount=0.1)

    # messenger 4 pc buffs: cannot afford the SP for t his
    #DrRatioCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    #SilverWolfCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    #LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5*3/4)

    # Silver Wolf Debuffs
    SilverWolfCharacter.applyDebuffs(team=team,targetingUptime=1.0,rotationDuration=3.0,numSkillUses=0.0) 
        
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    
    # Dr Ratio Buff
    DrRatioCharacter.applyTalentBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% DrRatio SilverWolf Bronya Luocha Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long

    numSkillRatio = 4.0
    numUltRatio = 1.0
    numTalentRatio = numSkillRatio + 2 * numUltRatio
    DrRatioRotation = [ # 110 max energy
            DrRatioCharacter.useSkill() * numSkillRatio / 2,
            DrRatioCharacter.useTalent() * (numSkillRatio / 2 + 2 * numUltRatio),
    ]

    BronyaCharacter.applySkillBuff(DrRatioCharacter,uptime=1.0)
    BronyaCharacter.applyUltBuff(DrRatioCharacter,uptime=0.5) # only get Bronya ult buff every other rotation
    DrRatioCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition)
    
    DrRatioRotation += [DrRatioCharacter.useSkill() * numSkillRatio / 2]
    DrRatioRotation += [DrRatioCharacter.useUltimate() * numUltRatio]
    DrRatioRotation += [DrRatioCharacter.useTalent() * numSkillRatio / 2]
    DrRatioRotation += [BronyaCharacter.useAdvanceForward() * 2] #Dr Ratio rotation is 4 turns


    numBasicSW = 3
    numSkillSW = 0
    numUltSW = 1
    SilverWolfRotation = [ # 
            SilverWolfCharacter.useBasic() * numBasicSW,
            SilverWolfCharacter.useSkill() * numSkillSW, #
            SilverWolfCharacter.useUltimate() * numUltSW, #
    ]

    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% DrRatio SilverWolf Bronya Luocha Rotation Math

    totalDrRatioEffect = sumEffects(DrRatioRotation)
    totalSilverWolfEffect = sumEffects(SilverWolfRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    DrRatioRotationDuration = totalDrRatioEffect.actionvalue * 100.0 / DrRatioCharacter.getTotalStat('SPD')
    SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('DrRatio: ',DrRatioRotationDuration)
    print('SilverWolf: ',SilverWolfRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # Scale other character's rotation
    SilverWolfRotation = [x * DrRatioRotationDuration / SilverWolfRotationDuration for x in SilverWolfRotation]
    BronyaRotation = [x * DrRatioRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    LuochaRotation = [x * DrRatioRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    DrRatioEstimate = DefaultEstimator(f'DrRatio: {numSkillRatio:.0f}E {numTalentRatio:.1f}T {numUltRatio:.0f}Q, max debuffs on target', DrRatioRotation, DrRatioCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    SilverWolfEstimate = DefaultEstimator(f'SilverWolf {numBasicSW:.0f}N {numSkillSW:.0f}E {numUltSW:.0f}Q', SilverWolfRotation, SilverWolfCharacter, config)
    LuochaEstimate = DefaultEstimator(f'Luocha: 3N 1E 1Q, S{LuochaCharacter.lightcone.superposition:d} {LuochaCharacter.lightcone.name}', 
                                    LuochaRotation, LuochaCharacter, config)

    return([DrRatioEstimate, SilverWolfEstimate, BronyaEstimate, LuochaEstimate])

