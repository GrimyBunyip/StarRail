from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Blade import Blade
from characters.destruction.Jingliu import Jingliu
from characters.harmony.Hanya import Hanya
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.ASecretVow import ASecretVow
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc, HunterOfGlacialForest4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def JingliuHanyaBladeLuocha(config):
    #%% Jingliu Hanya Blade Luocha Characters
    JingliuCharacter = Jingliu(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.ice'],
                        substats = {'CR': 12, 'CD': 8, 'SPD.flat': 5, 'ATK.percent': 3}),
                        lightcone = OnTheFallOfAnAeon(uptime = 0.25, **config),
                        relicsetone = HunterOfGlacialForest2pc(), relicsettwo = HunterOfGlacialForest4pc(uptime=0.4), planarset = RutilantArena(uptime=0.0),
                        **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                        substats = {'CR': 8, 'SPD.flat': 12, 'CD': 5, 'ATK.percent': 3}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

    BladeCharacter = Blade(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'HP.percent'],
                        substats = {'CR': 12, 'CD': 8, 'SPD.flat': 5, 'HP.percent': 3}),
                        lightcone = ASecretVow(**config),
                        relicsetone = LongevousDisciple2pc(), relicsettwo = LongevousDisciple4pc(), planarset = InertSalsotto(),
                        **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [JingliuCharacter, HanyaCharacter, BladeCharacter, LuochaCharacter]

    #%% Jingliu Hanya Blade Luocha Team Buffs
    # only enhanced skills have rutilant arena buff
    JingliuCharacter.addStat('DMG',description='Rutilant Arena', amount=0.20, type=['enhancedSkill']) # take care of rutilant arena manually

    # Broken Keel Buff
    for character in [JingliuCharacter, HanyaCharacter, BladeCharacter]:
        character.addStat('CD',description='Broken Keel Luocha',amount=0.10)
    for character in [JingliuCharacter, BladeCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel Hanya',amount=0.10)

    # Hanya Messenger 4 pc
    JingliuCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/5.0)
    BladeCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)

    # apply buffs now that we calculated approximate rotation times
    # Hanya Buff
    for character in [JingliuCharacter, BladeCharacter, LuochaCharacter]:
        character.addStat('ATK.percent',description='Hanya trace',amount=0.10,uptime=0.5)
        character.addStat('DMG',description='Burden',amount=(0.33 if HanyaCharacter.eidolon >= 5 else 0.30) + (0.10 if HanyaCharacter.eidolon >= 6 else 0.0))

    # about 80% uptime on ult buf
    JingliuCharacter.addStat('SPD.flat',description='Hanya Ult',amount=(0.21 if HanyaCharacter.eidolon >= 5 else 0.20) * HanyaCharacter.getTotalStat('SPD'),uptime=0.8)
    JingliuCharacter.addStat('ATK.percent',description='Hanya Ult',amount=0.648 if HanyaCharacter.eidolon >= 5 else 0.60,uptime=0.8)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Jingliu Hanya Blade Luocha Rotations
    HanyaRotation = [HanyaCharacter.useSkill() * 4,
                    HanyaCharacter.useUltimate(),]

    # Assume Hanya skill buff applies to skills, and only applies a fraction of the time to the remaining abilities
    numSkill = 2.0
    numEnhanced = 3.0
    numUlt = 1.0

    JingliuRotation = [ # 140 max energy
            JingliuCharacter.useSkill() * numSkill,
            JingliuCharacter.useEnhancedSkill() * numEnhanced, # 60 energy, -3 stacks
            JingliuCharacter.useUltimate() * numUlt, # 5 energy, 1 stack
            JingliuCharacter.extraTurn() * 0.9, # multiply by 0.9 because it tends to overlap with skill advances
    ]

    numBasicBlade = 3.0
    numUltBlade = 1.0

    BladeRotation = [ # 3 enhanced basics per ult roughly
                    BladeCharacter.useSkill() * numBasicBlade / 4.0, # 0.75 charges
                    BladeCharacter.useEnhancedBasic() * numBasicBlade, # 3 charges, 6 charges with Jingliu
                    BladeCharacter.useUltimate() * numUltBlade, # 1 charge
                ]

    # assuming Blade takes 1 turn every 1 jingliu turn, so we multiply number of hits per enhanced basic by 2
    numEnemyAttacks = BladeCharacter.enemySpeed * BladeCharacter.numEnemies * sum([x.actionvalue for x in BladeRotation]) / BladeCharacter.getTotalStat('SPD')
    numHitsTaken = numEnemyAttacks * 5 / (5 + 5 + 4 + 4) #
    jingliuDrainRate = (4.0 / 4.1 ) * ( JingliuCharacter.getTotalStat('SPD') / BladeCharacter.getTotalStat('SPD'))
    numTalentBlade = (numBasicBlade / 4.0 + (1 + jingliuDrainRate) * numBasicBlade + numUltBlade + numHitsTaken) / 5.0 # skill, basics, ult, hits taken
    BladeRotation.append(BladeCharacter.useTalent() * numTalentBlade)

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast

    #%% Jingliu Hanya Blade Luocha Rotation Math
    totalJingliuEffect = sumEffects(JingliuRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalBladeEffect = sumEffects(BladeRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    JingliuRotationDuration = totalJingliuEffect.actionvalue * 100.0 / JingliuCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    BladeRotationDuration = totalBladeEffect.actionvalue * 100.0 / BladeCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Jingliu: ',JingliuRotationDuration)
    print('Hanya: ',HanyaRotationDuration)
    print('Blade: ',BladeRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # scale other character's rotation
    HanyaRotation = [x * JingliuRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    BladeRotation = [x * JingliuRotationDuration / BladeRotationDuration for x in BladeRotation]
    LuochaRotation = [x * JingliuRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    JingliuEstimate = DefaultEstimator('Jingliu {:.0f}E {:.0f}Moon {:.0f}Q'.format(numSkill, numEnhanced, numUlt),
                                                    JingliuRotation, JingliuCharacter, config)
    HanyaEstimate = DefaultEstimator('E0 Hanya S{:.0f} {}, 12 Spd Substats'.format(HanyaCharacter.lightcone.superposition, HanyaCharacter.lightcone.name), 
                                    HanyaRotation, HanyaCharacter, config)
    BladeEstimate = DefaultEstimator(f'Blade: {numBasicBlade:.0f}N {numTalentBlade:.1f}T {numUltBlade:.0f}Q',
                                    BladeRotation, BladeCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name),
                                    LuochaRotation, LuochaCharacter, config)

    return([JingliuEstimate, HanyaEstimate, BladeEstimate, LuochaEstimate])
