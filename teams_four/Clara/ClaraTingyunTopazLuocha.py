from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Clara import Clara
from characters.harmony.Tingyun import Tingyun
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.hunt.Swordplay import Swordplay
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def ClaraTingyunTopazLuocha(config):
    #%% Clara Tingyun Topaz Luocha Characters
    ClaraCharacter = Clara(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.physical'],
                            substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                            lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=5.0, **config),
                            relicsetone = ChampionOfStreetwiseBoxing2pc(),
                            relicsettwo = ChampionOfStreetwiseBoxing4pc(),
                            planarset = InertSalsotto(),
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                            benedictionTarget=ClaraCharacter,
                            **config)

    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                            substats = {'CR': 5, 'CD': 12, 'ATK.percent': 3, 'SPD.flat': 8}),
                            lightcone = Swordplay(**config),
                            relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 5, 'SPD.flat': 12, 'HP.percent': 4, 'RES': 7}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                            **config)
    
    team = [ClaraCharacter, TingyunCharacter, TopazCharacter, LuochaCharacter]

    #%% Clara Tingyun Topaz Luocha Team Buffs
    for character in [TingyunCharacter, ClaraCharacter, TopazCharacter]:
        character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)

    # messenger 4 pc buffs from Tingyun:
    ClaraCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    TopazCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5*3/4)
    
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(ClaraCharacter)
    TingyunCharacter.applyUltBuff(ClaraCharacter)
    
    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff([TopazCharacter],uptime=1.0)
    TopazCharacter.applyVulnerabilityDebuff([ClaraCharacter],uptime=1.0/ClaraCharacter.numEnemies)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Clara Tingyun Topaz Luocha Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long
    numSkillClara = 1.25
    numEnemyAttacks = ClaraCharacter.enemySpeed * ClaraCharacter.numEnemies * numSkillClara / ClaraCharacter.getTotalStat('SPD')
    numEnhancedTalents = 2
    numUnenhancedTalents = (numEnemyAttacks - numEnhancedTalents) * (5*6) / (5*6 + 3 + 4 + 4)
    numSvarogCounters = numEnemyAttacks * (5*6) / (5*6 + 3 + 4 + 4)

    ClaraRotation = [ # 110 max energy
            ClaraCharacter.useSkill() * numSkillClara,
            ClaraCharacter.useMarkOfSvarog() * numSvarogCounters, 
            ClaraCharacter.useTalent(enhanced=True) * numEnhancedTalents,
            ClaraCharacter.useUltimate(),
            ClaraCharacter.useTalent(enhanced=False) * numUnenhancedTalents,
            TingyunCharacter.useBenediction(['skill']) * numSkillClara,
            TingyunCharacter.useBenediction(['talent','followup']) * numEnhancedTalents,
            TingyunCharacter.useBenediction(['talent','followup']) * numUnenhancedTalents,
    ]
    
    TingyunRotation = [ 
        TingyunCharacter.useBasic() * 2, 
        TingyunCharacter.useSkill(),
        TingyunCharacter.useUltimate(),
    ]

    numBasicTopaz = 1.0
    numSkillTopaz = 3.0
    TopazRotation = [ # 130 max energy
            TopazCharacter.useBasic() * numBasicTopaz,
            TopazCharacter.useSkill() * numSkillTopaz,
            TopazCharacter.useUltimate(),
            TopazCharacter.useTalent(windfall=True) * 2, # two talents from windfall
    ]


    topazTurns = sum([x.actionvalue for x in TopazRotation])
    claraTurns = sum([x.actionvalue for x in ClaraRotation])
    numbyTurns = topazTurns * 80 / TopazCharacter.getTotalStat('SPD')
    claraFollowups = (numEnhancedTalents + numUnenhancedTalents / TopazCharacter.numEnemies) * (topazTurns / TopazCharacter.getTotalStat('SPD')) / (claraTurns / ClaraCharacter.getTotalStat('SPD'))
    numbyAdvanceForwards = topazTurns / 2 + claraFollowups * 3 / 8 # treat clara followups as 0.375 advances because they might be out of sync    
    TopazRotation.append(TopazCharacter.useTalent(windfall=False) * (numbyTurns + numbyAdvanceForwards)) # about 1 talent per basic/skill

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Clara Tingyun Topaz Luocha Rotation Math

    totalClaraEffect = sumEffects(ClaraRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    ClaraRotationDuration = totalClaraEffect.actionvalue * 100.0 / ClaraCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    ClaraRotation.append(TingyunCharacter.giveUltEnergy() * ClaraRotationDuration / TingyunRotationDuration)
    
    print('##### Rotation Durations #####')
    print('Clara: ',ClaraRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Topaz: ',TopazRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # Scale other character's rotation
    TingyunRotation = [x * ClaraRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    TopazRotation = [x * ClaraRotationDuration / TopazRotationDuration for x in TopazRotation]
    LuochaRotation = [x * ClaraRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    ClaraEstimate = DefaultEstimator(f'Clara: {numSkillClara:.1f}E {numSvarogCounters:.1f}T 1Q', ClaraRotation, ClaraCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats', TingyunRotation, TingyunCharacter, config)
    TopazEstimate = DefaultEstimator(f'Topaz: {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numbyTurns + numbyAdvanceForwards:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    LuochaEstimate = DefaultEstimator(f'Luocha: 3N 1E 1Q, S{LuochaCharacter.lightcone.superposition:d} {LuochaCharacter.lightcone.name}', 
                                    LuochaRotation, LuochaCharacter, config)

    return([ClaraEstimate, TopazEstimate, TingyunEstimate, LuochaEstimate])

