from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Lunae import Lunae
from characters.harmony.RuanMei import RuanMei
from characters.harmony.Tingyun import Tingyun
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def LunaeRuanMeiTingyunLuocha(config):
    #%% Lunae RuanMei Tingyun Luocha Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                        substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                        **config)
    
    LunaeCharacter = Lunae(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
                        substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'ATK.flat': 3}),
                        lightcone = OnTheFallOfAnAeon(**config),
                        relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = WastelanderOfBanditryDesert4pc(), planarset = RutilantArena(),
                        **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                            benedictionTarget=LunaeCharacter,
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'RES': 3}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = PenaconyLandOfDreams(),
                            **config)
    
    team = [LunaeCharacter, RuanMeiCharacter, TingyunCharacter, LuochaCharacter]

    #%% Lunae RuanMei Tingyun Luocha Team Buffs
    # Penacony Buff
    for character in [LunaeCharacter, RuanMeiCharacter, TingyunCharacter]:
        character.addStat('DMG.imaginary',description='Penacony from Luocha',amount=0.1)

    # RuanMei Debuffs, max skill uptime
    RuanMeiCharacter.applyWeaknessModifiers(team=team)
    RuanMeiCharacter.applyPassiveBuffs(team=team)
    RuanMeiCharacter.applySkillBuff(team=team,uptime=2.0/3.0)
    RuanMeiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)
            
    # Tingyun Messenger Buff
    LuochaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4.0)
    for character in [LunaeCharacter, RuanMeiCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/2.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(LunaeCharacter)
    TingyunCharacter.applyUltBuff(LunaeCharacter)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Lunae RuanMei Tingyun Luocha Rotations
    numBasicRuanMei = 2.0
    numSkillRuanMei = 1.0
    RuanMeiRotation = [RuanMeiCharacter.useBasic() * numBasicRuanMei,
                       RuanMeiCharacter.useSkill() * numSkillRuanMei,
                    RuanMeiCharacter.useUltimate(),
                    RuanMeiCharacter.useTalent() * numBasicRuanMei] # append ruan mei talent damage
        
    numBlast = min(3, LunaeCharacter.numEnemies)
    LunaeRotation = [  # 140 energy needed. EndTurn needed to factor in his buffs
                LunaeCharacter.useSkill()*3,
                LunaeCharacter.useEnhancedBasic3(), # -3 SP, 40 energy
                LunaeCharacter.endTurn(),
                LunaeCharacter.useSkill()*3,
                LunaeCharacter.useEnhancedBasic3(), # -3 SP, 40 energy
                LunaeCharacter.useUltimate(), # +2 SP, 5 energy
                TingyunCharacter.useBenediction(['basic','enhancedBasic']) * 2, # apply benedictions with buffs
                TingyunCharacter.useBenediction(['ultimate']) * 1,
                LunaeCharacter.endTurn(),
                TingyunCharacter.giveUltEnergy() , # rough estimate of rotation, tingyun is about 10% faster
                RuanMeiCharacter.useTalent() * 3 * numBlast,
    ]

    TingyunRotation = [ 
            TingyunCharacter.useBasic() * 2, 
            TingyunCharacter.useSkill(),
            TingyunCharacter.useUltimate(),
            RuanMeiCharacter.useTalent() * 2, # append ruan mei talent damage
    ]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useSkill() * 1,
                    RuanMeiCharacter.useTalent() * (3 + 1 * LuochaCharacter.numEnemies), # append ruan mei talent damage
                    LuochaCharacter.useUltimate() * 1]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Lunae RuanMei Tingyun Luocha Rotation Math
    totalLunaeEffect = sumEffects(LunaeRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    LunaeRotationDuration = totalLunaeEffect.actionvalue * 100.0 / LunaeCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's rotation
    RuanMeiRotation = [x * LunaeRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    TingyunRotation = [x * LunaeRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    LuochaRotation = [x * LunaeRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    LunaeEstimate = DefaultEstimator('Lunae: 2N^3 1Q', LunaeRotation, LunaeCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'RuanMei {numSkillRuanMei:.1f}E {numBasicRuanMei:.1f}N S{RuanMeiCharacter.lightcone.superposition:.0f} {RuanMeiCharacter.lightcone.name}, 12 Spd Substats', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.1f} Tingyun S{TingyunCharacter.lightcone.superposition:.1f} {TingyunCharacter.lightcone.name}, 12 spd substats', 
                                    TingyunRotation, TingyunCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([LunaeEstimate,RuanMeiEstimate,TingyunEstimate,LuochaEstimate])