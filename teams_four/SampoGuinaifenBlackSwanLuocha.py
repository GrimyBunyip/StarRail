from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.nihility.Guinaifen import Guinaifen
from characters.nihility.Sampo import Sampo
from characters.nihility.BlackSwan import BlackSwan
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.nihility.BeforeTheTutorialMissionStarts import BeforeTheTutorialMissionStarts
from lightCones.nihility.EyesOfThePrey import EyesOfThePrey
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.PanCosmicCommercialEnterprise import PanCosmicCommercialEnterprise
from relicSets.planarSets.PenaconyLandOfDreams import PenaconyLandOfDreams
from relicSets.planarSets.SpaceSealingStation import SpaceSealingStation
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc

def SampoGuinaifenBlackSwanLuocha(config):
    #%% Sampo Guinaifen BlackSwan Luocha
    SampoCharacter = Sampo(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ER', 'DMG.wind'],
                            substats = {'ATK.percent': 5, 'SPD.flat': 12, 'EHR': 8, 'BreakEffect': 3}),
                            lightcone = BeforeTheTutorialMissionStarts(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = PenaconyLandOfDreams(stacks=2),
                            **config)

    GuinaifenCharacter = Guinaifen(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.fire'],
                            substats = {'ATK.percent': 7, 'SPD.flat': 13, 'EHR': 4, 'BreakEffect': 4}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

    # I'm just going to assume 100% uptime on firmament frontline glamoth
    # Sampo and Guinaifen are a few substats short of base 160 with a 12 substat cap
    # But I'll just generously assume you are able to get there

    BlackSwanCharacter = BlackSwan(RelicStats(mainstats = ['EHR', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 8, 'SPD.flat': 12, 'EHR': 5, 'BreakEffect': 3}),
                            lightcone = EyesOfThePrey(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = PanCosmicCommercialEnterprise(),
                            **config)

    LuochaCharacter = Luocha(RelicStats(mainstats = ['ER', 'SPD.flat', 'ATK.percent', 'ATK.percent'],
                            substats = {'ATK.percent': 7, 'SPD.flat': 12, 'HP.percent': 3, 'RES': 6}),
                            lightcone = Multiplication(**config),
                            relicsetone = PasserbyOfWanderingCloud2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = FleetOfTheAgeless(),
                            **config)
    
    team = [SampoCharacter, GuinaifenCharacter, BlackSwanCharacter, LuochaCharacter]

    #%% Sampo Guinaifen BlackSwan Luocha Team Buffs
    # Fleet of the Ageless Buff
    for character in [SampoCharacter, GuinaifenCharacter, BlackSwanCharacter]:
        character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)
    for character in [BlackSwanCharacter, GuinaifenCharacter, BlackSwanCharacter]:
        character.addStat('DMG.wind',description='Penacony Sampo',amount=0.10)
        
    # Apply Guinaifen Debuff
    GuinaifenCharacter.applyFirekiss(team=team,uptime=1.0)
        
    # Apply Sampo Vulnerability Debuff
    SampoCharacter.applyUltDebuff(team,rotationDuration=2.0)
        
    # Apply BlackSwan Vulnerability Debuff
    SwanUltRotation = 5.0
    BlackSwanCharacter.applySkillDebuff(team,rotationDuration=2.0)
    # BlackSwanCharacter.applyUltDebuff(team,rotationDuration=SwanUltRotation)
    # Epiphany does not apply to detonations, so bump this buff til after the rotation cone

    #%% Print Statements
    for character in team:
        character.print()

    #%% Sampo Guinaifen BlackSwan Luocha Rotations
    # Napkin Math for stacks applied
    
    numDots = 3
    adjacentStackRate = 2 # adjacent ticks when you have 2 enemies
    dotStackRate = numDots * SampoCharacter.numEnemies
    
    # let's not assume sampo skill detonations in this
    SampoStackRate = 0
    
    # Guinaifen applies 2 stacks every ult, 4 turn rotation
    GuinaifenStackRate = 2 * GuinaifenCharacter.numEnemies / 4
    
    # Swan alternates applying basic and skill stacks
    swanBasicStacks = 1 + numDots
    swanSkillStacks = (1 + numDots) * min(3.0,BlackSwanCharacter.numEnemies)
    
    SwanStackRate = (swanBasicStacks + swanSkillStacks) / 2
    
    SwanUltMultiplier = 1.0 + 1.0 / SwanUltRotation # swan ult effectively applies 1 extra rotation of dots every N turns
    netStackRate = adjacentStackRate * SampoCharacter.enemySpeed * SwanUltMultiplier
    netStackRate += dotStackRate * SampoCharacter.enemySpeed * SwanUltMultiplier
    netStackRate += SampoStackRate * SampoCharacter.getTotalStat('SPD') * SwanUltMultiplier
    netStackRate += GuinaifenStackRate * GuinaifenCharacter.getTotalStat('SPD') * SwanUltMultiplier
    netStackRate += SwanStackRate * BlackSwanCharacter.getTotalStat('SPD') * SwanUltMultiplier
    netStackRate = netStackRate / SampoCharacter.enemySpeed / SampoCharacter.numEnemies
    print(f'net Stack Rate per Enemy {netStackRate}')
    
    BlackSwanCharacter.setSacramentStacks(netStackRate)
    
    numBasicSampo = 0
    numSkillSampo = 2
    numUltSampo = 1
    SampoRotation = [
                    SampoCharacter.useBasic() * numBasicSampo,
                    SampoCharacter.useSkill() * numSkillSampo,
                    SampoCharacter.useUltimate() * numUltSampo]

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


    #%% Sampo Guinaifen BlackSwan Luocha Rotation Math
    numDotGuinaifen = DotEstimator(GuinaifenRotation, GuinaifenCharacter, config, dotMode='alwaysBlast')
    numDotGuinaifen = min(numDotGuinaifen, 2.0 * numSkillGuinaifen * min(3.0, GuinaifenCharacter.numEnemies))
    numDotBlackSwan = DotEstimator(BlackSwanRotation, BlackSwanCharacter, config, dotMode='alwaysAll')
    numDotBlackSwan = min(numDotBlackSwan, 3.0 * (numSkillBlackSwan + numUltBlackSwan) * BlackSwanCharacter.numEnemies)
    numDotSampo = DotEstimator(SampoRotation, SampoCharacter, config, dotMode='alwaysBlast')
    numDotSampo = min(numDotSampo, 3.0 * (numSkillSampo + numUltSampo) * SampoCharacter.numEnemies)

    totalSampoEffect = sumEffects(SampoRotation)
    totalGuinaifenEffect = sumEffects(GuinaifenRotation)
    totalBlackSwanEffect = sumEffects(BlackSwanRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    SampoRotationDuration = totalSampoEffect.actionvalue * 100.0 / SampoCharacter.getTotalStat('SPD')
    GuinaifenRotationDuration = totalGuinaifenEffect.actionvalue * 100.0 / GuinaifenCharacter.getTotalStat('SPD')
    BlackSwanRotationDuration = totalBlackSwanEffect.actionvalue * 100.0 / BlackSwanCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's character's rotation
    GuinaifenRotation = [x * SampoRotationDuration / GuinaifenRotationDuration for x in GuinaifenRotation]
    BlackSwanRotation = [x * SampoRotationDuration / BlackSwanRotationDuration for x in BlackSwanRotation]
    LuochaRotation = [x * SampoRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    numDotGuinaifen *= SampoRotationDuration / GuinaifenRotationDuration
    numDotBlackSwan *= SampoRotationDuration / BlackSwanRotationDuration

    SampoEstimate = DefaultEstimator('Sampo S{:.0f} {} {:.0f}N {:.0f}E {:.0f}Q {:.1f}Dot'.format(SampoCharacter.lightcone.superposition, SampoCharacter.lightcone.name, 
                                                                                                numBasicSampo, numSkillSampo, numUltSampo, numDotSampo), 
                                                                                                SampoRotation, SampoCharacter, config, numDot=numDotSampo)
    GuinaifenEstimate = DefaultEstimator('E6 Guinaifen S{:.0f} {} {:.0f}N {:.0f}E {:.0f}Q {:.1f}Dot'.format(GuinaifenCharacter.lightcone.superposition, GuinaifenCharacter.lightcone.name,
                                                                                                            numBasicGuinaifen, numSkillGuinaifen, numUltGuinaifen, numDotGuinaifen),
                                                                                                            GuinaifenRotation, GuinaifenCharacter, config, numDot=numDotGuinaifen)
    BlackSwanEstimate = DefaultEstimator(f'BlackSwan S{BlackSwanCharacter.lightcone.superposition:.0f} {BlackSwanCharacter.lightcone.name} {numBasicBlackSwan:.0f}N {numSkillBlackSwan:.0f}E {numUltBlackSwan:.0f}Q {numDotBlackSwan:.1f}Dot {BlackSwanCharacter.sacramentStacks:.1f}Sacrament', 
                                                                                                BlackSwanRotation, BlackSwanCharacter, config, numDot=numDotBlackSwan)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([SampoEstimate, GuinaifenEstimate, BlackSwanEstimate, LuochaEstimate])