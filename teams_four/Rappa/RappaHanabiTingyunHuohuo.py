from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Huohuo import Huohuo
from characters.erudition.Rappa import Rappa
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
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.SacerdosRelivedOrdeal import SacerdosRelivedOrdeal2pc, SacerdosRelivedOrdeal4pc
from relicSets.relicSets.ScholarLostInErudition import ScholarLostInErudition2pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc

def RappaHanabiTingyunHuohuo(config):
    #%% Rappa Hanabi Tingyun Huohuo Characters
    RappaCharacter = Rappa(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
                        substats = {'CR': 8, 'CD': 12, 'ATK.flat': 3, 'ATK.percent': 5}),
                        lightcone =  TodayIsAnotherPeacefulDay(**config),
                        relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = ScholarLostInErudition2pc(), planarset = RutilantArena(),
                        **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'SPD.flat', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'RES': 5, 'DEF.percent': 3}),
                        lightcone = PastAndFuture(**config),
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = BrokenKeel(),
                        **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = LushakaTheSunkenSeas(),
                        benedictionTarget=RappaCharacter,
                        **config)

    HuohuoCharacter = Huohuo(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'HP.flat': 3, 'RES': 6}),
                        lightcone = PostOpConversation(**config),
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [RappaCharacter, HanabiCharacter, TingyunCharacter, HuohuoCharacter]

    #%% Rappa Hanabi Tingyun Huohuo Team Buffs

    # Past and Future
    RappaCharacter.addStat('DMG',description='Past and Future',amount=0.32)
    
    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=RappaCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=2.0/2.75) # let's say half the time huohuo can shave off a turn
    RappaCharacter.addStat('CD',description='Sacerdos Hanabi',amount=0.20)
    
    # Huohuo Buffs
    HuohuoCharacter.applyUltBuff([TingyunCharacter,HanabiCharacter],uptime=2.0/4.0)
    HuohuoCharacter.applyUltBuff([RappaCharacter],uptime=2.0/5.0)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(RappaCharacter)
    TingyunCharacter.applyUltBuff(RappaCharacter,tingRotationDuration=2.75)  # let's say half the time, huohuo can shave off a turn
    RappaCharacter.addStat('CD',description='Sacerdos Tingyun',amount=0.20)
    
    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
    for character in team:
        character.print()

    #%% Rappa Hanabi Tingyun Huohuo Rotations
    numBasicHanabi = 0.0
    numSkillHanabi = 2.75 # let's say half the time, huohuo can shave off a turn
    HanabiRotation = [HanabiCharacter.useBasic() * numBasicHanabi,
                       HanabiCharacter.useSkill() * numSkillHanabi,
                    HanabiCharacter.useUltimate()]

    # Rappa & Tingyun Rotation
    rappaBreakRate = 0.25
    
    TingyunEnergyPerTurn = (60.0 if TingyunCharacter.eidolon >= 6 else 50.0) / 2.75  # let's say half the time, huohuo can shave off a turn
    HuohuoEnergyPerTurn = RappaCharacter.maxEnergy * (0.21 if HuohuoCharacter.eidolon >= 5 else 0.20)  / 4.0
    TingyunEnergyPerTurn *= TingyunCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')
    HuohuoEnergyPerTurn *= HuohuoCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')
    numTurnsRappa = (160.0 - 35.0 - 8.0 * RappaCharacter.numEnemies * rappaBreakRate) / (30.0 + TingyunEnergyPerTurn + HuohuoEnergyPerTurn + 3 * RappaCharacter.numEnemies)
    numEnhancedRappa = min(3.0,numTurnsRappa + 1.0)
    numSkillRappa = min(0,numTurnsRappa + 1.0 - 3.0)
    numTalentRappa = (numTurnsRappa + 1.0) * RappaCharacter.numEnemies * (1.0 - RappaCharacter.weaknessBrokenUptime) * rappaBreakRate

    RappaRotation = [RappaCharacter.useSkill() * numSkillRappa,
                     RappaCharacter.useEnhancedBasic() * numEnhancedRappa,
                     RappaCharacter.useSuperBreak(baseGauge=120.0) * numEnhancedRappa,
                     RappaCharacter.useTalent() * numTalentRappa,
                     RappaCharacter.useUltimate(),
                     HanabiCharacter.useAdvanceForward(advanceAmount=1.0 - RappaCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')) * numTurnsRappa,
    ]

    RappaRotation.append(TingyunCharacter.useBenediction(['skill']) * numSkillRappa)
    RappaRotation.append(TingyunCharacter.useBenediction(['basic','enhancedBasic']) * numEnhancedRappa)

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

    #%% Rappa Hanabi Tingyun Huohuo Rotation Math
    totalRappaEffect = sumEffects(RappaRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    RappaRotationDuration = totalRappaEffect.actionvalue * 100.0 / RappaCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    RappaRotation.append(HuohuoCharacter.giveUltEnergy(RappaCharacter) * RappaRotationDuration / HuohuoRotationDuration)
    RappaRotation.append(TingyunCharacter.giveUltEnergy() * RappaRotationDuration / TingyunRotationDuration)

    print('##### Rotation Durations #####')
    print('Rappa: ',RappaRotationDuration)
    print('Hanabi: ',HanabiRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Huohuo: ',HuohuoRotationDuration)

    # scale other character's rotation
    HanabiRotation = [x * RappaRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    TingyunRotation = [x * RappaRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HuohuoRotation = [x * RappaRotationDuration / HuohuoRotationDuration for x in HuohuoRotation]

    RappaEstimate = DefaultEstimator(f'{RappaCharacter.fullName()} {numSkillRappa:.0f}E {numEnhancedRappa:.0f}Enh {numTalentRappa:.1f}T 1Q', 
                                            RappaRotation, RappaCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats',
                                    TingyunRotation, TingyunCharacter, config)
    HuohuoEstimate = DefaultEstimator(f'Huohuo: {numBasicHuohuo:.0f}N {numSkillHuohuo:.0f}E 1Q, S{HuohuoCharacter.lightcone.superposition:.0f} {HuohuoCharacter.lightcone.name}',
                                    HuohuoRotation, HuohuoCharacter, config)

    return([RappaEstimate, HanabiEstimate, TingyunEstimate, HuohuoEstimate])
