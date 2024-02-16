from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.nihility.Guinaifen import Guinaifen
from characters.harmony.RuanMei import RuanMei
from characters.nihility.BlackSwan import BlackSwan
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.nihility.EyesOfThePrey import EyesOfThePrey
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.PanCosmicCommercialEnterprise import PanCosmicCommercialEnterprise
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation
from relicSets.planarSets.SprightlyVonwacq import SprightlyVonwacq
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc
from relicSets.relicSets.ThiefOfShootingMeteor import ThiefOfShootingMeteor2pc, ThiefOfShootingMeteor4pc

def RuanMeiGuinaifenBlackSwanLuocha(config):
    #%% RuanMei Guinaifen BlackSwan Luocha
    
    # do ruan mei first because she needs to alter the enemy speed and toughness uptime
    RuanMeiCharacter = RuanMei(RelicStats(mainstats = ['HP.percent', 'SPD.flat', 'DEF.percent', 'ER'],
                        substats = {'DEF.percent': 3, 'BreakEffect': 12, 'SPD.flat': 8, 'HP.percent': 5}),
                        lightcone = MemoriesOfThePast(**config),
                        relicsetone = ThiefOfShootingMeteor2pc(), relicsettwo = ThiefOfShootingMeteor4pc(), planarset = SprightlyVonwacq(),
                        **config)

    GuinaifenCharacter = Guinaifen(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.fire'],
                            substats = {'ATK.percent': 7, 'SPD.flat': 13, 'EHR': 4, 'BreakEffect': 4}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(stacks=2), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    # I'm just going to assume 100% uptime on firmament frontline glamoth
    # RuanMei and Guinaifen are a few substats short of base 160 with a 12 substat cap
    # But I'll just generously assume you are able to get there

    BlackSwanCharacter = BlackSwan(RelicStats(mainstats = ['EHR', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 12, 'SPD.flat': 5, 'EHR': 8, 'BreakEffect': 3}),
                            lightcone = EyesOfThePrey(**config),
                            sacramentStacks=5.0, # we do not consistently reach def shred stacks here, this number will be recalculated below
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(stacks=2), planarset = PanCosmicCommercialEnterprise(),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                            **config)
    
    team = [RuanMeiCharacter, GuinaifenCharacter, BlackSwanCharacter, LuochaCharacter]

    #%% RuanMei Guinaifen BlackSwan Luocha Team Buffs
    # Fleet of the Ageless Buff
    for character in [RuanMeiCharacter, GuinaifenCharacter, BlackSwanCharacter]:
        character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)
        
    # Apply Guinaifen Debuff
    GuinaifenCharacter.applyFirekiss(team=team,uptime=1.0)
        
    # RuanMei Buffs, max skill uptime
    RuanMeiCharacter.applyWeaknessModifiers(team=team)
    RuanMeiCharacter.applyPassiveBuffs(team=team)
    RuanMeiCharacter.applySkillBuff(team=team,uptime=3.0/3.0)
    RuanMeiCharacter.applyUltBuff(team=team,uptime=2.0/3.0)
        
    # Apply BlackSwan Vulnerability Debuff
    SwanUltRotation = 5.0
    BlackSwanCharacter.applySkillDebuff(team,rotationDuration=2.0)
    # BlackSwanCharacter.applyUltDebuff(team,rotationDuration=SwanUltRotation)
    # Epiphany does not apply to detonations, so bump this buff til after the rotation cone

    #%% Print Statements
    for character in team:
        character.print()

    #%% RuanMei Guinaifen BlackSwan Luocha Rotations
    # Napkin Math for stacks applied
    
    numDots = 2
    adjacentStackRate = 2 * (BlackSwanCharacter.numEnemies - 1) / BlackSwanCharacter.numEnemies
    dotStackRate = numDots * RuanMeiCharacter.numEnemies
    
    # no ruan mei dots
    RuanMeiStackRate = 0
    
    # Guinaifen applies 1 stack every ult, 4 turn rotation
    GuinaifenStackRate = GuinaifenCharacter.numEnemies / 4
    
    # Swan alternates applying basic and skill stacks
    swanBasicStacks = 1 + numDots
    swanSkillStacks = (1 + numDots) * min(3.0,BlackSwanCharacter.numEnemies)
    
    SwanStackRate = (swanBasicStacks + swanSkillStacks) / 2
    
    netStackRate = adjacentStackRate * RuanMeiCharacter.enemyDotSpeed
    netStackRate += dotStackRate * RuanMeiCharacter.enemyDotSpeed
    netStackRate += RuanMeiStackRate * RuanMeiCharacter.getTotalStat('SPD')
    netStackRate += GuinaifenStackRate * GuinaifenCharacter.getTotalStat('SPD')
    netStackRate += SwanStackRate * BlackSwanCharacter.getTotalStat('SPD')
    netStackRate = netStackRate / RuanMeiCharacter.enemyDotSpeed / RuanMeiCharacter.numEnemies
    netStackRate *= 1.0 + 1.0 / SwanUltRotation # swan ult effectively applies 1 extra rotation of dots every N turns
    print(f'net Stack Rate per Enemy {netStackRate}')
    
    BlackSwanCharacter.setSacramentStacks(netStackRate)
    
    numBasicRuanMei = 2.0
    numSkillRuanMei = 1.0
    RuanMeiRotation = [RuanMeiCharacter.useBasic() * numBasicRuanMei,
                       RuanMeiCharacter.useSkill() * numSkillRuanMei,
                    RuanMeiCharacter.useUltimate()]

    BlackSwanDot = BlackSwanCharacter.useDotDetonation()
    numBasicGuinaifen = 2.0
    numSkillGuinaifen = 2.0
    numUltGuinaifen = 1.0
    GuinaifenRotation = [ # 
            GuinaifenCharacter.useBasic() * numBasicGuinaifen,
            GuinaifenCharacter.useSkill() * numSkillGuinaifen,
            GuinaifenCharacter.useUltimate() * numUltGuinaifen,
            BlackSwanDot * GuinaifenCharacter.numEnemies, # Guinaifen detonates swan dot
    ]

    numBasicBlackSwan = SwanUltRotation / 2.0
    numSkillBlackSwan = SwanUltRotation / 2.0
    numUltBlackSwan = 1
    BlackSwanRotation = [
                    BlackSwanCharacter.useBasic() * numBasicBlackSwan,
                    BlackSwanCharacter.useSkill() * numSkillBlackSwan,
                    BlackSwanCharacter.useUltimate() * numUltBlackSwan]
        
    LuochaRotation = [LuochaCharacter.useBasic() * 3,
                    LuochaCharacter.useUltimate() * 1,
                    LuochaCharacter.useSkill() * 1,]
    LuochaRotation[-1].actionvalue = 0.0 #Assume free luocha skill cast
    LuochaRotation[-1].skillpoints = 0.0 #Assume free luocha skill cast
    
    BlackSwanCharacter.applyUltDebuff(team,rotationDuration=SwanUltRotation)
    # Epiphany does not apply to detonations, so bump this buff til after the rotation cone


    #%% RuanMei Guinaifen BlackSwan Luocha Rotation Math
    numDotGuinaifen = DotEstimator(GuinaifenRotation, GuinaifenCharacter, config, dotMode='alwaysBlast')
    numDotGuinaifen = min(numDotGuinaifen, 2.0 * numSkillGuinaifen * min(3.0, GuinaifenCharacter.numEnemies))
    numDotBlackSwan = DotEstimator(BlackSwanRotation, BlackSwanCharacter, config, dotMode='alwaysAll')
    numDotBlackSwan = min(numDotBlackSwan, 3.0 * (numSkillBlackSwan + numUltBlackSwan) * BlackSwanCharacter.numEnemies)

    totalRuanMeiEffect = sumEffects(RuanMeiRotation)
    totalGuinaifenEffect = sumEffects(GuinaifenRotation)
    totalBlackSwanEffect = sumEffects(BlackSwanRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    RuanMeiRotationDuration = totalRuanMeiEffect.actionvalue * 100.0 / RuanMeiCharacter.getTotalStat('SPD')
    GuinaifenRotationDuration = totalGuinaifenEffect.actionvalue * 100.0 / GuinaifenCharacter.getTotalStat('SPD')
    BlackSwanRotationDuration = totalBlackSwanEffect.actionvalue * 100.0 / BlackSwanCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's character's rotation
    GuinaifenRotation = [x * RuanMeiRotationDuration / GuinaifenRotationDuration for x in GuinaifenRotation]
    BlackSwanRotation = [x * RuanMeiRotationDuration / BlackSwanRotationDuration for x in BlackSwanRotation]
    LuochaRotation = [x * RuanMeiRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    numDotGuinaifen *= RuanMeiRotationDuration / GuinaifenRotationDuration
    numDotBlackSwan *= RuanMeiRotationDuration / BlackSwanRotationDuration

    RuanMeiEstimate = DefaultEstimator(f'RuanMei {numSkillRuanMei:.1f}E {numBasicRuanMei:.1f}N S{RuanMeiCharacter.lightcone.superposition:.0f} {RuanMeiCharacter.lightcone.name}, 12 Spd Substats', 
                                    RuanMeiRotation, RuanMeiCharacter, config)
    GuinaifenEstimate = DefaultEstimator('E6 Guinaifen S{:.0f} {} {:.0f}N {:.0f}E {:.0f}Q {:.1f}Dot'.format(GuinaifenCharacter.lightcone.superposition, GuinaifenCharacter.lightcone.name,
                                                                                                            numBasicGuinaifen, numSkillGuinaifen, numUltGuinaifen, numDotGuinaifen),
                                                                                                            GuinaifenRotation, GuinaifenCharacter, config, numDot=numDotGuinaifen)
    BlackSwanEstimate = DefaultEstimator(f'BlackSwan S{BlackSwanCharacter.lightcone.superposition:.0f} {BlackSwanCharacter.lightcone.name} {numBasicBlackSwan:.0f}N {numSkillBlackSwan:.0f}E {numUltBlackSwan:.0f}Q {numDotBlackSwan:.1f}Dot {BlackSwanCharacter.sacramentStacks:.1f}Sacrament', 
                                                                                                BlackSwanRotation, BlackSwanCharacter, config, numDot=numDotBlackSwan)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([BlackSwanEstimate, RuanMeiEstimate, GuinaifenEstimate, LuochaEstimate])