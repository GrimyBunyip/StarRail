from copy import deepcopy
from baseClasses.BaseEffect import sumEffects, BaseEffect
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.hunt.ImaginaryMarch import ImaginaryMarch
from characters.harmony.Robin import Robin
from characters.nihility.SilverWolf import SilverWolf
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.QuidProQuo import QuidProQuo
from lightCones.harmony.FlowingNightglow import FlowingNightglow
from lightCones.harmony.ForTomorrowsJourney import ForTomorrowsJourney
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.GeniusOfBrilliantStars import GeniusOfBrilliantStars2pc, GeniusOfBrilliantStars4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc, MusketeerOfWildWheat4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc

def MarchSilverWolfRobinE2Gallagher(config, robinSuperposition:int=0):
    #%% March SilverWolf Robin Gallagher Characters
    SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'DMG.quantum'],
                                    substats = {'SPD.flat':9,'CR':11, 'CD':5, 'EHR': 3}),
                                    lightcone = BeforeTheTutorialMissionStarts(**config),
                                    relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo = GeniusOfBrilliantStars4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                                    **config)

    MarchCharacter = ImaginaryMarch(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.imaginary'],
                                    substats = {'CR': 5, 'CD': 12, 'ATK.percent': 4, 'SPD.flat': 7}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = MusketeerOfWildWheat2pc(),
                                    relicsettwo = MusketeerOfWildWheat4pc(),
                                    planarset = RutilantArena(),
                                    master=SilverWolfCharacter,
                                    **config)
    
    RobinUltUptime = 1.0 # assume better robin ult uptime because of shorter robin rotation
    robinLightCone = FlowingNightglow(superposition=robinSuperposition,uptime=RobinUltUptime,**config) if robinSuperposition >= 1 else ForTomorrowsJourney(**config)
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 12, 'ATK.flat': 8, 'RES': 5, 'SPD.flat': 3}),
                                    lightcone = robinLightCone,
                                    relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                                    eidolon=2,
                                    **config)

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                                    substats = {'BreakEffect': 6, 'SPD.flat': 13, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = QuidProQuo(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = ThiefOfShootingMeteor2pc(), planarset = ForgeOfTheKalpagniLantern(),
                                    **config)
    
    team = [MarchCharacter, SilverWolfCharacter, RobinCharacter, GallagherCharacter]

    #%% March SilverWolf Robin Gallagher Team Buffs
    for character in [SilverWolfCharacter, MarchCharacter]:
        character.addStat('CD',description='Poised to Bloom',amount=0.12+0.04*RobinCharacter.lightcone.superposition)
    if robinSuperposition >= 1:
        for character in team:
            character.addStat('DMG',description='Flowing Nightglow',amount=0.36+0.12*robinSuperposition,uptime=RobinUltUptime)

    # Silver Wolf Debuffs
    SilverWolfCharacter.applyDebuffs(team=team,targetingUptime=1.0,rotationDuration=1.5,numSkillUses=1.0) 
    
    # March Buff
    MarchCharacter.applySkillBuff(SilverWolfCharacter)
    MarchCharacter.applyTalentBuff(SilverWolfCharacter,uptime=1.0)
    
    # Gallagher Buffs
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=3.0)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinCharacter.applyUltBuff([MarchCharacter,SilverWolfCharacter,GallagherCharacter],uptime=RobinUltUptime)

    #%% Print Statements
    for character in team:
        character.print()

    #%% March SilverWolf Robin Gallagher Rotations
    # assume 154 ish spd March and SilverWolf, March slower than SilverWolf, and 134 ish spd robin
    
    numBasicRobin = 0.0
    numSkillRobin = 1.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0) # apply robin buff after we calculate damage for her basics

    numBasicSW = 0.0
    numSkillSW = 1.5
    numUltSW = 1
    SilverWolfRotation = [ # 
            SilverWolfCharacter.useBasic() * numBasicSW,
            SilverWolfCharacter.useSkill() * numSkillSW, #
            SilverWolfCharacter.useUltimate() * numUltSW, #
    ]
    
    RobinRotationSilverWolf = [RobinCharacter.useTalent() * (numBasicSW + numSkillSW + numUltSW)]
    RobinRotationSilverWolf += [RobinCharacter.useConcertoDamage(['basic']) * numBasicSW * RobinUltUptime]
    RobinRotationSilverWolf += [RobinCharacter.useConcertoDamage(['skill']) * numSkillSW * RobinUltUptime]
    RobinRotationSilverWolf += [RobinCharacter.useConcertoDamage(['ultimate']) * numUltSW * RobinUltUptime]
    SilverWolfRotation += [RobinCharacter.useAdvanceForward() * (numBasicSW + numSkillSW) / 3.0]
    
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
    MarchRotation += [RobinCharacter.useAdvanceForward() * numBasicMarch / 3.0] 

    numBasicGallagher = 2.0
    numSkillGallagher = 1.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useSkill() * numSkillGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1,]

    RobinRotationGallagher = [RobinCharacter.useTalent() * (numBasicGallagher + numEnhancedGallagher + 1.0)]
    RobinRotationGallagher += [RobinCharacter.useConcertoDamage(['basic']) * (numBasicGallagher + numEnhancedGallagher) * RobinUltUptime]
    RobinRotationGallagher += [RobinCharacter.useConcertoDamage(['ultimate']) * 1.0 * RobinUltUptime]
    GallagherRotation += [RobinCharacter.useAdvanceForward() * (numBasicGallagher + numSkillGallagher) / 3.0] 
    
    # assume 2 procs go to robin, then other 2 split between the rest
    QPQEffect = BaseEffect()
    QPQEffect.energy = 16.0
    GallagherCharacter.addDebugInfo(QPQEffect,['buff'],'Quid Pro Quo Energy')
    MarchRotation.append(deepcopy(QPQEffect) * MarchCharacter.getER() * 2)
    RobinRotation.append(deepcopy(QPQEffect) * 2 * RobinCharacter.getER())
    # assume wolf is always above 50%

    #%% March SilverWolf Robin Gallagher Rotation Math

    totalMarchEffect = sumEffects(MarchRotation)
    totalSilverWolfEffect = sumEffects(SilverWolfRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
    SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')    

    print('##### Rotation Durations #####')
    print('March: ',MarchRotationDuration)
    print('SilverWolf: ',SilverWolfRotationDuration)
    print('Robin: ',RobinRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    SilverWolfRotation = [x * MarchRotationDuration / SilverWolfRotationDuration for x in SilverWolfRotation]
    RobinRotationSilverWolf = [x * MarchRotationDuration / SilverWolfRotationDuration for x in RobinRotationSilverWolf]
    RobinRotation = [x * MarchRotationDuration / RobinRotationDuration for x in RobinRotation]
    GallagherRotation = [x * MarchRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    RobinRotationGallagher = [x * MarchRotationDuration / GallagherRotationDuration for x in RobinRotationGallagher]
    
    RobinRotation += RobinRotationMarch
    RobinRotation += RobinRotationSilverWolf
    RobinRotation += RobinRotationGallagher
    totalRobinEffect = sumEffects(RobinRotation)

    MarchEstimate = DefaultEstimator(f'March: {numBasicMarch:.1f}N {numEnhancedMarch:.1f}Enh 1Q', MarchRotation, MarchCharacter, config)
    SilverWolfEstimate = DefaultEstimator(f'SilverWolf {numBasicSW:.1f}N {numSkillSW:.1f}E {numUltSW:.0f}Q', SilverWolfRotation, SilverWolfCharacter, config)
    RobinEstimate = DefaultEstimator(f'Robin: {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q, S{RobinCharacter.lightcone.superposition:d} {RobinCharacter.lightcone.name}', 
                                    RobinRotation, RobinCharacter, config)
    GallagherEstimate = DefaultEstimator(f'Gallagher: {numBasicGallagher:.0f}N {numSkillGallagher:.0f}E {numEnhancedGallagher:.0f}Enh 1Q, S{GallagherCharacter.lightcone.superposition:d} {GallagherCharacter.lightcone.name}', 
                                    GallagherRotation, GallagherCharacter, config)

    return([MarchEstimate, SilverWolfEstimate, GallagherEstimate, RobinEstimate])

