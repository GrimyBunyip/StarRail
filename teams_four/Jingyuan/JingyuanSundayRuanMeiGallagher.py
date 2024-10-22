from copy import deepcopy
from baseClasses import BaseLightCone
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.erudition.JingYuan import JingYuan
from characters.harmony.Sunday import Sunday
from characters.harmony.RuanMei import RuanMei
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.erudition.EternalCalculus import EternalCalculus
from lightCones.erudition.TheSeriousnessOfBreakfast import TheSeriousnessOfBreakfast
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.Swordplay import Swordplay
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.DuranDynastyOfRunningWolves import DuranDynastyOfRunningWolves
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.LushakaTheSunkenSeas import LushakaTheSunkenSeas
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.planarSets.TheWondrousBananAmusementPark import TheWondrousBananAmusementPark
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc, MusketeerOfWildWheat4pc
from relicSets.relicSets.SacerdosRelivedOrdeal import SacerdosRelivedOrdeal2pc, SacerdosRelivedOrdeal4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def JingYuanSundayRuanMeiGallagher(config, 
                                jingyuanCone:BaseLightCone = 'EternalCalculus',
                                sundayCone:BaseLightCone = 'DanceDanceDance',):
    #%% JingYuan Sunday RuanMei Gallagher Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                        substats = {'DEF.percent': 3, 'BreakEffect': 8, 'SPD.flat': 12, 'HP.percent': 5}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = LushakaTheSunkenSeas(),
                        **config)
    
    if jingyuanCone == 'EternalCalculus':
        JingyuanLightCone = EternalCalculus(**config)
    elif jingyuanCone == 'TheSeriousnessOfBreakfast':
        JingyuanLightCone = TheSeriousnessOfBreakfast(**config)
    JingYuanCharacter = JingYuan(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CD', 'DMG.lightning'],
                        substats = {'CD': 8, 'CR': 11, 'ATK.percent': 3, 'SPD.flat': 6}),
                        lightcone = JingyuanLightCone,
                        relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(followupStacks=6.5,stacks=8.0,uptime=1.0), planarset = TheWondrousBananAmusementPark(),
                        **config)

    if sundayCone == 'DanceDanceDance':
        SundayLightCone = DanceDanceDance(**config)
    SundayCharacter = Sunday(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'ER'],
                        substats = {'CD': 12, 'SPD.flat': 0, 'HP.percent': 9, 'DEF.percent': 3}),
                        lightcone = SundayLightCone,
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = BrokenKeel(),
                        **config)

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                        substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = SacerdosRelivedOrdeal2pc(), planarset = LushakaTheSunkenSeas(),
                        **config)
    
    team = [JingYuanCharacter, SundayCharacter, RuanMeiCharacter, GallagherCharacter]

    #%% JingYuan Sunday RuanMei Gallagher Team Buffs
            
    # Sunday Buffs
    SundayCharacter.applyTraceBuff(team)
    SundayCharacter.applySkillBuff(JingYuanCharacter,uptime=1.0,hasSummon=True)
    SundayUltUptime = 1.0 if SundayCharacter.lightcone.name == 'A Grounded Ascent' else 0.75
    SundayCharacter.applyUltBuff(JingYuanCharacter,uptime=SundayUltUptime)
    SundayCharacter.applySkillBuff(JingYuanCharacter,uptime=1.0)
    JingYuanCharacter.addStat('CD',description='Sacerdos Sunday',amount=0.18 * (1.0 + SundayUltUptime / 3.0))
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)

    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
    for character in team:
        character.print()

    #%% JingYuan Sunday RuanMei Gallagher Rotations
    SundayRotation = [SundayCharacter.useSkill() * 3.0 / SundayUltUptime,
                    SundayCharacter.useUltimate(),]

    # Rotation is calculated per ult, so we'll attenuate this to fit 3 Sunday turns    
    numSkill = 3.5
    numUlt = 1.0

    numTalent = 3.0 * numSkill / 2.0 # lightning lord base
    numTalent += 2.0 * numSkill # +2 from skill
    numTalent += 3.0 # +3 from ultimate

    JingYuanRotation = [ # 3 enhanced basics per ult roughly
                    JingYuanCharacter.useSkill() * numSkill,
                    JingYuanCharacter.useTalent() * numTalent,
                    JingYuanCharacter.useUltimate() * numUlt, # 1 charge
                    SundayCharacter.useAdvanceForward() * numSkill / 2.0, # 1 advance forward every 2 skills
                ]

    numBasicRuanMei = 2.0
    numSkillRuanMei = 1.0
    RuanMeiRotation = [RuanMeiCharacter.useBasic() * numBasicRuanMei,
                       RuanMeiCharacter.useSkill() * numSkillRuanMei,
                    RuanMeiCharacter.useUltimate()]

    numBasicGallagher = 4.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1,]
    if GallagherCharacter.lightcone.name == 'Multiplication':
        GallagherRotation[-1].actionvalue += 0.20 # advance foward cannot exceed a certain amount

    #%% JingYuan Sunday RuanMei Gallagher Rotation Math
    totalJingYuanEffect = sumEffects(JingYuanRotation)
    totalSundayEffect = sumEffects(SundayRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    JingYuanRotationDuration = totalJingYuanEffect.actionvalue * 100.0 / JingYuanCharacter.getTotalStat('SPD')
    SundayRotationDuration = totalSundayEffect.actionvalue * 100.0 / SundayCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()

    DanceDanceDanceEffect.actionvalue = -0.24
    SundayCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    SundayRotation.append(deepcopy(DanceDanceDanceEffect))
    totalHanabiEffect = sumEffects(SundayRotation)
    SundayRotationDuration = totalHanabiEffect.actionvalue * 100.0 / SundayCharacter.getTotalStat('SPD')

    DanceDanceDanceEffect.actionvalue = -0.24 * JingYuanRotationDuration / SundayRotationDuration
    JingYuanCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    JingYuanRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * RuanMeiRotationDuration / SundayRotationDuration
    RuanMeiCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    RuanMeiRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * GallagherRotationDuration / SundayRotationDuration
    GallagherCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    GallagherRotation.append(deepcopy(DanceDanceDanceEffect))
    
    totalTingyunEffect = sumEffects(RuanMeiRotation)
    totalJingYuanEffect = sumEffects(JingYuanRotation)
    totalHuohuoEffect = sumEffects(GallagherRotation)

    JingYuanRotationDuration = totalJingYuanEffect.actionvalue * 100.0 / JingYuanCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalTingyunEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    JingYuanRotation.append(SundayCharacter.giveUltEnergy(JingYuanCharacter) * JingYuanRotationDuration / SundayRotationDuration)
    
    print('##### Rotation Durations #####')
    print('JingYuan: ',JingYuanRotationDuration)
    print('Sunday: ',SundayRotationDuration)
    print('RuanMei: ',RuanMeiRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # scale other character's rotation
    SundayRotation = [x * JingYuanRotationDuration / SundayRotationDuration for x in SundayRotation]
    RuanMeiRotation = [x * JingYuanRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    GallagherRotation = [x * JingYuanRotationDuration / GallagherRotationDuration for x in GallagherRotation]

    JingYuanEstimate = DefaultEstimator(f'Jing Yuan {numSkill:.1f}E {numUlt:.0f}Q', JingYuanRotation, JingYuanCharacter, config)
    SundayEstimate = DefaultEstimator(f'E0 Sunday S{SundayCharacter.lightcone.superposition:d} {SundayCharacter.lightcone.name}', 
                                    SundayRotation, SundayCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'{RuanMeiCharacter.fullName()} {numBasicRuanMei:.0f}N {numSkillRuanMei:.0f}E 1Q', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    GallagherEstimate = DefaultEstimator(f'{GallagherCharacter.fullName()} {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q', 
                                    GallagherRotation, GallagherCharacter, config)

    return([JingYuanEstimate, SundayEstimate, RuanMeiEstimate, GallagherEstimate])

