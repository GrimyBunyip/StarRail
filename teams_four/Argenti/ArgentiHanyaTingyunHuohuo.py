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
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
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
    ArgentiCharacter = Argenti(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.physical'],
                        substats = {'CR': 8, 'CD': 12, 'SPD.flat': 5, 'ATK.percent': 3}),
                        lightcone =  GeniusesRepose(**config),
                        relicsetone = ChampionOfStreetwiseBoxing2pc(), relicsettwo = ChampionOfStreetwiseBoxing4pc(uptime=0.4), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                        substats = {'CR': 8, 'SPD.flat': 12, 'CD': 5, 'ATK.percent': 3}),
                        lightcone = PlanetaryRendezvous(**config),
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

    # Broken Keel & Penacony Buff
    for character in [ArgentiCharacter, HanyaCharacter, TingyunCharacter]:
        character.addStat('CD',description='Broken Keel Huohuo',amount=0.10)
    for character in [ArgentiCharacter, TingyunCharacter, HuohuoCharacter]:
        character.addStat('DMG.physical',description='Penacony Hanya',amount=0.10)
    for character in team:
        character.addStat('DMG.physical',description='Planetary Rendezvous',amount=0.24)

    # Hanya Messenger 4 pc
    for character in [ArgentiCharacter, TingyunCharacter, HuohuoCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/2.75) # let's say half the time, huohuo can shave off a turn
        
    # Tingyun Messenger 4 pc
    for character in [ArgentiCharacter, HanyaCharacter, HuohuoCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/2.75) # let's say half the time, huohuo can shave off a turn
    
    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(ArgentiCharacter,uptime=1.0)
    
    # Huohuo Buffs
    HuohuoCharacter.applyUltBuff([TingyunCharacter,HanyaCharacter],uptime=2.0/4.0)
    HuohuoCharacter.applyUltBuff([ArgentiCharacter],uptime=2.0/5.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(ArgentiCharacter)
    TingyunCharacter.applyUltBuff(ArgentiCharacter,tingRotationDuration=2.75) # let's say half the time, huohuo can shave off a turn
    
    #%% Print Statements
    for character in team:
        character.print()

    #%% Argenti Hanya Tingyun Huohuo Rotations
    numHanyaSkill = 4
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]

    # Argenti & Tingyun Rotation
    TingyunEnergyPerTurn = (60.0 if TingyunCharacter.eidolon >= 6 else 50.0) / 2.75 # let's say half the time, huohuo can shave off a turn
    HuohuoEnergyPerTurn = ArgentiCharacter.maxEnergy * (0.21 if HuohuoCharacter.eidolon >= 5 else 0.20)  / 4.0
    TingyunEnergyPerTurn *= TingyunCharacter.getTotalStat('SPD') / ArgentiCharacter.getTotalStat('SPD')
    HuohuoEnergyPerTurn *= HuohuoCharacter.getTotalStat('SPD') / ArgentiCharacters.getTotalStat('SPD')
    numSkill = (180.0 - 5.0 - 3.0 * ArgentiCharacter.numEnemies) / (30.0 + TingyunEnergyPerTurn + HuohuoEnergyPerTurn + 3 * ArgentiCharacter.numEnemies)
    numUlt = 1

    ArgentiRotation = [ArgentiCharacter.useSkill() * numSkill,
                        ArgentiCharacter.useEnhancedUltimate() * numUlt,]

    ArgentiRotation.append(TingyunCharacter.useBenediction(['skill']) * numSkill * ArgentiCharacter.numEnemies)
    ArgentiRotation.append(TingyunCharacter.useBenediction(['ultimate','enhancedUltimate']) * numUlt * ArgentiCharacter.numEnemies)

    numBasicTingyun = 2.0
    numSkillTingyun = 1.0
    TingyunRotation = [ 
            TingyunCharacter.useBasic() * numBasicTingyun, 
            TingyunCharacter.useSkill() * numSkillTingyun,
            TingyunCharacter.useUltimate(),
    ]

    numBasicHuohuo = 3.0
    numSkillHuohuo = 1.0
    HuohuoRotation = [HuohuoCharacter.useBasic() * numBasicHuohuo,
                    HuohuoCharacter.useSkill() * numSkillHuohuo,
                    HuohuoCharacter.useUltimate(),]

    #%% Argenti Hanya Tingyun Huohuo Rotation Math
    totalArgentiEffect = sumEffects(ArgentiRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    ArgentiRotationDuration = totalArgentiEffect.actionvalue * 100.0 / ArgentiCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    ArgentiRotation.append(HuohuoCharacter.giveUltEnergy(ArgentiCharacter) * ArgentiRotationDuration / HuohuoRotationDuration)
    ArgentiRotation.append(TingyunCharacter.giveUltEnergy() * ArgentiRotationDuration / TingyunRotationDuration)

    print('##### Rotation Durations #####')
    print('Argenti: ',ArgentiRotationDuration)
    print('Hanya: ',HanyaRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Huohuo: ',HuohuoRotationDuration)

    # scale other character's rotation
    HanyaRotation = [x * ArgentiRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    TingyunRotation = [x * ArgentiRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HuohuoRotation = [x * ArgentiRotationDuration / HuohuoRotationDuration for x in HuohuoRotation]

    ArgentiEstimate = DefaultEstimator(f'Argenti: {numSkill:.1f}E {numUlt:.1f}EnhQ', 
                                            ArgentiRotation, ArgentiCharacter, config)
    HanyaEstimate = DefaultEstimator(f'Hanya {numHanyaSkill:.0f}E {numHanyaUlt:.0f}Q S{HanyaCharacter.lightcone.superposition:.0f} {HanyaCharacter.lightcone.name}, 12 Spd Substats',
                                    HanyaRotation, HanyaCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats',
                                    TingyunRotation, TingyunCharacter, config)
    HuohuoEstimate = DefaultEstimator(f'Huohuo: {numBasicHuohuo:.0f}N {numSkillHuohuo:.0f}E 1Q, S{HuohuoCharacter.lightcone.superposition:.0f} {HuohuoCharacter.lightcone.name}',
                                    HuohuoRotation, HuohuoCharacter, config)

    return([ArgentiEstimate, HanyaEstimate, TingyunEstimate, HuohuoEstimate])
