from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Huohuo import Huohuo
from characters.erudition.Argenti import Argenti
from characters.harmony.Tingyun import Tingyun
from characters.harmony.Hanya import Hanya
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.PostOpConversation import PostOpConversation
from lightCones.destruction.ASecretVow import ASecretVow
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.erudition.GeniusesRepose import GeniusesRepose
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def ArgentiHanyaTingyunHuohuo(config):
    #%% Argenti Hanya Tingyun Huohuo Characters
    ArgentiCharacter = Argenti(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.physical'],
                        substats = {'CR': 12, 'CD': 8, 'SPD.flat': 5, 'ATK.percent': 3}),
                        lightcone =  GeniusesRepose(**config),
                        relicsetone = ChampionOfStreetwiseBoxing2pc(), relicsettwo = ChampionOfStreetwiseBoxing4pc(uptime=0.4), planarset = FirmamentFrontlineGlamoth(uptime=0.0),
                        **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                        substats = {'CR': 8, 'SPD.flat': 12, 'CD': 5, 'ATK.percent': 3}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                        **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                            benedictionTarget=ArgentiCharacter,
                            **config)

    HuohuoCharacter = Huohuo(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'HP.flat': 3, 'RES': 6}),
                        lightcone = PostOpConversation(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [ArgentiCharacter, HanyaCharacter, TingyunCharacter, HuohuoCharacter]

    #%% Argenti Hanya Tingyun Huohuo Team Buffs
    # only enhanced skills have rutilant arena buff
    ArgentiCharacter.addStat('DMG',description='Rutilant Arena', amount=0.20, type=['enhancedSkill']) # take care of rutilant arena manually

    # Broken Keel & Penacony Buff
    for character in [ArgentiCharacter, HanyaCharacter, TingyunCharacter]:
        character.addStat('CD',description='Broken Keel Huohuo',amount=0.10)
    for character in [ArgentiCharacter, TingyunCharacter, HuohuoCharacter]:
        character.addStat('DMG.physical',description='Penacony Hanya',amount=0.10)

    # Hanya Messenger 4 pc
    ArgentiCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/5.0)
    TingyunCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
    HuohuoCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)

    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(ArgentiCharacter,uptime=0.8)
    
    # Huohuo Buffs
    HuohuoCharacter.applyUltBuff([TingyunCharacter,HanyaCharacter],uptime=2.0/4.0)
    HuohuoCharacter.applyUltBuff([ArgentiCharacter],uptime=2.0/5.0)
    
    #%% Print Statements
    for character in team:
        character.print()

    #%% Argenti Hanya Tingyun Huohuo Rotations
    HanyaRotation = [HanyaCharacter.useSkill() * 4,
                    HanyaCharacter.useUltimate(),]

    # Assume Hanya skill buff applies to skills, and only applies a fraction of the time to the remaining abilities
    numSkill = 1.5
    numEnhanced = 2.5
    numUlt = 1

    ArgentiRotation = [ # 140 max energy
            ArgentiCharacter.useSkill() * numSkill,
            ArgentiCharacter.useEnhancedSkill() * numEnhanced, # 60 energy, -3 stacks
            ArgentiCharacter.useUltimate() * numUlt, # 5 energy, 1 stack
            ArgentiCharacter.extraTurn() * 0.9 * numSkill / 2.0, # multiply by 0.9 because it tends to overlap with skill advances
            HuohuoCharacter.giveUltEnergy(ArgentiCharacter),
    ]

    numBasicTingyun = 2.5
    numUltTingyun = 1

    TingyunRotation = [ # 3 enhanced basics per ult roughly
                    TingyunCharacter.useSkill() * numBasicTingyun / 4.0, # 0.75 charges
                    TingyunCharacter.useEnhancedBasic() * numBasicTingyun, # 3 charges, 6 charges with Argenti
                    TingyunCharacter.useUltimate() * numUltTingyun, # 1 charge
                    HuohuoCharacter.giveUltEnergy(TingyunCharacter) * 2.5 / 4.0,
                ]

    # assuming Tingyun takes 1 turn every 1 Argenti turn, so we multiply number of hits per enhanced basic by 2
    numEnemyAttacks = TingyunCharacter.enemySpeed * TingyunCharacter.numEnemies * sum([x.actionvalue for x in TingyunRotation]) / TingyunCharacter.getTotalStat('SPD')
    numHitsTaken = numEnemyAttacks * 5 / (5 + 5 + 4 + 4) #
    ArgentiDrainRate = (4.0 / 4.1 ) * ( ArgentiCharacter.getTotalStat('SPD') / TingyunCharacter.getTotalStat('SPD'))
    numTalentTingyun = (numBasicTingyun / 4.0 + (1 + ArgentiDrainRate) * numBasicTingyun + numUltTingyun + numHitsTaken) / 5.0 # skill, basics, ult, hits taken
    TingyunRotation.append(TingyunCharacter.useTalent() * numTalentTingyun)

    HuohuoRotation = [HuohuoCharacter.useBasic() * 3,
                    HuohuoCharacter.useSkill() * 1,
                    HuohuoCharacter.useUltimate() * 1,]

    #%% Argenti Hanya Tingyun Huohuo Rotation Math
    totalArgentiEffect = sumEffects(ArgentiRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    ArgentiRotationDuration = totalArgentiEffect.actionvalue * 100.0 / ArgentiCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Argenti: ',ArgentiRotationDuration)
    print('Hanya: ',HanyaRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Huohuo: ',HuohuoRotationDuration)

    # scale other character's rotation
    HanyaRotation = [x * ArgentiRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    TingyunRotation = [x * ArgentiRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HuohuoRotation = [x * ArgentiRotationDuration / HuohuoRotationDuration for x in HuohuoRotation]

    ArgentiEstimate = DefaultEstimator('Argenti {:.1f}E {:.1f}Moon {:.0f}Q'.format(numSkill, numEnhanced, numUlt),
                                                    ArgentiRotation, ArgentiCharacter, config)
    HanyaEstimate = DefaultEstimator('E0 Hanya S{:.0f} {}, 12 Spd Substats'.format(HanyaCharacter.lightcone.superposition, HanyaCharacter.lightcone.name), 
                                    HanyaRotation, HanyaCharacter, config)
    TingyunEstimate = DefaultEstimator(f'Tingyun: {numBasicTingyun:.1f}N {numTalentTingyun:.1f}T {numUltTingyun:.0f}Q',
                                    TingyunRotation, TingyunCharacter, config)
    HuohuoEstimate = DefaultEstimator('Huohuo: 3N 1E 1Q, S{:.0f} {}'.format(HuohuoCharacter.lightcone.superposition, HuohuoCharacter.lightcone.name),
                                    HuohuoRotation, HuohuoCharacter, config)

    return([ArgentiEstimate, HanyaEstimate, TingyunEstimate, HuohuoEstimate])
