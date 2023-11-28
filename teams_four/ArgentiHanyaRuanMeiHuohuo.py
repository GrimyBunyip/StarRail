from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Huohuo import Huohuo
from characters.erudition.Argenti import Argenti
from characters.harmony.RuanMei import RuanMei
from characters.harmony.Hanya import Hanya
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.PostOpConversation import PostOpConversation
from lightCones.erudition.GeniusesRepose import GeniusesRepose
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def ArgentiHanyaRuanMeiHuohuo(config):
    #%% Argenti Hanya RuanMei Huohuo Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                        substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                        **config)
    
    ArgentiCharacter = Argenti(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.physical'],
                        substats = {'CR': 8, 'CD': 12, 'SPD.flat': 5, 'ATK.percent': 3}),
                        lightcone =  GeniusesRepose(**config),
                        relicsetone = ChampionOfStreetwiseBoxing2pc(), relicsettwo = ChampionOfStreetwiseBoxing4pc(uptime=0.4), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                        substats = {'CR': 8, 'SPD.flat': 12, 'CD': 5, 'ATK.percent': 3}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                        **config)

    HuohuoCharacter = Huohuo(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'HP.flat': 3, 'RES': 6}),
                        lightcone = PostOpConversation(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [ArgentiCharacter, HanyaCharacter, RuanMeiCharacter, HuohuoCharacter]

    #%% Argenti Hanya RuanMei Huohuo Team Buffs

    # Broken Keel & Penacony Buff
    for character in [ArgentiCharacter, HanyaCharacter, RuanMeiCharacter]:
        character.addStat('CD',description='Broken Keel Huohuo',amount=0.10)
    for character in [ArgentiCharacter, RuanMeiCharacter, HuohuoCharacter]:
        character.addStat('DMG.physical',description='Penacony Hanya',amount=0.10)

    # Hanya Messenger 4 pc
    for character in [ArgentiCharacter, RuanMeiCharacter, HuohuoCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # RuanMei Messenger 4 pc
    for character in [ArgentiCharacter, HanyaCharacter, HuohuoCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
    
    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(ArgentiCharacter,uptime=1.0)
    
    # Huohuo Buffs
    HuohuoCharacter.applyUltBuff([RuanMeiCharacter,HanyaCharacter],uptime=2.0/4.0)
    HuohuoCharacter.applyUltBuff([ArgentiCharacter],uptime=2.0/5.0)
        
    # RuanMei Buffs, 3 turn RuanMei rotation
    RuanMeiCharacter.applyWeaknessModifiers(team=team)
    RuanMeiCharacter.applyPassiveBuffs(team=team)
    RuanMeiCharacter.applySkillBuff(team=team,uptime=3.0/3.0)
    RuanMeiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)
    
    #%% Print Statements
    for character in team:
        character.print()

    #%% Argenti Hanya RuanMei Huohuo Rotations
    numHanyaSkill = 3
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]

    # Argenti & RuanMei Rotation
    HuohuoEnergyPerTurn = (36.0 if HuohuoCharacter.eidolon >= 5 else 36.0) / 4.0
    numSkill = (180.0 - 5.0 - 3.0 * ArgentiCharacter.numEnemies) / (30.0 + HuohuoEnergyPerTurn + 3 * ArgentiCharacter.numEnemies)
    numUlt = 1

    ArgentiRotation = [ArgentiCharacter.useSkill() * numSkill,
                        ArgentiCharacter.useEnhancedUltimate() * numUlt,]

    numBasicRuanMei = 2.0
    numSkillRuanMei = 1.0
    RuanMeiRotation = [RuanMeiCharacter.useBasic() * numBasicRuanMei,
                       RuanMeiCharacter.useSkill() * numSkillRuanMei,
                    RuanMeiCharacter.useUltimate(),
                    RuanMeiCharacter.useTalent() * numBasicRuanMei] # append ruan mei talent damage

    HuohuoRotation = [HuohuoCharacter.useBasic() * 3,
                    HuohuoCharacter.useSkill() * 1,
                    HuohuoCharacter.useUltimate() * 1,]

    #%% Argenti Hanya RuanMei Huohuo Rotation Math
    totalArgentiEffect = sumEffects(ArgentiRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    ArgentiRotationDuration = totalArgentiEffect.actionvalue * 100.0 / ArgentiCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    ArgentiRotation.append(HuohuoCharacter.giveUltEnergy(ArgentiCharacter) * ArgentiRotationDuration / HuohuoRotationDuration)

    print('##### Rotation Durations #####')
    print('Argenti: ',ArgentiRotationDuration)
    print('Hanya: ',HanyaRotationDuration)
    print('RuanMei: ',RuanMeiRotationDuration)
    print('Huohuo: ',HuohuoRotationDuration)

    # scale other character's rotation
    HanyaRotation = [x * ArgentiRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    RuanMeiRotation = [x * ArgentiRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    HuohuoRotation = [x * ArgentiRotationDuration / HuohuoRotationDuration for x in HuohuoRotation]

    ArgentiEstimate = DefaultEstimator(f'Argenti: {numSkill:.1f}E {numUlt:.1f}EnhQ', 
                                            ArgentiRotation, ArgentiCharacter, config)
    HanyaEstimate = DefaultEstimator('Hanya {:.0f}E {:.0f}Q S{:.0f} {}, 12 Spd Substats'.format(numHanyaSkill, numHanyaUlt,
                                    HanyaCharacter.lightcone.superposition, HanyaCharacter.lightcone.name), 
                                    HanyaRotation, HanyaCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'Ruan Mei: {numBasicRuanMei:.0f}N {numSkillRuanMei:.0f}E 1Q, S{RuanMeiCharacter.lightcone.superposition:d} {RuanMeiCharacter.lightcone.name}', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    HuohuoEstimate = DefaultEstimator('Huohuo: 3N 1E 1Q, S{:.0f} {}'.format(HuohuoCharacter.lightcone.superposition, HuohuoCharacter.lightcone.name),
                                    HuohuoRotation, HuohuoCharacter, config)

    return([ArgentiEstimate, HanyaEstimate, RuanMeiEstimate, HuohuoEstimate])
