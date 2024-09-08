from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Huohuo import Huohuo
from characters.destruction.Yunli import Yunli
from characters.harmony.Tingyun import Tingyun
from characters.harmony.Robin import Robin
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.QuidProQuo import QuidProQuo
from lightCones.destruction.DanceAtSunset import DanceAtSunset
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.CarveTheMoonWeaveTheClouds import CarveTheMoonWeaveTheClouds
from lightCones.harmony.ForTomorrowsJourney import ForTomorrowsJourney
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.SacerdosRelivedOrdeal import SacerdosRelivedOrdeal2pc, SacerdosRelivedOrdeal4pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def YunliTingyunRobinHuohuo(config, yunliEidolon:int=None, yunliSuperposition:int=0):
    #%% Yunli Tingyun Robin Huohuo Characters
    yunliLightCone = OnTheFallOfAnAeon(uptime = 0.5, stacks=4.0, **config) if yunliSuperposition == 0 else DanceAtSunset(superposition=yunliSuperposition, **config)
    YunliCharacter = Yunli(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.physical'],
                            substats = {'CD': 10, 'CR': 10, 'ATK.percent': 4, 'SPD.flat': 4}),
                            lightcone = yunliLightCone,
                            relicsetone = WindSoaringValorous2pc(),
                            relicsettwo = WindSoaringValorous4pc(),
                            planarset = InertSalsotto(),
                            eidolon = yunliEidolon,
                            **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                            lightcone = CarveTheMoonWeaveTheClouds(**config),
                            relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = FleetOfTheAgeless(),
                            benedictionTarget=YunliCharacter,
                            **config)
    
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 11, 'SPD.flat': 9, 'RES': 3, 'ATK.flat': 5}),
                            lightcone = ForTomorrowsJourney(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                            **config)

    HuohuoCharacter = Huohuo(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'HP.flat': 3, 'RES': 6}),
                        lightcone = QuidProQuo(**config),
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [YunliCharacter, TingyunCharacter, RobinCharacter, HuohuoCharacter]

    #%% Yunli Tingyun Robin Huohuo Team Buffs
    for character in [TingyunCharacter, YunliCharacter, RobinCharacter]:
        character.addStat('CD',description='Broken Keel from Huohuo',amount=0.1)
    for character in [RobinCharacter, YunliCharacter, RobinCharacter]:
        character.addStat('ATK.percent',description='Fleet from Tingyun',amount=0.08)
        
    # Carve the Moon Buffs
    for character in team:
        character.addStat('ATK.percent',description='Carve The Moon',amount=0.2, uptime=1.0/3.0)
        character.addStat('CD',description='Carve The Moon',amount=0.24, uptime=1.0/3.0)
        character.addStat('ER',description='Carve The Moon',amount=0.12, uptime=1.0/3.0)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinUltUptime = 0.5 # assume better robin ult uptime because of shorter robin rotation
    RobinCharacter.applyUltBuff([YunliCharacter,TingyunCharacter,HuohuoCharacter],uptime=RobinUltUptime)
        
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(YunliCharacter)
    TingyunCharacter.applyUltBuff(YunliCharacter,targetSpdMult=RobinCharacter.getTotalStat('SPD')/YunliCharacter.getTotalStat('SPD'))
    YunliCharacter.addStat('CD',description='Sacerdos Tingyun',amount=0.20)
    
    # Huohuo Buffs
    HuohuoCharacter.applyUltBuff([TingyunCharacter,RobinCharacter, YunliCharacter],uptime=2.0/4.0)
    YunliCharacter.addStat('CD',description='Sacerdos Huohuo',amount=0.20,uptime=2.0/3.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Yunli Tingyun Robin Huohuo Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long
    numSkillYunli = 1.5 if yunliSuperposition == 0 else 1.3
    numUltYunli = 2.0
    
    numEnemyAttacks = YunliCharacter.enemySpeed * YunliCharacter.numEnemies * numSkillYunli / RobinCharacter.getTotalStat('SPD') # enemy attacks now scale to Robin speed
    numTalentYunli = (numEnemyAttacks - numUltYunli) 
    numTalentYunli *= YunliCharacter.getTotalStat('Taunt')
    numTalentYunli /= (YunliCharacter.getTotalStat('Taunt') + 
                       TingyunCharacter.getTotalStat('Taunt') + 
                       RobinCharacter.getTotalStat('Taunt') + 
                       HuohuoCharacter.getTotalStat('Taunt'))

    YunliRotation = [
            YunliCharacter.useSkill() * numSkillYunli,
            YunliCharacter.useTalent() * numTalentYunli,
            YunliCharacter.useEnhancedUltimate() * numUltYunli,
            RobinCharacter.useAdvanceForward() * numSkillYunli / 4.0,
    ]
    
    RobinRotationYunli = [RobinCharacter.useTalent() * (numSkillYunli + numTalentYunli + numUltYunli)]
    RobinRotationYunli += [RobinCharacter.useConcertoDamage(['skill']) * numSkillYunli * RobinUltUptime]
    RobinRotationYunli += [RobinCharacter.useConcertoDamage(['followup']) * numTalentYunli * RobinUltUptime]
    RobinRotationYunli += [RobinCharacter.useConcertoDamage(['followup','ultimate']) * numUltYunli * RobinUltUptime]
    
    TingyunRotation = [ 
        TingyunCharacter.useBasic() * 2, 
        TingyunCharacter.useSkill(),
        TingyunCharacter.useUltimate(),
        RobinCharacter.useAdvanceForward() * 3.0 / 6.0,
    ]
    
    RobinRotationTingyun = [RobinCharacter.useTalent() * (2.0)]
    RobinRotationTingyun += [RobinCharacter.useConcertoDamage(['basic']) * 2.0 * RobinUltUptime]
    
    numBasicRobin = 2.0
    numSkillRobin = 1.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0, ignoreSpeed=True) # apply robin buff after we calculate damage for her basics


    numBasicHuohuo = 3.0
    numSkillHuohuo = 1.0
    HuohuoRotation = [HuohuoCharacter.useBasic() * numBasicHuohuo,
                    HuohuoCharacter.useSkill() * numSkillHuohuo,
                    HuohuoCharacter.useUltimate(),
                    RobinCharacter.useAdvanceForward() * (numBasicHuohuo + numSkillHuohuo) / 5.0]
    
    RobinRotationHuohuo = [RobinCharacter.useTalent() * (3.0)]
    RobinRotationHuohuo += [RobinCharacter.useConcertoDamage(['basic']) * 3.0 * RobinUltUptime]

    #%% Yunli Tingyun Robin Huohuo Rotation Math

    totalYunliEffect = sumEffects(YunliRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    YunliRotationDuration = totalYunliEffect.actionvalue * 100.0 / YunliCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
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
    print('Robin: ',RobinRotationDuration)
    print('Huohuo: ',HuohuoRotationDuration)

    # Scale other character's rotation
    TingyunRotation = [x * YunliRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    RobinRotationTingyun = [x * YunliRotationDuration / TingyunRotationDuration for x in RobinRotationTingyun]
    RobinRotation = [x * YunliRotationDuration / RobinRotationDuration for x in RobinRotation]
    HuohuoRotation = [x * YunliRotationDuration / HuohuoRotationDuration for x in HuohuoRotation]
    RobinRotationHuohuo = [x * YunliRotationDuration / HuohuoRotationDuration for x in RobinRotationHuohuo]
    
    RobinRotation += RobinRotationYunli
    RobinRotation += RobinRotationTingyun
    RobinRotation += RobinRotationHuohuo
    totalRobinEffect = sumEffects(RobinRotation)

    YunliEstimate = DefaultEstimator(f'Yunli: {numSkillYunli:.1f}E {numTalentYunli:.1f}T {numUltYunli:.0f}Q', YunliRotation, YunliCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, 12 spd substats',
                                    TingyunRotation, TingyunCharacter, config)
    RobinEstimate = DefaultEstimator(f'Robin: {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q, S{RobinCharacter.lightcone.superposition:d} {RobinCharacter.lightcone.name}', 
                                    RobinRotation, RobinCharacter, config)
    HuohuoEstimate = DefaultEstimator(f'Huohuo: {numBasicHuohuo:.0f}N {numSkillHuohuo:.0f}E 1Q, S{HuohuoCharacter.lightcone.superposition:.0f} {HuohuoCharacter.lightcone.name}',
                                    HuohuoRotation, HuohuoCharacter, config)

    return([YunliEstimate, TingyunEstimate, RobinEstimate, HuohuoEstimate])

