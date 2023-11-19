from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.hunt.DrRatio import DrRatio
from characters.harmony.Asta import Asta
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.Swordplay import Swordplay
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def DrRatioTopazAstaLuocha(config):
    #%% DrRatio Topaz Asta Luocha Characters
    DrRatioCharacter = DrRatio(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
                                    substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = WastelanderOfBanditryDesert2pc(),
                                    relicsettwo = WastelanderOfBanditryDesert4pc(),
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
    
    team = [DrRatioCharacter, TopazCharacter, AstaCharacter, LuochaCharacter]

    #%% DrRatio Topaz Asta Luocha Team Buffs
    for character in [TopazCharacter, DrRatioCharacter, AstaCharacter]:
        character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
    for character in [TopazCharacter, DrRatioCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel from Asta',amount=0.1)

    # messenger 4 pc buffs:
    DrRatioCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    TopazCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5*3/4)

    # Asta Buffs
    AstaCharacter.applyChargingBuff(team)
    AstaCharacter.applyTraceBuff(team)

    # Luocha's uptime is lower because he is very fast with the multiplication light cone
    AstaCharacter.applyUltBuff([TopazCharacter,DrRatioCharacter,AstaCharacter],uptime=1.0)
    AstaCharacter.applyUltBuff([LuochaCharacter],uptime=0.75)

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff([TopazCharacter,DrRatioCharacter],uptime=1.0)
    
    # Dr Ratio Buff
    DrRatioCharacter.applyTalentBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% DrRatio Topaz Asta Luocha Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long

    numSkillRatio = 4.0
    numUltRatio = 1.0
    numTalentRatio = numSkillRatio + 2 * numUltRatio
    DrRatioRotation = [ # 110 max energy
            DrRatioCharacter.useSkill() * numSkillRatio,
            DrRatioCharacter.useUltimate() * numUltRatio,
            DrRatioCharacter.useTalent() * numTalentRatio,
    ]

    numBasicTopaz = 4.0
    numSkillTopaz = 1.0
    TopazRotation = [ # 130 max energy
            TopazCharacter.useBasic() * numBasicTopaz,
            TopazCharacter.useSkill() * numSkillTopaz,
            TopazCharacter.useUltimate(),
            TopazCharacter.useTalent(windfall=True) * 2, # two talents from windfall
    ]

    topazTurns = sum([x.actionvalue for x in TopazRotation])
    numbyTurns = topazTurns * 80 / TopazCharacter.getTotalStat('SPD')
    numbyAdvanceForwards = topazTurns / 2 + numTalentRatio    
    TopazRotation.append(TopazCharacter.useTalent(windfall=False) * (numbyTurns + numbyAdvanceForwards)) # about 1 talent per basic/skill

    AstaRotation = [AstaCharacter.useSkill() * 2,
                    AstaCharacter.useUltimate() * 1,]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% DrRatio Topaz Asta Luocha Rotation Math

    totalDrRatioEffect = sumEffects(DrRatioRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalAstaEffect = sumEffects(AstaRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    DrRatioRotationDuration = totalDrRatioEffect.actionvalue * 100.0 / DrRatioCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    AstaRotationDuration = totalAstaEffect.actionvalue * 100.0 / AstaCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('DrRatio: ',DrRatioRotationDuration)
    print('Topaz: ',TopazRotationDuration)
    print('Asta: ',AstaRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # Scale other character's rotation
    TopazRotation = [x * DrRatioRotationDuration / TopazRotationDuration for x in TopazRotation]
    AstaRotation = [x * DrRatioRotationDuration / AstaRotationDuration for x in AstaRotation]
    LuochaRotation = [x * DrRatioRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    DrRatioEstimate = DefaultEstimator(f'DrRatio: {numSkillRatio:.0f}E {numTalentRatio:.1f}T {numUltRatio:.0f}Q, max debuffs on target', DrRatioRotation, DrRatioCharacter, config)
    TopazEstimate = DefaultEstimator(f'Topaz: {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numbyTurns + numbyAdvanceForwards:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    AstaEstimate = DefaultEstimator(f'Slow Asta: 2E 1Q, S{AstaCharacter.lightcone.superposition:d} {AstaCharacter.lightcone.name}', 
                                    AstaRotation, AstaCharacter, config)
    LuochaEstimate = DefaultEstimator(f'Luocha: 3N 1E 1Q, S{LuochaCharacter.lightcone.superposition:d} {LuochaCharacter.lightcone.name}', 
                                    LuochaRotation, LuochaCharacter, config)

    return([DrRatioEstimate, TopazEstimate, LuochaEstimate, AstaEstimate])

