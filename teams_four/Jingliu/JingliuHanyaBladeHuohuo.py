from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Huohuo import Huohuo
from characters.destruction.Blade import Blade
from characters.destruction.Jingliu import Jingliu
from characters.harmony.Hanya import Hanya
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.PostOpConversation import PostOpConversation
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

def JingliuHanyaBladeHuohuo(config):
    #%% Jingliu Hanya Blade Huohuo Characters
    JingliuCharacter = Jingliu(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.ice'],
                        substats = {'CR': 12, 'CD': 8, 'SPD.flat': 5, 'ATK.percent': 3}),
                        lightcone = OnTheFallOfAnAeon(**config),
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

    HuohuoCharacter = Huohuo(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'HP.flat': 3, 'RES': 6}),
                        lightcone = PostOpConversation(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [JingliuCharacter, HanyaCharacter, BladeCharacter, HuohuoCharacter]

    #%% Jingliu Hanya Blade Huohuo Team Buffs
    # only enhanced skills have rutilant arena buff
    JingliuCharacter.addStat('DMG',description='Rutilant Arena', amount=0.20, type=['enhancedSkill']) # take care of rutilant arena manually

    # Broken Keel Buff
    for character in [JingliuCharacter, HanyaCharacter, BladeCharacter]:
        character.addStat('CD',description='Broken Keel Huohuo',amount=0.10)
    for character in [JingliuCharacter, BladeCharacter, HuohuoCharacter]:
        character.addStat('CD',description='Broken Keel Hanya',amount=0.10)

    # Hanya Messenger 4 pc
    JingliuCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/5.0)
    BladeCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
    HuohuoCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)

    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(JingliuCharacter,uptime=0.8)
    
    # Huohuo Buffs
    HuohuoCharacter.applyUltBuff([BladeCharacter,HanyaCharacter],uptime=2.0/4.0)
    HuohuoCharacter.applyUltBuff([JingliuCharacter],uptime=2.0/5.0)
    
    #%% Print Statements
    for character in team:
        character.print()

    #%% Jingliu Hanya Blade Huohuo Rotations
    numHanyaSkill = 3
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]

    # Assume Hanya skill buff applies to skills, and only applies a fraction of the time to the remaining abilities
    numSkill = 1.5
    numEnhanced = 2.5
    numUlt = 1

    JingliuRotation = [ # 140 max energy
            JingliuCharacter.useSkill() * numSkill,
            JingliuCharacter.useEnhancedSkill() * numEnhanced, # 60 energy, -3 stacks
            JingliuCharacter.useUltimate() * numUlt, # 5 energy, 1 stack
            JingliuCharacter.extraTurn() * 0.9 * numSkill / 2.0, # multiply by 0.9 because it tends to overlap with skill advances
            HuohuoCharacter.giveUltEnergy(JingliuCharacter),
    ]

    numBasicBlade = 2.5
    numUltBlade = 1

    BladeRotation = [ # 3 enhanced basics per ult roughly
                    BladeCharacter.useSkill() * numBasicBlade / 4.0, # 0.75 charges
                    BladeCharacter.useEnhancedBasic() * numBasicBlade, # 3 charges, 6 charges with Jingliu
                    BladeCharacter.useUltimate() * numUltBlade, # 1 charge
                    HuohuoCharacter.giveUltEnergy(BladeCharacter) * 2.5 / 4.0,
                ]

    # assuming Blade takes 1 turn every 1 jingliu turn, so we multiply number of hits per enhanced basic by 2
    numEnemyAttacks = BladeCharacter.enemySpeed * BladeCharacter.numEnemies * sum([x.actionvalue for x in BladeRotation]) / BladeCharacter.getTotalStat('SPD')
    numHitsTaken = numEnemyAttacks * 5 / (5 + 5 + 4 + 4) #
    jingliuDrainRate = (4.0 / 4.1 ) * ( JingliuCharacter.getTotalStat('SPD') / BladeCharacter.getTotalStat('SPD'))
    numTalentBlade = (numBasicBlade / 4.0 + (1 + jingliuDrainRate) * numBasicBlade + numUltBlade + numHitsTaken) / 5.0 # skill, basics, ult, hits taken
    BladeRotation.append(BladeCharacter.useTalent() * numTalentBlade)

    numBasicHuohuo = 3.0
    numSkillHuohuo = 1.0
    HuohuoRotation = [HuohuoCharacter.useBasic() * numBasicHuohuo,
                    HuohuoCharacter.useSkill() * numSkillHuohuo,
                    HuohuoCharacter.useUltimate(),]

    #%% Jingliu Hanya Blade Huohuo Rotation Math
    totalJingliuEffect = sumEffects(JingliuRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalBladeEffect = sumEffects(BladeRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    JingliuRotationDuration = totalJingliuEffect.actionvalue * 100.0 / JingliuCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    BladeRotationDuration = totalBladeEffect.actionvalue * 100.0 / BladeCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Jingliu: ',JingliuRotationDuration)
    print('Hanya: ',HanyaRotationDuration)
    print('Blade: ',BladeRotationDuration)
    print('Huohuo: ',HuohuoRotationDuration)

    # scale other character's rotation
    HanyaRotation = [x * JingliuRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    BladeRotation = [x * JingliuRotationDuration / BladeRotationDuration for x in BladeRotation]
    HuohuoRotation = [x * JingliuRotationDuration / HuohuoRotationDuration for x in HuohuoRotation]

    JingliuEstimate = DefaultEstimator(f'Jingliu: {numSkill:.1f}E {numEnhanced:.1f}Moon {numUlt:.0f}Q',
                                                    JingliuRotation, JingliuCharacter, config)
    HanyaEstimate = DefaultEstimator(f'Hanya: {numHanyaSkill:.0f}E {numHanyaUlt:.0f}Q S{HanyaCharacter.lightcone.superposition:.0f} {HanyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanyaRotation, HanyaCharacter, config)
    BladeEstimate = DefaultEstimator(f'Blade: {numBasicBlade:.1f}N {numTalentBlade:.1f}T {numUltBlade:.0f}Q',
                                    BladeRotation, BladeCharacter, config)
    HuohuoEstimate = DefaultEstimator('Huohuo: 3N 1E 1Q, S{HuohuoCharacter.lightcone.superposition:.0f} {HuohuoCharacter.lightcone.name}',
                                    HuohuoRotation, HuohuoCharacter, config)

    return([JingliuEstimate, HanyaEstimate, BladeEstimate, HuohuoEstimate])
