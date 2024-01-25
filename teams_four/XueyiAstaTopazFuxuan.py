from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Fuxuan import Fuxuan
from characters.destruction.Xueyi import Xueyi
from characters.harmony.Asta import Asta
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.GeniusOfBrilliantStars import GeniusOfBrilliantStars2pc, GeniusOfBrilliantStars4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc

def XueyiAstaTopazFuxuan(config, breakRatio:float=0.5):
    #%% Xueyi Asta Topaz Fuxuan Characters
    XueyiCharacter = Xueyi(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'BreakEffect'],
                            substats = {'CR': 8, 'CD': 12, 'BreakEffect': 5, 'SPD.flat': 3}),
                            lightcone = OnTheFallOfAnAeon(uptime=1.0,**config),
                            relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo = GeniusOfBrilliantStars4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    AstaCharacter = Asta(RelicStats(mainstats = ['ER', 'ATK.percent', 'CR', 'ATK.percent'],
                            substats = {'CR': 8, 'CD': 12, 'HP.percent': 3, 'ATK.percent': 5}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(uptime=0.5), planarset = BrokenKeel(),
                            **config)

    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'ATK.percent', 'CR', 'ATK.percent'],
                            substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                            lightcone = Swordplay(**config),
                            relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = InertSalsotto(),
                            **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                            substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                            lightcone = DayOneOfMyNewLife(**config),
                            relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                            **config)
    
    team = [XueyiCharacter, AstaCharacter, TopazCharacter, FuxuanCharacter]

    #%% Xueyi Asta Topaz Fuxuan Team Buffs
    # Broken Keel Buffs
    for character in [XueyiCharacter, TopazCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel from Asta',amount=0.1)
    for character in [XueyiCharacter, AstaCharacter, TopazCharacter]:
        character.addStat('CD',description='Broken Keel from Fuxuan',amount=0.1)
        
    # Asta Messenger Buff
    FuxuanCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)
    for character in [XueyiCharacter, TopazCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)

    # Asta Buffs
    AstaCharacter.applyChargingBuff(team)
    AstaCharacter.applyTraceBuff(team)
    AstaCharacter.applyUltBuff(team,uptime=1.0)
    
    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff([TopazCharacter,XueyiCharacter],uptime=0.5)

    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Xueyi Asta Topaz Fuxuan Rotations
    numSkillXueyi = 3.0
    numUltXueyi = 1.0
    numBlast = min(3,XueyiCharacter.numEnemies)
    numAllyAttacks = 14.0 # 4 ish hits from Asta, 8 ish hits from Topaz, 2 ish hits from fu xuan
    numTalentXueyi = numSkillXueyi * (1 + numBlast) + 4 * numUltXueyi + numAllyAttacks
    numTalentXueyi *= 3.0 / (6.0 if XueyiCharacter.eidolon >= 6 else 8.0)
    numTalentXueyi *= breakRatio # balance this with the weakness broken uptime
    XueyiRotation = [  # 140 energy needed. EndTurn needed to factor in his buffs
                XueyiCharacter.useSkill() * numSkillXueyi,
                XueyiCharacter.useUltimate() * numUltXueyi,
                XueyiCharacter.useTalent() * numTalentXueyi,
    ]
    
    AstaRotation = [AstaCharacter.useSkill() * 2,
                    AstaCharacter.useUltimate() * 1,]

    numBasicTopaz = 0.0
    numSkillTopaz = 3.83
    TopazRotation = [ # 130 max energy
            TopazCharacter.useBasic() * numBasicTopaz,
            TopazCharacter.useSkill() * numSkillTopaz,
            TopazCharacter.useUltimate(),
            TopazCharacter.useTalent(windfall=True) * 2, # two talents from windfall
    ]

    topazTurns = sum([x.actionvalue for x in TopazRotation])
    numbyTurns = topazTurns * 80 / TopazCharacter.getTotalStat('SPD')
    numbyAdvanceForwards = topazTurns / 2 + numTalentXueyi / TopazCharacter.numEnemies
    TopazRotation.append(TopazCharacter.useTalent(windfall=False) * (numbyTurns + numbyAdvanceForwards*0.8)) # about 1 talent per basic/skill, 0.8 on advances because I want to assume some desync with Hanya in the mix

    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% Xueyi Asta Topaz Fuxuan Rotation Math
    totalXueyiEffect = sumEffects(XueyiRotation)
    totalAstaEffect = sumEffects(AstaRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    XueyiRotationDuration = totalXueyiEffect.actionvalue * 100.0 / XueyiCharacter.getTotalStat('SPD')
    AstaRotationDuration = totalAstaEffect.actionvalue * 100.0 / AstaCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    # scale other character's rotation
    AstaRotation = [x * XueyiRotationDuration / AstaRotationDuration for x in AstaRotation]
    TopazRotation = [x * XueyiRotationDuration / TopazRotationDuration for x in TopazRotation]
    FuxuanRotation = [x * XueyiRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    XueyiEstimate = DefaultEstimator(f'Xueyi: {numSkillXueyi:.0f}E {numUltXueyi:.0f}Q {numTalentXueyi:.1f}T with {breakRatio*100.0:.0f}% of hits depleting toughness', XueyiRotation, XueyiCharacter, config)
    AstaEstimate = DefaultEstimator(f'Slow Asta: 2E 1Q, S{AstaCharacter.lightcone.superposition:d} {AstaCharacter.lightcone.name}', 
                                    AstaRotation, AstaCharacter, config)
    TopazEstimate = DefaultEstimator(f'Topaz: {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numbyTurns + numbyAdvanceForwards:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    FuxuanEstimate = DefaultEstimator('Fuxuan: 2N 1E 1Q, S{:.0f} {}'.format(FuxuanCharacter.lightcone.superposition, FuxuanCharacter.lightcone.name),
                                    FuxuanRotation, FuxuanCharacter, config)

    return([XueyiEstimate,AstaEstimate,TopazEstimate,FuxuanEstimate])