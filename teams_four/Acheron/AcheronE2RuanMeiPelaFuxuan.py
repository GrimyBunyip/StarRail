from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Fuxuan import Fuxuan
from characters.nihility.Acheron import Acheron
from characters.nihility.Pela import Pela
from characters.harmony.RuanMei import RuanMei
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def AcheronE2RuanMeiPelaFuxuan(config):
    #%% Acheron Ruan Mei Pela Fuxuan Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                        substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                        **config)
    
    originalFivestarEidolons = config['fivestarEidolons']
    config['fivestarEidolons'] = 2
    AcheronCharacter = Acheron(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.lightning'],
                            substats = {'CR': 4, 'CD': 12, 'ATK.percent': 9, 'ATK.flat': 3}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Pioneer2pc(), relicsettwo = Pioneer4pc(),
                            planarset = IzumoGenseiAndTakamaDivineRealm(),
                            **config)
    config['fivestarEidolons'] = originalFivestarEidolons

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
    
    team = [AcheronCharacter, RuanMeiCharacter, PelaCharacter, FuxuanCharacter]

    #%% Acheron Ruan Mei Pela Fuxuan Team Buffs
    for character in [RuanMeiCharacter, AcheronCharacter, PelaCharacter]:
        character.addStat('CD',description='Broken Keel from Fuxuan',amount=0.1)
    for character in [RuanMeiCharacter, AcheronCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel from Pela',amount=0.1)

    # Pela Debuffs, 3 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotationDuration=2)
        
    # Resolution Shines as Pearls of Sweat uptime
    sweatUptime = (1.0 / 2.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
    sweatUptime += (1.0 / 2.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
    sweatUptime = min(1.0, sweatUptime)
    for character in [AcheronCharacter, RuanMeiCharacter, PelaCharacter, FuxuanCharacter]:
        character.addStat('DefShred',description='Resolution Sweat',
                        amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                        uptime=sweatUptime)
    # RuanMei Messenger 4 pc
    for character in [AcheronCharacter, PelaCharacter, FuxuanCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # RuanMei Buffs, 3 turn RuanMei rotation
    RuanMeiCharacter.applyWeaknessModifiers(team=team)
    RuanMeiCharacter.applyPassiveBuffs(team=team)
    RuanMeiCharacter.applySkillBuff(team=team,uptime=3.0/3.0)
    RuanMeiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)

    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)        
    #%% Print Statements
    for character in team:
        character.print()

    #%% Acheron Ruan Mei Pela Fuxuan Rotations
    
    numStacks = 1 + 1 # Assume Acheron generates 1 stack when she skills, plus 1 from E2
    numStacks += (3 / 2) * PelaCharacter.getTotalStat('SPD') / AcheronCharacter.getTotalStat('SPD') # 3 pela attacks per 2 turn wolf rotation
    numStacks += (2/3) * (2/3) * RuanMeiCharacter.getTotalStat('SPD') / AcheronCharacter.getTotalStat('SPD')
    numStacks += (2/3) * FuxuanCharacter.getTotalStat('SPD') / AcheronCharacter.getTotalStat('SPD')
    
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

    numBasicRuanMei = 2.0
    numSkillRuanMei = 1.0
    RuanMeiRotation = [RuanMeiCharacter.useBasic() * numBasicRuanMei,
                       RuanMeiCharacter.useSkill() * numSkillRuanMei,
                    RuanMeiCharacter.useUltimate()]

    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% Acheron Ruan Mei Pela Fuxuan Rotation Math

    totalAcheronEffect = sumEffects(AcheronRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    AcheronRotationDuration = totalAcheronEffect.actionvalue * 100.0 / AcheronCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Acheron: ',AcheronRotationDuration)
    print('Pela: ',PelaRotationDuration)
    print('RuanMei: ',RuanMeiRotationDuration)
    print('Fuxuan: ',FuxuanRotationDuration)

    # Scale other character's rotation
    PelaRotation = [x * AcheronRotationDuration / PelaRotationDuration for x in PelaRotation]
    RuanMeiRotation = [x * AcheronRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    FuxuanRotation = [x * AcheronRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    AcheronEstimate = DefaultEstimator(f'Acheron E{AcheronCharacter.eidolon:d} S{AcheronCharacter.lightcone.superposition:d} {AcheronCharacter.lightcone.shortname}: {numSkillAcheron:.1f}E 1Q', AcheronRotation, AcheronCharacter, config)
    PelaEstimate = DefaultEstimator(f'Pela: 1 kill {numBasicPela:.0f}N {numSkillPela:.0f}E 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'Ruan Mei: {numBasicRuanMei:.0f}N {numSkillRuanMei:.0f}E 1Q, S{RuanMeiCharacter.lightcone.superposition:d} {RuanMeiCharacter.lightcone.name}', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    FuxuanEstimate = DefaultEstimator('Fuxuan: 2N 1E 1Q, S{:.0f} {}'.format(FuxuanCharacter.lightcone.superposition, FuxuanCharacter.lightcone.name),
                                    FuxuanRotation, FuxuanCharacter, config)

    return([AcheronEstimate, RuanMeiEstimate, PelaEstimate, FuxuanEstimate])