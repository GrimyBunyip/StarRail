from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Huohuo import Huohuo
from characters.destruction.Yunli import Yunli
from characters.harmony.Tingyun import Tingyun
from characters.harmony.Hanabi import Hanabi
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.QuidProQuo import QuidProQuo
from lightCones.destruction.DanceAtSunset import DanceAtSunset
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.SacerdosRelivedOrdeal import SacerdosRelivedOrdeal2pc, SacerdosRelivedOrdeal4pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def YunliTingyunHanabiHuohuo(config, yunliSuperposition:int=0):
    #%% Yunli Tingyun Hanabi Huohuo Characters
    yunliLightCone = OnTheFallOfAnAeon(uptime = 0.5, stacks=4.0, **config) if yunliSuperposition == 0 else DanceAtSunset(superposition=yunliSuperposition, **config)
    YunliCharacter = Yunli(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.physical'],
                            substats = {'CD': 8, 'CR': 12, 'ATK.percent': 5, 'BreakEffect': 3}),
                            lightcone = yunliLightCone,
                            relicsetone = WindSoaringValorous2pc(),
                            relicsettwo = WindSoaringValorous4pc(),
                            planarset = InertSalsotto(),
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = FleetOfTheAgeless(),
                            benedictionTarget=YunliCharacter,
                            **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'SPD.flat', 'ER'],
                            substats = {'CD': 8, 'SPD.flat': 12, 'RES': 5, 'DEF.percent': 3}),
                            lightcone = DanceDanceDance(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                            **config)

    HuohuoCharacter = Huohuo(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'HP.flat': 3, 'RES': 6}),
                        lightcone = QuidProQuo(**config),
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [YunliCharacter, TingyunCharacter, HanabiCharacter, HuohuoCharacter]

    #%% Yunli Tingyun Hanabi Huohuo Team Buffs

    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=YunliCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=3.0/3.0)
    YunliCharacter.addStat('CD',description='Sacerdos Hanabi',amount=0.18, stacks=2)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(YunliCharacter)
    TingyunCharacter.applyUltBuff(YunliCharacter,targetSpdMult=HanabiCharacter.getTotalStat('SPD')/YunliCharacter.getTotalStat('SPD'))
    YunliCharacter.addStat('CD',description='Sacerdos Tingyun',amount=0.18, stacks=4.0/3.0)
    
    # Huohuo Buffs
    HuohuoCharacter.applyUltBuff([TingyunCharacter,HanabiCharacter, YunliCharacter],uptime=2.0/4.0)

    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
    for character in team:
        character.print()

    #%% Yunli Tingyun Hanabi Huohuo Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long
    numSkillYunli = 1.9
    numUltYunli = 2.0
    
    numEnemyAttacks = YunliCharacter.enemySpeed * YunliCharacter.numEnemies * numSkillYunli / (HanabiCharacter.getTotalStat('SPD') / 0.92 ) # enemy attacks now scale to hanabi speed, account for S5 dance dance in denominator
    numTalentYunli = (numEnemyAttacks - numUltYunli) 
    numTalentYunli *= YunliCharacter.getTotalStat('Taunt')
    numTalentYunli /= (YunliCharacter.getTotalStat('Taunt') + 
                       TingyunCharacter.getTotalStat('Taunt') + 
                       HanabiCharacter.getTotalStat('Taunt') + 
                       HuohuoCharacter.getTotalStat('Taunt'))

    YunliRotation = [
            YunliCharacter.useSkill() * numSkillYunli,
            YunliCharacter.useTalent() * numTalentYunli,
            YunliCharacter.useEnhancedUltimate() * numUltYunli,
            HanabiCharacter.useAdvanceForward(advanceAmount=1.0 - YunliCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')) * numSkillYunli,
    ]
    
    TingyunRotation = [ 
        TingyunCharacter.useBasic() * 2, 
        TingyunCharacter.useSkill(),
        TingyunCharacter.useUltimate(),
    ]
    
    numBasicHanabi = 0.0
    numSkillHanabi = 3.0
    HanabiRotation = [HanabiCharacter.useBasic() * numBasicHanabi,
                       HanabiCharacter.useSkill() * numSkillHanabi,
                    HanabiCharacter.useUltimate()]

    numBasicHuohuo = 3.0
    numSkillHuohuo = 1.0
    HuohuoRotation = [HuohuoCharacter.useBasic() * numBasicHuohuo,
                    HuohuoCharacter.useSkill() * numSkillHuohuo,
                    HuohuoCharacter.useUltimate(),]

    #%% Yunli Tingyun Hanabi Huohuo Rotation Math

    totalYunliEffect = sumEffects(YunliRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    YunliRotationDuration = totalYunliEffect.actionvalue * 100.0 / YunliCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()

    DanceDanceDanceEffect.actionvalue = -0.24
    HanabiCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    HanabiRotation.append(deepcopy(DanceDanceDanceEffect))
    totalHanabiEffect = sumEffects(HanabiRotation)
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')

    DanceDanceDanceEffect.actionvalue = -0.24 * YunliRotationDuration / HanabiRotationDuration
    YunliCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    YunliRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * TingyunRotationDuration / HanabiRotationDuration
    TingyunCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    TingyunRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * HuohuoRotationDuration / HanabiRotationDuration
    HuohuoCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    HuohuoRotation.append(deepcopy(DanceDanceDanceEffect))
    
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalYunliEffect = sumEffects(YunliRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    YunliRotationDuration = totalYunliEffect.actionvalue * 100.0 / YunliCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    YunliRotation.append(HuohuoCharacter.giveUltEnergy(YunliCharacter) * YunliRotationDuration / HuohuoRotationDuration)
    YunliRotation.append(TingyunCharacter.giveUltEnergy() * YunliRotationDuration / TingyunRotationDuration)
    
    QPQEffect = BaseEffect()
    QPQEffect.energy = 16.0 
    QPQEffect.energy *= 4 # 4  huohuo turns
    QPQEffect.energy *= 3 / (1 + 3 + 1 + 1) # let's say yunli is 3x more likely to get quid pro quo energy
    
    YunliRotation.append(QPQEffect * YunliRotationDuration / HuohuoRotationDuration)
    
    print('##### Rotation Durations #####')
    print('Yunli: ',YunliRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Hanabi: ',HanabiRotationDuration)
    print('Huohuo: ',HuohuoRotationDuration)

    # Scale other character's rotation
    TingyunRotation = [x * YunliRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HanabiRotation = [x * YunliRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    HuohuoRotation = [x * YunliRotationDuration / HuohuoRotationDuration for x in HuohuoRotation]

    YunliEstimate = DefaultEstimator(f'Yunli: {numSkillYunli:.1f}E {numTalentYunli:.1f}T {numUltYunli:.0f}Q', YunliRotation, YunliCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats',
                                    TingyunRotation, TingyunCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    HuohuoEstimate = DefaultEstimator(f'Huohuo: {numBasicHuohuo:.0f}N {numSkillHuohuo:.0f}E 1Q, S{HuohuoCharacter.lightcone.superposition:.0f} {HuohuoCharacter.lightcone.name}',
                                    HuohuoRotation, HuohuoCharacter, config)

    return([YunliEstimate, TingyunEstimate, HanabiEstimate, HuohuoEstimate])

