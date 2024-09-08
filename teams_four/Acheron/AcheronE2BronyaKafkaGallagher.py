from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.nihility.Acheron import Acheron
from characters.nihility.Kafka import Kafka
from characters.harmony.Bronya import Bronya
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.nihility.AlongThePassingShore import AlongThePassingShore
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.PatienceIsAllYouNeed import PatienceIsAllYouNeed
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.LushakaTheSunkenSeas import LushakaTheSunkenSeas
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc
from relicSets.relicSets.SacerdosRelivedOrdeal import SacerdosRelivedOrdeal2pc, SacerdosRelivedOrdeal4pc

def AcheronE2BronyaKafkaGallagher(config, acheronSuperposition:int=0):
    #%% Acheron Bronya Kafka Gallagher Characters
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
    
    KafkaCharacter = Kafka(relicstats = RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.lightning'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'BreakEffect': 5, 'ATK.flat': 3}),
                        lightcone = PatienceIsAllYouNeed(**config),
                        relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(stacks=2), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                        substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = SacerdosRelivedOrdeal2pc(), planarset = LushakaTheSunkenSeas(),
                        **config)
    
    team = [AcheronCharacter, BronyaCharacter, KafkaCharacter, GallagherCharacter]

    #%% Acheron Bronya Kafka Gallagher Team Buffs
        
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    BronyaCharacter.applyUltBuff(AcheronCharacter,uptime=0.25) # only get Bronya ult buff every 4 bronya turns
    BronyaCharacter.applyUltBuff(KafkaCharacter,uptime=0.5) # only get Bronya ult buff every 4 bronya turns
    BronyaCharacter.applyUltBuff(GallagherCharacter,uptime=0.5) # only get Bronya ult buff every 4 bronya turns
    AcheronCharacter.addStat('CD',description='Sacerdos Bronya',amount=0.2)
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)
      
    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
    for character in team:
        character.print()

    #%% Acheron Bronya Kafka Gallagher Rotations
    
    numStacks =  2 * KafkaCharacter.getTotalStat('SPD') # 2 stacks per kafka turn
    numStacks += 1.25 * (2/4) * GallagherCharacter.getTotalStat('SPD') # 1.25 from multiplication, 2 debuffs per 4 turn rotation
    numStacks *= 0.5 # halve the stacks from outside of Acheron because of Bronya
    numStacks /= BronyaCharacter.getTotalStat('SPD')
    numStacks += 1 + 1
    numStacks += 1 if AcheronCharacter.lightcone.name == 'Along the Passing Shore' else 0
    
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
    
    numBasicKafka = 4.0
    numSkillKafka = 0.0
    numTalentKafka = numBasicKafka + numSkillKafka
    numUltKafka = 1.0
    extraDots = []
    extraDotsUlt = []
    KafkaRotation = [
            KafkaCharacter.useBasic() * numBasicKafka,
            KafkaCharacter.useSkill(extraDots=extraDots) * numSkillKafka,
            KafkaCharacter.useTalent() * numTalentKafka,
            KafkaCharacter.useUltimate(extraDots=extraDotsUlt) * numUltKafka,
    ]

    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    numBasicGallagher = 4.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1,]
    if GallagherCharacter.lightcone.name == 'Multiplication':
        GallagherRotation[-1].actionvalue += 0.20 # advance foward cannot exceed a certain amount

    #%% Acheron Bronya Kafka Gallagher Rotation Math
    numDotKafka = DotEstimator(KafkaRotation, KafkaCharacter, config, dotMode='alwaysAll')
    numDotKafka = min(numDotKafka, 2 * numUltKafka * KafkaCharacter.numEnemies + 2 * numTalentKafka)

    totalAcheronEffect = sumEffects(AcheronRotation)
    totalKafkaEffect = sumEffects(KafkaRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    AcheronRotationDuration = totalAcheronEffect.actionvalue * 100.0 / AcheronCharacter.getTotalStat('SPD')
    KafkaRotationDuration = totalKafkaEffect.actionvalue * 100.0 / KafkaCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Acheron: ',AcheronRotationDuration)
    print('Kafka: ',KafkaRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    KafkaRotation = [x * AcheronRotationDuration / KafkaRotationDuration for x in KafkaRotation]
    BronyaRotation = [x * AcheronRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    GallagherRotation = [x * AcheronRotationDuration / GallagherRotationDuration for x in GallagherRotation]

    AcheronEstimate = DefaultEstimator(f'Acheron E{AcheronCharacter.eidolon:d} S{AcheronCharacter.lightcone.superposition:d} {AcheronCharacter.lightcone.shortname}: {numSkillAcheron:.1f}E 1Q', AcheronRotation, AcheronCharacter, config)
    KafkaEstimate = DefaultEstimator(f'Kafka {numBasicKafka:.0f}N {numSkillKafka:.0f}E {numTalentKafka:.0f}T {numUltKafka:.0f}Q {numDotKafka:.1f}Dot, {KafkaCharacter.lightcone.name} S{KafkaCharacter.lightcone.superposition}',
                                    KafkaRotation, KafkaCharacter, config, numDot=numDotKafka)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    GallagherEstimate = DefaultEstimator(f'{GallagherCharacter.fullName()} {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q', 
                                    GallagherRotation, GallagherCharacter, config)

    return([AcheronEstimate, BronyaEstimate, KafkaEstimate, GallagherEstimate])