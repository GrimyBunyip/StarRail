from copy import deepcopy
from baseClasses import BaseLightCone
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.harmony.Hanya import Hanya
from characters.abundance.Lingsha import Lingsha
from characters.harmony.Sunday import Sunday
from characters.erudition.Jade import Jade
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.DreamsMontage import DreamsMontage
from lightCones.abundance.EchoesOfTheCoffin import EchoesOfTheCoffin
from lightCones.erudition.TheSeriousnessOfBreakfast import TheSeriousnessOfBreakfast
from lightCones.harmony.AGroundedAscent import AGroundedAscent
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.DuranDynastyOfRunningWolves import DuranDynastyOfRunningWolves
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.SacerdosRelivedOrdeal import SacerdosRelivedOrdeal2pc, SacerdosRelivedOrdeal4pc
from relicSets.relicSets.ScholarLostInErudition import ScholarLostInErudition2pc, ScholarLostInErudition4pc

def LingshaSundayJadeHanya(config, 
                          jadeCone:BaseLightCone = None,
                          sundayCone:BaseLightCone = 'DanceDanceDance',
                          lingshaSuperposition = 0,
                          lingshaEidolon = None,):
    #%% Lingsha Sunday Jade Hanya Characters

    lingshaLightcone = DreamsMontage(**config) if lingshaSuperposition == 0 else EchoesOfTheCoffin(**config)
    LingshaCharacter = Lingsha(RelicStats(mainstats = ['ER', 'ATK.percent', 'CR', 'DMG.fire'],
                                    substats = {'SPD.flat': 7, 'CR': 12, 'CD': 6, 'ATK.percent': 3}),
                                    lightcone = lingshaLightcone,
                                    eidolon = lingshaEidolon,
                                    relicsetone = ScholarLostInErudition2pc(), relicsettwo = ScholarLostInErudition4pc(), planarset = DuranDynastyOfRunningWolves(),
                                    **config)

    if sundayCone == 'DanceDanceDance':
        SundayLightCone = DanceDanceDance(**config)
    elif sundayCone == 'A Grounded Ascent':
        SundayLightCone = AGroundedAscent(**config)
        
    SundayCharacter = Sunday(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = SundayLightCone,
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = BrokenKeel(),
                        **config)

    JadeCharacter = Jade(RelicStats(mainstats = ['CR', 'DMG.quantum', 'ATK.percent', 'ATK.percent'],
                        substats = {'CR': 12, 'CD': 8, 'ATK.percent': 5, 'SPD.flat': 3}),
                        lightcone = TheSeriousnessOfBreakfast(**config) if jadeCone == None else jadeCone,
                        relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(followupStacks=6.5,stacks=8.0,uptime=1.0), planarset = DuranDynastyOfRunningWolves(),
                        **config)
    
    HanyaCharacter = Hanya(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [LingshaCharacter, SundayCharacter, JadeCharacter, HanyaCharacter]

    #%% Lingsha Sunday Jade Hanya Team Buffs

    # Jade Buffs, 3 turn Jade rotation
    JadeCharacter.applySkillBuff(LingshaCharacter)
    
    # Sunday Buffs
    SundayCharacter.applySkillBuff(LingshaCharacter,uptime=1.0,hasSummon=True)
    SundayUltUptime = 1.0 if SundayCharacter.lightcone.name == 'A Grounded Ascent' else 0.75
    SundayCharacter.applyUltBuff(LingshaCharacter,uptime=SundayUltUptime)
    LingshaCharacter.addStat('CD',description='Sacerdos Sunday',amount=0.18, stacks=(1.0 + SundayUltUptime / 3.0))
    
    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(JadeCharacter,uptime=1.0)

    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
    for character in team:
        character.print()

    #%% Lingsha Sunday Jade Hanya Rotations
    SundayRotation = [SundayCharacter.useSkill() * 3.0 / SundayUltUptime,
                      SundayCharacter.useUltimate(),]

    numSkillLingsha = 2.0
    numUltLingsha = 1.0
    numTalentLingsha = 2.0

    LingshaRotation = [
                    LingshaCharacter.useSkill() * numSkillLingsha,
                    LingshaCharacter.useUltimate() * numUltLingsha,
                    LingshaCharacter.useTalent() * numTalentLingsha,
                    SundayCharacter.useAdvanceForward() * numSkillLingsha / 2.0,
                ]

    numBasicJade = 2.0
    numSkillJade = 1.0
    JadeRotation = [JadeCharacter.useBasic() * numBasicJade,
                    JadeCharacter.useSkill() * numSkillJade,
                    JadeCharacter.useUltimate(),
                    JadeCharacter.useEnhancedTalent() * 2.0]

    HanyaRotation = [HanyaCharacter.useSkill() * 3,
                    HanyaCharacter.useUltimate() * 1,]

    #%% Lingsha Sunday Jade Hanya Rotation Math
    totalLingshaEffect = sumEffects(LingshaRotation)
    totalSundayEffect = sumEffects(SundayRotation)
    totalJadeEffect = sumEffects(JadeRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)

    LingshaRotationDuration = totalLingshaEffect.actionvalue * 100.0 / LingshaCharacter.getTotalStat('SPD')
    SundayRotationDuration = totalSundayEffect.actionvalue * 100.0 / SundayCharacter.getTotalStat('SPD')
    JadeRotationDuration = totalJadeEffect.actionvalue * 100.0 / JadeCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    
    # Apply Dance Dance Dance Effect
    if SundayCharacter.lightcone.name == 'Dance! Dance! Dance!':
        DanceDanceDanceEffect = BaseEffect()

        DanceDanceDanceEffect.actionvalue = -0.24
        SundayCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
        SundayRotation.append(deepcopy(DanceDanceDanceEffect))
        totalHanabiEffect = sumEffects(SundayRotation)
        SundayRotationDuration = totalHanabiEffect.actionvalue * 100.0 / SundayCharacter.getTotalStat('SPD')

        DanceDanceDanceEffect.actionvalue = -0.24 * LingshaRotationDuration / SundayRotationDuration
        LingshaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
        LingshaRotation.append(deepcopy(DanceDanceDanceEffect))
        
        DanceDanceDanceEffect.actionvalue = -0.24 * JadeRotationDuration / SundayRotationDuration
        JadeCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
        JadeRotation.append(deepcopy(DanceDanceDanceEffect))
        
        DanceDanceDanceEffect.actionvalue = -0.24 * HanyaRotationDuration / SundayRotationDuration
        HanyaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
        HanyaRotation.append(deepcopy(DanceDanceDanceEffect))
        
        totalTingyunEffect = sumEffects(JadeRotation)
        totalLingshaEffect = sumEffects(LingshaRotation)
        totalJadeEffect = sumEffects(HanyaRotation)

        LingshaRotationDuration = totalLingshaEffect.actionvalue * 100.0 / LingshaCharacter.getTotalStat('SPD')
        JadeRotationDuration = totalTingyunEffect.actionvalue * 100.0 / JadeCharacter.getTotalStat('SPD')
        HanyaRotationDuration = totalJadeEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    
    num_adjacents = min( JadeCharacter.numEnemies - 1, 2 )
    num_adjacents = min(num_adjacents,2) if JadeCharacter.eidolon >= 1 else num_adjacents
    numTalentJade = 0
    numSkillDamageJade = 0
    
    # apply Lingsha attack stacks first
    numTalentJade += (numSkillLingsha + numUltLingsha + numTalentLingsha) * LingshaCharacter.numEnemies
    numTalentJade *= JadeRotationDuration / LingshaRotationDuration
    numSkillDamageJade += numTalentJade

    # apply jade's own attack stacks
    numTalentJade += numBasicJade * (1 + num_adjacents)
    numTalentJade += 1.0 * JadeCharacter.numEnemies
    numTalentJade /= 8
    JadeRotation += [JadeCharacter.useTalent() * numTalentJade]
    JadeRotation += [JadeCharacter.useSkillDamage() * numSkillDamageJade]
    
    print('##### Rotation Durations #####')
    print('Lingsha: ',LingshaRotationDuration)
    print('Sunday: ',SundayRotationDuration)
    print('Jade: ',JadeRotationDuration)
    print('Hanya: ',HanyaRotationDuration)

    # scale other character's rotation
    SundayRotation = [x * LingshaRotationDuration / SundayRotationDuration for x in SundayRotation]
    JadeRotation = [x * LingshaRotationDuration / JadeRotationDuration for x in JadeRotation]
    HanyaRotation = [x * LingshaRotationDuration / HanyaRotationDuration for x in HanyaRotation]

    LingshaEstimate = DefaultEstimator(f'{LingshaCharacter.fullName()} {numSkillLingsha:.0f}E {numTalentLingsha:.1f}T 1Q',
                                    LingshaRotation, LingshaCharacter, config)
    SundayEstimate = DefaultEstimator(f'E0 Sunday S{SundayCharacter.lightcone.superposition:d} {SundayCharacter.lightcone.name}', 
                                    SundayRotation, SundayCharacter, config)
    JadeEstimate = DefaultEstimator(f'Jade: {numBasicJade:.1f}N {numSkillJade:.1f}E {numTalentJade:.1f}T 1Q, E{JadeCharacter.eidolon:d} S{JadeCharacter.lightcone.superposition:d} {JadeCharacter.lightcone.name}', 
                                    JadeRotation, JadeCharacter, config)
    HanyaEstimate = DefaultEstimator('Hanya: 3E 1Q, S{:.0f} {}'.format(HanyaCharacter.lightcone.superposition, HanyaCharacter.lightcone.name),
                                    HanyaRotation, HanyaCharacter, config)

    return([LingshaEstimate, SundayEstimate, JadeEstimate, HanyaEstimate])

