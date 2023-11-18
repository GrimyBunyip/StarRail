from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Fuxuan import Fuxuan
from characters.destruction.Blade import Blade
from characters.harmony.Bronya import Bronya
from characters.nihility.Pela import Pela
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.destruction.ASecretVow import ASecretVow
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc

def BladeBronyaPelaFuxuan(config):
    #%% Blade Bronya Pela Fuxuan Characters
    BladeCharacter = Blade(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'HP.percent'],
                        substats = {'CR': 12, 'CD': 8, 'SPD.flat': 5, 'HP.percent': 3}),
                        lightcone = ASecretVow(uptime=1.0,**config),
                        relicsetone = LongevousDisciple2pc(), relicsettwo = LongevousDisciple4pc(), planarset = InertSalsotto(),
                        **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CD', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = PlanetaryRendezvous(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                        **config)

    PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                            substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
                            lightcone = BeforeTheTutorialMissionStarts(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
                            **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                        lightcone = DayOneOfMyNewLife(**config),
                        relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [BladeCharacter, BronyaCharacter, PelaCharacter, FuxuanCharacter]

    #%% Blade Bronya Pela Fuxuan Team Buffs
    # Broken Keel Buff
    for character in [BladeCharacter, BronyaCharacter, PelaCharacter]:
        character.addStat('CD',description='Broken Keel Fuxuan',amount=0.10)
    for character in [BladeCharacter, BronyaCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel Pela',amount=0.10)
    for character in [BladeCharacter, PelaCharacter, FuxuanCharacter]:
        character.addStat('DMG.wind',description='Penacony Bronya',amount=0.10)

    # Bronya Planetary Rendezvous
    BladeCharacter.addStat('DMG',description='Planetary Rendezvous',amount=0.09 + 0.03 * BronyaCharacter.lightcone.superposition)

    # Messenger 4 pc
    for character in [BladeCharacter, PelaCharacter, FuxuanCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)

    # Pela Debuffs, 2 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotationDuration=2)
        
    # Resolution Shines as Pearls of Sweat uptime
    #sweatUptime = (1.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
    #sweatUptime += (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
    #sweatUptime = min(1.0, sweatUptime)
    #for character in team:
    #    character.addStat('DefShred',description='Resolution Sweat',
    #                    amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
    #                    uptime=sweatUptime)
        
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    BronyaCharacter.applyUltBuff(BladeCharacter,uptime=1.0/4.0) # estimate 1 bronya buff per 4 rotations
    BronyaCharacter.applySkillBuff(BladeCharacter,uptime=1.0/2.0) # estimate 1 bronya skill buff per 2 blade attacks
    
    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Blade Bronya Pela Fuxuan Rotations
    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    # Rotation is calculated per ult, so we'll attenuate this to fit 3 bronya turns    
    numBasic = 3.5
    numUlt = 1.0

    BladeRotation = [ # 3 enhanced basics per ult roughly
                    BladeCharacter.useSkill() * numBasic / 4.0, # 0.75 charges
                    BladeCharacter.useEnhancedBasic() * numBasic, # 3 charges
                    BladeCharacter.useUltimate() * numUlt, # 1 charge
                    BronyaCharacter.useAdvanceForward() * numBasic / 2.0, # 1 advance forward every 2 basics
                ]

    numEnemyAttacks = BladeCharacter.enemySpeed * BladeCharacter.numEnemies * sum([x.actionvalue for x in BladeRotation]) / BladeCharacter.getTotalStat('SPD')
    numHitsTaken = numEnemyAttacks * 5 / (5 + 4 + 4 + 4) # assume 3 average threat teammates
    numTalent = (0.75 + 3 + 1 + numHitsTaken) / 5.0
    BladeRotation.append(BladeCharacter.useTalent() * numTalent)

    numBasicPela = 2.0
    PelaRotation = [PelaCharacter.useBasic() * numBasicPela,
                    PelaCharacter.useUltimate(),]

    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% Blade Bronya Pela Fuxuan Rotation Math
    totalBladeEffect = sumEffects(BladeRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    BladeRotationDuration = totalBladeEffect.actionvalue * 100.0 / BladeCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Blade: ',BladeRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Pela: ',PelaRotationDuration)
    print('Fuxuan: ',FuxuanRotationDuration)

    # scale other character's rotation
    BronyaRotation = [x * BladeRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    PelaRotation = [x * BladeRotationDuration / PelaRotationDuration for x in PelaRotation]
    FuxuanRotation = [x * BladeRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    BladeEstimate = DefaultEstimator(f'Blade: {numBasic:.1f}N {numTalent:.1f}T {numUlt:.0f}Q',
                                    BladeRotation, BladeCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    PelaEstimate = DefaultEstimator(f'Pela: {numBasicPela:.0f}N 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    FuxuanEstimate = DefaultEstimator('Fuxuan: 2N 1E 1Q, S{:.0f} {}'.format(FuxuanCharacter.lightcone.superposition, FuxuanCharacter.lightcone.name),
                                    FuxuanRotation, FuxuanCharacter, config)

    return([BladeEstimate, BronyaEstimate, PelaEstimate, FuxuanEstimate])

