from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.destruction.Jingliu import Jingliu
from characters.harmony.Bronya import Bronya
from characters.harmony.Robin import Robin
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.QuidProQuo import QuidProQuo
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.CarveTheMoonWeaveTheClouds import CarveTheMoonWeaveTheClouds
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.FlowingNightglow import FlowingNightglow
from lightCones.harmony.ForTomorrowsJourney import ForTomorrowsJourney
from lightCones.harmony.PoisedToBloom import PoisedToBloom
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.LushakaTheSunkenSeas import LushakaTheSunkenSeas
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.SacerdosRelivedOrdeal import SacerdosRelivedOrdeal2pc, SacerdosRelivedOrdeal4pc
from relicSets.relicSets.ScholarLostInErudition import ScholarLostInErudition2pc, ScholarLostInErudition4pc

def JingliuBronyaRobinGallagher(config,
                                robinEidolon:int=None, 
                                robinLightCone:str='ForTomorrowsJourney'):
    #%% Jingliu Bronya Robin Gallagher Characters
    JingliuCharacter = Jingliu(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.ice'],
                        substats = {'CR': 7, 'CD': 5, 'SPD.flat': 13, 'ATK.percent': 3}),
                        lightcone = OnTheFallOfAnAeon(**config),
                        relicsetone = ScholarLostInErudition2pc(), relicsettwo = ScholarLostInErudition4pc(), planarset = RutilantArena(uptime=0.0),
                        **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'ER'],
                        substats = {'CD': 7, 'SPD.flat': 13, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = DanceDanceDance(**config),
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = BrokenKeel(),
                        **config)
    
    RobinUltUptime = 0.5 if robinEidolon is None or robinEidolon < 2 else 1.0
    if robinLightCone == 'PoisedToBloom':
        RobinLightCone = PoisedToBloom(**config)
    elif robinLightCone == 'FlowingNightglow':
        RobinLightCone = FlowingNightglow(**config, uptime=RobinUltUptime)
    elif robinLightCone == 'ForTomorrowsJourney':
        RobinLightCone = ForTomorrowsJourney(**config)
    elif robinLightCone == 'CarveTheMoonWeaveTheClouds':
        RobinLightCone = CarveTheMoonWeaveTheClouds(**config)
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 11, 'SPD.flat': 9, 'RES': 3, 'ATK.flat': 6}),
                        lightcone = RobinLightCone,
                        relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                        eidolon=robinEidolon,
                        ultUptime=RobinUltUptime,
                        **config)


    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                        substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = QuidProQuo(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = SacerdosRelivedOrdeal2pc(), planarset = LushakaTheSunkenSeas(),
                        **config)
    
    team = [JingliuCharacter, BronyaCharacter, RobinCharacter, GallagherCharacter]

    #%% Jingliu Bronya Robin Gallagher Team Buffs
    # only enhanced skills have rutilant arena buff
    JingliuCharacter.addStat('DMG',description='Rutilant Arena', amount=0.20, type=['enhancedSkill']) # take care of rutilant arena manually
        
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    
    # Robin Buffs
    RobinCharacter.applyUltBuff(team,uptime=1.0)
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)

    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
    for character in team:
        character.print()

    #%% Jingliu Bronya Robin Gallagher Rotations
    numSkillBronya = 3.0
    BronyaRotation = [BronyaCharacter.useSkill() * numSkillBronya,
                    BronyaCharacter.useUltimate(),]

    # Assume Bronya skill buff applies to skills, and only applies a fraction of the time to the remaining abilities
    numSkill = 2.0
    numEnhanced = 3.0
    numUlt = 1.0

    JingliuRotation = []

    # 1 skill should have bronya buff, 1 should not.
    JingliuRotation += [JingliuCharacter.useSkill()]
    JingliuRotation[-1].actionvalue = 1.0
    BronyaCharacter.applySkillBuff(JingliuCharacter,uptime=1.0)
    JingliuCharacter.addStat('CD',description='Sacerdos',amount=0.2)
    JingliuRotation += [JingliuCharacter.useSkill()]
    JingliuRotation[-1].actionvalue = 1.0
    JingliuCharacter.stats['DMG'].pop() # remove bronya skill buff
    JingliuCharacter.stats['DMG'].pop() # remove bronya Sacerdos buff

    # 2 enhanced skills will not have bronya buff
    JingliuRotation += [JingliuCharacter.useEnhancedSkill() * 2]

    # 1 enhanced skill and the ultimate will both have bronya buff
    BronyaCharacter.applySkillBuff(JingliuCharacter,uptime=1.0)
    JingliuCharacter.addStat('CD',description='Sacerdos',amount=0.2)
    BronyaCharacter.applyUltBuff(JingliuCharacter,uptime=0.5) # only get Bronya ult buff every other rotation
    JingliuRotation += [JingliuCharacter.useEnhancedSkill()]
    JingliuRotation += [JingliuCharacter.useUltimate()]
    JingliuRotation += [JingliuCharacter.extraTurn()]
    JingliuRotation += [BronyaCharacter.useAdvanceForward() * (2.0 if BronyaCharacter.eidolon >= 1 else 1.0)]

    RobinRotationJingliu = [RobinCharacter.useTalent() * (numSkill + numEnhanced + numUlt)]
    RobinRotationJingliu += [RobinCharacter.useConcertoDamage(['skill']) * numSkill * RobinUltUptime]
    RobinRotationJingliu += [RobinCharacter.useConcertoDamage(['skill','enhancedSkill']) * numEnhanced * RobinUltUptime]
    RobinRotationJingliu += [RobinCharacter.useConcertoDamage(['ultimate']) * numUlt * RobinUltUptime]
    
    if BronyaCharacter.eidolon >= 1:
        JingliuRotation = [entry * 1.2 for entry in JingliuRotation]
        RobinRotationJingliu = [entry * 1.2 for entry in RobinRotationJingliu]

    numBasicRobin = 0.0
    numSkillRobin = 2.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                     RobinCharacter.useSkill() * numSkillRobin,
                     RobinCharacter.useUltimate(),
                     BronyaCharacter.useAdvanceForward()]

    numBasicGallagher = 4.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1]
    if GallagherCharacter.lightcone.name == 'Multiplication':
        GallagherRotation[-1].actionvalue += 0.20 # advance foward cannot exceed a certain amount
        
    RobinRotationGallagher = [RobinCharacter.useTalent() * (numBasicGallagher + numEnhancedGallagher + 1.0)]
    RobinRotationGallagher += [RobinCharacter.useConcertoDamage(['basic']) * numBasicGallagher * RobinUltUptime]
    RobinRotationGallagher += [RobinCharacter.useConcertoDamage(['basic','enhancedBasic']) * numEnhancedGallagher * RobinUltUptime]
    RobinRotationGallagher += [RobinCharacter.useConcertoDamage(['ultimate']) * RobinUltUptime]
        
    # scale Gallagher's rotation down
    if BronyaCharacter.eidolon >= 1:
        GallagherRotation = [entry * 3.0 / numBasicGallagher for entry in GallagherRotation]
        RobinRotationGallagher = [entry * 3.0 / numBasicGallagher for entry in RobinRotationGallagher]
    else:
        GallagherRotation += [BronyaCharacter.useAdvanceForward()]

    #%% Jingliu Bronya Robin Gallagher Rotation Math
    # four turn robin advance math
    totalRobinEffect = sumEffects(RobinRotation)
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    
    numTurnAV = 300

    BronyaTurns = numTurnAV * BronyaCharacter.useSkill().actionvalue / BronyaCharacter.getTotalStat('SPD')
    JingliuTurns = numTurnAV * JingliuCharacter.useEnhancedSkill().actionvalue / JingliuCharacter.getTotalStat('SPD')
    GallagherTurns = numTurnAV * GallagherCharacter.useBasic().actionvalue / GallagherCharacter.getTotalStat('SPD')
    longestTurn = [BronyaTurns - 124.0 * BronyaCharacter.useSkill().actionvalue / BronyaCharacter.getTotalStat('SPD'),
                   JingliuTurns - 124.0 * JingliuCharacter.useEnhancedSkill().actionvalue / JingliuCharacter.getTotalStat('SPD'),
                   GallagherTurns - 124.0 * GallagherCharacter.useBasic().actionvalue / GallagherCharacter.getTotalStat('SPD'),
                   RobinRotationDuration]
    longestTurn = max(longestTurn)
    
    BronyaRotation += [RobinCharacter.useAdvanceForward() * (BronyaTurns - longestTurn) * BronyaCharacter.getTotalStat('SPD') * 3.0 / numTurnAV]
    JingliuRotation += [RobinCharacter.useAdvanceForward() * (JingliuTurns - longestTurn) * JingliuCharacter.getTotalStat('SPD') * 3.0 / numTurnAV]
    GallagherRotation += [RobinCharacter.useAdvanceForward() * (GallagherTurns - longestTurn) * GallagherCharacter.getTotalStat('SPD') * 3.0 / numTurnAV]
        
    if BronyaCharacter.eidolon >= 1:
        JingliuRotation = [JingliuEntry / 1.2 for JingliuEntry in JingliuRotation]
        
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalJingliuEffect = sumEffects(JingliuRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)
    
    RobinRotation += RobinRotationJingliu
    RobinRotation += RobinRotationGallagher
    totalRobinEffect = sumEffects(RobinRotation)
    
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    JingliuRotationDuration = totalJingliuEffect.actionvalue * 100.0 / JingliuCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Jingliu: ',JingliuRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Ruan Mei: ',RobinRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # scale other character's rotation
    BronyaRotation = [x * JingliuRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    RobinRotation = [x * JingliuRotationDuration / RobinRotationDuration for x in RobinRotation]
    GallagherRotation = [x * JingliuRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    
    # calculate total number of breaks for Ruan Mei Talent
    totalEffect = sumEffects(JingliuRotation + BronyaRotation + RobinRotation + GallagherRotation)
    numBreaks = totalEffect.gauge * RobinCharacter.weaknessBrokenUptime / RobinCharacter.enemyToughness
    RobinRotation.append(RobinCharacter.useTalent() * numBreaks)

    JingliuEstimate = DefaultEstimator('Jingliu {:.0f}E {:.0f}Moon {:.0f}Q'.format(numSkill, numEnhanced, numUlt),
                                                    JingliuRotation, JingliuCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    RobinEstimate = DefaultEstimator(f'{RobinCharacter.fullName()} {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q', 
                                    RobinRotation, RobinCharacter, config)
    GallagherEstimate = DefaultEstimator(f'{GallagherCharacter.fullName()} {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q', 
                                    GallagherRotation, GallagherCharacter, config)

    return([JingliuEstimate, BronyaEstimate, RobinEstimate, GallagherEstimate])