from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Gallagher import Gallagher
from characters.destruction.Firefly import Firefly
from characters.harmony.RuanMei import RuanMei
from characters.harmony.Bronya import Bronya
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.destruction.OnTheFallOfAnAeon import OnTheFallOfAnAeon
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.harmony.PastAndFuture import PastAndFuture
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.ForgeOfTheKalpagniLantern import ForgeOfTheKalpagniLantern
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.IronCavalryAgainstTheScourge import IronCavalryAgainstTheScourge2pc, IronCavalryAgainstTheScourge4pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def FireflyBronyaRuanMeiGallagher(config):
    #%% Firefly Bronya RuanMei Gallagher Characters
    # DEPRECATED BY 2.3V3 beta
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                                    substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                                    lightcone = MemoriesOfThePast(**config),
                                    relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                                    **config)
    
    FireflyCharacter = Firefly(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'BreakEffect'],
                                    substats = {'CD': 5, 'CR': 8, 'BreakEffect': 12, 'SPD.flat': 3}),
                                    lightcone = OnTheFallOfAnAeon(**config),
                                    relicsetone = IronCavalryAgainstTheScourge2pc(),
                                    relicsettwo = IronCavalryAgainstTheScourge4pc(),
                                    planarset = ForgeOfTheKalpagniLantern(),
                                    breakEffectMV=2.681,
                                    **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'CD', 'ER'],
                                    substats = {'CD': 6, 'SPD.flat': 14, 'HP.percent': 5, 'DEF.percent': 3}),
                                    lightcone = PastAndFuture(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = ForgeOfTheKalpagniLantern(),
                                    **config)

    GallagherCharacter = Gallagher(RelicStats(mainstats = ['BreakEffect', 'SPD.flat', 'HP.percent', 'DEF.percent'],
                                    substats = {'BreakEffect': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                                    lightcone = Multiplication(**config),
                                    relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = PenaconyLandOfDreams(),
                                    **config)
    
    team = [FireflyCharacter, BronyaCharacter, RuanMeiCharacter, GallagherCharacter]

    #%% Firefly Bronya RuanMei Gallagher Team Buffs
    for character in team:
        character.addStat('DMG.fire',description='Penacony from Gallagher',amount=0.1)

    # RuanMei Buffs, 3 turn RuanMei rotation
    RuanMeiCharacter.applyWeaknessModifiers(team=team)
    RuanMeiCharacter.applyPassiveBuffs(team=team)
    RuanMeiCharacter.applySkillBuff(team=team,uptime=3.0/3.0)
    RuanMeiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)
    
    # Handle firefly's ult vulnerability separately
    FireflyCharacter.applyUltVulnerability(team=[BronyaCharacter, GallagherCharacter, RuanMeiCharacter])
    
    # Apply Gallagher Debuff
    GallagherCharacter.applyUltDebuff(team=team,rotationDuration=4.0)
        
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    for character in team:
        BronyaCharacter.applyUltBuff(character,uptime=0.4) # only get Bronya ult buff every other rotation


    #%% Print Statements
    for character in team:
        character.print()

    #%% Firefly Bronya RuanMei Gallagher Rotations
    # assume each elite performs 1 single target attack per turn
    # times 2 as the rotation is 2 of her turns long

    numSkillFirefly = 2.0
    numEnhancedFirefly = 5.0
    numUltFirefly = 1.0
    FireflyRotation = [ 
            FireflyCharacter.useSkill() * numSkillFirefly,
            FireflyCharacter.useUltimate() * numUltFirefly,
    ]

    FireflyCharacter.applyUltVulnerability([FireflyCharacter],uptime=1.0)
    
    FireflyRotation += [FireflyCharacter.useEnhancedSkill() * 3.0]

    BronyaCharacter.applySkillBuff(FireflyCharacter,uptime=1.0)
    FireflyCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition)

    FireflyRotation += [FireflyCharacter.useEnhancedSkill() * 2.0]
    
    # Easier to math the necessary number of advance forwards needed to set firefly's rotation Action Value to Bronya's
    bronyaAV = 370.0 / BronyaCharacter.getTotalStat('SPD')
    fireflyAV = 200.0 / FireflyCharacter.getTotalStat('SPD') + 500.0 / (FireflyCharacter.getTotalStat('SPD') + 50.0)
    FireflyRotation += [BronyaCharacter.useAdvanceForward() * (fireflyAV - bronyaAV) * FireflyCharacter.getTotalStat('SPD') / 100.0]
    
    # AV = 3.7 / bronya spd
    # AV_firefly = 7.0 / spd

    numBasicBronya = 1.0
    numSkillBronya = 3.0
    BronyaRotation = [ # 130 max energy
            BronyaCharacter.useBasic() * numBasicBronya,
            BronyaCharacter.useSkill() * numSkillBronya,
            BronyaCharacter.useUltimate(),
    ]

    numBasicRuanMei = 2.0
    numSkillRuanMei = 1.0
    RuanMeiRotation = [RuanMeiCharacter.useBasic() * numBasicRuanMei,
                       RuanMeiCharacter.useSkill() * numSkillRuanMei,
                       RuanMeiCharacter.useUltimate(),]

    numBasicGallagher = 4.0
    numEnhancedGallagher = 1.0
    GallagherRotation = [GallagherCharacter.useBasic() * numBasicGallagher,
                         GallagherCharacter.useEnhancedBasic() * numEnhancedGallagher,
                         GallagherCharacter.useUltimate() * 1,]
    if GallagherCharacter.lightcone.name == 'Multiplication':
        GallagherRotation[-1].actionvalue += 0.20 # advance foward cannot exceed a certain amount

    #%% Firefly Bronya RuanMei Gallagher Rotation Math

    totalFireflyEffect = sumEffects(FireflyRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalGallagherEffect = sumEffects(GallagherRotation)

    FireflyRotationDuration = totalFireflyEffect.actionvalue * 100.0 / FireflyCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    GallagherRotationDuration = totalGallagherEffect.actionvalue * 100.0 / GallagherCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Firefly: ',FireflyRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('RuanMei: ',RuanMeiRotationDuration)
    print('Gallagher: ',GallagherRotationDuration)

    # Scale other character's rotation
    BronyaRotation = [x * FireflyRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    RuanMeiRotation = [x * FireflyRotationDuration / RuanMeiRotationDuration for x in RuanMeiRotation]
    GallagherRotation = [x * FireflyRotationDuration / GallagherRotationDuration for x in GallagherRotation]

    FireflyEstimate = DefaultEstimator(f'Firefly: {numSkillFirefly:.1f}E {numEnhancedFirefly:.1f}Enh {numUltFirefly:.0f}Q', FireflyRotation, FireflyCharacter, config)
    BronyaEstimate = DefaultEstimator(f'Bronya: {numSkillBronya:.0f}E {numBasicBronya:.0f}N Q', BronyaRotation, BronyaCharacter, config)
    RuanMeiEstimate = DefaultEstimator(f'Ruan Mei: {numBasicRuanMei:.0f}N {numSkillRuanMei:.0f}E 1Q, S{RuanMeiCharacter.lightcone.superposition:d} {RuanMeiCharacter.lightcone.name}', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    GallagherEstimate = DefaultEstimator(f'Gallagher: {numBasicGallagher:.0f}N {numEnhancedGallagher:.0f}Enh 1Q, S{GallagherCharacter.lightcone.superposition:d} {GallagherCharacter.lightcone.name}', 
                                    GallagherRotation, GallagherCharacter, config)

    return([FireflyEstimate, BronyaEstimate, GallagherEstimate, RuanMeiEstimate])

