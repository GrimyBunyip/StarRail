from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.destruction.Lunae import Lunae
from characters.harmony.Hanabi import Hanabi
from characters.harmony.Tingyun import Tingyun
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PastAndFuture import PastAndFuture
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.LushakaTheSunkenSeas import LushakaTheSunkenSeas
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.SacerdosRelivedOrdeal import SacerdosRelivedOrdeal2pc, SacerdosRelivedOrdeal4pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def LunaeHanabiTingyunGallagher(config):
    #%% Lunae Hanabi Tingyun Gallagher Characters
    
    LunaeCharacter = Lunae(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.imaginary'],
                            substats = {'CR': 11, 'CD': 9, 'ATK.percent': 5, 'BreakEffect': 3}),
                            lightcone = OnTheFallOfAnAeon(uptime=1.0,**config),
                            relicsetone = WastelanderOfBanditryDesert2pc(), relicsettwo = WastelanderOfBanditryDesert4pc(), planarset = RutilantArena(),
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = LushakaTheSunkenSeas(),
                            benedictionTarget=LunaeCharacter,
                            **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'SPD.flat', 'ER'],
                            substats = {'CD': 8, 'SPD.flat': 12, 'RES': 5, 'DEF.percent': 3}),
                            lightcone = PastAndFuture(**config),
                            relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = BrokenKeel(),
                            **config)

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                            substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                            lightcone = Multiplication(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = SacerdosRelivedOrdeal2pc(), planarset = LushakaTheSunkenSeas(),
                            **config)
    
    team = [LunaeCharacter, HanabiCharacter, TingyunCharacter, GallagherCharacter]

    #%% Lunae Hanabi Tingyun Gallagher Team Buffs

    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=LunaeCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=3.0/3.0)
    LunaeCharacter.addStat('CD',description='Sacerdos Tingyun',amount=0.20)
    
    # Past and Future
    LunaeCharacter.addStat('DMG',description='Past and Future',amount=0.32)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(LunaeCharacter)
    TingyunCharacter.applyUltBuff(LunaeCharacter,targetSpdMult=HanabiCharacter.getTotalStat('SPD')/LunaeCharacter.getTotalStat('SPD'))
    LunaeCharacter.addStat('CD',description='Sacerdos Tingyun',amount=0.20)
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)

    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
    for character in team:
        character.print()

    #%% Lunae Hanabi Tingyun Gallagher Rotations
    numBasicHanabi = 0.0
    numSkillHanabi = 3.0
    HanabiRotation = [HanabiCharacter.useBasic() * numBasicHanabi,
                       HanabiCharacter.useSkill() * numSkillHanabi,
                    HanabiCharacter.useUltimate()]
        
    # Lunae should be about the same speed as tingyun, estimate 2.3 turn rotations
    lunaeRotation = 2.3
    LunaeRotation = [  # 140 energy needed. EndTurn needed to factor in his buffs
                LunaeCharacter.useSkill() * 3 * lunaeRotation,
                LunaeCharacter.useEnhancedBasic3() * lunaeRotation, # -3 SP, 40 energy
                LunaeCharacter.useUltimate(), # +2 SP, 5 energy
                TingyunCharacter.useBenediction(['basic','enhancedBasic']) * 2, # apply benedictions with buffs
                TingyunCharacter.useBenediction(['ultimate']) * 1,
                LunaeCharacter.endTurn(),
                HanabiCharacter.useAdvanceForward(advanceAmount=1.0 - LunaeCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')) * lunaeRotation, 
    ]

    numBasicTingyun = 2.0
    numSkillTingyun = 1.0
    TingyunRotation = [ 
            TingyunCharacter.useBasic() * numBasicTingyun, 
            TingyunCharacter.useSkill() * numSkillTingyun,
            TingyunCharacter.useUltimate(),
    ]

    numBasicGallagher = 4.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1,]
    if GallagherCharacter.lightcone.name == 'Multiplication':
        GallagherRotation[-1].actionvalue += 0.20 # advance foward cannot exceed a certain amount

    #%% Lunae Hanabi Tingyun Gallagher Rotation Math
    totalLunaeEffect = sumEffects(LunaeRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    LunaeRotationDuration = totalLunaeEffect.actionvalue * 100.0 / LunaeCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    LunaeRotation.append(TingyunCharacter.giveUltEnergy() * LunaeRotationDuration / TingyunRotationDuration)

    # scale other character's rotation
    HanabiRotation = [x * LunaeRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    TingyunRotation = [x * LunaeRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    GallagherRotation = [x * LunaeRotationDuration / GallagherRotationDuration for x in GallagherRotation]

    LunaeEstimate = DefaultEstimator(f'Lunae: {lunaeRotation:.1f}N^3 1Q', LunaeRotation, LunaeCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, {numBasicTingyun:.1f}N {numSkillTingyun:.1f}E 1Q, 12 spd substats', 
                                    TingyunRotation, TingyunCharacter, config)
    GallagherEstimate = DefaultEstimator(f'{GallagherCharacter.fullName()} {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q', 
                                    GallagherRotation, GallagherCharacter, config)

    return([LunaeEstimate,HanabiEstimate,TingyunEstimate,GallagherEstimate])