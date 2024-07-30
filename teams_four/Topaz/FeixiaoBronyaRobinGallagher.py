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
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc, MusketeerOfWildWheat4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def FeixiaoBronyaRobinGallagher(config, robinSuperposition:int=0):
    #%% Feixiao Bronya Robin Gallagher Characters
    BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'ER'],
                                    substats = {'CD': 12, 'SPD.flat': 5, 'HP.percent': 8, 'DEF.percent': 3}),
                                    lightcone = DanceDanceDance(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = SprightlyVonwacq(),
                                    **config)

    FeixiaoCharacter = Feixiao(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CD', 'DMG.wind'],
                                    substats = {'CR': 12, 'CD': 9, 'ATK.percent': 3, 'SPD.flat': 4}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = WindSoaringValorous2pc(),
                                    relicsettwo = WindSoaringValorous4pc(),
                                    planarset = InertSalsotto(),
                                    **config)
    
    RobinUltUptime = 1.0 # assume better robin ult uptime because of shorter robin rotation
    robinLightCone = FlowingNightglow(superposition=robinSuperposition,uptime=RobinUltUptime,**config) if robinSuperposition >= 1 else ForTomorrowsJourney(**config)
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 12, 'ATK.flat': 8, 'RES': 5, 'SPD.flat': 3}),
                                    lightcone = robinLightCone,
                                    relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                                    eidolon=2,
                                    **config)

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                                    substats = {'BreakEffect': 12, 'SPD.flat': 6, 'HP.percent': 4, 'RES': 6}),
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
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,
                    BronyaCharacter.useAdvanceForward(),]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0) # apply robin buff after we calculate damage for her basics

    DanceDanceDanceEffect = BaseEffect()
    DanceDanceDanceEffect.actionvalue = -0.24
    numBasicBronya = 0.0
    numSkillBronya = 3.0
    BronyaRotation = [ # 130 max energy
            BronyaCharacter.useBasic() * numBasicBronya,
            BronyaCharacter.useSkill() * numSkillBronya,
            BronyaCharacter.useUltimate(),
            DanceDanceDanceEffect,
            RobinCharacter.useAdvanceForward(),
    ]
    
    # number of attacks in a 3 turn robin rotation
    numAttacks = 6.0 # feixiao actions + followups
    numAttacks += 5.0 # gallagher turns
    numAttacks += 1.25 * 2 # gallagher ultimates
    
    numBasicFeixiao = 1.0
    numSkillFeixiao = 2.0
    numFollowupFeixiao = (numBasicFeixiao + numSkillFeixiao)
    numUltFeixiao = numAttacks / 2.0
    
    FeixiaoRotation = []
    FeixiaoRotation += [FeixiaoCharacter.useBasic() * numBasicFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useSkill() * numSkillFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useTalent() * numFollowupFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useUltimate() * numUltFeixiao] 
    FeixiaoRotation += [DanceDanceDanceEffect * (numBasicFeixiao + numSkillFeixiao) / 3.0]

    RobinRotationFeixiao = [RobinCharacter.useTalent() * (numBasicFeixiao + numSkillFeixiao + numFollowupFeixiao + 1.0)]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['basic']) * numBasicFeixiao * RobinUltUptime]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['skill']) * numSkillFeixiao * RobinUltUptime]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['followup']) * numFollowupFeixiao * RobinUltUptime]
    RobinRotationFeixiao += [RobinCharacter.useConcertoDamage(['ultimate','followup']) * RobinUltUptime]
    FeixiaoRotation += [RobinCharacter.useAdvanceForward() * (numBasicFeixiao + numSkillFeixiao) / 3.0] 

    numBasicGallagher = 4.0
    numSkillGallagher = 0.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useSkill() * numSkillGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1,]

    RobinRotationGallagher = [RobinCharacter.useTalent() * (numBasicGallagher + numEnhancedGallagher + 1.0)]
    RobinRotationGallagher += [RobinCharacter.useConcertoDamage(['basic']) * (numBasicGallagher + numEnhancedGallagher) * RobinUltUptime]
    RobinRotationGallagher += [RobinCharacter.useConcertoDamage(['ultimate']) * 1.0 * RobinUltUptime]
    GallagherRotation += [RobinCharacter.useAdvanceForward() * (numBasicGallagher + numSkillGallagher) / 5.0]
    GallagherRotation += [DanceDanceDanceEffect * numBasicGallagher / 5.0]
    GallagherRotation += [BronyaCharacter.useAdvanceForward() * numBasicGallagher * 2.0 / 5.0]
    
    # assume 2 procs go to robin, then other 2 split between the rest
    QPQEffect = BaseEffect()
    QPQEffect.energy = 16.0
    GallagherCharacter.addDebugInfo(QPQEffect,['buff'],'Quid Pro Quo Energy')
    RobinRotation.append(deepcopy(QPQEffect) * 2 * RobinCharacter.getER() )
    BronyaRotation.append(deepcopy(QPQEffect) * BronyaCharacter.getER() )

    #%% Feixiao Bronya Robin Gallagher Rotation Math

    totalFeixiaoEffect = sumEffects(FeixiaoRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    FeixiaoRotationDuration = totalFeixiaoEffect.actionvalue * 100.0 / FeixiaoCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')    

    print('##### Rotation Durations #####')
    print('Feixiao: ',FeixiaoRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Robin: ',RobinRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    BronyaRotation = [x * FeixiaoRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    RobinRotation = [x * FeixiaoRotationDuration / RobinRotationDuration for x in RobinRotation]
    GallagherRotation = [x * FeixiaoRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    RobinRotationGallagher = [x * FeixiaoRotationDuration / GallagherRotationDuration for x in RobinRotationGallagher]
    
    RobinRotation += RobinRotationFeixiao
    RobinRotation += RobinRotationGallagher
    totalRobinEffect = sumEffects(RobinRotation)

    FeixiaoEstimate = DefaultEstimator(f'Feixiao: {numBasicFeixiao:.1f}N {numSkillFeixiao:.1f}E {numFollowupFeixiao:.1f}T {numUltFeixiao:.1f}Q, S{FeixiaoCharacter.lightcone.superposition:d} {FeixiaoCharacter.lightcone.name}', FeixiaoRotation, FeixiaoCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    RobinEstimate = DefaultEstimator(f'Robin: {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q, S{RobinCharacter.lightcone.superposition:d} {RobinCharacter.lightcone.name}', 
                                    RobinRotation, RobinCharacter, config)
    GallagherEstimate = DefaultEstimator(f'Gallagher: {numBasicGallagher:.0f}N {numSkillGallagher:.0f}E {numEnhancedGallagher:.0f}Enh 1Q, S{GallagherCharacter.lightcone.superposition:d} {GallagherCharacter.lightcone.name}', 
                                    GallagherRotation, GallagherCharacter, config)

    return([FeixiaoEstimate, BronyaEstimate, GallagherEstimate, RobinEstimate])

