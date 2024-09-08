from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.nihility.Acheron import Acheron
from characters.nihility.Pela import Pela
from characters.harmony.Bronya import Bronya
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.nihility.AlongThePassingShore import AlongThePassingShore
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.LushakaTheSunkenSeas import LushakaTheSunkenSeas
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc
from relicSets.relicSets.SacerdosRelivedOrdeal import SacerdosRelivedOrdeal2pc, SacerdosRelivedOrdeal4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def AcheronE2BronyaPelaGallagher(config, acheronSuperposition:int=0):
    #%% Acheron Bronya Pela Gallagher Characters
    acheronLightCone = GoodNightAndSleepWell(**config) if acheronSuperposition == 0 else AlongThePassingShore(superposition=acheronSuperposition,**config)
    AcheronCharacter = Acheron(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'ATK.percent'],
                            substats = {'CR': 8, 'CD': 6, 'ATK.percent': 3, 'SPD.flat': 11}),
                            lightcone = acheronLightCone,
                            relicsetone = Pioneer2pc(), relicsettwo = Pioneer4pc(),
                            planarset = IzumoGenseiAndTakamaDivineRealm(),
                            eidolon=2,
                            **config)
    
    BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'HP.percent', 'CD', 'ER'],
                        substats = {'CD': 12, 'SPD.flat': 8, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = PastAndFuture(**config),
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = BrokenKeel(),
                        **config)

    PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                            substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
                            lightcone = ResolutionShinesAsPearlsOfSweat(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
                            **config)

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                            substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                            lightcone = Multiplication(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = SacerdosRelivedOrdeal2pc(), planarset = LushakaTheSunkenSeas(),
                            **config)
    
    team = [AcheronCharacter, BronyaCharacter, PelaCharacter, GallagherCharacter]

    #%% Acheron Bronya Pela Gallagher Team Buffs
    for character in [BronyaCharacter, AcheronCharacter, GallagherCharacter]:
        character.addStat('CD',description='Broken Keel from Pela',amount=0.1)
    for character in [PelaCharacter, AcheronCharacter, GallagherCharacter]:
        character.addStat('CD',description='Broken Keel from Bronya',amount=0.1)

    # Pela Debuffs, 3 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotationDuration=3)
        
    # Resolution Shines as Pearls of Sweat uptime
    sweatUptime = (1.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
    sweatUptime += (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
    sweatUptime = min(1.0, sweatUptime)
    for character in [AcheronCharacter, BronyaCharacter, PelaCharacter, GallagherCharacter]:
        character.addStat('DefShred',description='Resolution Sweat',
                        amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                        uptime=sweatUptime)
        
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    BronyaCharacter.applyUltBuff(AcheronCharacter,uptime=0.25) # only get Bronya ult buff every 4 bronya turns
    BronyaCharacter.applyUltBuff(PelaCharacter,uptime=0.5) # only get Bronya ult buff every 4 bronya turns
    BronyaCharacter.applyUltBuff(GallagherCharacter,uptime=0.5) # only get Bronya ult buff every 4 bronya turns
    AcheronCharacter.addStat('CD',description='Sacerdos Bronya',amount=0.2)
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)
    AcheronCharacter.addStat('ATK.percent',description='Lushaka Gallagher',amount=0.12)
      
    #%% Print Statements
    for character in team:
        character.print()

    #%% Acheron Bronya Pela Gallagher Rotations
    
    numStacks =  (4/3) * PelaCharacter.getTotalStat('SPD') # 4 stacks per 3 basics
    numStacks += 1.25 * (2/4) * GallagherCharacter.getTotalStat('SPD') # 1.25 from multiplication, 2 debuffs per 4 turn rotation
    numStacks *= 0.5 # halve the stacks from outside of Acheron because of Bronya
    numStacks /= BronyaCharacter.getTotalStat('SPD')
    numStacks += 1 + 1 # Assume Acheron generates 1 stack when she skills, plus 1 from E2 
    
    numSkillAcheron = 9.0 / numStacks
    print(f"{numStacks * AcheronCharacter.getTotalStat('SPD'):.2f} stack rate")

    AcheronRotation = []

    AcheronRotation += [AcheronCharacter.useSkill() * numSkillAcheron * 0.5] # half of acheron skills will not be bronya buffed
    
    BronyaCharacter.applySkillBuff(AcheronCharacter,uptime=1.0)
    AcheronCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition)
    AcheronRotation += [AcheronCharacter.useSkill() * numSkillAcheron * 0.5]
    AcheronRotation += [AcheronCharacter.useUltimate_st() * 3]
    AcheronRotation += [AcheronCharacter.useUltimate_aoe(num_stacks=3.0) * 3.0]
    AcheronRotation += [AcheronCharacter.useUltimate_end()]
    AcheronRotation += [BronyaCharacter.useAdvanceForward() * numSkillAcheron * 0.5] # Half of the turns

    numBasicPela = 3.0
    PelaRotation = [PelaCharacter.useBasic() * numBasicPela,
                    PelaCharacter.useUltimate(),]

    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    numBasicGallagher = 4.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1,]
    if GallagherCharacter.lightcone.name == 'Multiplication':
        GallagherRotation[-1].actionvalue += 0.20 # advance foward cannot exceed a certain amount

    #%% Acheron Bronya Pela Gallagher Rotation Math

    totalAcheronEffect = sumEffects(AcheronRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    AcheronRotationDuration = totalAcheronEffect.actionvalue * 100.0 / AcheronCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Acheron: ',AcheronRotationDuration)
    print('Pela: ',PelaRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    PelaRotation = [x * AcheronRotationDuration / PelaRotationDuration for x in PelaRotation]
    BronyaRotation = [x * AcheronRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    GallagherRotation = [x * AcheronRotationDuration / GallagherRotationDuration for x in GallagherRotation]

    AcheronEstimate = DefaultEstimator(f'Acheron E{AcheronCharacter.eidolon:d} S{AcheronCharacter.lightcone.superposition:d} {AcheronCharacter.lightcone.shortname}: {numSkillAcheron:.1f}E 1Q', AcheronRotation, AcheronCharacter, config)
    PelaEstimate = DefaultEstimator(f'Pela: 3N 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    GallagherEstimate = DefaultEstimator(f'{GallagherCharacter.fullName()} {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q', 
                                    GallagherRotation, GallagherCharacter, config)

    return([AcheronEstimate, BronyaEstimate, PelaEstimate, GallagherEstimate])