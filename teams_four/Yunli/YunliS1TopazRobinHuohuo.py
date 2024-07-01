from copy import deepcopy
from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Huohuo import Huohuo
from characters.destruction.Yunli import Yunli
from characters.hunt.Topaz import Topaz
from characters.harmony.Robin import Robin
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.PostOpConversation import PostOpConversation
from lightCones.abundance.QuidProQuo import QuidProQuo
from lightCones.destruction.DanceAtSunset import DanceAtSunset
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.ForTomorrowsJourney import ForTomorrowsJourney
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.DuranDynastyOfRunningWolves import DuranDynastyOfRunningWolves
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.InertSalsotto import InertSalsotto
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def YunliS1TopazRobinHuohuo(config):
    #%% Yunli Topaz Robin Huohuo Characters
    YunliCharacter = Yunli(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.physical'],
                            substats = {'CD': 10, 'CR': 10, 'ATK.percent': 4, 'SPD.flat': 4}),
                            lightcone = DanceAtSunset(**config),
                            relicsetone = WindSoaringValorous2pc(),
                            relicsettwo = WindSoaringValorous4pc(),
                            planarset = InertSalsotto(),
                            **config)
    
    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                            substats = {'CR': 8, 'CD': 8, 'ATK.percent': 3, 'SPD.flat': 9}),
                            lightcone = Swordplay(**config), 
                            relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = DuranDynastyOfRunningWolves(),
                            **config)
    
    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 11, 'SPD.flat': 9, 'RES': 3, 'ATK.flat': 5}),
                            lightcone = ForTomorrowsJourney(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = SprightlyVonwacq(),
                            **config)

    HuohuoCharacter = Huohuo(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'HP.flat': 3, 'RES': 6}),
                        lightcone = QuidProQuo(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [YunliCharacter, TopazCharacter, RobinCharacter, HuohuoCharacter]

    #%% Yunli Topaz Robin Huohuo Team Buffs
    for character in [TopazCharacter, YunliCharacter, RobinCharacter]:
        character.addStat('CD',description='Broken Keel from Huohuo',amount=0.1)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinUltUptime = 0.5 # assume better robin ult uptime because of shorter robin rotation
    RobinCharacter.applyUltBuff([YunliCharacter,TopazCharacter,HuohuoCharacter],uptime=RobinUltUptime)
        

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff([TopazCharacter],uptime=1.0)
    TopazCharacter.applyVulnerabilityDebuff([YunliCharacter, RobinCharacter, HuohuoCharacter],uptime=0.5 + 0.5/YunliCharacter.numEnemies)
    
    # Huohuo Buffs
    HuohuoCharacter.applyUltBuff([TopazCharacter,RobinCharacter, YunliCharacter],uptime=2.0/4.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Yunli Topaz Robin Huohuo Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long
    numSkillYunli = 1.63
    numUltYunli = 2.0
    
    numEnemyAttacks = YunliCharacter.enemySpeed * YunliCharacter.numEnemies * numSkillYunli / (RobinCharacter.getTotalStat('SPD') / 0.92 ) # enemy attacks now scale to Robin speed, account for S5 dance dance in denominator
    numTalentYunli = (numEnemyAttacks - numUltYunli) * (5*6) / (5*6 + 3 + 4 + 4)

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

    numBasicTopaz = 2.0
    numSkillTopaz = 2.0
    numTalentTopaz = (numBasicTopaz + numSkillTopaz) * 0.75 + 1.0 # rough estimate, assume yunli isn't as efficient as others
    TopazRotation = []
    TopazRotation += [TopazCharacter.useBasic() * numBasicTopaz]
    TopazRotation += [TopazCharacter.useSkill() * numSkillTopaz]
    TopazRotation += [TopazCharacter.useUltimate()]
    TopazRotation += [TopazCharacter.useTalent(windfall=True) * 2.0] # two talents from windfall
    TopazRotation += [TopazCharacter.useTalent(windfall=False) * (numTalentTopaz - 1.0)] # deducted windfall advances
    
    RobinRotationTopaz = [RobinCharacter.useTalent() * (numBasicTopaz + numSkillTopaz + numTalentTopaz + 2.0)]
    RobinRotationTopaz += [RobinCharacter.useConcertoDamage(['basic','followup']) * numBasicTopaz * RobinUltUptime]
    RobinRotationTopaz += [RobinCharacter.useConcertoDamage(['skill','followup']) * numSkillTopaz * RobinUltUptime]
    RobinRotationTopaz += [RobinCharacter.useConcertoDamage(['followup']) * numTalentTopaz * RobinUltUptime]
    TopazRotation += [RobinCharacter.useAdvanceForward() * (numSkillTopaz + numBasicTopaz) / 5.0]
    
    numBasicRobin = 2.0
    numSkillRobin = 1.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0) # apply robin buff after we calculate damage for her basics


    numHuohuoBasic = 3.0
    numHuohuoSkill = 1.0
    HuohuoRotation = [HuohuoCharacter.useBasic() * numHuohuoBasic,
                    HuohuoCharacter.useSkill() * numHuohuoSkill,
                    HuohuoCharacter.useUltimate(),
                    RobinCharacter.useAdvanceForward() * (numHuohuoBasic + numHuohuoSkill) / 4.0]
    
    RobinRotationHuohuo = [RobinCharacter.useTalent() * (3.0)]
    RobinRotationHuohuo += [RobinCharacter.useConcertoDamage(['basic']) * 3.0 * RobinUltUptime]

    #%% Yunli Topaz Robin Huohuo Rotation Math

    totalYunliEffect = sumEffects(YunliRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    YunliRotationDuration = totalYunliEffect.actionvalue * 100.0 / YunliCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()

    DanceDanceDanceEffect.actionvalue = -0.24
    RobinCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    RobinRotation.append(deepcopy(DanceDanceDanceEffect))
    totalRobinEffect = sumEffects(RobinRotation)
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')

    DanceDanceDanceEffect.actionvalue = -0.24 * YunliRotationDuration / RobinRotationDuration
    YunliCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    YunliRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * TopazRotationDuration / RobinRotationDuration
    TopazCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    TopazRotation.append(deepcopy(DanceDanceDanceEffect))
    
    DanceDanceDanceEffect.actionvalue = -0.24 * HuohuoRotationDuration / RobinRotationDuration
    HuohuoCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    HuohuoRotation.append(deepcopy(DanceDanceDanceEffect))
    
    totalTopazEffect = sumEffects(TopazRotation)
    totalYunliEffect = sumEffects(YunliRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    YunliRotationDuration = totalYunliEffect.actionvalue * 100.0 / YunliCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    YunliRotation.append(HuohuoCharacter.giveUltEnergy(YunliCharacter) * YunliRotationDuration / HuohuoRotationDuration)
    
    QPQEffect = BaseEffect()
    QPQEffect.energy = 16.0 
    QPQEffect.energy *= 4 # 4  huohuo turns
    QPQEffect.energy *= 3 / (1 + 3 + 1 + 1) # let's say yunli is 3x more likely to get quid pro quo energy
    
    YunliRotation.append(QPQEffect * YunliRotationDuration / HuohuoRotationDuration)
    
    print('##### Rotation Durations #####')
    print('Yunli: ',YunliRotationDuration)
    print('Topaz: ',TopazRotationDuration)
    print('Robin: ',RobinRotationDuration)
    print('Huohuo: ',HuohuoRotationDuration)

    # Scale other character's rotation
    TopazRotation = [x * YunliRotationDuration / TopazRotationDuration for x in TopazRotation]
    RobinRotationTopaz = [x * YunliRotationDuration / TopazRotationDuration for x in RobinRotationTopaz]
    RobinRotation = [x * YunliRotationDuration / RobinRotationDuration for x in RobinRotation]
    HuohuoRotation = [x * YunliRotationDuration / HuohuoRotationDuration for x in HuohuoRotation]
    RobinRotationHuohuo = [x * YunliRotationDuration / HuohuoRotationDuration for x in RobinRotationHuohuo]
    
    RobinRotation += RobinRotationYunli
    RobinRotation += RobinRotationTopaz
    RobinRotation += RobinRotationHuohuo
    totalRobinEffect = sumEffects(RobinRotation)

    YunliEstimate = DefaultEstimator(f'Yunli: {numSkillYunli:.1f}E {numTalentYunli:.1f}T {numUltYunli:.0f}Q', YunliRotation, YunliCharacter, config)
    TopazEstimate = DefaultEstimator(f'Topaz: {TopazCharacter.lightcone.name} {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numTalentTopaz:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    RobinEstimate = DefaultEstimator(f'Robin: {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q, S{RobinCharacter.lightcone.superposition:d} {RobinCharacter.lightcone.name}', 
                                    RobinRotation, RobinCharacter, config)
    HuohuoEstimate = DefaultEstimator(f'Huohuo: {numHuohuoBasic:.0f}N {numHuohuoSkill:.0f}E 1Q, S{HuohuoCharacter.lightcone.superposition:.0f} {HuohuoCharacter.lightcone.name}',
                                    HuohuoRotation, HuohuoCharacter, config)

    return([YunliEstimate, TopazEstimate, RobinEstimate, HuohuoEstimate])

