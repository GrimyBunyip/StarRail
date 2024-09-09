from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Huohuo import Huohuo
from characters.destruction.Yunli import Yunli
from characters.harmony.Hanabi import Hanabi
from characters.harmony.Robin import Robin
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.QuidProQuo import QuidProQuo
from lightCones.destruction.DanceAtSunset import DanceAtSunset
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.CarveTheMoonWeaveTheClouds import CarveTheMoonWeaveTheClouds
from lightCones.harmony.ForTomorrowsJourney import ForTomorrowsJourney
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.SacerdosRelivedOrdeal import SacerdosRelivedOrdeal2pc, SacerdosRelivedOrdeal4pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def YunliHanabiRobinHuohuo(config, yunliEidolon:int=None, yunliSuperposition:int=0):
    #%% Yunli Hanabi Robin Huohuo Characters
    yunliLightCone = OnTheFallOfAnAeon(uptime = 0.5, stacks=4.0, **config) if yunliSuperposition == 0 else DanceAtSunset(superposition=yunliSuperposition, **config)
    YunliCharacter = Yunli(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.physical'],
                            substats = {'CD': 8, 'CR': 12, 'ATK.percent': 5, 'ATK.flat': 3}),
                            lightcone = yunliLightCone,
                            relicsetone = WindSoaringValorous2pc(),
                            relicsettwo = WindSoaringValorous4pc(),
                            planarset = InertSalsotto(),
                            eidolon = yunliEidolon,
                            **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'SPD.flat', 'ER'],
                            substats = {'CD': 8, 'SPD.flat': 12, 'RES': 5, 'DEF.percent': 3}),
                            lightcone = CarveTheMoonWeaveTheClouds(**config),
                            relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = SacerdosRelivedOrdeal4pc(), planarset = BrokenKeel(),
                            **config)
    
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'SPD.flat'],
                            substats = {'ATK.percent': 12, 'SPD.flat': 6, 'RES': 3, 'ATK.flat': 7}),
                            lightcone = ForTomorrowsJourney(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                            **config)

    HuohuoCharacter = Huohuo(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'HP.flat': 3, 'RES': 6}),
                        lightcone = QuidProQuo(**config),
                        relicsetone = SacerdosRelivedOrdeal2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [YunliCharacter, HanabiCharacter, RobinCharacter, HuohuoCharacter]

    #%% Yunli Hanabi Robin Huohuo Team Buffs
        
    # Robin Buffs
    RobinUltUptime = 0.5 # assume better robin ult uptime because of shorter robin rotation
    RobinCharacter.applyUltBuff([YunliCharacter,HanabiCharacter,HuohuoCharacter],uptime=RobinUltUptime)

    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    HanabiCharacter.applySkillBuff(character=YunliCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=3.0/3.0)
    YunliCharacter.addStat('CD',description='Sacerdos Hanabi',amount=0.20, stacks=2)
    
    # Huohuo Buffs
    HuohuoCharacter.applyUltBuff([HanabiCharacter,RobinCharacter, YunliCharacter],uptime=2.0/4.0)

    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
    for character in team:
        character.print()

    #%% Yunli Hanabi Robin Huohuo Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long
    numSkillYunli = 2.15 if yunliSuperposition == 0 else 1.75
    numUltYunli = 2.0
    
    numEnemyAttacks = YunliCharacter.enemySpeed * YunliCharacter.numEnemies * numSkillYunli / RobinCharacter.getTotalStat('SPD') # enemy attacks now scale to Robin speed
    numTalentYunli = (numEnemyAttacks - numUltYunli) 
    numTalentYunli *= YunliCharacter.getTotalStat('Taunt')
    numTalentYunli /= (YunliCharacter.getTotalStat('Taunt') + 
                       HanabiCharacter.getTotalStat('Taunt') + 
                       RobinCharacter.getTotalStat('Taunt') + 
                       HuohuoCharacter.getTotalStat('Taunt'))

    # calculate hanabi advance combined with hanabi advance
    advanceAmount = 1.0 - YunliCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')
    advanceCount = numSkillYunli * 4.0 / 5.0 # one robin advance every 4 yunli turns
    YunliRotation = [
            YunliCharacter.useSkill() * numSkillYunli,
            YunliCharacter.useTalent() * numTalentYunli,
            YunliCharacter.useEnhancedUltimate() * numUltYunli,
            RobinCharacter.useAdvanceForward() * (numSkillYunli / 5.0) * (YunliCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')),
            HanabiCharacter.useAdvanceForward(advanceAmount=advanceAmount) * advanceCount,
    ]
    
    RobinRotationYunli = [RobinCharacter.useTalent() * (numSkillYunli + numTalentYunli + numUltYunli)]
    RobinRotationYunli += [RobinCharacter.useConcertoDamage(['skill']) * numSkillYunli * RobinUltUptime]
    RobinRotationYunli += [RobinCharacter.useConcertoDamage(['followup']) * numTalentYunli * RobinUltUptime]
    RobinRotationYunli += [RobinCharacter.useConcertoDamage(['followup','ultimate']) * numUltYunli * RobinUltUptime]
   
    
    numBasicHanabi = 0.0
    numSkillHanabi = 3.0
    HanabiRotation = [HanabiCharacter.useBasic() * numBasicHanabi,
                    HanabiCharacter.useSkill() * numSkillHanabi,
                    HanabiCharacter.useUltimate(),
                    RobinCharacter.useAdvanceForward() * numSkillHanabi / 5.0,]
    
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

    #%% Yunli Hanabi Robin Huohuo Rotation Math

    totalYunliEffect = sumEffects(YunliRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    YunliRotationDuration = totalYunliEffect.actionvalue * 100.0 / YunliCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    YunliRotation.append(HuohuoCharacter.giveUltEnergy(YunliCharacter) * YunliRotationDuration / HuohuoRotationDuration)
    
    QPQEffect = BaseEffect()
    QPQEffect.energy = 16.0 
    QPQEffect.energy *= 4 # 4  huohuo turns
    QPQEffect.energy *= 3 / (1 + 3 + 1 + 1) # let's say yunli is 3x more likely to get quid pro quo energy
    
    YunliRotation.append(QPQEffect * YunliRotationDuration / HuohuoRotationDuration)
    
    print('##### Rotation Durations #####')
    print('Yunli: ',YunliRotationDuration)
    print('Hanabi: ',HanabiRotationDuration)
    print('Robin: ',RobinRotationDuration)
    print('Huohuo: ',HuohuoRotationDuration)

    # Scale other character's rotation
    HanabiRotation = [x * YunliRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    RobinRotation = [x * YunliRotationDuration / RobinRotationDuration for x in RobinRotation]
    HuohuoRotation = [x * YunliRotationDuration / HuohuoRotationDuration for x in HuohuoRotation]
    RobinRotationHuohuo = [x * YunliRotationDuration / HuohuoRotationDuration for x in RobinRotationHuohuo]
    
    RobinRotation += RobinRotationYunli
    RobinRotation += RobinRotationHuohuo
    totalRobinEffect = sumEffects(RobinRotation)

    YunliEstimate = DefaultEstimator(f'Yunli: {numSkillYunli:.1f}E {numTalentYunli:.1f}T {numUltYunli:.0f}Q', YunliRotation, YunliCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    RobinEstimate = DefaultEstimator(f'Robin: {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q, S{RobinCharacter.lightcone.superposition:d} {RobinCharacter.lightcone.name}', 
                                    RobinRotation, RobinCharacter, config)
    HuohuoEstimate = DefaultEstimator(f'Huohuo: {numBasicHuohuo:.0f}N {numSkillHuohuo:.0f}E 1Q, S{HuohuoCharacter.lightcone.superposition:.0f} {HuohuoCharacter.lightcone.name}',
                                    HuohuoRotation, HuohuoCharacter, config)

    return([YunliEstimate, HanabiEstimate, RobinEstimate, HuohuoEstimate])

