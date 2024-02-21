from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Fuxuan import Fuxuan
from characters.nihility.Acheron import Acheron
from characters.nihility.Pela import Pela
from characters.harmony.Asta import Asta
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc

def AcheronE2AstaPelaFuxuan(config):
    #%% Acheron Asta Pela Fuxuan Characters
    originalFivestarEidolons = config['fivestarEidolons']
    config['fivestarEidolons'] = 2
    AcheronCharacter = Acheron(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.lightning'],
                            substats = {'CR': 4, 'CD': 12, 'ATK.percent': 9, 'ATK.flat': 3}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Pioneer2pc(), relicsettwo = Pioneer4pc(),
                            planarset = IzumoGenseiAndTakamaDivineRealm(),
                            **config)
    config['fivestarEidolons'] = originalFivestarEidolons

    AstaCharacter = Asta(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'HP.percent'],
                            substats = {'EHR': 8, 'SPD.flat': 12, 'HP.percent': 3, 'ATK.percent': 5}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(uptime=0.5), planarset = SprightlyVonwacq(),
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
    
    team = [AcheronCharacter, AstaCharacter, PelaCharacter, FuxuanCharacter]

    #%% Acheron Asta Pela Fuxuan Team Buffs
    for character in [AstaCharacter, AcheronCharacter, PelaCharacter]:
        character.addStat('CD',description='Broken Keel from Fuxuan',amount=0.1)
    for character in [AstaCharacter, AcheronCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel from Pela',amount=0.1)

    # Pela Debuffs, 3 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotationDuration=2)
        
    # Resolution Shines as Pearls of Sweat uptime
    sweatUptime = (1.0 / 2.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
    sweatUptime += (1.0 / 2.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
    sweatUptime = min(1.0, sweatUptime)
    for character in [AcheronCharacter, AstaCharacter, PelaCharacter, FuxuanCharacter]:
        character.addStat('DefShred',description='Resolution Sweat',
                        amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                        uptime=sweatUptime)
    # Asta Messenger 4 pc
    for character in [AcheronCharacter, PelaCharacter, FuxuanCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)

    # Asta Buffs
    AstaCharacter.applyChargingBuff(team)
    AstaCharacter.applyTraceBuff(team)
    AstaCharacter.applyUltBuff(team,rotation=3.0)

    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)        
    #%% Print Statements
    for character in team:
        character.print()

    #%% Acheron Asta Pela Fuxuan Rotations
    
    numStacks = 1 + 1 # Assume Acheron generates 1 stack when she skills, plus 1 from E2
    numStacks += (3 / 2) * PelaCharacter.getTotalStat('SPD') / AcheronCharacter.getTotalStat('SPD') # 3 pela attacks per 2 turn wolf rotation
    numStacks += AstaCharacter.getTotalStat('SPD') / AcheronCharacter.getTotalStat('SPD') # 1 asta stack per attack
    
    numSkillAcheron = 9.0 / numStacks
    print(f"{numStacks * AcheronCharacter.getTotalStat('SPD'):.2f} stack rate")

    AcheronRotation = [ 
            AcheronCharacter.useSkill() * numSkillAcheron,
            AcheronCharacter.useUltimate_st() * 3,
            AcheronCharacter.useUltimate_aoe(num_stacks=3.0) * 3.0,
            AcheronCharacter.useUltimate_end(),
    ]

    numBasicPela = 1.0
    numSkillPela = 1.0
    PelaRotation = [PelaCharacter.useBasic() * numBasicPela,
                    PelaCharacter.useSkill() * numSkillPela,
                    PelaCharacter.useUltimate(),]

    numBasicAsta = 3.0
    numSkillAsta = 0.0
    AstaRotation = [AstaCharacter.useBasic() * numBasicAsta,
                    AstaCharacter.useSkill() * numSkillAsta,
                    AstaCharacter.useUltimate() * 1,]

    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% Acheron Asta Pela Fuxuan Rotation Math

    totalAcheronEffect = sumEffects(AcheronRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalAstaEffect = sumEffects(AstaRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    AcheronRotationDuration = totalAcheronEffect.actionvalue * 100.0 / AcheronCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    AstaRotationDuration = totalAstaEffect.actionvalue * 100.0 / AstaCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Acheron: ',AcheronRotationDuration)
    print('Pela: ',PelaRotationDuration)
    print('Asta: ',AstaRotationDuration)
    print('Fuxuan: ',FuxuanRotationDuration)

    # Scale other character's rotation
    PelaRotation = [x * AcheronRotationDuration / PelaRotationDuration for x in PelaRotation]
    AstaRotation = [x * AcheronRotationDuration / AstaRotationDuration for x in AstaRotation]
    FuxuanRotation = [x * AcheronRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    AcheronEstimate = DefaultEstimator(f'Acheron E{AcheronCharacter.eidolon:d} S{AcheronCharacter.lightcone.superposition:d} {AcheronCharacter.lightcone.shortname}: {numSkillAcheron:.1f}E 1Q', AcheronRotation, AcheronCharacter, config)
    PelaEstimate = DefaultEstimator(f'Pela: 1 kill {numBasicPela:.0f}N {numSkillPela:.0f}E 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    AstaEstimate = DefaultEstimator(f'Asta vs fire weak {numSkillAsta:.1f}E {numBasicAsta:.1f}N S{AstaCharacter.lightcone.superposition:.0f} {AstaCharacter.lightcone.name}, 12 Spd Substats', 
                                    AstaRotation, AstaCharacter, config)
    FuxuanEstimate = DefaultEstimator('Fuxuan: 2N 1E 1Q, S{:.0f} {}'.format(FuxuanCharacter.lightcone.superposition, FuxuanCharacter.lightcone.name),
                                    FuxuanRotation, FuxuanCharacter, config)

    return([AcheronEstimate, AstaEstimate, PelaEstimate, FuxuanEstimate])