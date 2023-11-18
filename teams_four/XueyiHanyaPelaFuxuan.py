from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Fuxuan import Fuxuan
from characters.destruction.Xueyi import Xueyi
from characters.harmony.Hanya import Hanya
from characters.nihility.Pela import Pela
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.relicSets.GeniusOfBrilliantStars import GeniusOfBrilliantStars2pc, GeniusOfBrilliantStars4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc

def XueyiHanyaPelaFuxuan(config, breakRatio:float=0.5):
    #%% Xueyi Hanya Pela Fuxuan Characters
    XueyiCharacter = Xueyi(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'BreakEffect'],
                            substats = {'CR': 8, 'CD': 12, 'BreakEffect': 3, 'SPD.flat': 5}),
                            lightcone = OnTheFallOfAnAeon(**config),
                            relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo = GeniusOfBrilliantStars4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                            substats = {'RES': 7, 'SPD.flat': 12, 'CD': 5, 'CR': 4}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                            **config)

    PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                            substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
                            lightcone = ResolutionShinesAsPearlsOfSweat(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
                            **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                            substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                            lightcone = DayOneOfMyNewLife(**config),
                            relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                            **config)
    
    team = [XueyiCharacter, HanyaCharacter, PelaCharacter, FuxuanCharacter]

    #%% Xueyi Hanya Pela Fuxuan Team Buffs
    # Broken Keel Buffs
    for character in [XueyiCharacter, PelaCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel from Hanya',amount=0.1)
    for character in [XueyiCharacter, HanyaCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel from Pela',amount=0.1)
    for character in [XueyiCharacter, HanyaCharacter, PelaCharacter]:
        character.addStat('CD',description='Broken Keel from Fuxuan',amount=0.1)
        
    # Hanya Messenger Buff
    FuxuanCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)
    for character in [XueyiCharacter, PelaCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)

    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(XueyiCharacter,uptime=1.0)
    
    # Pela Debuffs, 3 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotationDuration=3)
        
    # Resolution Shines as Pearls of Sweat uptime
    sweatUptime = (1.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
    sweatUptime += (2.0 / 3.0) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
    sweatUptime = min(1.0, sweatUptime)
    for character in [XueyiCharacter,HanyaCharacter,PelaCharacter,FuxuanCharacter]:
        character.addStat('DefShred',description='Resolution Sweat',
                        amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                        uptime=sweatUptime)

    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Xueyi Hanya Pela Fuxuan Rotations
    numSkillXueyi = 3.0
    numUltXueyi = 1.0
    numBlast = min(3,XueyiCharacter.numEnemies)
    numAllyAttacks = 10.0 # 4 ish hits from hanya, 4 ish hits from pela, 2 ish hits from fu xuan
    numTalentXueyi = numSkillXueyi * (1 + numBlast) + 4 * numUltXueyi + numAllyAttacks
    numTalentXueyi *= 3.0 / (6.0 if XueyiCharacter.eidolon >= 6 else 8.0)
    numTalentXueyi *= breakRatio # balance this with the weakness broken uptime
    XueyiRotation = [  # 140 energy needed. EndTurn needed to factor in his buffs
                XueyiCharacter.useSkill() * numSkillXueyi,
                XueyiCharacter.useUltimate() * numUltXueyi,
                XueyiCharacter.useTalent() * numTalentXueyi,
    ]
    
    numHanyaSkill = 3
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]

    PelaRotation = [PelaCharacter.useBasic() * 3,
                    PelaCharacter.useUltimate(),]

    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% Xueyi Hanya Pela Fuxuan Rotation Math
    totalXueyiEffect = sumEffects(XueyiRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    XueyiRotationDuration = totalXueyiEffect.actionvalue * 100.0 / XueyiCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    # scale other character's rotation
    HanyaRotation = [x * XueyiRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    PelaRotation = [x * XueyiRotationDuration / PelaRotationDuration for x in PelaRotation]
    FuxuanRotation = [x * XueyiRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    XueyiEstimate = DefaultEstimator(f'Xueyi: {numSkillXueyi:.0f}E {numUltXueyi:.0f}Q {numTalentXueyi:.1f}T with {breakRatio*100.0:.0f}% of hits depleting toughness', XueyiRotation, XueyiCharacter, config)
    HanyaEstimate = DefaultEstimator('Hanya {:.0f}E {:.0f}Q S{:.0f} {}, 12 Spd Substats'.format(numHanyaSkill, numHanyaUlt,
                                    HanyaCharacter.lightcone.superposition, HanyaCharacter.lightcone.name), 
                                    HanyaRotation, HanyaCharacter, config)
    PelaEstimate = DefaultEstimator(f'Pela: 3N 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    FuxuanEstimate = DefaultEstimator('Fuxuan: 2N 1E 1Q, S{:.0f} {}'.format(FuxuanCharacter.lightcone.superposition, FuxuanCharacter.lightcone.name),
                                    FuxuanRotation, FuxuanCharacter, config)

    return([XueyiEstimate,HanyaEstimate,PelaEstimate,FuxuanEstimate])