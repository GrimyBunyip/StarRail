from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Blade import Blade
from characters.harmony.Bronya import Bronya
from characters.harmony.RuanMei import RuanMei
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.ASecretVow import ASecretVow
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def BladeBronyaRuanMeiLuocha(config):
    #%% Blade Bronya RuanMei Luocha Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                        substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = PenaconyLandOfDreams(),
                        **config)
    
    BladeCharacter = Blade(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'HP.percent'],
                        substats = {'CR': 12, 'CD': 8, 'SPD.flat': 5, 'HP.percent': 3}),
                        lightcone = ASecretVow(uptime=0.0,**config),
                        relicsetone = LongevousDisciple2pc(), relicsettwo = LongevousDisciple4pc(), planarset = RutilantArena(),
                        **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CD', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = PlanetaryRendezvous(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                        **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [BladeCharacter, BronyaCharacter, RuanMeiCharacter, LuochaCharacter]

    #%% Blade Bronya RuanMei Luocha Team Buffs
    # Broken Keel Buff
    for character in [BladeCharacter, BronyaCharacter, RuanMeiCharacter]:
        character.addStat('CD',description='Broken Keel Luocha',amount=0.10)
    for character in [BladeCharacter, RuanMeiCharacter, LuochaCharacter]:
        character.addStat('DMG.wind',description='Penacony Bronya',amount=0.10)

    # Bronya Planetary Rendezvous
    BladeCharacter.addStat('DMG.wind',description='Planetary Rendezvous',amount=0.09 + 0.03 * BronyaCharacter.lightcone.superposition)

    # Messenger 4 pc
    for character in [BladeCharacter, RuanMeiCharacter, LuochaCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)

    # RuanMei Buffs, 3 turn RuanMei rotation
    RuanMeiCharacter.applyWeaknessModifiers(team=team)
    RuanMeiCharacter.applyPassiveBuffs(team=team)
    RuanMeiCharacter.applySkillBuff(team=team,uptime=3.0/3.0)
    RuanMeiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)
            
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    BronyaCharacter.applyUltBuff(BladeCharacter,uptime=1.0/4.0) # estimate 1 bronya buff per 4 rotations
    BronyaCharacter.applySkillBuff(BladeCharacter,uptime=1.0/2.0) # estimate 1 bronya skill buff per 2 blade attacks
    BronyaCharacter.applyUltBuff(RuanMeiCharacter,uptime=(1.0/4.0) * BronyaCharacter.getTotalStat('SPD') / RuanMeiCharacter.getTotalStat('SPD'))
    BronyaCharacter.applyUltBuff(LuochaCharacter,uptime=(1.0/4.0) * BronyaCharacter.getTotalStat('SPD') / LuochaCharacter.getTotalStat('SPD') / 0.8) # 0.8 for multiplication

    #%% Print Statements
    for character in team:
        character.print()

    #%% Blade Bronya RuanMei Luocha Rotations
    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    # Rotation is calculated per ult, so we'll attenuate this to fit 3 bronya turns    
    numBasic = 3.5
    numUlt = 1.0

    BladeRotation = [ # 3 enhanced basics per ult roughly
                    BladeCharacter.useSkill() * numBasic / 4.0, # 0.75 charges
                    BladeCharacter.useEnhancedBasic() * numBasic, # 3 charges
                    BladeCharacter.useUltimate() * numUlt, # 1 charge
                    BronyaCharacter.useAdvanceForward() * numBasic / 2.0, # 1 advance forward every 2 basics
                ]

    numEnemyAttacks = BladeCharacter.enemySpeed * BladeCharacter.numEnemies * sum([x.actionvalue for x in BladeRotation]) / BladeCharacter.getTotalStat('SPD')
    numHitsTaken = numEnemyAttacks * 5 / (5 + 4 + 4 + 4) # assume 3 average threat teammates
    numTalent = (0.75 + 3 + 1 + numHitsTaken) / 5.0
    BladeRotation.append(BladeCharacter.useTalent() * numTalent)

    numBasicRuanMei = 2.0
    numSkillRuanMei = 1.0
    RuanMeiRotation = [RuanMeiCharacter.useBasic() * numBasicRuanMei,
                       RuanMeiCharacter.useSkill() * numSkillRuanMei,
                    RuanMeiCharacter.useUltimate()]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Blade Bronya RuanMei Luocha Rotation Math
    totalBladeEffect = sumEffects(BladeRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    BladeRotationDuration = totalBladeEffect.actionvalue * 100.0 / BladeCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Blade: ',BladeRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('RuanMei: ',RuanMeiRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # scale other character's rotation
    BronyaRotation = [x * BladeRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    RuanMeiRotation = [x * BladeRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    LuochaRotation = [x * BladeRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    
    # calculate total number of breaks for Ruan Mei Talent
    totalEffect = sumEffects(BladeRotation + BronyaRotation + RuanMeiRotation + LuochaRotation)
    numBreaks = totalEffect.gauge * RuanMeiCharacter.weaknessBrokenUptime / RuanMeiCharacter.enemyToughness
    RuanMeiRotation.append(RuanMeiCharacter.useTalent() * numBreaks)

    BladeEstimate = DefaultEstimator(f'Blade: {numBasic:.1f}N {numTalent:.1f}T {numUlt:.0f}Q',
                                    BladeRotation, BladeCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'{RuanMeiCharacter.fullName()} {numBasicRuanMei:.0f}N {numSkillRuanMei:.0f}E 1Q', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name),
                                    LuochaRotation, LuochaCharacter, config)

    return([BladeEstimate, BronyaEstimate, RuanMeiEstimate, LuochaEstimate])

