from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.harmony.Hanya import Hanya
from characters.harmony.Tingyun import Tingyun
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.hunt.Swordplay import Swordplay
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.GrandDukeIncineratedToAshes import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def TopazTingyunHanyaLuocha(config):
    #%% Topaz Tingyun Hanya Luocha Characters
    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'ATK.percent', 'CR', 'ATK.percent'],
                        substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                        lightcone = Swordplay(**config),
                        relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                        benedictionTarget=TopazCharacter,
                        **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                        substats = {'CR': 8, 'SPD.flat': 12, 'CD': 5, 'ATK.percent': 3}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 5, 'SPD.flat': 12, 'HP.percent': 4, 'RES': 7}),
                        lightcone = Multiplication(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [TopazCharacter, TingyunCharacter, HanyaCharacter, LuochaCharacter]

    #%% Topaz Tingyun Hanya Luocha Team Buffs
    for character in [TopazCharacter, TingyunCharacter, HanyaCharacter]:
        character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
    for character in [TopazCharacter, TingyunCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel from Hanya',amount=0.1)
        
    # messenger 4 pc buffs from Hanya:
    TopazCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
    TingyunCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4)

    # messenger 4 pc buffs from Tingyun:
    TopazCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
    HanyaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4)

    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(TopazCharacter,uptime=1.0)
    
    # Tingyun Buffs
    TopazCharacter.addStat('SPD.percent',description='Tingyun E1',amount=0.20,uptime=1.0/3.0)
    TopazCharacter.addStat('ATK.percent',description='Benediction',
                            amount=0.55 if TingyunCharacter.eidolon >= 5 else 0.50)
    TopazCharacter.addStat('DMG',description='Tingyun Ult',amount=0.65 if TingyunCharacter.eidolon >= 3 else 0.6,uptime=2.0/3.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Topaz Tingyun Hanya Luocha Rotations
    numSkillTopaz = 2.5
    numUltTopaz = 1.0
    TopazRotation = [ # 130 max energy
            TopazCharacter.useSkill() * numSkillTopaz,
            TopazCharacter.useUltimate() * numUltTopaz,
            TopazCharacter.useTalent(windfall=True) * 2, # two talents from windfall
            TingyunCharacter.giveUltEnergy() * ( TingyunCharacter.getTotalStat('SPD') * 2.5 / TopazCharacter.getTotalStat('SPD') / 3.0 ), # average tingyun energy
    ]

    topazTurns = sum([x.actionvalue for x in TopazRotation])
    numbyTurns = topazTurns * 80 / TopazCharacter.getTotalStat('SPD')
    numbyAdvanceForwards = topazTurns / 2    
    TopazRotation.append(TopazCharacter.useTalent(windfall=False) * (numbyTurns + numbyAdvanceForwards)) # about 1 talent per basic/skill

    numHanyaSkill = 3
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]

    TingyunRotation = [ 
            TingyunCharacter.useBasic() * 2, 
            TingyunCharacter.useSkill(),
            TingyunCharacter.useUltimate(),
    ]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast

    #%% Topaz Tingyun Hanya Luocha Rotation Math

    totalTopazEffect = sumEffects(TopazRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Topaz: ',TopazRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Hanya: ',HanyaRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # Scale other character's rotation
    TingyunRotation = [x * TopazRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HanyaRotation = [x * TopazRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    LuochaRotation = [x * TopazRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    TopazEstimate = DefaultEstimator(f'Topaz: {numSkillTopaz:.1f}E {numbyTurns + numbyAdvanceForwards:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.1f} Tingyun S{TingyunCharacter.lightcone.superposition:.1f} {TingyunCharacter.lightcone.name}, 12 spd substats', [totalTingyunEffect], TingyunCharacter, config)
    HanyaEstimate = DefaultEstimator('E0 Hanya S{:.0f} {}, 12 Spd Substats'.format(HanyaCharacter.lightcone.superposition, HanyaCharacter.lightcone.name), 
                                      HanyaRotation, HanyaCharacter, config)
    LuochaEstimate = DefaultEstimator(f'Luocha: 3N 1E 1Q, S{LuochaCharacter.lightcone.superposition:d} {LuochaCharacter.lightcone.name}', 
                                    LuochaRotation, LuochaCharacter, config)

    return([TopazEstimate, TingyunEstimate, HanyaEstimate, LuochaEstimate])
