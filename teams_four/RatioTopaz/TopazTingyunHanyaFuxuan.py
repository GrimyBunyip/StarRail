from baseClasses.BaseEffect import BaseEffect, sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Fuxuan import Fuxuan
from characters.harmony.Hanya import Hanya
from characters.harmony.Tingyun import Tingyun
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.DanceDanceDance import DanceDanceDance
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc

def TopazTingyunHanyaFuxuan(config):
    #%% Topaz Tingyun Hanya Fuxuan Characters
    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'ATK.percent', 'CR', 'ATK.percent'],
                        substats = {'CR': 8, 'CD': 12, 'ATK.percent': 5, 'SPD.flat': 3}),
                        lightcone = Swordplay(**config),
                        relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                        **config)

    TingyunCharacter = Tingyun(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'ER'],
                        substats = {'ATK.percent': 8, 'SPD.flat': 12, 'HP.percent': 5, 'DEF.percent': 3}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = SprightlyVonwacq(),
                        benedictionTarget=TopazCharacter,
                        **config)

    HanyaCharacter = Hanya(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CR', 'ER'],
                        substats = {'CR': 8, 'SPD.flat': 12, 'CD': 5, 'ATK.percent': 3}),
                        lightcone = DanceDanceDance(**config),
                        relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(), planarset = BrokenKeel(),
                        **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                        substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                        lightcone = DayOneOfMyNewLife(**config),
                        relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                        **config)
    
    team = [TopazCharacter, TingyunCharacter, HanyaCharacter, FuxuanCharacter]

    #%% Topaz Tingyun Hanya Fuxuan Team Buffs
    for character in [TopazCharacter, TingyunCharacter, HanyaCharacter]:
        character.addStat('CD',description='Broken Keel from Fuxuan',amount=0.1)
    for character in [TopazCharacter, TingyunCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel from Hanya',amount=0.1)
        
    # messenger 4 pc buffs from Hanya:
    TopazCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
    TingyunCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
    FuxuanCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4)

    # messenger 4 pc buffs from Tingyun:
    TopazCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
    HanyaCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/3.0)
    FuxuanCharacter.addStat('SPD.percent',description='Messenger 4 pc',amount=0.12,uptime=1.0/4)

    # Hanya Buffs
    HanyaCharacter.applyBurdenBuff(team)
    HanyaCharacter.applyUltBuff(TopazCharacter,uptime=1.0)
    
    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff([TopazCharacter],uptime=1.0)
    
    # Tingyun Buffs
    TingyunCharacter.applySkillBuff(TopazCharacter)
    TingyunCharacter.applyUltBuff(TopazCharacter)
    
    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)

    #%% Print Statements
    for character in team:
        character.print()

    #%% Topaz Tingyun Hanya Fuxuan Rotations
    numSkillTopaz = 1.7
    numUltTopaz = 1.0
    TopazRotation = [ # 130 max energy
            TopazCharacter.useSkill() * numSkillTopaz,
            TopazCharacter.useUltimate() * numUltTopaz,
            TopazCharacter.useTalent(windfall=True) * 2, # two talents from windfall
            TingyunCharacter.giveUltEnergy() * ( TingyunCharacter.getTotalStat('SPD') * numSkillTopaz / TopazCharacter.getTotalStat('SPD') / 3.0 ), # average tingyun energy
    ]

    topazTurns = sum([x.actionvalue for x in TopazRotation])
    numbyTurns = topazTurns * 80 / TopazCharacter.getTotalStat('SPD')
    numbyAdvanceForwards = topazTurns / 2    
    TopazRotation.append(TopazCharacter.useTalent(windfall=False) * (numbyTurns + numbyAdvanceForwards)) # about 1 talent per basic/skill

    # add benedictions
    TopazRotation.append(TingyunCharacter.useBenediction(['skill','followup']) * numSkillTopaz)
    TopazRotation.append(TingyunCharacter.useBenediction(['talent','followup']) * 2)
    TopazRotation.append(TingyunCharacter.useBenediction(['talent','followup']) * (numbyTurns + numbyAdvanceForwards))

    numHanyaSkill = 4
    numHanyaUlt = 1
    HanyaRotation = [HanyaCharacter.useSkill() * numHanyaSkill,
                    HanyaCharacter.useUltimate() * numHanyaUlt]

    numBasicTingyun = 2.0
    numSkillTingyun = 1.0
    TingyunRotation = [ 
            TingyunCharacter.useBasic() * numBasicTingyun, 
            TingyunCharacter.useSkill() * numSkillTingyun,
            TingyunCharacter.useUltimate(),
    ]

    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]

    #%% Topaz Tingyun Hanya Fuxuan Rotation Math

    totalTopazEffect = sumEffects(TopazRotation)
    totalTingyunEffect = sumEffects(TingyunRotation)
    totalHanyaEffect = sumEffects(HanyaRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    TingyunRotationDuration = totalTingyunEffect.actionvalue * 100.0 / TingyunCharacter.getTotalStat('SPD')
    HanyaRotationDuration = totalHanyaEffect.actionvalue * 100.0 / HanyaCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')

    print('##### Rotation Durations #####')
    print('Topaz: ',TopazRotationDuration)
    print('Tingyun: ',TingyunRotationDuration)
    print('Hanya: ',HanyaRotationDuration)
    print('Fuxuan: ',FuxuanRotationDuration)

    # Scale other character's rotation
    TingyunRotation = [x * TopazRotationDuration / TingyunRotationDuration for x in TingyunRotation]
    HanyaRotation = [x * TopazRotationDuration / HanyaRotationDuration for x in HanyaRotation]
    FuxuanRotation = [x * TopazRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]

    # Apply Dance Dance Dance Effect
    DanceDanceDanceEffect = BaseEffect()
    DanceDanceDanceEffect.actionvalue = -0.24 * TopazRotationDuration / HanyaRotationDuration
    TopazCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    TopazRotation.append(DanceDanceDanceEffect)
    
    TopazCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    TopazRotation.append(DanceDanceDanceEffect)
    
    FuxuanCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    FuxuanRotation.append(DanceDanceDanceEffect)
    
    HanyaCharacter.addDebugInfo(DanceDanceDanceEffect,['buff'],'Dance Dance Dance Effect')
    HanyaRotation.append(DanceDanceDanceEffect)

    TopazEstimate = DefaultEstimator(f'Topaz: {numSkillTopaz:.1f}E {numbyTurns + numbyAdvanceForwards:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    TingyunEstimate = DefaultEstimator(f'E{TingyunCharacter.eidolon:.0f} Tingyun S{TingyunCharacter.lightcone.superposition:.0f} {TingyunCharacter.lightcone.name}, {numBasicTingyun:.1f}N {numSkillTingyun:.1f}E 1Q, 12 spd substats', 
                                    TingyunRotation, TingyunCharacter, config)
    HanyaEstimate = DefaultEstimator('E0 Hanya S{:.0f} {}, 12 Spd Substats'.format(HanyaCharacter.lightcone.superposition, HanyaCharacter.lightcone.name), 
                                      HanyaRotation, HanyaCharacter, config)
    FuxuanEstimate = DefaultEstimator('Fuxuan: 2N 1E 1Q, S{:.0f} {}'.format(FuxuanCharacter.lightcone.superposition, FuxuanCharacter.lightcone.name),
                                    FuxuanRotation, FuxuanCharacter, config)

    return([TopazEstimate, TingyunEstimate, HanyaEstimate, FuxuanEstimate])
