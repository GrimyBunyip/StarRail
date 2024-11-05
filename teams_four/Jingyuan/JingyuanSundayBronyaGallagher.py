from copy import deepcopy
from baseClasses import BaseLightCone
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.erudition.JingYuan import JingYuan
from characters.harmony.Sunday import Sunday
from characters.harmony.Bronya import Bronya
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.erudition.EternalCalculus import EternalCalculus
from lightCones.erudition.TheSeriousnessOfBreakfast import TheSeriousnessOfBreakfast
from lightCones.harmony.AGroundedAscent import AGroundedAscent
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.LushakaTheSunkenSeas import LushakaTheSunkenSeas
from relicSets.planarSets.TheWondrousBananAmusementPark import TheWondrousBananAmusementPark
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.SacerdosRelivedOrdeal import SacerdosRelivedOrdeal2pc, SacerdosRelivedOrdeal4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def JingYuanSundayBronyaGallagher(config, 
                                jingyuanCone:BaseLightCone = 'EternalCalculus',
                                sundayCone:BaseLightCone = 'DanceDanceDance',
                                bronyaEidolon:int = None,):
    #%% JingYuan Sunday Bronya Gallagher Characters
    JingYuanMainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.lightning']
    JingYuanSubstats = {'CD': 13, 'CR': 7, 'ATK.percent': 3, 'SPD.flat': 5}
    SundaySubstats = {'CD': 10, 'SPD.flat': 10, 'HP.percent': 5, 'DEF.percent': 3}

    if sundayCone == 'DanceDanceDance':
        SundayLightCone = DanceDanceDance(**config)
    elif sundayCone == 'A Grounded Ascent':
        SundayLightCone = AGroundedAscent(**config)
        
    SundayCharacter = Sunday(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'ER'],
                        substats = SundaySubstats),
                        lightcone = SundayLightCone,
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = LushakaTheSunkenSeas(),
                        **config)
    
    if jingyuanCone == 'EternalCalculus':
        JingyuanLightCone = EternalCalculus(**config)
    elif jingyuanCone == 'TheSeriousnessOfBreakfast':
        JingyuanLightCone = TheSeriousnessOfBreakfast(**config)        
    JingYuanCharacter = JingYuan(RelicStats(mainstats = JingYuanMainstats,
                        substats = JingYuanSubstats),
                        lightcone = JingyuanLightCone,
                        relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(followupStacks=6.5,stacks=8.0,uptime=1.0), planarset = TheWondrousBananAmusementPark(),
                        **config)
    
    BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'ER'],
                        substats = {'CD': 12, 'SPD.flat': 8, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = DanceDanceDance(**config),
                        eidolon = bronyaEidolon,
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = LushakaTheSunkenSeas(),
                        **config)
    
    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                        substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = SacerdosRelivedOrdeal2pc(), planarset = LushakaTheSunkenSeas(),
                        **config)
    
    team = [JingYuanCharacter, SundayCharacter, BronyaCharacter, GallagherCharacter]

    #%% JingYuan Sunday Bronya Gallagher Team Buffs
            
    # Sunday Buffs
    SundayCharacter.addStat('CD',description='Sacerdos Bronya',amount=0.18, stacks=1.0)
    SundayCharacter.applySkillBuff(JingYuanCharacter,uptime=1.0,hasSummon=True)
    SundayUltUptime = 1.0 if SundayCharacter.lightcone.name == 'A Grounded Ascent' else 0.75
    SundayCharacter.applyUltBuff(JingYuanCharacter,uptime=SundayUltUptime)
    JingYuanCharacter.addStat('CD',description='Sacerdos Sunday',amount=0.18, stacks=(1.0 + SundayUltUptime / 3.0))
    
    if SundayCharacter.lightcone.name == 'A Grounded Ascent':
        JingYuanCharacter.addStat('DMG',description='A Grounded Ascent',
                                  amount = 0.1275 + 0.0225 * SundayCharacter.lightcone.superposition,
                                  stacks=3.0)
        
    # Bronya Buffs
    BronyaUltUptime = 0.5
    BronyaCharacter.applyTraceBuff(team)
    BronyaCharacter.applyUltBuff(JingYuanCharacter,uptime=BronyaUltUptime / 3) 
    BronyaCharacter.applyUltBuff(SundayCharacter,uptime=BronyaUltUptime / 2) 
    BronyaCharacter.applyUltBuff(GallagherCharacter,uptime=BronyaUltUptime) 
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)

    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
    for character in team:
        character.print()

    #%% JingYuan Sunday Bronya Gallagher Rotations
    SundayRotation = [SundayCharacter.useSkill() * 3.0 / SundayUltUptime,
                      BronyaCharacter.useAdvanceForward() * 3.0 / SundayUltUptime / 2.0,
                      SundayCharacter.useUltimate(),]

    # Rotation is calculated per ult, so we'll attenuate this to fit 3 Sunday turns    
    numSkill = 3.5
    numUlt = 1.0

    numTalent = 3.0 * numSkill * (2.0 / 3.0) # lightning lord base
    numTalent += 2.0 * numSkill # +2 from skill
    numTalent += 3.0 # +3 from ultimate

    JingYuanRotation = [ # 3 enhanced basics per ult roughly
                    JingYuanCharacter.useSkill() * numSkill,
                    JingYuanCharacter.useTalent() * numTalent,
                    JingYuanCharacter.useUltimate() * numUlt, # 1 charge
                    SundayCharacter.useAdvanceForward() * numSkill * 2.0 / 3.0, # 2 advance forwards for every 3 skills
                ]

    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    numBasicGallagher = 4.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1,]
    if GallagherCharacter.lightcone.name == 'Multiplication':
        GallagherRotation[-1].actionvalue += 0.20 # advance foward cannot exceed a certain amount

    #%% JingYuan Sunday Bronya Gallagher Rotation Math
    totalJingYuanEffect = sumEffects(JingYuanRotation)
    totalSundayEffect = sumEffects(SundayRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    JingYuanRotationDuration = totalJingYuanEffect.actionvalue * 100.0 / JingYuanCharacter.getTotalStat('SPD')
    SundayRotationDuration = totalSundayEffect.actionvalue * 100.0 / SundayCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()

    DanceDanceDanceEffect.actionvalue = -0.24
    if SundayCharacter.lightcone.name == 'Dance! Dance! Dance!':
        DanceDanceDanceEffect.actionvalue *= 3 # bronya ults every 4 turns, so does sunday, but sunday acts twice as often
    BronyaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    BronyaRotation.append(deepcopy(DanceDanceDanceEffect))
    totalBronyaEffect = sumEffects(BronyaRotation)
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')

    DanceDanceDanceEffect.actionvalue = -0.24 * JingYuanRotationDuration / BronyaRotationDuration
    JingYuanCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    JingYuanRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * SundayRotationDuration / BronyaRotationDuration
    SundayCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    SundayRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * GallagherRotationDuration / BronyaRotationDuration
    GallagherCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    GallagherRotation.append(deepcopy(DanceDanceDanceEffect))
    
    totalSundayEffect = sumEffects(SundayRotation)
    totalJingYuanEffect = sumEffects(JingYuanRotation)
    totalHuohuoEffect = sumEffects(GallagherRotation)

    JingYuanRotationDuration = totalJingYuanEffect.actionvalue * 100.0 / JingYuanCharacter.getTotalStat('SPD')
    SundayRotationDuration = totalSundayEffect.actionvalue * 100.0 / SundayCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    JingYuanRotation.append(SundayCharacter.giveUltEnergy(JingYuanCharacter) * JingYuanRotationDuration / SundayRotationDuration)
    
    print('##### Rotation Durations #####')
    print('JingYuan: ',JingYuanRotationDuration)
    print('Sunday: ',SundayRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # scale other character's rotation
    SundayRotation = [x * JingYuanRotationDuration / SundayRotationDuration for x in SundayRotation]
    BronyaRotation = [x * JingYuanRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    GallagherRotation = [x * JingYuanRotationDuration / GallagherRotationDuration for x in GallagherRotation]

    JingYuanEstimate = DefaultEstimator(f'Jing Yuan {numSkill:.1f}E {numUlt:.0f}Q', JingYuanRotation, JingYuanCharacter, config)
    SundayEstimate = DefaultEstimator(f'E0 Sunday S{SundayCharacter.lightcone.superposition:d} {SundayCharacter.lightcone.name}', 
                                    SundayRotation, SundayCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E{BronyaCharacter.eidolon} Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    GallagherEstimate = DefaultEstimator(f'{GallagherCharacter.fullName()} {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q', 
                                    GallagherRotation, GallagherCharacter, config)

    return([JingYuanEstimate, SundayEstimate, BronyaEstimate, GallagherEstimate])

