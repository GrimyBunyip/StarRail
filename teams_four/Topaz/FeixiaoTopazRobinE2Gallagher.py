from copy import deepcopy
from baseClasses.BaseEffect import sumEffects, BaseEffect
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.hunt.Feixiao import Feixiao
from characters.harmony.Robin import Robin
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.QuidProQuo import QuidProQuo
from lightCones.harmony.FlowingNightglow import FlowingNightglow
from lightCones.harmony.PoisedToBloom import PoisedToBloom
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.Swordplay import Swordplay
from relicSets.planarSets.DuranDynastyOfRunningWolves import DuranDynastyOfRunningWolves
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc, MusketeerOfWildWheat4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def FeixiaoTopazRobinE2Gallagher(config, robinSuperposition:int=0):
    #%% Feixiao Topaz Robin Gallagher Characters
    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                                    substats = {'CR': 5, 'CD': 7, 'ATK.percent': 3, 'SPD.flat': 13}),
                                    lightcone = Swordplay(**config), 
                                    relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    **config)

    FeixiaoCharacter = Feixiao(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.wind'],
                                    substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = WindSoaringValorous2pc(),
                                    relicsettwo = WindSoaringValorous4pc(),
                                    planarset = DuranDynastyOfRunningWolves(),
                                    **config)
    
    RobinUltUptime = 1.0 # assume better robin ult uptime because of shorter robin rotation
    robinLightCone = FlowingNightglow(superposition=robinSuperposition,uptime=RobinUltUptime,**config) if robinSuperposition >= 1 else PoisedToBloom(**config)
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
    
    team = [FeixiaoCharacter, TopazCharacter, RobinCharacter, GallagherCharacter]

    #%% Feixiao Topaz Robin Gallagher Team Buffs
    if robinSuperposition == 0:
        for character in [TopazCharacter, FeixiaoCharacter]:
            character.addStat('CD',description='Poised to Bloom',amount=0.12+0.04*RobinCharacter.lightcone.superposition)
    if robinSuperposition >= 1:
        for character in team:
            character.addStat('DMG',description='Flowing Nightglow',amount=0.36+0.12*robinSuperposition,uptime=RobinUltUptime)

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff(team,uptime=1.0)
    
    # Gallagher Buffs
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=3.0)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinCharacter.applyUltBuff([FeixiaoCharacter,TopazCharacter,GallagherCharacter],uptime=RobinUltUptime)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Feixiao Topaz Robin Gallagher Rotations
    # assume 154 ish spd Feixiao and topaz, Feixiao slower than Topaz, and 134 ish spd robin
    
    numBasicRobin = 0.0
    numSkillRobin = 1.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0) # apply robin buff after we calculate damage for her basics

    numBasicTopaz = 2.0
    numSkillTopaz = 2.0
    numTalentTopaz = (numBasicTopaz + numSkillTopaz) * 1.0 + 1.0 # rough estimate
    TopazRotation = []
    TopazRotation += [TopazCharacter.useBasic() * numBasicTopaz]
    TopazRotation += [TopazCharacter.useSkill() * numSkillTopaz]
    TopazRotation += [TopazCharacter.useUltimate()]
    TopazRotation += [TopazCharacter.useTalent(windfall=True) * 2.0] # two talents from windfall
    TopazRotation += [TopazCharacter.useTalent(windfall=False) * (numTalentTopaz - 1.0)] # deducted windfall advances
    
    RobinRotationTopaz = [RobinCharacter.useTalent() * (numBasicTopaz + numSkillTopaz + numTalentTopaz + 2.0)]
    RobinRotationTopaz += [RobinCharacter.useConcertoDamage(['basic','followup']) * numBasicTopaz * RobinUltUptime]
    RobinRotationTopaz += [RobinCharacter.useConcertoDamage(['skill','followup']) * numSkillTopaz * RobinUltUptime]
    RobinRotationTopaz += [RobinCharacter.useConcertoDamage(['followup']) * numTalentTopaz * RobinUltUptime]
    TopazRotation += [RobinCharacter.useAdvanceForward() * (numSkillTopaz + numBasicTopaz) / 3.0]

    # number of attacks in a 3 turn robin rotation
    numTurns = 3.0
    numAttacks = numTurns * 2.0 # feixiao attacks
    numAttacks += numTurns * (1.0 + numTalentTopaz / (numBasicTopaz + numSkillTopaz))  # topaz attacks
    numAttacks += numTurns * (1.0 + 2.0 / 4.0) # gallagher attacks
    
    numBasicFeixiao = 1.0
    numSkillFeixiao = 2.0
    numFollowupFeixiao = (numBasicFeixiao + numSkillFeixiao)
    numUltFeixiao = numAttacks / 2.0
    
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
    FeixiaoRotation += [RobinCharacter.useAdvanceForward() * (numBasicFeixiao + numSkillFeixiao) / 3.0]

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
    RobinRotation.append(deepcopy(QPQEffect) * 2 * RobinCharacter.getER())
    TopazRotation.append(deepcopy(QPQEffect) * TopazCharacter.getER())

    #%% Feixiao Topaz Robin Gallagher Rotation Math

    totalFeixiaoEffect = sumEffects(FeixiaoRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    FeixiaoRotationDuration = totalFeixiaoEffect.actionvalue * 100.0 / FeixiaoCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')    

    print('##### Rotation Durations #####')
    print('Feixiao: ',FeixiaoRotationDuration)
    print('Topaz: ',TopazRotationDuration)
    print('Robin: ',RobinRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    TopazRotation = [x * FeixiaoRotationDuration / TopazRotationDuration for x in TopazRotation]
    RobinRotationTopaz = [x * FeixiaoRotationDuration / TopazRotationDuration for x in RobinRotationTopaz]
    RobinRotation = [x * FeixiaoRotationDuration / RobinRotationDuration for x in RobinRotation]
    GallagherRotation = [x * FeixiaoRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    RobinRotationGallagher = [x * FeixiaoRotationDuration / GallagherRotationDuration for x in RobinRotationGallagher]
    
    RobinRotation += RobinRotationFeixiao
    RobinRotation += RobinRotationTopaz
    RobinRotation += RobinRotationGallagher
    totalRobinEffect = sumEffects(RobinRotation)

    FeixiaoEstimate = DefaultEstimator(f'Feixiao: {numBasicFeixiao:.1f}N {numSkillFeixiao:.1f}E {numFollowupFeixiao:.1f}T {numUltFeixiao:.1f}Q, S{FeixiaoCharacter.lightcone.superposition:d} {FeixiaoCharacter.lightcone.name}', FeixiaoRotation, FeixiaoCharacter, config)
    TopazEstimate = DefaultEstimator(f'Topaz: {TopazCharacter.lightcone.name} {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numTalentTopaz:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    RobinEstimate = DefaultEstimator(f'Robin: {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q, S{RobinCharacter.lightcone.superposition:d} {RobinCharacter.lightcone.name}', 
                                    RobinRotation, RobinCharacter, config)
    GallagherEstimate = DefaultEstimator(f'Gallagher: {numBasicGallagher:.0f}N {numSkillGallagher:.0f}E {numEnhancedGallagher:.0f}Enh 1Q, S{GallagherCharacter.lightcone.superposition:d} {GallagherCharacter.lightcone.name}', 
                                    GallagherRotation, GallagherCharacter, config)

    return([FeixiaoEstimate, TopazEstimate, GallagherEstimate, RobinEstimate])

