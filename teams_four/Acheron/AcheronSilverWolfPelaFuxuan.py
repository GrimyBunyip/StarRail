from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Fuxuan import Fuxuan
from characters.nihility.Acheron import Acheron
from characters.nihility.Pela import Pela
from characters.nihility.SilverWolf import SilverWolf
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def AcheronSilverWolfPelaFuxuan(config):
    #%% Acheron Silver Wolf Pela Fuxuan Characters
    AcheronCharacter = Acheron(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'ATK.percent'],
                            substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Pioneer2pc(), relicsettwo = Pioneer4pc(),
                            planarset = IzumoGenseiAndTakamaDivineRealm(),
                            **config)

    SilverWolfCharacter = SilverWolf(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'BreakEffect'],
                            substats = {'SPD.flat':12,'BreakEffect':8, 'ATK.percent': 5, 'ATK.flat': 3}),
                            lightcone = BeforeTheTutorialMissionStarts(**config),
                            relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                            **config)

    PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                            substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
                            lightcone = ResolutionShinesAsPearlsOfSweat(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
                            **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                        lightcone = DayOneOfMyNewLife(**config),
                        relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [AcheronCharacter, SilverWolfCharacter, PelaCharacter, FuxuanCharacter]

    #%% Acheron Silver Wolf Pela Fuxuan Team Buffs
    for character in [SilverWolfCharacter, AcheronCharacter, PelaCharacter]:
        character.addStat('CD',description='Broken Keel from Fuxuan',amount=0.1)
    for character in [SilverWolfCharacter, AcheronCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel from Pela',amount=0.1)

    # Pela Debuffs, 3 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotationDuration=3)
        
    # Resolution Shines as Pearls of Sweat uptime
    sweatUptime = (1.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
    sweatUptime += (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
    sweatUptime = min(1.0, sweatUptime)
    for character in [AcheronCharacter, SilverWolfCharacter, PelaCharacter, FuxuanCharacter]:
        character.addStat('DefShred',description='Resolution Sweat',
                        amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                        uptime=sweatUptime)

    # Silver Wolf Debuffs
    SilverWolfCharacter.applyDebuffs([SilverWolfCharacter, FuxuanCharacter])
    SilverWolfCharacter.applyDebuffs([AcheronCharacter, PelaCharacter],targetingUptime=1.0/AcheronCharacter.numEnemies) # Acheron and pela won't consistently target the debuffed enemy

    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)        
    #%% Print Statements
    for character in team:
        character.print()

    #%% Acheron Silver Wolf Pela Fuxuan Rotations
    
    numStacks = 1 # Assume Acheron generates 1 stack when she skills
    numStacks += (3 / 2) * SilverWolfCharacter.getTotalStat('SPD') / AcheronCharacter.getTotalStat('SPD') # 3 silver wolf attacks per 2 turn wolf rotation
    numStacks +=  (4 / 3) * PelaCharacter.getTotalStat('SPD') / AcheronCharacter.getTotalStat('SPD') # 4 pela attacks per 3 turn wolf rotation
    
    numSkillAcheron = 9.0 / numStacks
    print(f"{numStacks * AcheronCharacter.getTotalStat('SPD'):.2f} stack rate")

    AcheronRotation = [ 
            AcheronCharacter.useSkill() * numSkillAcheron,
            AcheronCharacter.useUltimate_st() * 3,
            AcheronCharacter.useUltimate_aoe(num_stacks=3.0) * 3.0,
            AcheronCharacter.useUltimate_end(),
    ]

    numBasicSW = 0.0
    numSkillSW = 2.0
    numUltSW = 1
    SilverWolfRotation = [ # 
            SilverWolfCharacter.useBasic() * numBasicSW, #
            SilverWolfCharacter.useSkill() * numSkillSW, #
            SilverWolfCharacter.useUltimate() * numUltSW, #
    ]

    numBasicPela = 3.0
    PelaRotation = [PelaCharacter.useBasic() * numBasicPela,
                    PelaCharacter.useUltimate(),]

    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% Acheron Silver Wolf Pela Fuxuan Rotation Math

    totalAcheronEffect = sumEffects(AcheronRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalSilverWolfEffect = sumEffects(SilverWolfRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    AcheronRotationDuration = totalAcheronEffect.actionvalue * 100.0 / AcheronCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    SilverWolfRotationDuration = totalSilverWolfEffect.actionvalue * 100.0 / SilverWolfCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Acheron: ',AcheronRotationDuration)
    print('Pela: ',PelaRotationDuration)
    print('SilverWolf: ',SilverWolfRotationDuration)
    print('Fuxuan: ',FuxuanRotationDuration)

    # Scale other character's rotation
    PelaRotation = [x * AcheronRotationDuration / PelaRotationDuration for x in PelaRotation]
    SilverWolfRotation = [x * AcheronRotationDuration / SilverWolfRotationDuration for x in SilverWolfRotation]
    FuxuanRotation = [x * AcheronRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    AcheronEstimate = DefaultEstimator(f'Acheron E{AcheronCharacter.eidolon:d} S{AcheronCharacter.lightcone.superposition:d} {AcheronCharacter.lightcone.shortname}: {numSkillAcheron:.1f}E 1Q', AcheronRotation, AcheronCharacter, config)
    PelaEstimate = DefaultEstimator(f'Pela: 3N 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    SilverWolfEstimate = DefaultEstimator(f'SilverWolf {numBasicSW:.0f}N {numSkillSW:.0f}E {numUltSW:.0f}Q', SilverWolfRotation, SilverWolfCharacter, config)
    FuxuanEstimate = DefaultEstimator('Fuxuan: 2N 1E 1Q, S{:.0f} {}'.format(FuxuanCharacter.lightcone.superposition, FuxuanCharacter.lightcone.name),
                                    FuxuanRotation, FuxuanCharacter, config)

    return([AcheronEstimate, SilverWolfEstimate, PelaEstimate, FuxuanEstimate])