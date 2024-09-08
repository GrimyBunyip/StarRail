from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Jingliu import Jingliu
from characters.harmony.Bronya import Bronya
from characters.harmony.Hanabi import Hanabi
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.PastAndFuture import PastAndFuture
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.SacerdosRelivedOrdeal import SacerdosRelivedOrdeal2pc, SacerdosRelivedOrdeal4pc
from relicSets.relicSets.ScholarLostInErudition import ScholarLostInErudition2pc, ScholarLostInErudition4pc

def JingliuBronyaHanabiLuocha(config):
    #%% Jingliu Bronya Hanabi Luocha Characters
    JingliuCharacter = Jingliu(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CD', 'DMG.ice'],
                        substats = {'CR': 12, 'CD': 8, 'ATK.flat': 3, 'ATK.percent': 5}),
                        lightcone = OnTheFallOfAnAeon(**config),
                        relicsetone = ScholarLostInErudition2pc(), relicsettwo = ScholarLostInErudition4pc(), planarset = RutilantArena(uptime=0.0),
                        **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = PastAndFuture(**config),
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = BrokenKeel(),
                        **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'SPD.flat', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'RES': 5, 'DEF.percent': 3}),
                        lightcone = PastAndFuture(**config),
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = BrokenKeel(),
                        **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [JingliuCharacter, BronyaCharacter, HanabiCharacter, LuochaCharacter]

    #%% Jingliu Bronya Hanabi Luocha Team Buffs
    # only enhanced skills have rutilant arena buff
    JingliuCharacter.addStat('DMG',description='Rutilant Arena', amount=0.20, type=['enhancedSkill']) # take care of rutilant arena manually

    # Broken Keel and Penacony Buff
    for character in [JingliuCharacter, BronyaCharacter, HanabiCharacter]:
        character.addStat('CD',description='Broken Keel Luocha',amount=0.10)
    for character in [JingliuCharacter, HanabiCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel Bronya',amount=0.10)
    for character in [JingliuCharacter, BronyaCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel Hanabi',amount=0.10)
        
    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    #HanabiCharacter.applySkillBuff(character=JingliuCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=1.0/4.0)
    JingliuCharacter.addStat('CD',description='Sacerdos Hanabi',amount=0.2,uptime=2.0/3.0)
    
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    JingliuCharacter.addStat('CD',description='Sacerdos Bronya',amount=0.2,uptime=2.0/3.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Jingliu Bronya Hanabi Luocha Rotations
    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    # Assume Bronya skill buff applies to skills, and only applies a fraction of the time to the remaining abilities
    numSkill = 2.0
    numEnhanced = 3.0
    numUlt = 1.0

    JingliuRotation = []
    
    # Rotation should be:
    # Skill (Bronya Buffed) from the end of last rotation or because we started with a technique
    # Skill (Hanabi Buffed) -> Advanced Forward
    # Enhanced Skill (Unbuffed)
    # Enhanced Skill (Bronya Buffed)
    # Enhanced Skill (Hanabi Buffed, Bronya Buffed half the time)
    # Ultimate (Hanabi Buffed, Bronya Buffed half the time)

    BronyaCharacter.applySkillBuff(JingliuCharacter,uptime=1.0)
    JingliuCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition)
    JingliuRotation += [JingliuCharacter.useSkill()]
    JingliuCharacter.stats['DMG'].pop() # remove bronya skill buff
    JingliuCharacter.stats['DMG'].pop() # remove past and future
    
    HanabiCharacter.applySkillBuff(character=JingliuCharacter,uptime=1.0)
    JingliuCharacter.addStat('DMG',description='Past and Future',amount=0.32)
    JingliuRotation += [JingliuCharacter.useSkill()]
    JingliuCharacter.stats['CD'].pop() # remove hanabi skill buff
    JingliuCharacter.stats['DMG'].pop() # remove past and future
    
    JingliuRotation += [JingliuCharacter.useEnhancedSkill()]

    BronyaCharacter.applySkillBuff(JingliuCharacter,uptime=1.0)
    JingliuCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition)
    JingliuRotation += [JingliuCharacter.useEnhancedSkill()]
    JingliuCharacter.stats['DMG'].pop() # remove bronya skill buff
    JingliuCharacter.stats['DMG'].pop() # remove past and future

    HanabiCharacter.applySkillBuff(character=JingliuCharacter,uptime=1.0)
    JingliuCharacter.addStat('DMG',description='Past and Future',amount=0.32)
    BronyaCharacter.applyUltBuff(JingliuCharacter,uptime=0.5) # only get Bronya ult buff every other rotation
    JingliuRotation += [JingliuCharacter.useEnhancedSkill()]
    JingliuRotation += [JingliuCharacter.useUltimate()]

    JingliuRotation += [JingliuCharacter.extraTurn() * 0.9] # multiply by 0.9 because it tends to overlap with skill advances
    JingliuRotation += [BronyaCharacter.useAdvanceForward() * (numSkill + numEnhanced - 1.0) / 2.0] # Half of the turns
    JingliuRotation += [HanabiCharacter.useAdvanceForward(advanceAmount=1.0 - JingliuCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')) * (numSkill + numEnhanced - 1.0) / 2.0] # multiply by 0.9 because it tends to overlap with skill advances

    numBasicHanabi = 0.0
    numSkillHanabi = 3.0
    HanabiRotation = [HanabiCharacter.useBasic() * numBasicHanabi,
                       HanabiCharacter.useSkill() * numSkillHanabi,
                    HanabiCharacter.useUltimate()]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Jingliu Bronya Hanabi Luocha Rotation Math
    totalJingliuEffect = sumEffects(JingliuRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    JingliuRotationDuration = totalJingliuEffect.actionvalue * 100.0 / JingliuCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Jingliu: ',JingliuRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Hanabi: ',HanabiRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # scale other character's rotation
    BronyaRotation = [x * JingliuRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    HanabiRotation = [x * JingliuRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    LuochaRotation = [x * JingliuRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    JingliuEstimate = DefaultEstimator('Jingliu {:.0f}E {:.0f}Moon {:.0f}Q'.format(numSkill, numEnhanced, numUlt),
                                                    JingliuRotation, JingliuCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name),
                                    LuochaRotation, LuochaCharacter, config)

    return([JingliuEstimate, BronyaEstimate, HanabiEstimate, LuochaEstimate])