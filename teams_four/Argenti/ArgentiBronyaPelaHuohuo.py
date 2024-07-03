from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Huohuo import Huohuo
from characters.abundance.Huohuo import Huohuo
from characters.erudition.Argenti import Argenti
from characters.harmony.Bronya import Bronya
from characters.nihility.Pela import Pela
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.PostOpConversation import PostOpConversation
from lightCones.erudition.GeniusesRepose import GeniusesRepose
from lightCones.harmony.PastAndFuture import PastAndFuture
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.nihility.ResolutionShinesAsPearlsOfSweat import ResolutionShinesAsPearlsOfSweat
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation
from relicSets.relicSets.ChampionOfStreetwiseBoxing import ChampionOfStreetwiseBoxing2pc, ChampionOfStreetwiseBoxing4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def ArgentiBronyaPelaHuohuo(config):
    #%% Argenti Bronya Pela Huohuo Characters
    ArgentiCharacter = Argenti(RelicStats(mainstats = ['ATK.percent', 'ATK.percent', 'CR', 'DMG.physical'],
                        substats = {'CR': 12, 'CD': 8, 'SPD.flat': 3, 'ATK.percent': 5}),
                        lightcone =  GeniusesRepose(**config),
                        relicsetone = ChampionOfStreetwiseBoxing2pc(), relicsettwo = ChampionOfStreetwiseBoxing4pc(uptime=0.4), planarset = SpaceSealingStation(),
                        **config)

    BronyaCharacter = Bronya(RelicStats(mainstats = ['HP.percent', 'HP.percent', 'CD', 'ER'],
                        substats = {'CD': 12, 'RES': 6, 'HP.percent': 7, 'DEF.percent': 3}),
                        lightcone = PastAndFuture(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

    PelaCharacter = Pela(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'EHR', 'ER'],
                            substats = {'RES': 6, 'SPD.flat': 12, 'EHR': 7, 'HP.percent': 3}),
                            lightcone = ResolutionShinesAsPearlsOfSweat(**config),
                            relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = LongevousDisciple2pc(), planarset = BrokenKeel(),
                            **config)

    HuohuoCharacter = Huohuo(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'HP.flat': 3, 'RES': 6}),
                        lightcone = PostOpConversation(**config),
                        relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [ArgentiCharacter, BronyaCharacter, PelaCharacter, HuohuoCharacter]

    #%% Argenti Bronya Pela Huohuo Team Buffs
    # Broken Keel and Penacony Buff
    for character in [ArgentiCharacter, BronyaCharacter, PelaCharacter]:
        character.addStat('CD',description='Broken Keel Huohuo',amount=0.10)
    for character in [ArgentiCharacter, PelaCharacter, HuohuoCharacter]:
        character.addStat('CD',description='Broken Keel Bronya',amount=0.10)
    for character in [ArgentiCharacter, PelaCharacter, HuohuoCharacter]:
        character.addStat('CD',description='Broken Keel Pela',amount=0.10)

    # Messenger 4 pc
    for character in [ArgentiCharacter, PelaCharacter, HuohuoCharacter]:
        character.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/5.0)

    # Pela Debuffs, 3 turn pela rotation
    PelaCharacter.applyUltDebuff(team,rotationDuration=3.0)
        
    # Resolution Shines as Pearls of Sweat uptime
    sweatUptime = (1.0 / 2.5) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed
    sweatUptime += (2.0 / 2.5) * PelaCharacter.getTotalStat('SPD') / PelaCharacter.enemySpeed / PelaCharacter.numEnemies
    sweatUptime = min(1.0, sweatUptime)
    for character in team:
        character.addStat('DefShred',description='Resolution Sweat',
                        amount=0.11 + 0.01 * PelaCharacter.lightcone.superposition,
                        uptime=sweatUptime)
        
    # Bronya Buffs
    BronyaCharacter.applyTraceBuff(team)
        
    # Huohuo Buffs
    HuohuoCharacter.applyUltBuff([ArgentiCharacter,BronyaCharacter,PelaCharacter],uptime=2.0/4.0)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Argenti Bronya Pela Huohuo Rotations
    BronyaRotation = [BronyaCharacter.useSkill() * 3, # 3 turn bronya rotation with huohuo
                    BronyaCharacter.useUltimate(),]

    # Assume Bronya skill buff applies to skills, and only applies a fraction of the time to the remaining abilities
    HuohuoEnergyPerRotation = ArgentiCharacter.maxEnergy * (0.21 if HuohuoCharacter.eidolon >= 5 else 0.20)  / 2.0 # estimate about huohuo ult every 2 ults
    HuohuoEnergyPerTurn *= HuohuoCharacter.getTotalStat('SPD') / ArgentiCharacter.getTotalStat('SPD')
    numSkill = (180.0 / ArgentiCharacter.getER() - 5.0 - HuohuoEnergyPerRotation) / (30.0 + 3.0 * ArgentiCharacter.numEnemies)
    numUlt = 1.0

    ArgentiRotation = []

    # 1 skill should have bronya buff, 1 should not.
    ArgentiRotation += [ArgentiCharacter.useSkill() * numSkill / 2.0]
    BronyaCharacter.applySkillBuff(ArgentiCharacter,uptime=1.0)
    ArgentiCharacter.addStat('DMG',description='Past and Future', amount=0.12 + 0.04 * BronyaCharacter.lightcone.superposition)
    ArgentiRotation += [ArgentiCharacter.useSkill() * numSkill / 2.0]
    ArgentiRotation += [ArgentiCharacter.useUltimate() * numUlt]
    ArgentiRotation += [BronyaCharacter.useAdvanceForward() * numSkill / 2.0]

    numBasicPela = 3.0
    PelaRotation = [PelaCharacter.useBasic() * numBasicPela,
                    PelaCharacter.useUltimate(),]

    numBasicHuohuo = 3.0
    numSkillHuohuo = 1.0
    HuohuoRotation = [HuohuoCharacter.useBasic() * numBasicHuohuo,
                    HuohuoCharacter.useSkill() * numSkillHuohuo,
                    HuohuoCharacter.useUltimate(),]

    #%% Argenti Bronya Pela Huohuo Rotation Math
    totalArgentiEffect = sumEffects(ArgentiRotation)
    totalBronyaEffect = sumEffects(BronyaRotation)
    totalPelaEffect = sumEffects(PelaRotation)
    totalHuohuoEffect = sumEffects(HuohuoRotation)

    ArgentiRotationDuration = totalArgentiEffect.actionvalue * 100.0 / ArgentiCharacter.getTotalStat('SPD')
    BronyaRotationDuration = totalBronyaEffect.actionvalue * 100.0 / BronyaCharacter.getTotalStat('SPD')
    PelaRotationDuration = totalPelaEffect.actionvalue * 100.0 / PelaCharacter.getTotalStat('SPD')
    HuohuoRotationDuration = totalHuohuoEffect.actionvalue * 100.0 / HuohuoCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Argenti: ',ArgentiRotationDuration)
    print('Bronya: ',BronyaRotationDuration)
    print('Pela: ',PelaRotationDuration)
    print('Huohuo: ',HuohuoRotationDuration)
    
    ArgentiRotation.append(HuohuoCharacter.giveUltEnergy(ArgentiCharacter) * ArgentiRotationDuration / HuohuoRotationDuration)

    # scale other character's rotation
    BronyaRotation = [x * ArgentiRotationDuration / BronyaRotationDuration for x in BronyaRotation]
    PelaRotation = [x * ArgentiRotationDuration / PelaRotationDuration for x in PelaRotation]
    HuohuoRotation = [x * ArgentiRotationDuration / HuohuoRotationDuration for x in HuohuoRotation]

    ArgentiEstimate = DefaultEstimator(f'Argenti: {numSkill:.1f}E {numUlt:.1f}EnhQ', 
                                            ArgentiRotation, ArgentiCharacter, config)
    BronyaEstimate = DefaultEstimator(f'E0 Bronya S{BronyaCharacter.lightcone.superposition:d} {BronyaCharacter.lightcone.name}, 12 Spd Substats', 
                                    BronyaRotation, BronyaCharacter, config)
    PelaEstimate = DefaultEstimator(f'Pela: {numBasicPela:.0f}N 1Q, S{PelaCharacter.lightcone.superposition:d} {PelaCharacter.lightcone.name}', 
                                    PelaRotation, PelaCharacter, config)
    HuohuoEstimate = DefaultEstimator(f'Huohuo: {numBasicHuohuo:.0f}N {numSkillHuohuo:.0f}E 1Q, S{HuohuoCharacter.lightcone.superposition:.0f} {HuohuoCharacter.lightcone.name}',
                                    HuohuoRotation, HuohuoCharacter, config)
    
    return([ArgentiEstimate, BronyaEstimate, PelaEstimate, HuohuoEstimate])