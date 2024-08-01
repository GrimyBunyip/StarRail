from copy import deepcopy
from baseClasses.BaseEffect import sumEffects, BaseEffect
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.hunt.ImaginaryMarch import ImaginaryMarch
from characters.harmony.Robin import Robin
from characters.harmony.Bronya import Bronya
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.QuidProQuo import QuidProQuo
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.FlowingNightglow import FlowingNightglow
from lightCones.harmony.ForTomorrowsJourney import ForTomorrowsJourney
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc, MusketeerOfWildWheat4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc

def MarchBronyaRobinGallagher(config, 
                                robinEidolon:int=None, 
                                robinSuperposition:int=0):
    #%% March Bronya Robin Gallagher Characters
    BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'ER'],
                                    substats = {'CD': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                                    lightcone = DanceDanceDance(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = SprightlyVonwacq(),
                                    **config)

    MarchCharacter = ImaginaryMarch(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.imaginary'],
                                    substats = {'CR': 8, 'CD': 12, 'ATK.percent': 3, 'SPD.flat': 5}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = MusketeerOfWildWheat2pc(),
                                    relicsettwo = MusketeerOfWildWheat4pc(),
                                    planarset = RutilantArena(),
                                    master=BronyaCharacter,
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
                                    substats = {'BreakEffect': 10, 'SPD.flat': 9, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = QuidProQuo(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = ThiefOfShootingMeteor2pc(), planarset = SprightlyVonwacq(),
                                    **config)
    
    team = [MarchCharacter, BronyaCharacter, RobinCharacter, GallagherCharacter]

    #%% March Bronya Robin Gallagher Team Buffs
    if robinSuperposition >= 1:
        for character in team:
            character.addStat('DMG',description='Flowing Nightglow',amount=0.36+0.12*robinSuperposition,uptime=RobinUltUptime)
        
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    BronyaCharacter.applySkillBuff(GallagherCharacter,uptime=2.0/5.0)
    BronyaCharacter.applyUltBuff(RobinCharacter,uptime=1.0)
    for character in [MarchCharacter, GallagherCharacter, BronyaCharacter]:
        BronyaCharacter.applyUltBuff(character,uptime=2.0/3.0)
    
    # March Buff
    MarchCharacter.applySkillBuff(GallagherCharacter)
    MarchCharacter.applyTalentBuff(GallagherCharacter,uptime=1.0)
    
    # Gallagher Buffs
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=3.0)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinCharacter.applyUltBuff([MarchCharacter,BronyaCharacter,GallagherCharacter],uptime=RobinUltUptime)

    #%% Print Statements
    for character in team:
        character.print()

    #%% March Bronya Robin Gallagher Rotations
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
    
    numBasicMarch = 2.0
    numFollowupMarch = numBasicMarch
    numEnhancedMarch = 1.0
    
    MarchRotation = []
    MarchRotation += [MarchCharacter.useBasic() * numBasicMarch]
    MarchRotation += [MarchCharacter.useFollowup() * numFollowupMarch]
    MarchRotation += [MarchCharacter.useEnhancedBasic(actionValue=0.0, numHits=5.0, chance=0.8) * numEnhancedMarch]
    MarchRotation += [MarchCharacter.useUltimate()] 
    MarchRotation += [DanceDanceDanceEffect * numBasicMarch / 3.0]

    RobinRotationMarch = [RobinCharacter.useTalent() * (2.0 * numBasicMarch + numEnhancedMarch + 1.0)]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['basic']) * numBasicMarch * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['basic','enhancedBasic']) * numEnhancedMarch * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['ultimate']) * RobinUltUptime]
    RobinRotationMarch += [RobinCharacter.useConcertoDamage(['followup']) * numFollowupMarch * RobinUltUptime]

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
    
    # assume 2 procs go to robin, then other 2 split between the rest
    QPQEffect = BaseEffect()
    QPQEffect.energy = 16.0
    GallagherCharacter.addDebugInfo(QPQEffect,['buff'],'Quid Pro Quo Energy')
    MarchRotation.append(deepcopy(QPQEffect) * MarchCharacter.getER() )
    RobinRotation.append(deepcopy(QPQEffect) * 2 * RobinCharacter.getER() )
    BronyaRotation.append(deepcopy(QPQEffect) * BronyaCharacter.getER() )

    #%% March Bronya Robin Gallagher Rotation Math

    totalRobinEffect = sumEffects(RobinRotation)
    totalMarchEffect = sumEffects(MarchRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)
    
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    MarchRotationMult = 1.5
    BronyaRotationMult = 1.0
    GallagherRotationMult = 1.25

    MarchThreeTurns = MarchRotationDuration * MarchRotationMult
    BronyaThreeTurns = BronyaRotationDuration * BronyaRotationMult
    GallagherThreeTurns = GallagherRotationDuration * GallagherRotationMult
    
    MarchRotation += [RobinCharacter.useAdvanceForward() * (MarchThreeTurns - RobinRotationDuration) * MarchCharacter.getTotalStat('SPD') / 100 / MarchRotationMult]
    BronyaRotation += [RobinCharacter.useAdvanceForward() * (BronyaThreeTurns - RobinRotationDuration) * BronyaCharacter.getTotalStat('SPD') / 100 / BronyaRotationMult]
    GallagherRotation += [RobinCharacter.useAdvanceForward() * (GallagherThreeTurns - RobinRotationDuration) * GallagherCharacter.getTotalStat('SPD') / 100 / GallagherRotationMult]
        
    totalMarchEffect = sumEffects(MarchRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)
    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')
    
    print('##### Rotation Durations #####')
    print('March: ',MarchRotationDuration * MarchRotationMult)
    print('Bronya: ',BronyaRotationDuration * BronyaRotationMult)
    print('Robin: ',RobinRotationDuration)
    print('Gallagher: ',GallagherRotationDuration * GallagherRotationMult)

    # Scale other character's rotation
    BronyaRotation = [x * MarchRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    RobinRotation = [x * MarchRotationDuration / RobinRotationDuration for x in RobinRotation]
    GallagherRotation = [x * MarchRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    RobinRotationGallagher = [x * MarchRotationDuration / GallagherRotationDuration for x in RobinRotationGallagher]
    
    RobinRotation += RobinRotationMarch
    RobinRotation += RobinRotationGallagher
    totalRobinEffect = sumEffects(RobinRotation)

    MarchEstimate = DefaultEstimator(f'March: {numBasicMarch:.1f}N {numEnhancedMarch:.1f}Enh 1Q', MarchRotation, MarchCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    RobinEstimate = DefaultEstimator(f'{RobinCharacter.fullName()} {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q', 
                                    RobinRotation, RobinCharacter, config)
    GallagherEstimate = DefaultEstimator(f'Gallagher: {numBasicGallagher:.0f}N {numSkillGallagher:.0f}E {numEnhancedGallagher:.0f}Enh 1Q, S{GallagherCharacter.lightcone.superposition:d} {GallagherCharacter.lightcone.name}', 
                                    GallagherRotation, GallagherCharacter, config)

    return([MarchEstimate, BronyaEstimate, GallagherEstimate, RobinEstimate])

