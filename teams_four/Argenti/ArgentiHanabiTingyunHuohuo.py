from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Huohuo import Huohuo
from characters.erudition.Argenti import Argenti
from characters.harmony.Tingyun import Tingyun
from characters.harmony.Hanabi import Hanabi
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.PostOpConversation import PostOpConversation
from lightCones.erudition.GeniusesRepose import GeniusesRepose
from lightCones.erudition.TodayIsAnotherPeacefulDay import TodayIsAnotherPeacefulDay
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PastAndFuture import PastAndFuture
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.LushakaTheSunkenSeas import LushakaTheSunkenSeas
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.SacerdosRelivedOrdeal import SacerdosRelivedOrdeal2pc, SacerdosRelivedOrdeal4pc

def ArgentiHanabiTingyunHuohuo(config):
    #%% Argenti Hanabi Tingyun Huohuo Characters
    ArgentiCharacter = Argenti(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.physical'],
                        substats = {'CR': 8, 'CD': 12, 'ATK.flat': 3, 'ATK.percent': 5}),
                        lightcone =  TodayIsAnotherPeacefulDay(**config),
                        relicsetone = ChampionOfStreetwiseBoxing2pc(), relicsettwo = ChampionOfStreetwiseBoxing4pc(uptime=0.4), planarset = RutilantArena(),
                        **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'SPD.flat', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'RES': 5, 'DEF.percent': 3}),
                        lightcone = PastAndFuture(**config),
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = BrokenKeel(),
                        **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = LushakaTheSunkenSeas(),
                        benedictionTarget=ArgentiCharacter,
                        **config)

    HuohuoCharacter = Huohuo(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'HP.flat': 3, 'RES': 6}),
                        lightcone = PostOpConversation(**config),
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [ArgentiCharacter, HanabiCharacter, TingyunCharacter, HuohuoCharacter]

    #%% Argenti Hanabi Tingyun Huohuo Team Buffs

    # Past and Future
    ArgentiCharacter.addStat('DMG',description='Past and Future',amount=0.32)
    
    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=ArgentiCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=2.0/2.75) # let's say half the time huohuo can shave off a turn
    ArgentiCharacter.addStat('CD',description='Sacerdos Hanabi',amount=0.20, stacks=2)
    
    # Huohuo Buffs
    HuohuoCharacter.applyUltBuff([TingyunCharacter,HanabiCharacter],uptime=2.0/4.0)
    HuohuoCharacter.applyUltBuff([ArgentiCharacter],uptime=2.0/5.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(ArgentiCharacter)
    TingyunCharacter.applyUltBuff(ArgentiCharacter,tingRotationDuration=2.75)  # let's say half the time, huohuo can shave off a turn
    
    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
    for character in team:
        character.print()

    #%% Argenti Hanabi Tingyun Huohuo Rotations
    numBasicHanabi = 0.0
    numSkillHanabi = 2.75 # let's say half the time, huohuo can shave off a turn
    HanabiRotation = [HanabiCharacter.useBasic() * numBasicHanabi,
                       HanabiCharacter.useSkill() * numSkillHanabi,
                    HanabiCharacter.useUltimate()]

    # Argenti & Tingyun Rotation
    TingyunEnergyPerTurn = (60.0 if TingyunCharacter.eidolon >= 6 else 50.0) / 2.75  # let's say half the time, huohuo can shave off a turn
    HuohuoEnergyPerTurn = ArgentiCharacter.maxEnergy * (0.21 if HuohuoCharacter.eidolon >= 5 else 0.20)  / 4.0
    TingyunEnergyPerTurn *= TingyunCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')
    HuohuoEnergyPerTurn *= HuohuoCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')
    numSkill = (180.0 - 5.0 - 3.0 * ArgentiCharacter.numEnemies) / (30.0 + TingyunEnergyPerTurn + HuohuoEnergyPerTurn + 3 * ArgentiCharacter.numEnemies)
    numUlt = 1

    ArgentiRotation = [ArgentiCharacter.useSkill() * numSkill,
                        ArgentiCharacter.useEnhancedUltimate() * numUlt,
                        HanabiCharacter.useAdvanceForward(advanceAmount=1.0 - ArgentiCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')) * numSkill,
    ]

    ArgentiRotation.append(TingyunCharacter.useBenediction(['skill']) * numSkill * ArgentiCharacter.numEnemies)
    ArgentiRotation.append(TingyunCharacter.useBenediction(['ultimate','enhancedUltimate']) * numUlt * ArgentiCharacter.numEnemies)

    TingyunRotation = [ 
            TingyunCharacter.useBasic() * 1.5, # let's say half the time, huohuo can shave off a turn 
            TingyunCharacter.useSkill(),
            TingyunCharacter.useUltimate(),
    ]

    numBasicHuohuo = 3.0
    numSkillHuohuo = 1.0
    HuohuoRotation = [HuohuoCharacter.useBasic() * numBasicHuohuo,
                    HuohuoCharacter.useSkill() * numSkillHuohuo,
                    HuohuoCharacter.useUltimate(),]

    #%% Argenti Hanabi Tingyun Huohuo Rotation Math
    totalArgentiEffect = sumEffects(ArgentiRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    ArgentiRotationDuration = totalArgentiEffect.actionvalue * 100.0 / ArgentiCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    ArgentiRotation.append(HuohuoCharacter.giveUltEnergy(ArgentiCharacter) * ArgentiRotationDuration / HuohuoRotationDuration)
    ArgentiRotation.append(TingyunCharacter.giveUltEnergy() * ArgentiRotationDuration / TingyunRotationDuration)

    print('##### Rotation Durations #####')
    print('Argenti: ',ArgentiRotationDuration)
    print('Hanabi: ',HanabiRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Huohuo: ',HuohuoRotationDuration)

    # scale other character's rotation
    HanabiRotation = [x * ArgentiRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    TingyunRotation = [x * ArgentiRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HuohuoRotation = [x * ArgentiRotationDuration / HuohuoRotationDuration for x in HuohuoRotation]

    ArgentiEstimate = DefaultEstimator(f'Argenti: {numSkill:.1f}E {numUlt:.1f}EnhQ', 
                                            ArgentiRotation, ArgentiCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats',
                                    TingyunRotation, TingyunCharacter, config)
    HuohuoEstimate = DefaultEstimator(f'Huohuo: {numBasicHuohuo:.0f}N {numSkillHuohuo:.0f}E 1Q, S{HuohuoCharacter.lightcone.superposition:.0f} {HuohuoCharacter.lightcone.name}',
                                    HuohuoRotation, HuohuoCharacter, config)

    return([ArgentiEstimate, HanabiEstimate, TingyunEstimate, HuohuoEstimate])
