from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Lynx import Lynx
from characters.destruction.Blade import Blade
from characters.harmony.Bronya import Bronya
from characters.nihility.Pela import Pela
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.ASecretVow import ASecretVow
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def BladeBronyaPelaLynx(config):
    #%% Blade Bronya Pela Lynx Characters
    BladeCharacter = Blade(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'HP.percent'],
                        substats = {'CR': 12, 'CD': 8, 'SPD.flat': 5, 'HP.percent': 3}),
                        lightcone = ASecretVow(**config),
                        relicsetone = LongevousDisciple2pc(), relicsettwo = LongevousDisciple4pc(), planarset = InertSalsotto(),
                        **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CD', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = PlanetaryRendezvous(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                        **config)

    PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                        substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
                        lightcone = ResolutionShinesAsPearlsOfSweat(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
                        **config)

    LynxCharacter = Lynx(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'ATK.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [BladeCharacter, BronyaCharacter, PelaCharacter, LynxCharacter]

    #%% Blade Bronya Pela Lynx Team Buffs

    # Broken Keel Buff
    for character in [BladeCharacter, BronyaCharacter, PelaCharacter]:
        character.addStat('CD',description='Broken Keel Lynx',amount=0.10)
    for character in [BladeCharacter, BronyaCharacter, LynxCharacter]:
        character.addStat('CD',description='Broken Keel Pela',amount=0.10)
    for character in [BladeCharacter]:
        character.addStat('DMG',description='Penacony Bronya',amount=0.10)

    # Bronya Planetary Rendezvous
    BladeCharacter.addStat('DMG',description='Planetary Rendezvous',amount=0.09 + 0.03 * BronyaCharacter.lightcone.superposition)

    # Bronya A6 and Messenger 4 pc
    for character in [BladeCharacter, PelaCharacter, LynxCharacter]:
        character.addStat('DMG',description='Bronya A6',amount=0.10)
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)

    # Pela Debuffs, 3 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotation_turns=3)
        
    # Resolution Shines as Pearls of Sweat uptime
    sweatUptime = (1.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
    sweatUptime += (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
    sweatUptime = min(1.0, sweatUptime)
    for character in [BladeCharacter,BronyaCharacter,PelaCharacter,LynxCharacter]:
        character.addStat('DefShred',description='Resolution Sweat',
                        amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                        uptime=sweatUptime)
        
    # Bronya Buffs
    # since we are not assuming a sync'd rotation, I will just take the average of the Bronya Buffs.
    # Assume Bronya ult buffs every 4 attacks, and Bronya skill buffs every 2
    BladeCharacter.addStat('ATK.percent',description='Bronya Ult',
                        amount=0.594 if BronyaCharacter.eidolon >= 3 else 0.55,
                        uptime=1.0/4.0)
    BladeCharacter.addStat('CD',description='Bronya Ult',
                        amount=((0.168 * BronyaCharacter.getTotalStat('CD') + 0.216) if BronyaCharacter.eidolon >= 3 else (0.16 * BronyaCharacter.getTotalStat('CD') + 0.2)),
                        uptime=1.0/4.0)
    BladeCharacter.addStat('DMG',description='Bronya Skill',
                        amount=0.726 if BronyaCharacter.eidolon >= 5 else 0.66,
                        uptime=1.0/2.0)

    # Lynx Buffs
    LynxBuffUptime = LynxCharacter.getTotalStat('SPD') / BladeCharacter.getTotalStat('SPD') / (2.6/3.0) / 2.0
    BladeCharacter.addStat('HP.flat',description='Lynx E6',
                        amount=(LynxCharacter.getTotalStat('HP') * 0.08 + 223) if LynxCharacter.eidolon >= 3 else (LynxCharacter.getTotalStat('HP') * 0.075 + 200),
                        uptime=LynxBuffUptime)
    if LynxCharacter.eidolon >= 4:
        BladeCharacter.addStat('ATK.flat',description='Lynx E6',amount=LynxCharacter.getTotalStat('HP') * 0.03,uptime=LynxBuffUptime/3.0)
    if LynxCharacter.eidolon >= 6:
        BladeCharacter.addStat('HP.flat',description='Lynx E6',amount=LynxCharacter.getTotalStat('HP') * 0.06,uptime=LynxBuffUptime)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Blade Bronya Pela Lynx Rotations
    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    # Rotation is calculated per ult, so we'll attenuate this to fit 3 bronya turns    
    numBasic = 3.0
    numUlt = 1.0

    BladeRotation = [ # 3 enhanced basics per ult roughly
                    BladeCharacter.useSkill() * numBasic / 4.0, # 0.75 charges
                    BladeCharacter.useEnhancedBasic() * numBasic, # 3 charges
                    BladeCharacter.useUltimate() * numUlt, # 1 charge
                    BronyaCharacter.useAdvanceForward() * numBasic / 2.0, # 1 advance forward every 2 basics
                ]

    numEnemyAttacks = BladeCharacter.enemySpeed * BladeCharacter.numEnemies * sum([x.actionvalue for x in BladeRotation]) / BladeCharacter.getTotalStat('SPD')
    numHitsTaken = numEnemyAttacks * 5 / (5 * (1 + 5*LynxBuffUptime) + 4 + 4 + 4) # assume 3 average threat teammates
    numTalent = (0.75 + 3 + 1 + numHitsTaken) / 5.0
    BladeRotation.append(BladeCharacter.useTalent() * numTalent)

    PelaRotation = [PelaCharacter.useBasic() * 3,
                    PelaCharacter.useUltimate(),]

    LynxRotation = [LynxCharacter.useBasic() * 2,
                    LynxCharacter.useSkill() * 1,
                    LynxCharacter.useUltimate() * 1,]

    #%% Blade Bronya Pela Lynx Rotation Math
    totalBladeEffect = sumEffects(BladeRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalLynxEffect = sumEffects(LynxRotation)

    BladeRotationDuration = totalBladeEffect.actionvalue * 100.0 / BladeCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    LynxRotationDuration = totalLynxEffect.actionvalue * 100.0 / LynxCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Blade: ',BladeRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Pela: ',PelaRotationDuration)
    print('Lynx: ',LynxRotationDuration)

    # scale other character's rotation
    BronyaRotation = [x * BladeRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    PelaRotation = [x * BladeRotationDuration / PelaRotationDuration for x in PelaRotation]
    LynxRotation = [x * BladeRotationDuration / LynxRotationDuration for x in LynxRotation]

    BladeEstimate = DefaultEstimator(f'Blade: {numBasic:.0f}N {numTalent:.1f}T {numUlt:.0f}Q',
                                    BladeRotation, BladeCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    PelaEstimate = DefaultEstimator(f'Pela: 3N 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    LynxEstimate = DefaultEstimator('Lynx: 2N 1E 1Q, S{:.0f} {}'.format(LynxCharacter.lightcone.superposition, LynxCharacter.lightcone.name),
                                    LynxRotation, LynxCharacter, config)

    return([BladeEstimate, BronyaEstimate, PelaEstimate, LynxEstimate])

