from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Lingsha import Lingsha
from characters.hunt.Feixiao import Feixiao
from characters.harmony.Bronya import Bronya
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.abundance.QuidProQuo import QuidProQuo
from lightCones.abundance.ScentAloneStaysTrue import ScentAloneStaysTrue
from lightCones.harmony.PoisedToBloom import PoisedToBloom
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.IVentureForthToHunt import IVentureForthToHunt
from lightCones.hunt.Swordplay import Swordplay
from lightCones.hunt.WorrisomeBlissful import WorrisomeBlissful
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.DuranDynastyOfRunningWolves import DuranDynastyOfRunningWolves
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.IronCavalryAgainstTheScourge import IronCavalryAgainstTheScourge2pc, IronCavalryAgainstTheScourge4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.WindSoaringValorous import WindSoaringValorous2pc, WindSoaringValorous4pc

def FeixiaoBronyaTopazLingsha(config, 
                                feixiaoEidolon:int=None, 
                                feixiaoSuperposition:int=0,
                                topazEidolon:int=None,
                                topazSuperposition:int=0,
                                lingshaSuperposition:int=0):
    #%% Feixiao Bronya Topaz Lingsha Characters

    FeixiaoLightcone = CruisingInTheStellarSea(**config) if feixiaoSuperposition == 0 else IVentureForthToHunt(superposition=feixiaoSuperposition,**config)
    FeixiaoSubstats = {'CR': 7, 'CD': 9, 'ATK.percent': 3, 'SPD.flat':9} if feixiaoSuperposition == 0 else {'CR': 10, 'CD': 6, 'ATK.percent': 3, 'SPD.flat':9}
    FeixiaoCharacter = Feixiao(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'DMG.wind'],
                        substats = FeixiaoSubstats),
                        lightcone = FeixiaoLightcone,
                        relicsetone = WindSoaringValorous2pc(),
                        relicsettwo = WindSoaringValorous4pc(),
                        planarset = DuranDynastyOfRunningWolves(),
                        eidolon = feixiaoEidolon,
                        **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'ER'],
                        substats = {'CD': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = PoisedToBloom(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = WindSoaringValorous2pc(), planarset = BrokenKeel(),
                        **config)

    topazLightcone = Swordplay(**config) if topazSuperposition == 0 else WorrisomeBlissful(superposition=topazSuperposition,**config)
    TopazSubstats = {'CR': 10, 'CD': 5, 'ATK.percent': 3, 'SPD.flat': 10}
    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                        substats = TopazSubstats),
                        lightcone = topazLightcone, 
                        relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = DuranDynastyOfRunningWolves(),
                        eidolon=topazEidolon,
                        **config)

    lingshaLightcone = ScentAloneStaysTrue(**config) if lingshaSuperposition == 0 else QuidProQuo(**config)
    LingshaCharacter = Lingsha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                        substats = {'SPD.flat': 12, 'BreakEffect': 8, 'ATK.percent': 5, 'ATK.flat': 3}),
                        lightcone = lingshaLightcone,
                        relicsetone = IronCavalryAgainstTheScourge4pc(), relicsettwo = IronCavalryAgainstTheScourge2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [FeixiaoCharacter, BronyaCharacter, TopazCharacter, LingshaCharacter]

    #%% Feixiao Bronya Topaz Lingsha Team Buffs
    # Broken Keel Buff
    for character in [FeixiaoCharacter, BronyaCharacter, TopazCharacter]:
        character.addStat('CD',description='Broken Keel Lingsha',amount=0.10)
    for character in [FeixiaoCharacter, TopazCharacter, LingshaCharacter]:
        character.addStat('CD',description='Broken Keel Bronya',amount=0.10)
    for character in [FeixiaoCharacter, TopazCharacter]:
        character.addStat('CD',description='Poised to Bloom',amount=0.12+0.04*BronyaCharacter.lightcone.superposition)

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff(team,uptime=1.0)
    if topazSuperposition > 0:
        for character in [FeixiaoCharacter, BronyaCharacter, LingshaCharacter]:
                character.addStat('CD',description='Worrisome, Blissful',
                                        amount=0.10 + 0.02 * TopazCharacter.lightcone.superposition,
                                        stacks=2.0)
        
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
    BronyaCharacter.applyUltBuff(FeixiaoCharacter,uptime=1.0/4.0) # estimate 1 bronya buff per 4 rotations
    BronyaCharacter.applySkillBuff(FeixiaoCharacter,uptime=1.0,type=['skill','followup','ultimate']) # assume bronya skill buff always applies to skill, fua, and ultimate
    BronyaCharacter.applyUltBuff(TopazCharacter,uptime=(1.0/4.0) * BronyaCharacter.getTotalStat('SPD') / TopazCharacter.getTotalStat('SPD'))
    BronyaCharacter.applyUltBuff(LingshaCharacter,uptime=(1.0/4.0) * BronyaCharacter.getTotalStat('SPD') / LingshaCharacter.getTotalStat('SPD'))
    
    # Apply Lingsha Debuff
    lingshaUltRotation = 3.0
    LingshaCharacter.applyUltDebuff(team=team,rotationDuration=lingshaUltRotation)
    if LingshaCharacter.eidolon >= 2:
        for character in team:
            character.addStat('BreakEffect',description='Lingsha E2',amount=0.4)
    if LingshaCharacter.lightcone.name == 'Scent Alone Stays True':
        for character in team:
            character.addStat('Vulnerability',description='Scent Alone Stays True', 
                              amount=0.14 + 0.04 * LingshaCharacter.lightcone.superposition,
                              uptime=min(1.0, 1.0 / lingshaUltRotation))
    
    # apply Firefly and Lingsha self buffs and MV calculations at the end
    LingshaCharacter.addAttackForTalent()

    #%% Print Statements
    for character in team:
        character.print()

    #%% Feixiao Bronya Topaz Lingsha Rotations
    BronyaRotation = [BronyaCharacter.useSkill() * 4,
                    BronyaCharacter.useUltimate(),]

    numBasicTopaz = 3.5
    numSkillTopaz = 1.0
    numTalentTopaz = (numBasicTopaz + numSkillTopaz) * 2.0 + 1.0 # rough estimate
    TopazRotation = []
    TopazRotation += [TopazCharacter.useBasic() * numBasicTopaz]
    TopazRotation += [TopazCharacter.useSkill() * numSkillTopaz]
    TopazRotation += [TopazCharacter.useUltimate()]
    TopazRotation += [TopazCharacter.useTalent(windfall=True) * 2.0] # two talents from windfall
    TopazRotation += [TopazCharacter.useTalent(windfall=False) * (numTalentTopaz - 1.0)] # deducted windfall advances

    numBasicLingsha = 2.0
    numSkillLingsha = 1.0
    # 1 from ultimate, 1.0 from autoheal, 2.0 from natural turns
    numTalentLingsha = 4.0
    
    LingshaRotation = [LingshaCharacter.useBasic() * numBasicLingsha,
                       LingshaCharacter.useSkill() * numSkillLingsha,
                       LingshaCharacter.useTalent() * numTalentLingsha,
                       LingshaCharacter.useUltimate() * 1,]
    LingshaRotation[0].actionvalue *= 0.8 if LingshaCharacter.lightcone.name == 'Multiplication' else 1.0
    
    
    numBasicFeixiao = 1.0
    numSkillFeixiao = 1.0
    numFollowupFeixiao = numSkillFeixiao * 2.0
    
    feiAttacks = (numBasicFeixiao + numSkillFeixiao + numFollowupFeixiao) # this should be 2 attacks, but dont divide by 2 because bronya
    topazAttacks = (numBasicTopaz + numSkillTopaz + numTalentTopaz + 1.0) / (numBasicTopaz + numSkillTopaz)
    lingshaAttacks = (numBasicLingsha + numSkillLingsha + numTalentLingsha + 1.0) / (numBasicLingsha + numSkillLingsha)
    
    feiTotalAttacks = feiAttacks
    feiTotalAttacks += topazAttacks * TopazCharacter.getTotalStat('SPD') / BronyaCharacter.getTotalStat('SPD')
    feiTotalAttacks += lingshaAttacks * LingshaCharacter.getTotalStat('SPD') / BronyaCharacter.getTotalStat('SPD')
    
    feiTotalStacks = feiTotalAttacks / 2.0
    feiTotalStacks += numBasicFeixiao # bonus stack from talent
    feiTotalStacks += (numFollowupFeixiao if FeixiaoCharacter.eidolon >= 2 else 0.0)
    
    numUltFeixiao = feiTotalStacks / 6.0
    
    FeixiaoRotation = []
    FeixiaoRotation += [FeixiaoCharacter.useBasic() * numBasicFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useSkill() * numSkillFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useTalent() * numFollowupFeixiao]
    FeixiaoRotation += [FeixiaoCharacter.useUltimate() * numUltFeixiao] 
    FeixiaoRotation += [BronyaCharacter.useAdvanceForward() * numBasicFeixiao]

    #%% Feixiao Bronya Topaz Lingsha Rotation Math
    totalFeixiaoEffect = sumEffects(FeixiaoRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalLingshaEffect = sumEffects(LingshaRotation)

    FeixiaoRotationDuration = totalFeixiaoEffect.actionvalue * 100.0 / FeixiaoCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    LingshaRotationDuration = totalLingshaEffect.actionvalue * 100.0 / LingshaCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Feixiao: ',FeixiaoRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Topaz: ',TopazRotationDuration)
    print('Lingsha: ',LingshaRotationDuration)

    # scale other character's rotation
    BronyaRotation = [x * FeixiaoRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    TopazRotation = [x * FeixiaoRotationDuration / TopazRotationDuration for x in TopazRotation]
    LingshaRotation = [x * FeixiaoRotationDuration / LingshaRotationDuration for x in LingshaRotation]

    FeixiaoEstimate = DefaultEstimator(f'{FeixiaoCharacter.fullName()} {numBasicFeixiao:.0f}N {numSkillFeixiao:.0f}E {numFollowupFeixiao:.1f}T {numUltFeixiao:.1f}Q', FeixiaoRotation, FeixiaoCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    TopazEstimate = DefaultEstimator(f'{TopazCharacter.fullName()} {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numTalentTopaz:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    LingshaEstimate = DefaultEstimator(f'{LingshaCharacter.fullName()} {numBasicLingsha:.0f}N {numSkillLingsha:.0f}E {numTalentLingsha:.1f}T 1Q',
                                    LingshaRotation, LingshaCharacter, config)

    return([FeixiaoEstimate, BronyaEstimate, TopazEstimate, LingshaEstimate])

