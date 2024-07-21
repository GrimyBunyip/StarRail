from copy import deepcopy
from baseClasses.BaseEffect import sumEffects, BaseEffect
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.hunt.ImaginaryMarch import ImaginaryMarch
from characters.harmony.Robin import Robin
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.QuidProQuo import QuidProQuo
from lightCones.harmony.PoisedToBloom import PoisedToBloom
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.DestinysThreadsForewoven import DestinysThreadsForewoven
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.KnightOfPurityPalace import KnightOfPurityPalace2pc, KnightOfPurityPalace4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc, MusketeerOfWildWheat4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def MarchTopazE2RobinGallagher(config):
    #%% March Topaz Robin Gallagher Characters
    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                                    substats = {'CR': 12, 'CD': 5, 'ATK.percent': 3, 'SPD.flat': 8}),
                                    lightcone = Swordplay(**config), 
                                    relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    **config)

    MarchCharacter = ImaginaryMarch(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.imaginary'],
                                    substats = {'CR': 5, 'CD': 12, 'ATK.percent': 4, 'SPD.flat': 7}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = MusketeerOfWildWheat2pc(),
                                    relicsettwo = MusketeerOfWildWheat4pc(),
                                    planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    master=TopazCharacter,
                                    **config)
    
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 12, 'ATK.flat': 8, 'RES': 5, 'SPD.flat': 3}),
                                    lightcone = PoisedToBloom(**config),
                                    relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                                    eidolon=2,
                                    **config)

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                                    substats = {'BreakEffect': 6, 'SPD.flat': 13, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = QuidProQuo(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = ThiefOfShootingMeteor2pc(), planarset = ForgeOfTheKalpagniLantern(),
                                    **config)
    
    team = [MarchCharacter, TopazCharacter, RobinCharacter, GallagherCharacter]

    #%% March Topaz Robin Gallagher Team Buffs
    for character in [TopazCharacter, MarchCharacter]:
        character.addStat('CD',description='Poised to Bloom',amount=0.12+0.04*RobinCharacter.lightcone.superposition)

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff(team,uptime=1.0)
    
    # March Buff
    MarchCharacter.applySkillBuff(TopazCharacter)
    MarchCharacter.applyTalentBuff(TopazCharacter,uptime=1.0)
    
    # Gallagher Buffs
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=3.0)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinUltUptime = 1.0 # assume better robin ult uptime because of shorter robin rotation
    RobinCharacter.applyUltBuff([MarchCharacter,TopazCharacter,GallagherCharacter],uptime=RobinUltUptime)

    #%% Print Statements
    for character in team:
        character.print()

    #%% March Topaz Robin Gallagher Rotations
    # assume 154 ish spd March and topaz, March slower than Topaz, and 134 ish spd robin
    
    numBasicRobin = 0.0
    numSkillRobin = 1.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0) # apply robin buff after we calculate damage for her basics

    numBasicTopaz = 0.0
    numSkillTopaz = 3.0
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
    GallagherRotation.append(deepcopy(QPQEffect) * GallagherCharacter.getER() * 2 / 3)
    MarchRotation.append(deepcopy(QPQEffect) * MarchCharacter.getER() * 2 / 3)
    RobinRotation.append(deepcopy(QPQEffect) * 2 * RobinCharacter.getER())
    TopazRotation.append(deepcopy(QPQEffect) * TopazCharacter.getER() * 2 / 3)

    #%% March Topaz Robin Gallagher Rotation Math

    totalMarchEffect = sumEffects(MarchRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')    

    print('##### Rotation Durations #####')
    print('March: ',MarchRotationDuration)
    print('Topaz: ',TopazRotationDuration)
    print('Robin: ',RobinRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    TopazRotation = [x * MarchRotationDuration / TopazRotationDuration for x in TopazRotation]
    RobinRotationTopaz = [x * MarchRotationDuration / TopazRotationDuration for x in RobinRotationTopaz]
    RobinRotation = [x * MarchRotationDuration / RobinRotationDuration for x in RobinRotation]
    GallagherRotation = [x * MarchRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    RobinRotationGallagher = [x * MarchRotationDuration / GallagherRotationDuration for x in RobinRotationGallagher]
    
    RobinRotation += RobinRotationMarch
    RobinRotation += RobinRotationTopaz
    RobinRotation += RobinRotationGallagher
    totalRobinEffect = sumEffects(RobinRotation)

    MarchEstimate = DefaultEstimator(f'March: {numBasicMarch:.1f}N {numEnhancedMarch:.1f}Enh 1Q', MarchRotation, MarchCharacter, config)
    TopazEstimate = DefaultEstimator(f'Topaz: {TopazCharacter.lightcone.name} {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numTalentTopaz:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    RobinEstimate = DefaultEstimator(f'Robin: {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q, S{RobinCharacter.lightcone.superposition:d} {RobinCharacter.lightcone.name}', 
                                    RobinRotation, RobinCharacter, config)
    GallagherEstimate = DefaultEstimator(f'Gallagher: {numBasicGallagher:.0f}N {numSkillGallagher:.0f}E {numEnhancedGallagher:.0f}Enh 1Q, S{GallagherCharacter.lightcone.superposition:d} {GallagherCharacter.lightcone.name}', 
                                    GallagherRotation, GallagherCharacter, config)

    return([MarchEstimate, TopazEstimate, GallagherEstimate, RobinEstimate])

