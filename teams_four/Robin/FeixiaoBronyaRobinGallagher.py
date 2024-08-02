from copy import deepcopy
from baseClasses.BaseEffect import sumEffects, BaseEffect
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.hunt.Feixiao import Feixiao
from characters.harmony.Robin import Robin
from characters.harmony.Bronya import Bronya
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.QuidProQuo import QuidProQuo
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.FlowingNightglow import FlowingNightglow
from lightCones.harmony.ForTomorrowsJourney import ForTomorrowsJourney
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.IVentureForthToHunt import IVentureForthToHunt
from relicSets.planarSets.DuranDynastyOfRunningWolves import DuranDynastyOfRunningWolves
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc, MusketeerOfWildWheat4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def FeixiaoBronyaRobinGallagher(config, 
                                feixiaoEidolon:int=None, 
                                feixiaoSuperposition:int=0, 
                                robinEidolon:int=None, 
                                robinSuperposition:int=0):
    #%% Feixiao Bronya Robin Gallagher Characters
    BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'ER'],
                                    substats = {'CD': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                                    lightcone = DanceDanceDance(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = SprightlyVonwacq(),
                                    **config)

    FeixiaoLightcone = CruisingInTheStellarSea(**config) if feixiaoSuperposition == 0 else IVentureForthToHunt(superposition=feixiaoSuperposition,**config)
    FeixiaoCharacter = Feixiao(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.wind'],
                                    substats = {'CR': 7, 'CD': 12, 'ATK.percent': 4, 'SPD.flat':5}),
                                    lightcone = FeixiaoLightcone,
                                    relicsetone = WindSoaringValorous2pc(),
                                    relicsettwo = WindSoaringValorous4pc(),
                                    planarset = DuranDynastyOfRunningWolves(),
                                    eidolon = feixiaoEidolon,
                                    **config)
    
    RobinUltUptime = 1.0 # assume better robin ult uptime because of shorter robin rotation
    robinLightCone = ForTomorrowsJourney(**config) if robinSuperposition == 0 else FlowingNightglow(superposition=robinSuperposition,uptime=RobinUltUptime,**config)
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 12, 'ATK.flat': 8, 'RES': 5, 'SPD.flat': 3}),
                                    lightcone = robinLightCone,
                                    relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                                    eidolon=robinEidolon,
                                    **config)

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                                    substats = {'BreakEffect': 7, 'SPD.flat': 13, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = QuidProQuo(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = ThiefOfShootingMeteor2pc(), planarset = SprightlyVonwacq(),
                                    **config)
    
    team = [FeixiaoCharacter, BronyaCharacter, RobinCharacter, GallagherCharacter]

    #%% Feixiao Bronya Robin Gallagher Team Buffs
    if robinSuperposition >= 1:
        for character in team:
            character.addStat('DMG',description='Flowing Nightglow',amount=0.36+0.12*robinSuperposition,uptime=RobinUltUptime)
        
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    BronyaCharacter.applySkillBuff(GallagherCharacter,uptime=2.0/5.0)
    BronyaCharacter.applyUltBuff(RobinCharacter,uptime=1.0)
    for character in [FeixiaoCharacter, GallagherCharacter, BronyaCharacter]:
        BronyaCharacter.applyUltBuff(character,uptime=2.0/3.0)
    
    # Gallagher Buffs
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=3.0)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinCharacter.applyUltBuff([FeixiaoCharacter,BronyaCharacter,GallagherCharacter],uptime=RobinUltUptime)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Feixiao Bronya Robin Gallagher Rotations
    numBasicRobin = 0.0
    numSkillRobin = 2.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin]
    RobinRotation += [RobinCharacter.useSkill() * numSkillRobin]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0) # do not apply robin buff to her basics or skills
    RobinRotation += [RobinCharacter.useUltimate() * 1]
    RobinRotation += [BronyaCharacter.useAdvanceForward()]

    DanceDanceDanceEffect = BaseEffect()
    DanceDanceDanceEffect.actionvalue = -0.24
    numBasicBronya = 0.0
    numSkillBronya = 3.0
    BronyaRotation = [ # 130 max energy
            BronyaCharacter.useBasic() * numBasicBronya,
            BronyaCharacter.useSkill() * numSkillBronya,
            BronyaCharacter.useUltimate(),
            DanceDanceDanceEffect,
    ]

    numBasicGallagher = 4.0
    numSkillGallagher = 0.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useSkill() * numSkillGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1,
                         BronyaCharacter.useAdvanceForward() * (numBasicGallagher + numSkillGallagher) * 2.0 / 5.0,
                         DanceDanceDanceEffect * (numBasicGallagher + numSkillGallagher) / 5.0,]

    RobinRotationGallagher = [RobinCharacter.useTalent() * (numBasicGallagher + numEnhancedGallagher + 1.0)]
    RobinRotationGallagher += [RobinCharacter.useConcertoDamage(['basic']) * (numBasicGallagher + numEnhancedGallagher) * RobinUltUptime]
    RobinRotationGallagher += [RobinCharacter.useConcertoDamage(['ultimate']) * 1.0 * RobinUltUptime]
    
    
    numBasicFeixiao = 1.0
    numSkillFeixiao = 2.0
    numFollowupFeixiao = (numBasicFeixiao + numSkillFeixiao)

    numTurns = numBasicFeixiao + numSkillFeixiao
    numAttacks = numTurns * 2.0 # feixiao attacks
    numAttacks += numTurns * 2.5  # 5 gallagher basics, 1.25 ult, 1.25 enhanced per 3 gallagher turns

    numUltFeixiao = numAttacks * (1.0 if FeixiaoCharacter.eidolon >= 2 else 0.5)
    
    numBasicFeixiao *= 6.0 / numUltFeixiao
    numSkillFeixiao *= 6.0 / numUltFeixiao
    numFollowupFeixiao *= 6.0 / numUltFeixiao
    numUltFeixiao = 6.0
    
    FeixiaoRotation = []
    FeixiaoRotation += [FeixiaoCharacter.useBasic() * numBasicFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useSkill() * numSkillFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useTalent() * numFollowupFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useUltimate() * numUltFeixiao] 

    RobinRotationFeixiao = [RobinCharacter.useTalent() * (numBasicFeixiao + numSkillFeixiao + numFollowupFeixiao + 1.0)]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['basic']) * numBasicFeixiao * RobinUltUptime]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['skill']) * numSkillFeixiao * RobinUltUptime]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['followup']) * numFollowupFeixiao * RobinUltUptime]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['ultimate','followup']) * RobinUltUptime]
    
    # assume 2 procs go to robin, then other 2 split between the rest
    QPQEffect = BaseEffect()
    QPQEffect.energy = 16.0
    GallagherCharacter.addDebugInfo(QPQEffect,['buff'],'Quid Pro Quo Energy')
    RobinRotation.append(deepcopy(QPQEffect) * 2 * RobinCharacter.getER() )
    BronyaRotation.append(deepcopy(QPQEffect) * BronyaCharacter.getER() )

    #%% Feixiao Bronya Robin Gallagher Rotation Math

    totalRobinEffect = sumEffects(RobinRotation)
    totalFeixiaoEffect = sumEffects(FeixiaoRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)
    
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    FeixiaoRotationDuration = totalFeixiaoEffect.actionvalue * 100.0 / FeixiaoCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    FeixiaoRotationMult = 1.0
    BronyaRotationMult = 1.0
    GallagherRotationMult = 1.25 
    
    FeixiaoThreeTurns = FeixiaoRotationDuration * FeixiaoRotationMult
    BronyaThreeTurns = BronyaRotationDuration * BronyaRotationMult
    GallagherThreeTurns = GallagherRotationDuration * GallagherRotationMult
    
    FeixiaoRotation += [RobinCharacter.useAdvanceForward() * (FeixiaoThreeTurns - RobinRotationDuration) * FeixiaoCharacter.getTotalStat('SPD') / 100 / FeixiaoRotationMult]
    BronyaRotation += [RobinCharacter.useAdvanceForward() * (BronyaThreeTurns - RobinRotationDuration) * BronyaCharacter.getTotalStat('SPD') / 100 / BronyaRotationMult]
    GallagherRotation += [RobinCharacter.useAdvanceForward() * (GallagherThreeTurns - RobinRotationDuration) * GallagherCharacter.getTotalStat('SPD') / 100 / GallagherRotationMult]
        
    totalFeixiaoEffect = sumEffects(FeixiaoRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)
    FeixiaoRotationDuration = totalFeixiaoEffect.actionvalue * 100.0 / FeixiaoCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')
    
    print('##### Rotation Durations #####')
    print('Feixiao: ',FeixiaoRotationDuration * FeixiaoRotationMult)
    print('Bronya: ',BronyaRotationDuration * BronyaRotationMult)
    print('Robin: ',RobinRotationDuration)
    print('Gallagher: ',GallagherRotationDuration * GallagherRotationMult)

    # Scale other character's rotation
    BronyaRotation = [x * FeixiaoRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    RobinRotation = [x * FeixiaoRotationDuration / RobinRotationDuration for x in RobinRotation]
    GallagherRotation = [x * FeixiaoRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    RobinRotationGallagher = [x * FeixiaoRotationDuration / GallagherRotationDuration for x in RobinRotationGallagher]
    
    RobinRotation += RobinRotationFeixiao
    RobinRotation += RobinRotationGallagher
    totalRobinEffect = sumEffects(RobinRotation)

    FeixiaoEstimate = DefaultEstimator(f'Feixiao: {numBasicFeixiao:.1f}N {numSkillFeixiao:.1f}E {numFollowupFeixiao:.1f}T {numUltFeixiao:.1f}Q, S{FeixiaoCharacter.lightcone.superposition:d} {FeixiaoCharacter.lightcone.name} E{FeixiaoCharacter.eidolon:d}', FeixiaoRotation, FeixiaoCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    RobinEstimate = DefaultEstimator(f'{RobinCharacter.fullName()} {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q', 
                                    RobinRotation, RobinCharacter, config)
    GallagherEstimate = DefaultEstimator(f'{GallagherCharacter.fullName()} {numBasicGallagher:.0f}N {numSkillGallagher:.0f}E {numEnhancedGallagher:.0f}Enh 1Q', 
                                    GallagherRotation, GallagherCharacter, config)

    return([FeixiaoEstimate, BronyaEstimate, GallagherEstimate, RobinEstimate])

