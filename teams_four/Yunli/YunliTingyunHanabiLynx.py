from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Lynx import Lynx
from characters.destruction.Yunli import Yunli
from characters.harmony.Tingyun import Tingyun
from characters.harmony.Hanabi import Hanabi
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.QuidProQuo import QuidProQuo
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.LushakaTheSunkenSeas import LushakaTheSunkenSeas
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.SacerdosRelivedOrdeal import SacerdosRelivedOrdeal2pc, SacerdosRelivedOrdeal4pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def YunliTingyunHanabiLynx(config):
    #%% Yunli Tingyun Hanabi Lynx Characters
    YunliCharacter = Yunli(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.physical'],
                            substats = {'CD': 8, 'CR': 12, 'ATK.percent': 5, 'BreakEffect': 3}),
                            lightcone = OnTheFallOfAnAeon(uptime = 0.5, stacks=4.0, **config),
                            relicsetone = WindSoaringValorous2pc(),
                            relicsettwo = WindSoaringValorous4pc(),
                            planarset = InertSalsotto(),
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = MemoriesOfThePast(**config),
                            relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = LushakaTheSunkenSeas(),
                            benedictionTarget=YunliCharacter,
                            **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'SPD.flat', 'ER'],
                            substats = {'CD': 8, 'SPD.flat': 12, 'RES': 5, 'DEF.percent': 3}),
                            lightcone = DanceDanceDance(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                            **config)

    LynxCharacter = Lynx(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                            substats = {'HP.percent': 7, 'SPD.flat': 12, 'ATK.percent': 3, 'RES': 6}),
                            lightcone = QuidProQuo(**config),
                            relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                            **config)
    
    team = [YunliCharacter, TingyunCharacter, HanabiCharacter, LynxCharacter]

    #%% Yunli Tingyun Hanabi Lynx Team Buffs

    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=YunliCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=3.0/3.0)
    YunliCharacter.addStat('CD',description='Sacerdos Hanabi',amount=0.18, stacks=2)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(YunliCharacter)
    TingyunCharacter.applyUltBuff(YunliCharacter,targetSpdMult=HanabiCharacter.getTotalStat('SPD')/YunliCharacter.getTotalStat('SPD'))
    YunliCharacter.addStat('CD',description='Sacerdos Tingyun',amount=0.18, stacks=4.0/3.0)

    # Lynx Buffs    
    LynxBuffUptime = LynxCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD') / 3.0
    LynxCharacter.applySkillBuff(YunliCharacter,uptime=LynxBuffUptime)

    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
    for character in team:
        character.print()

    #%% Yunli Tingyun Hanabi Lynx Rotations
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
                       LynxCharacter.getTotalStat('Taunt'))

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

    numBasicLynx = 2.6
    numSkillLynx = 1.4
    LynxRotation = [LynxCharacter.useBasic() * numBasicLynx,
                    LynxCharacter.useSkill() * numSkillLynx,
                    LynxCharacter.useUltimate(),]

    #%% Yunli Tingyun Hanabi Lynx Rotation Math

    totalYunliEffect = sumEffects(YunliRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalLynxEffect = sumEffects(LynxRotation)

    YunliRotationDuration = totalYunliEffect.actionvalue * 100.0 / YunliCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    LynxRotationDuration = totalLynxEffect.actionvalue * 100.0 / LynxCharacter.getTotalStat('SPD')

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
    
    DanceDanceDanceEffect.actionvalue = -0.24 * LynxRotationDuration / HanabiRotationDuration
    LynxCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    LynxRotation.append(deepcopy(DanceDanceDanceEffect))
    
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalYunliEffect = sumEffects(YunliRotation)
    totalLynxEffect = sumEffects(LynxRotation)

    YunliRotationDuration = totalYunliEffect.actionvalue * 100.0 / YunliCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    LynxRotationDuration = totalLynxEffect.actionvalue * 100.0 / LynxCharacter.getTotalStat('SPD')

    YunliRotation.append(TingyunCharacter.giveUltEnergy() * YunliRotationDuration / TingyunRotationDuration)
    
    QPQEffect = BaseEffect()
    QPQEffect.energy = 16.0 
    QPQEffect.energy *= 4 # 4  Lynx turns
    QPQEffect.energy *= 3 / (1 + 3 + 1 + 1) # let's say yunli is 3x more likely to get quid pro quo energy
    
    YunliRotation.append(QPQEffect * YunliRotationDuration / LynxRotationDuration)
    
    print('##### Rotation Durations #####')
    print('Yunli: ',YunliRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Hanabi: ',HanabiRotationDuration)
    print('Lynx: ',LynxRotationDuration)

    # Scale other character's rotation
    TingyunRotation = [x * YunliRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HanabiRotation = [x * YunliRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    LynxRotation = [x * YunliRotationDuration / LynxRotationDuration for x in LynxRotation]

    YunliEstimate = DefaultEstimator(f'Yunli: {numSkillYunli:.1f}E {numTalentYunli:.1f}T {numUltYunli:.0f}Q', YunliRotation, YunliCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats',
                                    TingyunRotation, TingyunCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    LynxEstimate = DefaultEstimator(f'Lynx: {numBasicLynx:.1f}N {numSkillLynx:.1f}E 1Q, S{LynxCharacter.lightcone.superposition:.0f} {LynxCharacter.lightcone.name}',
                                    LynxRotation, LynxCharacter, config)

    return([YunliEstimate, TingyunEstimate, HanabiEstimate, LynxEstimate])

