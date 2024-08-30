from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Huohuo import Huohuo
from characters.nihility.SilverWolf import SilverWolf
from characters.hunt.ImaginaryMarch import ImaginaryMarch
from characters.harmony.Robin import Robin
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.SharedFeeling import SharedFeeling
from lightCones.harmony.ForTomorrowsJourney import ForTomorrowsJourney
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.GeniusOfBrilliantStars import GeniusOfBrilliantStars2pc, GeniusOfBrilliantStars4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def SilverWolfMarchRobinHuohuo(config, silverwolfEidolon:int=1):
    #%% SilverWolf March Robin Huohuo Characters

    SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['CR', 'SPD.flat', 'ER', 'DMG.quantum'],
                            substats = {'CR':12,'CD':8, 'SPD.flat': 5, 'EHR': 3}),
                            lightcone = BeforeTheTutorialMissionStarts(**config),
                            relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo = GeniusOfBrilliantStars4pc(), planarset = SprightlyVonwacq(),
                            eidolon=silverwolfEidolon,
                            **config)

    MarchCharacter = ImaginaryMarch(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.imaginary'],
                            substats = {'CD': 6, 'CR': 12, 'ATK.percent': 3, 'SPD.flat': 7}),
                            lightcone = CruisingInTheStellarSea(**config),
                            relicsetone = WastelanderOfBanditryDesert2pc(),
                            relicsettwo = WastelanderOfBanditryDesert4pc(uptimeCD=0.0),
                            planarset = RutilantArena(),
                            master=SilverWolfCharacter,
                            **config)
    
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'RES': 3, 'ATK.flat': 5}),
                            lightcone = ForTomorrowsJourney(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                            **config)

    HuohuoCharacter = Huohuo(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'HP.flat': 3, 'RES': 6}),
                        lightcone = SharedFeeling(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [SilverWolfCharacter, MarchCharacter, RobinCharacter, HuohuoCharacter]

    #%% SilverWolf March Robin Huohuo Team Buffs
    for character in [MarchCharacter, SilverWolfCharacter, RobinCharacter]:
        character.addStat('CD',description='Broken Keel from Huohuo',amount=0.1)

    # Silver Wolf Debuffs
    SilverWolfCharacter.applyDebuffs(team=team,
                                     targetingUptime=1.0,
                                     rotationDuration=1.0 if silverwolfEidolon >= 1 else 2.0,
                                     numSkillUses=1.0 if silverwolfEidolon >= 1 else 2.0)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinUltUptime = 0.5 # assume better robin ult uptime because of shorter robin rotation
    RobinCharacter.applyUltBuff([SilverWolfCharacter,MarchCharacter,HuohuoCharacter],uptime=RobinUltUptime)
        
    # March Buff
    MarchCharacter.applySkillBuff(SilverWolfCharacter)
    MarchCharacter.applyTalentBuff(SilverWolfCharacter,uptime=1.0)
    
    # Huohuo Buffs
    HuohuoCharacter.applyUltBuff([MarchCharacter,RobinCharacter, SilverWolfCharacter],uptime=2.0/4.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% SilverWolf March Robin Huohuo Rotations

    numBasicSW = 0.0
    numSkillSW = 1.0 if silverwolfEidolon >= 1 else 2.0
    numUltSW = 1.0
    SilverWolfRotation = [ # 
            SilverWolfCharacter.useBasic() * numBasicSW,
            SilverWolfCharacter.useSkill() * numSkillSW, #
            SilverWolfCharacter.useUltimate() * numUltSW, #
            RobinCharacter.useAdvanceForward() * (numBasicSW + numSkillSW) / 5.0,
    ]
    
    RobinRotationSilverWolf = [RobinCharacter.useTalent() * (numBasicSW + numSkillSW + numUltSW)]
    RobinRotationSilverWolf += [RobinCharacter.useConcertoDamage(['basic']) * numBasicSW * RobinUltUptime]
    RobinRotationSilverWolf += [RobinCharacter.useConcertoDamage(['skill']) * numSkillSW * RobinUltUptime]
    RobinRotationSilverWolf += [RobinCharacter.useConcertoDamage(['ultimate']) * numUltSW * RobinUltUptime]
    
    numBasicMarch = 2.0
    numFollowupMarch = numBasicMarch
    numEnhancedMarch = 1.0
    
    MarchRotation = []
    MarchRotation += [MarchCharacter.useBasic() * numBasicMarch]
    MarchRotation += [MarchCharacter.useFollowup() * numFollowupMarch]
    MarchRotation += [MarchCharacter.useEnhancedBasic(actionValue=0.0, numHits=5.0, chance=0.8) * numEnhancedMarch]
    MarchRotation += [MarchCharacter.useUltimate()] 
    MarchRotation += [RobinCharacter.useAdvanceForward() * numBasicMarch / 5.0] 

    RobinRotationMarch = [RobinCharacter.useTalent() * (2.0 * numBasicMarch + numEnhancedMarch + 1.0)]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['basic']) * numBasicMarch * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['basic','enhancedBasic']) * numEnhancedMarch * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['ultimate']) * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['followup']) * numFollowupMarch * RobinUltUptime]
    
    numBasicRobin = 2.0
    numSkillRobin = 1.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0, ignoreSpeed=True) # apply robin buff after we calculate damage for her basics


    numBasicHuohuo = 3.5 * 1.0 / 3.0
    numSkillHuohuo = 3.5 * 2.0 / 3.0
    HuohuoRotation = [HuohuoCharacter.useBasic() * numBasicHuohuo,
                    HuohuoCharacter.useSkill() * numSkillHuohuo,
                    HuohuoCharacter.useUltimate(),
                    RobinCharacter.useAdvanceForward() * (numBasicHuohuo + numSkillHuohuo) / 5.0]
    
    RobinRotationHuohuo = [RobinCharacter.useTalent() * (3.0)]
    RobinRotationHuohuo += [RobinCharacter.useConcertoDamage(['basic']) * 3.0 * RobinUltUptime]

    #%% SilverWolf March Robin Huohuo Rotation Math

    totalSilverWolfEffect = sumEffects(SilverWolfRotation)
    totalMarchEffect = sumEffects(MarchRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    SilverWolfRotation.append(HuohuoCharacter.giveUltEnergy(SilverWolfCharacter) * SilverWolfRotationDuration / HuohuoRotationDuration)
    
    SharedFeelingEffect = BaseEffect()
    SharedFeelingEffect.energy = 4.0 
    SharedFeelingEffect.energy *= 4 # 4  huohuo turns
    SharedFeelingEffect.energy *= numSkillHuohuo / (numBasicHuohuo + numSkillHuohuo)
    
    SilverWolfRotation.append(SharedFeelingEffect * SilverWolfRotationDuration / HuohuoRotationDuration)
    
    print('##### Rotation Durations #####')
    print('SilverWolf: ',SilverWolfRotationDuration)
    print('March: ',MarchRotationDuration)
    print('Robin: ',RobinRotationDuration)
    print('Huohuo: ',HuohuoRotationDuration)

    # Scale other character's rotation
    MarchRotation = [x * SilverWolfRotationDuration / MarchRotationDuration for x in MarchRotation]
    RobinRotationMarch = [x * SilverWolfRotationDuration / MarchRotationDuration for x in RobinRotationMarch]
    RobinRotation = [x * SilverWolfRotationDuration / RobinRotationDuration for x in RobinRotation]
    HuohuoRotation = [x * SilverWolfRotationDuration / HuohuoRotationDuration for x in HuohuoRotation]
    RobinRotationHuohuo = [x * SilverWolfRotationDuration / HuohuoRotationDuration for x in RobinRotationHuohuo]
    
    RobinRotation += RobinRotationSilverWolf
    RobinRotation += RobinRotationMarch
    RobinRotation += RobinRotationHuohuo
    totalRobinEffect = sumEffects(RobinRotation)

    SilverWolfEstimate = DefaultEstimator(f'SilverWolf {numBasicSW:.0f}N {numSkillSW:.0f}E {numUltSW:.0f}Q', SilverWolfRotation, SilverWolfCharacter, config)
    MarchEstimate = DefaultEstimator(f'March: {numBasicMarch:.1f}N {numEnhancedMarch:.1f}Enh 1Q', MarchRotation, MarchCharacter, config)
    RobinEstimate = DefaultEstimator(f'Robin: {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q, S{RobinCharacter.lightcone.superposition:d} {RobinCharacter.lightcone.name}', 
                                    RobinRotation, RobinCharacter, config)
    HuohuoEstimate = DefaultEstimator(f'Huohuo: {numBasicHuohuo:.0f}N {numSkillHuohuo:.0f}E 1Q, S{HuohuoCharacter.lightcone.superposition:.0f} {HuohuoCharacter.lightcone.name}',
                                    HuohuoRotation, HuohuoCharacter, config)

    return([SilverWolfEstimate, MarchEstimate, RobinEstimate, HuohuoEstimate])

