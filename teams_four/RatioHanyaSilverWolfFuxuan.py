from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Fuxuan import Fuxuan
from characters.hunt.DrRatio import DrRatio
from characters.harmony.Hanya import Hanya
from characters.nihility.SilverWolf import SilverWolf
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def DrRatioHanyaSilverWolfFuxuan(config):
    #%% DrRatio SilverWolf Hanya Fuxuan Characters
    DrRatioCharacter = DrRatio(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.imaginary'],
                                    substats = {'CD': 12, 'CR': 8, 'ATK.percent': 5, 'SPD.flat': 3}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = Pioneer2pc(),
                                    relicsettwo = Pioneer4pc(),
                                    planarset = FirmamentFrontlineGlamoth(stacks=2),
                                    debuffStacks=5.0,
                                    **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                                    substats = {'CR': 8, 'SPD.flat': 12, 'CD': 5, 'ATK.percent': 3}),
                                    lightcone = DanceDanceDance(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                                    **config)

    SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'BreakEffect'],
                                    substats = {'SPD.flat':12,'BreakEffect':8, 'ATK.percent': 5, 'ATK.flat': 3}),
                                    lightcone = BeforeTheTutorialMissionStarts(**config),
                                    relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                                    **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                                    substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                                    lightcone = DayOneOfMyNewLife(**config),
                                    relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                                    **config)
    
    team = [DrRatioCharacter, SilverWolfCharacter, HanyaCharacter, FuxuanCharacter]

    #%% DrRatio SilverWolf Hanya Fuxuan Team Buffs
    for character in [SilverWolfCharacter, DrRatioCharacter, HanyaCharacter]:
        character.addStat('CD',description='Broken Keel from Fuxuan',amount=0.1)
    for character in [SilverWolfCharacter, DrRatioCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel from Hanya',amount=0.1)

    # messenger 4 pc buffs:
    DrRatioCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    SilverWolfCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    FuxuanCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5*3/4)

    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(DrRatioCharacter,uptime=0.9)

    # Silver Wolf Debuffs
    SilverWolfCharacter.applyDebuffs(team=team,targetingUptime=1.0,rotationDuration=2.2,numSkillUses=1.8)
    
    # Dr Ratio Buff
    DrRatioCharacter.applyTalentBuff(team)
    
    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% DrRatio SilverWolf Hanya Fuxuan Rotations
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

    numBasicSW = 0.4
    numSkillSW = 1.8
    numUltSW = 1
    SilverWolfRotation = [ # 
            SilverWolfCharacter.useBasic() * numBasicSW,
            SilverWolfCharacter.useSkill() * numSkillSW, #
            SilverWolfCharacter.useUltimate() * numUltSW, #
    ]

    numHanyaSkill = 4
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]
    
    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% DrRatio SilverWolf Hanya Fuxuan Rotation Math

    totalDrRatioEffect = sumEffects(DrRatioRotation)
    totalSilverWolfEffect = sumEffects(SilverWolfRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    DrRatioRotationDuration = totalDrRatioEffect.actionvalue * 100.0 / DrRatioCharacter.getTotalStat('SPD')
    SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('DrRatio: ',DrRatioRotationDuration)
    print('SilverWolf: ',SilverWolfRotationDuration)
    print('Hanya: ',HanyaRotationDuration)
    print('Fuxuan: ',FuxuanRotationDuration)

    # Scale other character's rotation
    SilverWolfRotation = [x * DrRatioRotationDuration / SilverWolfRotationDuration for x in SilverWolfRotation]
    HanyaRotation = [x * DrRatioRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    FuxuanRotation = [x * DrRatioRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()
    DanceDanceDanceEffect.actionvalue = -0.24 * DrRatioRotationDuration / HanyaRotationDuration
    DrRatioCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    DrRatioRotation.append(DanceDanceDanceEffect)
    
    SilverWolfCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    SilverWolfRotation.append(DanceDanceDanceEffect)
    
    FuxuanCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    FuxuanRotation.append(DanceDanceDanceEffect)
    
    HanyaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    HanyaRotation.append(DanceDanceDanceEffect)

    DrRatioEstimate = DefaultEstimator(f'DrRatio: {numSkillRatio:.1f}E {numTalentRatio:.1f}T {numUltRatio:.0f}Q, max debuffs on target', DrRatioRotation, DrRatioCharacter, config)
    HanyaEstimate = DefaultEstimator(f'Hanya: {numHanyaSkill:.0f}E {numHanyaUlt:.0f}Q S{HanyaCharacter.lightcone.superposition:.0f} {HanyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanyaRotation, HanyaCharacter, config)
    SilverWolfEstimate = DefaultEstimator(f'SilverWolf {numBasicSW:.0f}N {numSkillSW:.0f}E {numUltSW:.0f}Q', SilverWolfRotation, SilverWolfCharacter, config)
    FuxuanEstimate = DefaultEstimator(f'Fuxuan: 2N 1E 1Q, S{FuxuanCharacter.lightcone.superposition:.0f} {FuxuanCharacter.lightcone.name}',
                                    FuxuanRotation, FuxuanCharacter, config)

    return([DrRatioEstimate, SilverWolfEstimate, HanyaEstimate, FuxuanEstimate])

