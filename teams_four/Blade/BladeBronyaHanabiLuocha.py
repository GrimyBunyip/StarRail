from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.destruction.Blade import Blade
from characters.harmony.Bronya import Bronya
from characters.harmony.Hanabi import Hanabi
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.ASecretVow import ASecretVow
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.harmony.PlanetaryRendezvous import PlanetaryRendezvous
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.RutilantArena import RutilantArena
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc, LongevousDisciple4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def BladeBronyaHanabiLuocha(config):
    #%% Blade Bronya Hanabi Luocha Characters
    BladeCharacter = Blade(RelicStats(mainstats = ['HP.percent', 'HP.percent', 'CR', 'HP.percent'],
                        substats = {'CR': 8, 'CD': 12, 'HP.flat': 3, 'HP.percent': 5}),
                        lightcone = ASecretVow(**config,uptime=0.0),
                        relicsetone = LongevousDisciple2pc(), relicsettwo = LongevousDisciple4pc(), planarset = RutilantArena(),
                        **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = PlanetaryRendezvous(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = PenaconyLandOfDreams(),
                        **config)
    
    HanabiCharacter = Hanabi(RelicStats(mainstats = ['CD', 'HP.percent', 'SPD.flat', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'RES': 5, 'DEF.percent': 3}),
                        lightcone = PastAndFuture(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [BladeCharacter, BronyaCharacter, HanabiCharacter, LuochaCharacter]

    #%% Blade Bronya Hanabi Luocha Team Buffs
    # Broken Keel Buff
    for character in [BladeCharacter, BronyaCharacter, HanabiCharacter]:
        character.addStat('CD',description='Broken Keel Luocha',amount=0.10)
    for character in [BladeCharacter, BronyaCharacter, LuochaCharacter]:
        character.addStat('CD',description='Broken Keel Hanabi',amount=0.10)
    for character in [BladeCharacter, HanabiCharacter, LuochaCharacter]:
        character.addStat('DMG.wind',description='Penacony Bronya',amount=0.10)

    # Bronya Planetary Rendezvous
    BladeCharacter.addStat('DMG.wind',description='Planetary Rendezvous',amount=0.09 + 0.03 * BronyaCharacter.lightcone.superposition)

    # Messenger 4 pc from Bronya
    for character in [BladeCharacter, HanabiCharacter, LuochaCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
    # Messenger 4 pc from Hanabi
    for character in [BladeCharacter, BronyaCharacter, LuochaCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
        
    # Hanabi Buffs, max skill uptime
    HanabiCharacter.applyTraceBuff(team=team)
    #HanabiCharacter.applySkillBuff(character=BladeCharacter,uptime=1.0)
    HanabiCharacter.applyUltBuff(team=team,uptime=1.0/3.0)
        
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    BronyaCharacter.applyUltBuff(BladeCharacter,uptime=1.0/4.0) # estimate 1 bronya buff per 4 rotations
    BronyaCharacter.applyUltBuff(LuochaCharacter,uptime=(1.0/4.0) * BronyaCharacter.getTotalStat('SPD') / LuochaCharacter.getTotalStat('SPD') / 0.8)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Blade Bronya Hanabi Luocha Rotations
    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    # Rotation is calculated per ult, so we'll attenuate this to fit 3 bronya turns    
    numBasic = 3.0
    numUlt = 1.0


    BladeRotation = [ # 3 enhanced basics per ult roughly
                    BladeCharacter.useSkill() * numBasic / 4.0, # 0.75 charges
                    #BladeCharacter.useEnhancedBasic() * numBasic, # 3 charges
                    #BladeCharacter.useUltimate() * numUlt, # 1 charge
                    BronyaCharacter.useAdvanceForward() * numBasic / 2.0, # 1 advance forward every 2 basics
                    HanabiCharacter.useAdvanceForward(advanceAmount=1.0 - BladeCharacter.getTotalStat('SPD') / HanabiCharacter.getTotalStat('SPD')) * numBasic / 2.0,
                ]

    BronyaCharacter.applySkillBuff(BladeCharacter,uptime=1.0)
    BladeRotation += [BladeCharacter.useEnhancedBasic() * numBasic / 2.0]
    BladeRotation += [BladeCharacter.useUltimate() * numUlt / 2.0]
    BladeCharacter.stats['DMG'].pop() # remove bronya skill buff
    
    HanabiCharacter.applySkillBuff(character=BladeCharacter,uptime=1.0)
    BladeCharacter.addStat('DMG',description='Past and Future',amount=0.32)
    BladeRotation += [BladeCharacter.useEnhancedBasic() * numBasic / 2.0]
    BladeRotation += [BladeCharacter.useUltimate() * numUlt / 2.0]
    BladeCharacter.stats['CD'].pop() # remove hanabi skill buff
    BladeCharacter.stats['DMG'].pop() # remove Past and Future

    numEnemyAttacks = BladeCharacter.enemySpeed * BladeCharacter.numEnemies * sum([x.actionvalue for x in BladeRotation]) / BladeCharacter.getTotalStat('SPD')
    numHitsTaken = numEnemyAttacks * 5 / (5 + 4 + 4 + 4) # assume 3 average threat teammates
    numTalent = (0.75 + 3 + 1 + numHitsTaken) / 5.0
    BladeRotation.append(BladeCharacter.useTalent() * numTalent)
    
    numBasicHanabi = 0.0
    numSkillHanabi = 3.0
    HanabiRotation = [HanabiCharacter.useBasic() * numBasicHanabi,
                       HanabiCharacter.useSkill() * numSkillHanabi,
                    HanabiCharacter.useUltimate()]

    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast

    #%% Blade Bronya Hanabi Luocha Rotation Math
    totalBladeEffect = sumEffects(BladeRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalHanabiEffect = sumEffects(HanabiRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    BladeRotationDuration = totalBladeEffect.actionvalue * 100.0 / BladeCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    HanabiRotationDuration = totalHanabiEffect.actionvalue * 100.0 / HanabiCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Blade: ',BladeRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Hanabi: ',HanabiRotationDuration)
    print('Luocha: ',LuochaRotationDuration)

    # scale other character's rotation
    BronyaRotation = [x * BladeRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    HanabiRotation = [x * BladeRotationDuration / HanabiRotationDuration for x in HanabiRotation]
    LuochaRotation = [x * BladeRotationDuration / LuochaRotationDuration for x in LuochaRotation]

    BladeEstimate = DefaultEstimator(f'Blade: {numBasic:.0f}N {numTalent:.1f}T {numUlt:.0f}Q',
                                    BladeRotation, BladeCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    HanabiEstimate = DefaultEstimator(f'Hanabi {numSkillHanabi:.1f}E {numBasicHanabi:.1f}N S{HanabiCharacter.lightcone.superposition:.0f} {HanabiCharacter.lightcone.name}, 12 Spd Substats', 
                                    HanabiRotation, HanabiCharacter, config)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name),
                                    LuochaRotation, LuochaCharacter, config)

    return([BladeEstimate, BronyaEstimate, HanabiEstimate, LuochaEstimate])

