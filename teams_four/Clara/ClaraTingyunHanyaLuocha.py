from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Clara import Clara
from characters.harmony.Tingyun import Tingyun
from characters.harmony.Hanya import Hanya
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def ClaraTingyunHanyaLuocha(config):
    #%% Clara Tingyun Hanya Luocha Characters
    ClaraCharacter = Clara(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.physical'],
                            substats = {'CR': 8, 'CD': 12, 'ATK.percent': 3, 'SPD.flat': 5}),
                            lightcone = OnTheFallOfAnAeon(uptime = 0.5, stacks=4.0, **config),
                            relicsetone = ChampionOfStreetwiseBoxing2pc(),
                            relicsettwo = ChampionOfStreetwiseBoxing4pc(),
                            planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                            benedictionTarget=ClaraCharacter,
                            **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                            substats = {'CR': 8, 'SPD.flat': 12, 'CD': 5, 'ATK.percent': 3}),
                            lightcone = PlanetaryRendezvous(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 5, 'SPD.flat': 12, 'HP.percent': 4, 'RES': 7}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                            **config)
    
    team = [ClaraCharacter, TingyunCharacter, HanyaCharacter, LuochaCharacter]

    #%% Clara Tingyun Hanya Luocha Team Buffs
    for character in [TingyunCharacter, ClaraCharacter, HanyaCharacter]:
        character.addStat('CD',description='Broken Keel from Luocha',amount=0.1)
    for character in [TingyunCharacter, ClaraCharacter, LuochaCharacter]:
        character.addStat('DMG.physical',description='Penacony from Hanya',amount=0.1)
    for character in team:
        character.addStat('DMG.physical',description='Planetary Rendezvous',amount=0.24)

    # Hanya Messenger 4 pc
    for character in [ClaraCharacter, TingyunCharacter, LuochaCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # messenger 4 pc buffs from Tingyun:
    ClaraCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    HanyaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5)
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=0.5*3/4)
    
    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(ClaraCharacter,uptime=1.0)

    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(ClaraCharacter)
    TingyunCharacter.applyUltBuff(ClaraCharacter)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Clara Tingyun Hanya Luocha Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long
    numSkillClara = 1.25
    numEnemyAttacks = ClaraCharacter.enemySpeed * ClaraCharacter.numEnemies * numSkillClara / ClaraCharacter.getTotalStat('SPD')
    numEnhancedTalents = 2
    numUnenhancedTalents = (numEnemyAttacks - numEnhancedTalents) * (5*6) / (5*6 + 4 + 4 + 4)
    numSvarogCounters = numEnemyAttacks * (5*6) / (5*6 + 4 + 4 + 4)

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
    
    numHanyaSkill = 4
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Clara Tingyun Hanya Luocha Rotation Math

    totalClaraEffect = sumEffects(ClaraRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    ClaraRotationDuration = totalClaraEffect.actionvalue * 100.0 / ClaraCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    ClaraRotation.append(TingyunCharacter.giveUltEnergy() * ClaraRotationDuration / TingyunRotationDuration)
    
    print('##### Rotation Durations #####')
    print('Clara: ',ClaraRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Hanya: ',HanyaRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # Scale other character's rotation
    TingyunRotation = [x * ClaraRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HanyaRotation = [x * ClaraRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    LuochaRotation = [x * ClaraRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    ClaraEstimate = DefaultEstimator(f'Clara: {numSkillClara:.1f}E {numSvarogCounters:.1f}T 1Q', ClaraRotation, ClaraCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats',
                                    TingyunRotation, TingyunCharacter, config)
    HanyaEstimate = DefaultEstimator(f'Hanya {numHanyaSkill:.0f}E {numHanyaUlt:.0f}Q S{HanyaCharacter.lightcone.superposition:.0f} {HanyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanyaRotation, HanyaCharacter, config)
    LuochaEstimate = DefaultEstimator(f'Luocha: 3N 1E 1Q, S{LuochaCharacter.lightcone.superposition:d} {LuochaCharacter.lightcone.name}', 
                                    LuochaRotation, LuochaCharacter, config)

    return([ClaraEstimate, TingyunEstimate, HanyaEstimate, LuochaEstimate])

