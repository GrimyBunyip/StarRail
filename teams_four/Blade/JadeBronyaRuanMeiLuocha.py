from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.harmony.Bronya import Bronya
from characters.erudition.Jade import Jade
from characters.harmony.RuanMei import RuanMei
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.erudition.EternalCalculus import EternalCalculus
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.DuranDynastyOfRunningWolves import DuranDynastyOfRunningWolves
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.relicSets.GeniusOfBrilliantStars import GeniusOfBrilliantStars2pc, GeniusOfBrilliantStars4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def JadeBronyaRuanMeiLuocha(config):
    #%% Blade Bronya Jade Luocha Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                        substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = PenaconyLandOfDreams(),
                        **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = PastAndFuture(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

    JadeCharacter = Jade(RelicStats(mainstats = ['CR', 'DMG.quantum', 'ATK.percent', 'ATK.percent'],
                        substats = {'CR': 12, 'CD': 8, 'ATK.percent': 5, 'SPD.flat': 3}),
                        lightcone = EternalCalculus(**config),
                        relicsetone = GeniusOfBrilliantStars2pc(), relicsettwo = GeniusOfBrilliantStars4pc(), planarset = DuranDynastyOfRunningWolves(),
                        **config)
    
    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [RuanMeiCharacter, BronyaCharacter, JadeCharacter, LuochaCharacter]

    #%% Blade Bronya Jade Luocha Team Buffs
    # Broken Keel Buff
    for character in [RuanMeiCharacter, BronyaCharacter, JadeCharacter]:
        character.addStat('CD',description='Broken Keel Luocha',amount=0.10)
    for character in [RuanMeiCharacter, JadeCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel Bronya',amount=0.10)

    # Messenger 4 pc
    for character in [RuanMeiCharacter, JadeCharacter, LuochaCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
            
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    BronyaCharacter.applyUltBuff(JadeCharacter,uptime=1.0/4.0) # estimate 1 bronya buff per 4 turn rotations
    BronyaCharacter.applySkillBuff(JadeCharacter,uptime=1.0/2.0) # estimate 1 bronya skill buff per 2 jade attacks
    BronyaCharacter.applyUltBuff(JadeCharacter,uptime=(1.0/4.0) * BronyaCharacter.getTotalStat('SPD') / JadeCharacter.getTotalStat('SPD'))
    BronyaCharacter.applyUltBuff(LuochaCharacter,uptime=(1.0/4.0) * BronyaCharacter.getTotalStat('SPD') / LuochaCharacter.getTotalStat('SPD') / 0.8)
    JadeCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition, uptime=0.5)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Blade Bronya Jade Luocha Rotations
    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    numBasicRuanMei = 2.0
    numSkillRuanMei = 1.0
    RuanMeiRotation = [RuanMeiCharacter.useBasic() * numBasicRuanMei,
                       RuanMeiCharacter.useSkill() * numSkillRuanMei,
                    RuanMeiCharacter.useUltimate()]

    numBasicJade = 4.0 * 0.8
    numSkillJade = 2.0 * 0.8
    JadeRotation = [JadeCharacter.useBasic() * numBasicJade,
                    JadeCharacter.useSkill() * numSkillJade,
                    JadeCharacter.useUltimate(),
                    JadeCharacter.useEnhancedTalent() * 2.0,
                    BronyaCharacter.useAdvanceForward() * (numBasicJade + numSkillJade) / 2.0,] # 1 advance forward every other turn

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Blade Bronya Jade Luocha Rotation Math
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalJadeEffect = sumEffects(JadeRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    JadeRotationDuration = totalJadeEffect.actionvalue * 100.0 / JadeCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')
    
    num_adjacents = min( JadeCharacter.numEnemies - 1, 2 )
    numTalentJade = 0
    numSkillDamageJade = 0
    
    # apply blade attack stacks first
    numSkillDamageJade += numTalentJade

    # # apply jade's own attack stacks
    numTalentJade += numBasicJade * (1 + num_adjacents)
    numTalentJade += 1.0 * JadeCharacter.numEnemies
    numTalentJade /= 8
    JadeRotation += [JadeCharacter.useTalent() * numTalentJade]
    JadeRotation += [JadeCharacter.useSkillDamage() * numSkillDamageJade]
    
    print('##### Rotation Durations #####')
    print('RuanMei: ',RuanMeiRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Jade: ',JadeRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # scale other character's rotation
    BronyaRotation = [x * JadeRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    RuanMeiRotation = [x * JadeRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    LuochaRotation = [x * JadeRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    RuanMeiEstimate = DefaultEstimator(f'Ruan Mei: {numBasicRuanMei:.0f}N {numSkillRuanMei:.0f}E 1Q, S{RuanMeiCharacter.lightcone.superposition:d} {RuanMeiCharacter.lightcone.name}', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    JadeEstimate = DefaultEstimator(f'Jade: {numBasicJade:.0f}N {numSkillJade:.0f}E {numTalentJade:.1f}T 1Q, S{JadeCharacter.lightcone.superposition:d} {JadeCharacter.lightcone.name}', 
                                    JadeRotation, JadeCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name),
                                    LuochaRotation, LuochaCharacter, config)

    return([JadeEstimate, BronyaEstimate, RuanMeiEstimate, LuochaEstimate])

