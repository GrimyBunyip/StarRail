from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Blade import Blade
from characters.destruction.Jingliu import Jingliu
from characters.harmony.RuanMei import RuanMei
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.abundance.PostOpConversation import PostOpConversation
from lightCones.destruction.ASecretVow import ASecretVow
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc, HunterOfGlacialForest4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def JingliuRuanMeiBladeLuocha(config):
    #%% Jingliu RuanMei Blade Luocha Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                        substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = PenaconyLandOfDreams(),
                        **config)
    
    JingliuCharacter = Jingliu(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.ice'],
                        substats = {'CR': 12, 'CD': 8, 'SPD.flat': 5, 'ATK.percent': 3}),
                        lightcone = OnTheFallOfAnAeon(**config),
                        relicsetone = HunterOfGlacialForest2pc(), relicsettwo = HunterOfGlacialForest4pc(uptime=0.4), planarset = RutilantArena(uptime=0.0),
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
    
    team = [JingliuCharacter, RuanMeiCharacter, BladeCharacter, LuochaCharacter]

    #%% Jingliu RuanMei Blade Luocha Team Buffs
    # only enhanced skills have rutilant arena buff
    JingliuCharacter.addStat('DMG',description='Rutilant Arena', amount=0.20, type=['enhancedSkill']) # take care of rutilant arena manually

    # Broken Keel Buff
    for character in [JingliuCharacter, RuanMeiCharacter, BladeCharacter]:
        character.addStat('CD',description='Broken Keel Luocha',amount=0.10)
        
    for character in [JingliuCharacter, BladeCharacter, LuochaCharacter]:
        character.addStat('DMG.ice',description='Penacony Ruan Mei',amount=0.10)

    # RuanMei Buffs, max skill uptime
    RuanMeiCharacter.applyWeaknessModifiers(team=team)
    RuanMeiCharacter.applyPassiveBuffs(team=team)
    RuanMeiCharacter.applySkillBuff(team=team,uptime=3.0/3.0)
    RuanMeiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)
    
    #%% Print Statements
    for character in team:
        character.print()

    #%% Jingliu RuanMei Blade Luocha Rotations
    numBasicRuanMei = 2
    numSkillRuanMei = 1
    RuanMeiRotation = [RuanMeiCharacter.useBasic() * numBasicRuanMei,
                       RuanMeiCharacter.useSkill() * numSkillRuanMei,
                    RuanMeiCharacter.useUltimate(),
                    RuanMeiCharacter.useTalent() * numBasicRuanMei] # append ruan mei talent damage

    numSkill = 1.5
    numEnhanced = 2.5
    numUlt = 1
    numBlast = min(3, JingliuCharacter.numEnemies)

    JingliuRotation = [ # 140 max energy
            JingliuCharacter.useSkill() * numSkill,
            JingliuCharacter.useEnhancedSkill() * numEnhanced, # 60 energy, -3 stacks
            JingliuCharacter.useUltimate() * numUlt, # 5 energy, 1 stack
            JingliuCharacter.extraTurn() * 0.9 * numSkill / 2.0, # multiply by 0.9 because it tends to overlap with skill advances
            RuanMeiCharacter.useTalent() * (numSkill + numBlast * (numEnhanced + numUlt)),
    ]

    numBasicBlade = 2.5
    numUltBlade = 1

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
    BladeRotation.append(RuanMeiCharacter.useTalent() * (numTalentBlade * BladeCharacter.numEnemies + numBlast * (numBasicBlade + numUltBlade)))

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useSkill() * 1,
                    RuanMeiCharacter.useTalent() * (3 + 1 * LuochaCharacter.numEnemies), # append ruan mei talent damage
                    LuochaCharacter.useUltimate() * 1]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Jingliu RuanMei Blade Luocha Rotation Math
    totalJingliuEffect = sumEffects(JingliuRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalBladeEffect = sumEffects(BladeRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    JingliuRotationDuration = totalJingliuEffect.actionvalue * 100.0 / JingliuCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    BladeRotationDuration = totalBladeEffect.actionvalue * 100.0 / BladeCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Jingliu: ',JingliuRotationDuration)
    print('RuanMei: ',RuanMeiRotationDuration)
    print('Blade: ',BladeRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # scale other character's rotation
    RuanMeiRotation = [x * JingliuRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    BladeRotation = [x * JingliuRotationDuration / BladeRotationDuration for x in BladeRotation]
    LuochaRotation = [x * JingliuRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    JingliuEstimate = DefaultEstimator('Jingliu {:.1f}E {:.1f}Moon {:.0f}Q'.format(numSkill, numEnhanced, numUlt),
                                                    JingliuRotation, JingliuCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'RuanMei {numSkillRuanMei:.1f}E {numBasicRuanMei:.1f}N S{RuanMeiCharacter.lightcone.superposition:.0f} {RuanMeiCharacter.lightcone.name}, 12 Spd Substats', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    BladeEstimate = DefaultEstimator(f'Blade: {numBasicBlade:.1f}N {numTalentBlade:.1f}T {numUltBlade:.0f}Q',
                                    BladeRotation, BladeCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name),
                                    LuochaRotation, LuochaCharacter, config)

    return([JingliuEstimate, BladeEstimate, RuanMeiEstimate, LuochaEstimate])
