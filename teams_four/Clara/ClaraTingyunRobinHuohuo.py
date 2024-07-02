from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Huohuo import Huohuo
from characters.destruction.Clara import Clara
from characters.harmony.Tingyun import Tingyun
from characters.harmony.Robin import Robin
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.PostOpConversation import PostOpConversation
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.ForTomorrowsJourney import ForTomorrowsJourney
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc

def ClaraTingyunRobinHuohuo(config):
    #%% Clara Tingyun Robin Huohuo Characters
    ClaraCharacter = Clara(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.physical'],
                            substats = {'CD': 8, 'CR': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                            lightcone = OnTheFallOfAnAeon(uptime = 0.5, stacks=4.0, **config),
                            relicsetone = ChampionOfStreetwiseBoxing2pc(),
                            relicsettwo = ChampionOfStreetwiseBoxing4pc(),
                            planarset = InertSalsotto(),
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = DanceDanceDance(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = FleetOfTheAgeless(),
                            benedictionTarget=ClaraCharacter,
                            **config)
    
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 11, 'SPD.flat': 9, 'RES': 3, 'ATK.flat': 5}),
                            lightcone = ForTomorrowsJourney(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                            **config)

    HuohuoCharacter = Huohuo(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'HP.flat': 3, 'RES': 6}),
                        lightcone = PostOpConversation(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [ClaraCharacter, TingyunCharacter, RobinCharacter, HuohuoCharacter]

    #%% Clara Tingyun Robin Huohuo Team Buffs
    for character in [TingyunCharacter, ClaraCharacter, RobinCharacter]:
        character.addStat('CD',description='Broken Keel from Huohuo',amount=0.1)
    for character in [RobinCharacter, ClaraCharacter, RobinCharacter]:
        character.addStat('ATK.percent',description='Fleet from Tingyun',amount=0.08)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinUltUptime = 0.5 # assume better robin ult uptime because of shorter robin rotation
    RobinCharacter.applyUltBuff([ClaraCharacter,TingyunCharacter,HuohuoCharacter],uptime=RobinUltUptime)
    
    # Robin Messenger 4 pc
    for character in [ClaraCharacter, TingyunCharacter, HuohuoCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Messenger Buff
    for character in [ClaraCharacter, RobinCharacter, HuohuoCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(ClaraCharacter)
    TingyunCharacter.applyUltBuff(ClaraCharacter,targetSpdMult=RobinCharacter.getTotalStat('SPD')/ClaraCharacter.getTotalStat('SPD'))
    
    # Huohuo Buffs
    HuohuoCharacter.applyUltBuff([TingyunCharacter,RobinCharacter],uptime=2.0/4.0)
    HuohuoCharacter.applyUltBuff([ClaraCharacter],uptime=2.0/5.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Clara Tingyun Robin Huohuo Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long
    numSkillClara = 0.9
    numEnemyAttacks = ClaraCharacter.enemySpeed * ClaraCharacter.numEnemies * numSkillClara / (RobinCharacter.getTotalStat('SPD') / 0.92 ) # enemy attacks now scale to Robin speed, account for S5 dance dance in denominator
    numEnhancedTalents = 2
    numUnenhancedTalents = (numEnemyAttacks - numEnhancedTalents) * (5*6) / (5*6 + 6 + 4 + 4)
    numSvarogCounters = numEnemyAttacks * (5*6) / (5*6 + 6 + 4 + 4)

    ClaraRotation = [ # 110 max energy
            ClaraCharacter.useSkill() * numSkillClara,
            ClaraCharacter.useMarkOfSvarog() * numSkillClara, 
            ClaraCharacter.useTalent(enhanced=True) * numEnhancedTalents,
            ClaraCharacter.useUltimate(),
            ClaraCharacter.useTalent(enhanced=False) * numUnenhancedTalents,
            TingyunCharacter.useBenediction(['skill']) * numSkillClara,
            TingyunCharacter.useBenediction(['talent','followup']) * numEnhancedTalents,
            TingyunCharacter.useBenediction(['talent','followup']) * numUnenhancedTalents,
            RobinCharacter.useAdvanceForward() * numSkillClara / 4.0,
            ]

    RobinRotationClara = [RobinCharacter.useTalent() * (numSkillClara + numEnhancedTalents + numUnenhancedTalents)]
    RobinRotationClara += [RobinCharacter.useConcertoDamage(['skill']) * numSkillClara * RobinUltUptime]
    RobinRotationClara += [RobinCharacter.useConcertoDamage(['followup']) * (numEnhancedTalents + numUnenhancedTalents) * RobinUltUptime]
    
    TingyunRotation = [ 
        TingyunCharacter.useBasic() * 2, 
        TingyunCharacter.useSkill(),
        TingyunCharacter.useUltimate(),
        RobinCharacter.useAdvanceForward() * 3.0 / 4.0,
    ]
    
    RobinRotationTingyun = [RobinCharacter.useTalent() * (2.0)]
    RobinRotationTingyun += [RobinCharacter.useConcertoDamage(['basic']) * 2.0 * RobinUltUptime]
    
    numBasicRobin = 2.0
    numSkillRobin = 1.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0) # apply robin buff after we calculate damage for her basics

    numHuohuoBasic = 3.0
    numHuohuoSkill = 1.0
    HuohuoRotation = [HuohuoCharacter.useBasic() * numHuohuoBasic,
                    HuohuoCharacter.useSkill() * numHuohuoSkill,
                    HuohuoCharacter.useUltimate(),
                    RobinCharacter.useAdvanceForward() * (numHuohuoBasic + numHuohuoSkill) / 4.0]
    
    RobinRotationHuohuo = [RobinCharacter.useTalent() * (3.0)]
    RobinRotationHuohuo += [RobinCharacter.useConcertoDamage(['basic']) * 3.0 * RobinUltUptime]

    #%% Clara Tingyun Robin Huohuo Rotation Math

    totalClaraEffect = sumEffects(ClaraRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    ClaraRotationDuration = totalClaraEffect.actionvalue * 100.0 / ClaraCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()

    DanceDanceDanceEffect.actionvalue = -0.24
    RobinCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    RobinRotation.append(deepcopy(DanceDanceDanceEffect))
    totalRobinEffect = sumEffects(RobinRotation)
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')

    DanceDanceDanceEffect.actionvalue = -0.24 * ClaraRotationDuration / RobinRotationDuration
    ClaraCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    ClaraRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * TingyunRotationDuration / RobinRotationDuration
    TingyunCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    TingyunRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * HuohuoRotationDuration / RobinRotationDuration
    HuohuoCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    HuohuoRotation.append(deepcopy(DanceDanceDanceEffect))
    
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalClaraEffect = sumEffects(ClaraRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    ClaraRotationDuration = totalClaraEffect.actionvalue * 100.0 / ClaraCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    ClaraRotation.append(HuohuoCharacter.giveUltEnergy(ClaraCharacter) * ClaraRotationDuration / HuohuoRotationDuration)
    ClaraRotation.append(TingyunCharacter.giveUltEnergy() * ClaraRotationDuration / TingyunRotationDuration)
    
    print('##### Rotation Durations #####')
    print('Clara: ',ClaraRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Robin: ',RobinRotationDuration)
    print('Huohuo: ',HuohuoRotationDuration)

    # Scale other character's rotation
    TingyunRotation = [x * ClaraRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    RobinRotation = [x * ClaraRotationDuration / RobinRotationDuration for x in RobinRotation]
    HuohuoRotation = [x * ClaraRotationDuration / HuohuoRotationDuration for x in HuohuoRotation]

    ClaraEstimate = DefaultEstimator(f'Clara: {numSkillClara:.1f}E {numSvarogCounters:.1f}T 1Q', ClaraRotation, ClaraCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats',
                                    TingyunRotation, TingyunCharacter, config)
    RobinEstimate = DefaultEstimator(f'Robin {numSkillRobin:.1f}E {numBasicRobin:.1f}N S{RobinCharacter.lightcone.superposition:.0f} {RobinCharacter.lightcone.name}, 12 Spd Substats', 
                                    RobinRotation, RobinCharacter, config)
    HuohuoEstimate = DefaultEstimator(f'Huohuo: {numHuohuoBasic:.0f}N {numHuohuoSkill:.0f}E 1Q, S{HuohuoCharacter.lightcone.superposition:.0f} {HuohuoCharacter.lightcone.name}',
                                    HuohuoRotation, HuohuoCharacter, config)

    return([ClaraEstimate, TingyunEstimate, RobinEstimate, HuohuoEstimate])

