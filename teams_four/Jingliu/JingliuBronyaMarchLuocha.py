from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Jingliu import Jingliu
from characters.harmony.Bronya import Bronya
from characters.hunt.ImaginaryMarch import ImaginaryMarch
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.HunterOfGlacialForest import HunterOfGlacialForest2pc, HunterOfGlacialForest4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc
from relicSets.relicSets.WastelanderOfBanditryDesert import WastelanderOfBanditryDesert2pc, WastelanderOfBanditryDesert4pc

def JingliuBronyaMarchLuocha(config):
    #%% Jingliu Bronya March Luocha Characters
    
    JingliuCharacter = Jingliu(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.ice'],
                        substats = {'CR': 12, 'CD': 6, 'SPD.flat': 7, 'ATK.percent': 3}),
                        lightcone = OnTheFallOfAnAeon(**config),
                        relicsetone = HunterOfGlacialForest2pc(), relicsettwo = HunterOfGlacialForest4pc(uptime=0.4), planarset = RutilantArena(uptime=0.0),
                        **config)

    MarchCharacter = ImaginaryMarch(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.imaginary'],
                                    substats = {'CD': 8, 'CR': 12, 'ATK.percent': 3, 'SPD.flat': 5}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = WastelanderOfBanditryDesert2pc(),
                                    relicsettwo = WastelanderOfBanditryDesert4pc(uptimeCD=0.0),
                                    planarset = RutilantArena(),
                                    master=JingliuCharacter,
                                    **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'ER'],
                        substats = {'CD': 10, 'SPD.flat': 10, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = PastAndFuture(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [JingliuCharacter, BronyaCharacter, MarchCharacter, LuochaCharacter]

    #%% Jingliu Bronya March Luocha Team Buffs
    # only enhanced skills have rutilant arena buff
    JingliuCharacter.addStat('DMG',description='Rutilant Arena', amount=0.20, type=['enhancedSkill']) # take care of rutilant arena manually

    # Broken Keel and Penacony Buff
    for character in [JingliuCharacter, BronyaCharacter, MarchCharacter]:
        character.addStat('CD',description='Broken Keel Luocha',amount=0.10)
    for character in [JingliuCharacter, MarchCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel Bronya',amount=0.10)

    # Messenger 4 pc Bronya
    for character in [JingliuCharacter, MarchCharacter, LuochaCharacter]: # uptime 1.0 because bronya casts every 4 jingliu turns
        character.addStat('SPD.percent',description='Messenger 4 pc Bronya',amount=0.12,uptime=1.0/4.0)

    # March Buff
    MarchCharacter.applySkillBuff(JingliuCharacter)
    MarchCharacter.applyE6Buff(JingliuCharacter,uptime=0.5)
        
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Jingliu Bronya March Luocha Rotations
    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    # Assume Bronya skill buff applies to skills, and only applies a fraction of the time to the remaining abilities
    numSkill = 2.0
    numEnhanced = 3.0
    numUlt = 1.0

    JingliuRotation = []

    # 1 skill should have bronya buff, 1 should not.
    JingliuRotation += [JingliuCharacter.useSkill()]
    BronyaCharacter.applySkillBuff(JingliuCharacter,uptime=1.0)
    JingliuCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition)
    JingliuRotation += [JingliuCharacter.useSkill()]
    JingliuCharacter.stats['DMG'].pop() # remove bronya skill buff
    JingliuCharacter.stats['DMG'].pop() # remove past and future

    # 2 enhanced skills will not have bronya buff
    JingliuRotation += [JingliuCharacter.useEnhancedSkill() * 2]

    # 1 enhanced skill and the ultimate will both have bronya buff
    BronyaCharacter.applySkillBuff(JingliuCharacter,uptime=1.0)
    BronyaCharacter.applyUltBuff(JingliuCharacter,uptime=0.5) # only get Bronya ult buff every other rotation
    JingliuCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition)
    JingliuRotation += [JingliuCharacter.useEnhancedSkill()]
    JingliuRotation += [JingliuCharacter.useUltimate()]
    JingliuRotation += [JingliuCharacter.extraTurn() * 0.9] # multiply by 0.9 because it tends to overlap with skill advances
    JingliuRotation += [BronyaCharacter.useAdvanceForward() * 2] #Jingliu rotation is basically 4 turns

    
    numBasicMarch = 2.0
    numEnhancedMarch = 1.4
    MarchRotation = []
    MarchRotation += [MarchCharacter.useBasic() * numBasicMarch]
    MarchRotation += [MarchCharacter.useFollowup() * numBasicMarch]
    MarchRotation += [MarchCharacter.useEnhancedBasic(actionValue=0.0, numHits=5.0, chance=0.8) * numEnhancedMarch]
    MarchRotation += [MarchCharacter.useUltimate()] 

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1] 
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Jingliu Bronya March Luocha Rotation Math
    totalJingliuEffect = sumEffects(JingliuRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalMarchEffect = sumEffects(MarchRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    JingliuRotationDuration = totalJingliuEffect.actionvalue * 100.0 / JingliuCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    MarchRotationDuration = totalMarchEffect.actionvalue * 100.0 / MarchCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Jingliu: ',JingliuRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Ruan Mei: ',MarchRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # scale other character's rotation
    BronyaRotation = [x * JingliuRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    MarchRotation = [x * JingliuRotationDuration / MarchRotationDuration for x in MarchRotation]
    LuochaRotation = [x * JingliuRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    
    # calculate total number of breaks for Ruan Mei Talent
    totalEffect = sumEffects(JingliuRotation + BronyaRotation + MarchRotation + LuochaRotation)
    numBreaks = totalEffect.gauge * MarchCharacter.weaknessBrokenUptime / MarchCharacter.enemyToughness
    MarchRotation.append(MarchCharacter.useTalent() * numBreaks)

    JingliuEstimate = DefaultEstimator('Jingliu {:.0f}E {:.0f}Moon {:.0f}Q'.format(numSkill, numEnhanced, numUlt),
                                                    JingliuRotation, JingliuCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    MarchEstimate = DefaultEstimator(f'March: {numBasicMarch:.1f}N {numEnhancedMarch:.1f}Enh 1Q', MarchRotation, MarchCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name),
                                    LuochaRotation, LuochaCharacter, config)

    return([JingliuEstimate, BronyaEstimate, MarchEstimate, LuochaEstimate])