from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Clara import Clara
from characters.harmony.Asta import Asta
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.hunt.Swordplay import Swordplay
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.GrandDukeIncineratedToAshes import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def ClaraTopazAstaLuocha(config):
    #%% Clara Topaz Asta Luocha Characters
    ClaraCharacter = Clara(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.physical'],
                                    substats = {'CR': 8, 'CD': 12, 'ATK.percent': 3, 'SPD.flat': 5}),
                                    lightcone = OnTheFallOfAnAeon(uptime = 0.25, stacks=5.0, **config),
                                    relicsetone = ChampionOfStreetwiseBoxing2pc(),
                                    relicsettwo = ChampionOfStreetwiseBoxing4pc(),
                                    planarset = FirmamentFrontlineGlamoth(stacks=2),
                                    **config)

    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'ATK.percent', 'CR', 'ATK.percent'],
                                    substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                                    lightcone = Swordplay(**config),
                                    relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                                    **config)

    AstaCharacter = Asta(RelicStats(mainstats = ['ER', 'ATK.percent', 'CR', 'ATK.percent'],
                                    substats = {'CR': 8, 'CD': 12, 'HP.percent': 3, 'ATK.percent': 5}),
                                    lightcone = MemoriesOfThePast(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(uptime=0.5), planarset = BrokenKeel(),
                                    **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 5, 'SPD.flat': 12, 'HP.percent': 4, 'RES': 7}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                                    **config)
    
    team = [ClaraCharacter, TopazCharacter, AstaCharacter, LuochaCharacter]

    #%% Clara Topaz Asta Luocha Team Buffs
    for character in [TopazCharacter, ClaraCharacter, AstaCharacter]:
        character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
    for character in [TopazCharacter, ClaraCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel from Asta',amount=0.1)

    # messenger 4 pc buffs:
    ClaraCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    TopazCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5*3/4)

    # Asta Buffs
    AstaCharacter.applyChargingBuff(team)
    AstaCharacter.applyTraceBuff(team)

    # Luocha's uptime is lower because he is very fast with the multiplication light cone
    AstaCharacter.applyUltBuff([TopazCharacter,ClaraCharacter,AstaCharacter],uptime=1.0)
    AstaCharacter.applyUltBuff([LuochaCharacter],uptime=0.75)

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff([TopazCharacter],uptime=1.0)
    TopazCharacter.applyVulnerabilityDebuff([ClaraCharacter],uptime=1.0/ClaraCharacter.numEnemies)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Clara Topaz Asta Luocha Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long
    numEnemyAttacks = ClaraCharacter.enemySpeed * ClaraCharacter.numEnemies * 2 / ClaraCharacter.getTotalStat('SPD')
    numEnhancedTalents = 2
    numUnenhancedTalents = (numEnemyAttacks - numEnhancedTalents) * (5*6) / (5*6 + 3 + 4 + 4)
    numSvarogCounters = numEnemyAttacks * (5*6) / (5*6 + 3 + 4 + 4)

    ClaraRotation = [ # 110 max energy
            ClaraCharacter.useSkill() * 2,
            ClaraCharacter.useMarkOfSvarog() * numSvarogCounters, 
            ClaraCharacter.useTalent(enhanced=True) * numEnhancedTalents,
            ClaraCharacter.useUltimate(),
    ]

    ClaraCharacter.stats['Vulnerability'].pop() # remove the previous vulnerability buff
    ClaraCharacter.addStat('Vulnerability',description='Topaz Vulnerability',
                        amount=0.55 if TopazCharacter.eidolon>= 3 else 0.5)
    ClaraRotation.append(ClaraCharacter.useTalent(enhanced=False) * numUnenhancedTalents)

    TopazRotation = [ # 130 max energy
            TopazCharacter.useBasic() * 4,
            TopazCharacter.useSkill(),
            TopazCharacter.useUltimate(),
            TopazCharacter.useTalent(windfall=True) * 2, # two talents from windfall
    ]

    topazTurns = sum([x.actionvalue for x in TopazRotation])
    claraTurns = sum([x.actionvalue for x in ClaraRotation])
    numbyTurns = topazTurns * 80 / TopazCharacter.getTotalStat('SPD')
    claraFollowups = (numEnhancedTalents + numUnenhancedTalents / TopazCharacter.numEnemies) * (topazTurns / TopazCharacter.getTotalStat('SPD')) / (claraTurns / ClaraCharacter.getTotalStat('SPD'))
    numbyAdvanceForwards = topazTurns / 2 + claraFollowups * 3 / 8 # treat clara followups as 0.375 advances because they might be out of sync    
    TopazRotation.append(TopazCharacter.useTalent(windfall=False) * (numbyTurns + numbyAdvanceForwards)) # about 1 talent per basic/skill

    AstaRotation = [AstaCharacter.useSkill() * 2,
                    AstaCharacter.useUltimate() * 1,]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast

    #%% Clara Topaz Asta Luocha Rotation Math

    totalClaraEffect = sumEffects(ClaraRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalAstaEffect = sumEffects(AstaRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    ClaraRotationDuration = totalClaraEffect.actionvalue * 100.0 / ClaraCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    AstaRotationDuration = totalAstaEffect.actionvalue * 100.0 / AstaCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Clara: ',ClaraRotationDuration)
    print('Topaz: ',TopazRotationDuration)
    print('Asta: ',AstaRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # Scale other character's rotation
    TopazRotation = [x * ClaraRotationDuration / TopazRotationDuration for x in TopazRotation]
    AstaRotation = [x * ClaraRotationDuration / AstaRotationDuration for x in AstaRotation]
    LuochaRotation = [x * ClaraRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    ClaraEstimate = DefaultEstimator(f'Clara: 2E {numSvarogCounters:.1f}T 1Q', ClaraRotation, ClaraCharacter, config)
    TopazEstimate = DefaultEstimator(f'Topaz: 1E 4N {numbyTurns + numbyAdvanceForwards:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    AstaEstimate = DefaultEstimator(f'Slow Asta: 2E 1Q, S{AstaCharacter.lightcone.superposition:d} {AstaCharacter.lightcone.name}', 
                                    AstaRotation, AstaCharacter, config)
    LuochaEstimate = DefaultEstimator(f'Luocha: 3N 1E 1Q, S{LuochaCharacter.lightcone.superposition:d} {LuochaCharacter.lightcone.name}', 
                                    LuochaRotation, LuochaCharacter, config)

    return([ClaraEstimate, TopazEstimate, LuochaEstimate, AstaEstimate])

