from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Huohuo import Huohuo
from characters.erudition.JingYuan import JingYuan
from characters.harmony.Tingyun import Tingyun
from characters.harmony.Hanabi import Hanabi
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.PostOpConversation import PostOpConversation
from lightCones.erudition.GeniusesRepose import GeniusesRepose
from lightCones.harmony.EarthlyEscapade import EarthlyEscapade
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def JingYuanHanabiS1TingyunHuohuo(config):
    #%% JingYuan Hanabi Tingyun Huohuo Characters
    JingYuanCharacter = JingYuan(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.lightning'],
                            substats = {'CD': 9, 'CR': 11, 'ATK.percent': 5, 'BreakEffect': 3}),
                            lightcone = GeniusesRepose(**config),
                            relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(followupStacks=6.5,stacks=8.0,uptime=1.0), planarset = InertSalsotto(),
                            **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'SPD.flat', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'RES': 5, 'DEF.percent': 3}),
                        lightcone = EarthlyEscapade(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = PlanetaryRendezvous(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                        benedictionTarget=JingYuanCharacter,
                        **config)

    HuohuoCharacter = Huohuo(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'HP.flat': 3, 'RES': 6}),
                        lightcone = PostOpConversation(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [JingYuanCharacter, HanabiCharacter, TingyunCharacter, HuohuoCharacter]

    #%% JingYuan Hanabi Tingyun Huohuo Team Buffs

    # Broken Keel & Penacony Buff
    for character in [JingYuanCharacter, HanabiCharacter, TingyunCharacter]:
        character.addStat('CD',description='Broken Keel Huohuo',amount=0.10)
    for character in [JingYuanCharacter, TingyunCharacter, HuohuoCharacter]:
        character.addStat('CD',description='Broken Keel Hanabi',amount=0.10)
    for character in [JingYuanCharacter, HuohuoCharacter, HanabiCharacter]:
        character.addStat('DMG.lightning',description='Penacony from Tingyun',amount=0.1)
        
    # Earthly Escapade
    for character in team:
        character.addStat('CR',description='Earthly Escapade',amount=0.10)
        character.addStat('CD',description='Earthly Escapade',amount=0.28)

    # Hanabi Messenger 4 pc
    for character in [JingYuanCharacter, TingyunCharacter, HuohuoCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/2.75) # let's say half the time, huohuo can shave off a turn
        
    # Tingyun Messenger 4 pc
    for character in [JingYuanCharacter, HanabiCharacter, HuohuoCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.2) # let's say half the time, huohuo can shave off a turn
    
    # Tingyun Planetary
    for character in team:
        character.addStat('DMG.lightning',description='Planetary from Tingyun',amount=0.24)
    
    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=JingYuanCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=2.0/2.75) # let's say half the time huohuo can shave off a turn
    
    # Huohuo Buffs
    HuohuoCharacter.applyUltBuff([TingyunCharacter,HanabiCharacter, JingYuanCharacter],uptime=2.0/4.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(JingYuanCharacter)
    TingyunCharacter.applyUltBuff(JingYuanCharacter,tingRotationDuration=3.2)
    
    #%% Print Statements
    for character in team:
        character.print()

    #%% JingYuan Hanabi Tingyun Huohuo Rotations
    numBasicHanabi = 0.0
    numSkillHanabi = 2.75 # let's say half the time, huohuo can shave off a turn
    HanabiRotation = [HanabiCharacter.useBasic() * numBasicHanabi,
                       HanabiCharacter.useSkill() * numSkillHanabi,
                    HanabiCharacter.useUltimate()]

    # JingYuan & Tingyun Rotation
    TingyunEnergyPerTurn = (60.0 if TingyunCharacter.eidolon >= 6 else 50.0) / 3.2  # let's say half the time, huohuo can shave off a turn
    HuohuoEnergyPerTurn = JingYuanCharacter.maxEnergy * (0.21 if HuohuoCharacter.eidolon >= 5 else 0.20)  / 4.0
    TingyunEnergyPerTurn *= TingyunCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')
    HuohuoEnergyPerTurn *= HuohuoCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')
    numSkill = (130.0 - 5.0) / (30.0 + TingyunEnergyPerTurn + HuohuoEnergyPerTurn)
    numUlt = 1
    
    JingYuanCharacter.getTotalStat('SPD')

    lordSpeed = 0.85 # close enough of an estimate
    numTalents = ( 3 * numSkill * lordSpeed / HanabiCharacter.getTotalStat('SPD') )  + 2 * numSkill + 3
    JingYuanRotation = [
        JingYuanCharacter.useSkill() * numSkill,
        JingYuanCharacter.useUltimate() * numUlt,
        JingYuanCharacter.useTalent() * numTalents,
        TingyunCharacter.useBenediction(['skill']) * numSkill,
        TingyunCharacter.useBenediction(['ultimate']),
        HanabiCharacter.useAdvanceForward(advanceAmount=1.0 - JingYuanCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')) * numSkill, 
    ]

    TingyunRotation = [ 
            TingyunCharacter.useBasic() * 3.2 * 2.0 / 3.0, # let's say half the time, huohuo can shave off a turn 
            TingyunCharacter.useSkill() * 3.2 * 1.0 / 3.0,
            TingyunCharacter.useUltimate(),
    ]

    HuohuoRotation = [HuohuoCharacter.useBasic() * 3,
                    HuohuoCharacter.useSkill() * 1,
                    HuohuoCharacter.useUltimate() * 1,]

    #%% JingYuan Hanabi Tingyun Huohuo Rotation Math
    totalJingYuanEffect = sumEffects(JingYuanRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    JingYuanRotationDuration = totalJingYuanEffect.actionvalue * 100.0 / JingYuanCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    JingYuanRotation.append(HuohuoCharacter.giveUltEnergy(JingYuanCharacter) * JingYuanRotationDuration / HuohuoRotationDuration)
    JingYuanRotation.append(TingyunCharacter.giveUltEnergy() * JingYuanRotationDuration / TingyunRotationDuration)

    print('##### Rotation Durations #####')
    print('JingYuan: ',JingYuanRotationDuration)
    print('Hanabi: ',HanabiRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Huohuo: ',HuohuoRotationDuration)

    # scale other character's rotation
    HanabiRotation = [x * JingYuanRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    TingyunRotation = [x * JingYuanRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HuohuoRotation = [x * JingYuanRotationDuration / HuohuoRotationDuration for x in HuohuoRotation]

    JingYuanEstimate = DefaultEstimator(f'Jing Yuan {numSkill:.1f}E {numUlt:.0f}Q', JingYuanRotation, JingYuanCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats',
                                    TingyunRotation, TingyunCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    HuohuoEstimate = DefaultEstimator('Huohuo: 3N 1E 1Q, S{:.0f} {}'.format(HuohuoCharacter.lightcone.superposition, HuohuoCharacter.lightcone.name),
                                    HuohuoRotation, HuohuoCharacter, config)

    return([JingYuanEstimate, TingyunEstimate, HanabiEstimate, HuohuoEstimate])
