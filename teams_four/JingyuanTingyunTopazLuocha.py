from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.erudition.JingYuan import JingYuan
from characters.harmony.Tingyun import Tingyun
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.erudition.GeniusesRepose import GeniusesRepose
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.hunt.Swordplay import Swordplay
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.relicSets.GrandDukeIncineratedToAshes import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def JingyuanTingyunTopazLuocha(config):
    #%% JingYuan Tingyun Topaz Luocha Characters
    JingYuanCharacter = JingYuan(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.lightning'],
                            substats = {'CD': 5, 'CR': 11, 'SPD.flat': 9, 'ATK.percent': 3}), # get to 140 speed before buffs, to just guarantee battalia crush
                            lightcone = GeniusesRepose(**config),
                            relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(followupStacks=5.2,uptime=1.0), planarset = InertSalsotto(stack=2),
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                            benedictionTarget=JingYuanCharacter,
                            **config)

    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                            substats = {'CR': 5, 'CD': 11, 'ATK.percent': 3, 'SPD.flat': 9}),
                            lightcone = Swordplay(**config),
                            relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 5, 'SPD.flat': 12, 'HP.percent': 4, 'RES': 7}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                            **config)
    
    team = [JingYuanCharacter, TingyunCharacter, TopazCharacter, LuochaCharacter]

    #%% JingYuan Tingyun Topaz Luocha Team Buffs
    # Broken Keel Buffs
    for character in [JingYuanCharacter, TopazCharacter]:
        character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
        
    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff([TopazCharacter],uptime=1.0)
    TopazCharacter.applyVulnerabilityDebuff([JingYuanCharacter],uptime=1.0/JingYuanCharacter.numEnemies)
        
    # Tingyun Messenger Buff
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)
    JingYuanCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/2.0)
    TopazCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(JingYuanCharacter)
    TingyunCharacter.applyUltBuff(JingYuanCharacter)

    # Tingyun and Jing Yuan are going to be out of sync so we just need to try and math out an average rotation
    print('Jing Yuan Speed: ', JingYuanCharacter.getTotalStat('SPD'), ' Tingyun Speed: ', TingyunCharacter.getTotalStat('SPD'))
    jyShortRotation = 2 / JingYuanCharacter.getTotalStat('SPD')
    jyLongRotation = 4 / JingYuanCharacter.getTotalStat('SPD')
    tyRotation = 3 / TingyunCharacter.getTotalStat('SPD')

    longToShort = (tyRotation - jyShortRotation) / jyLongRotation
    print('LongToShort Ratio', longToShort)

    # Use long to short ratio to estimate Jing Yuan Buff
    JingYuanCharacter.addStat('DMG',description='Tingyun Ult',
                            amount=0.65 if TingyunCharacter.eidolon >= 3 else 0.6,
                            uptime=1.0 - longToShort / 2)

    #%% Print Statements
    for character in team:
        character.print()

    #%% JingYuan Tingyun Topaz Luocha Rotations
    TingyunRotation = [ 
            TingyunCharacter.useBasic() * 2, 
            TingyunCharacter.useSkill(),
            TingyunCharacter.useUltimate(),
    ]
        
    lordSpeed = 0.85 # close enough of an estimate

    numSkill = 2.0 + 2.0 * longToShort
    numUlt = 1.0
    numTalents = ( 3 * numSkill * lordSpeed / JingYuanCharacter.getTotalStat('SPD') )  + 2 * numSkill + 3
    JingYuanRotation = [
        JingYuanCharacter.useSkill() * numSkill,
        JingYuanCharacter.useUltimate() * numUlt,
        JingYuanCharacter.useTalent() * numTalents,
        TingyunCharacter.useBenediction(['skill']) * numSkill,
        TingyunCharacter.useBenediction(['ultimate']),
        TingyunCharacter.giveUltEnergy(),
    ]

    numBasicTopaz = 1.5
    numSkillTopaz = 2.5 
    numUltTopaz = 1.0
    TopazRotation = [ # 130 max energy
            TopazCharacter.useBasic() * numBasicTopaz,
            TopazCharacter.useSkill() * numSkillTopaz,
            TopazCharacter.useUltimate() * numUltTopaz,
            TopazCharacter.useTalent(windfall=True) * 2, # two talents from windfall
    ]

    topazTurns = sum([x.actionvalue for x in TopazRotation])
    numbyTurns = topazTurns * 80 / TopazCharacter.getTotalStat('SPD')
    numbyAdvanceForwards = topazTurns / 2 + 1 * 3 / 8 # assume 1 jing yuan followup per rotation 
    TopazRotation.append(TopazCharacter.useTalent(windfall=False) * (numbyTurns + numbyAdvanceForwards)) # about 1 talent per basic/skill

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast

    #%% JingYuan Tingyun Topaz Luocha Rotation Math
    totalJingYuanEffect = sumEffects(JingYuanRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    JingYuanRotationDuration = totalJingYuanEffect.actionvalue * 100.0 / JingYuanCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's rotation
    TingyunRotation = [x * JingYuanRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    TopazRotation = [x * JingYuanRotationDuration / TopazRotationDuration for x in TopazRotation]
    LuochaRotation = [x * JingYuanRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    JingYuanEstimate = DefaultEstimator(f'Jing Yuan {numSkill:.1f}E {numUlt:.0f}Q', JingYuanRotation, JingYuanCharacter, config)
    TopazEstimate = DefaultEstimator(f'Topaz: {numSkillTopaz:.1f}E {numBasicTopaz:.1f}N {numbyTurns + numbyAdvanceForwards:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.1f} Tingyun S{TingyunCharacter.lightcone.superposition:.1f} {TingyunCharacter.lightcone.name}, 12 spd substats', 
                                    TingyunRotation, TingyunCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([JingYuanEstimate,TopazEstimate,TingyunEstimate,LuochaEstimate])