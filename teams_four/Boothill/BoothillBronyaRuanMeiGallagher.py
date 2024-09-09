from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.hunt.Boothill import Boothill
from characters.harmony.Bronya import Bronya
from characters.harmony.RuanMei import RuanMei
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.hunt.Swordplay import Swordplay
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.planarSets.TaliaKingdomOfBanditry import TaliaKingdomOfBanditry
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def BoothillBronyaRuanMeiGallagher(config):
    #%% Boothill Bronya RuanMei Gallagher Characters
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                        substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = PenaconyLandOfDreams(),
                        **config)
    
    BoothillCharacter = Boothill(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'BreakEffect'],
                        substats = {'SPD.flat': 8, 'BreakEffect': 12, 'CR': 5, 'CD': 3}),
                        lightcone = Swordplay(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = TaliaKingdomOfBanditry(),
                        **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'ER'],
                        substats = {'CD': 12, 'SPD.flat': 8, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = PastAndFuture(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                        substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                        lightcone = Multiplication(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                        **config)
    
    team = [BoothillCharacter, BronyaCharacter, RuanMeiCharacter, GallagherCharacter]

    #%% Boothill Bronya RuanMei Gallagher Team Buffs

    # Messenger 4 pc
    for character in [BoothillCharacter, RuanMeiCharacter, GallagherCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
            
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    BronyaCharacter.applyUltBuff(BoothillCharacter,uptime=1.0/4.0) # estimate 1 bronya buff per 4 rotations
    BronyaCharacter.applyUltBuff(RuanMeiCharacter,uptime=(1.0/4.0) * BronyaCharacter.getTotalStat('SPD') / RuanMeiCharacter.getTotalStat('SPD'))
    BronyaCharacter.applyUltBuff(GallagherCharacter,uptime=(1.0/4.0) * BronyaCharacter.getTotalStat('SPD') / GallagherCharacter.getTotalStat('SPD') / 0.8) # 0.8 for multiplication
    
    # Boothill can get 100% uptime on bronya's 1 turn buffs by using skill then receiving bronya buff
    BronyaCharacter.applySkillBuff(BoothillCharacter,uptime=1.0)
    BoothillCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition)
    
    # assume that weakness broken uptime is increased by 1 ult, and an extra 1.5 because let's say boothill breaks fast
    for character in team:
        character.weaknessBrokenUptime = 1.0 - (1.0 - character.weaknessBrokenUptime) / 1.4

    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)
    #%% Team Buffs and Print Statements
    for character in team:
        character.applyTeamBuffs(team)
        
    for character in team:
        character.print()

    #%% Boothill Bronya RuanMei Gallagher Rotations
    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    numEnhancedBasic = 3.0
    numSkill = 1.5
    numUlt = 1.0

    BoothillRotation = [BoothillCharacter.useSkill() * numSkill,
                        BoothillCharacter.useEnhancedBasic() * numEnhancedBasic,
                        BoothillCharacter.useUltimate() * numUlt, # 1 charge
                        BronyaCharacter.useAdvanceForward() * numEnhancedBasic / 2.0, # 1 advance forward every 2 basics
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

    #%% Boothill Bronya RuanMei Gallagher Rotation Math
    totalBoothillEffect = sumEffects(BoothillRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    BoothillRotationDuration = totalBoothillEffect.actionvalue * 100.0 / BoothillCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Boothill: ',BoothillRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('RuanMei: ',RuanMeiRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # scale other character's rotation
    BronyaRotation = [x * BoothillRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    RuanMeiRotation = [x * BoothillRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    GallagherRotation = [x * BoothillRotationDuration / GallagherRotationDuration for x in GallagherRotation]
    
    # calculate total number of breaks for Ruan Mei Talent
    totalEffect = sumEffects(BoothillRotation + BronyaRotation + RuanMeiRotation + GallagherRotation)
    numBreaks = totalEffect.gauge * RuanMeiCharacter.weaknessBrokenUptime / RuanMeiCharacter.enemyToughness
    RuanMeiRotation.append(RuanMeiCharacter.useTalent() * numBreaks)

    BoothillEstimate = DefaultEstimator(f'Boothill: {numEnhancedBasic:.1f}Enh {numSkill}E {numUlt:.0f}Q',
                                    BoothillRotation, BoothillCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'{RuanMeiCharacter.fullName()} {numBasicRuanMei:.0f}N {numSkillRuanMei:.0f}E 1Q', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    GallagherEstimate = DefaultEstimator(f'{GallagherCharacter.fullName()} {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q', 
                                    GallagherRotation, GallagherCharacter, config)

    return([BoothillEstimate, BronyaEstimate, RuanMeiEstimate, GallagherEstimate])

