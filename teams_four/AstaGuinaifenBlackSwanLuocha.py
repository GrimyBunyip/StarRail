from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.abundance.Luocha import Luocha
from characters.nihility.Guinaifen import Guinaifen
from characters.harmony.Asta import Asta
from characters.nihility.BlackSwan import BlackSwan
from estimator.DefaultEstimator import DefaultEstimator, DotEstimator
from lightCones.abundance.Multiplication import Multiplication
from lightCones.harmony.MemoriesOfThePast import MemoriesOfThePast
from lightCones.nihility.EyesOfThePrey import EyesOfThePrey
from lightCones.nihility.GoodNightAndSleepWell import GoodNightAndSleepWell
from relicSets.planarSets.FirmamentFrontlineGlamoth import FirmamentFrontlineGlamoth
from relicSets.planarSets.FleetOfTheAgeless import FleetOfTheAgeless
from relicSets.planarSets.PanCosmicCommercialEnterprise import PanCosmicCommercialEnterprise
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc, MessengerTraversingHackerspace4pc
from relicSets.relicSets.PasserbyOfWanderingCloud import PasserbyOfWanderingCloud2pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc, Prisoner4pc

def AstaGuinaifenBlackSwanLuocha(config):
    #%% Asta Guinaifen BlackSwan Luocha
    AstaCharacter = Asta(RelicStats(mainstats = ['ER', 'SPD.flat', 'EHR', 'ATK.percent'],
                                    substats = {'EHR': 8, 'SPD.flat': 12, 'BreakEffect': 3, 'ATK.percent': 5}),
                                    lightcone = MemoriesOfThePast(**config),
                                    relicsetone = MessengerTraversingHackerspace2pc(), relicsettwo = MessengerTraversingHackerspace4pc(uptime=0.5), planarset = FleetOfTheAgeless(),
                                    **config)

    GuinaifenCharacter = Guinaifen(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'ATK.percent', 'DMG.fire'],
                            substats = {'ATK.percent': 7, 'SPD.flat': 13, 'EHR': 4, 'BreakEffect': 4}),
                            lightcone = GoodNightAndSleepWell(**config),
                            relicsetone = Prisoner2pc(), relicsettwo = Prisoner4pc(), planarset = FirmamentFrontlineGlamoth(stacks=2),
                            **config)

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
    
    team = [AstaCharacter, GuinaifenCharacter, BlackSwanCharacter, LuochaCharacter]

    #%% Asta Guinaifen BlackSwan Luocha Team Buffs
    # Fleet of the Ageless Buff
    for character in [AstaCharacter, GuinaifenCharacter, BlackSwanCharacter]:
        character.addStat('ATK.percent',description='Fleet Luocha',amount=0.08)
    for character in [BlackSwanCharacter, GuinaifenCharacter, BlackSwanCharacter]:
        character.addStat('ATK.percent',description='Fleet Asta',amount=0.08)
        
    # Apply Guinaifen Debuff
    GuinaifenCharacter.applyFirekiss(team=team,uptime=1.0)

    # Asta Buffs
    AstaCharacter.applyChargingBuff(team)
    AstaCharacter.applyTraceBuff(team)
    AstaCharacter.applyUltBuff(team,rotation=2.0)
                
    # Apply BlackSwan Vulnerability Debuff
    SwanUltRotation = 5.0
    BlackSwanCharacter.applySkillDebuff(team,rotationDuration=2.0)
    # BlackSwanCharacter.applyUltDebuff(team,rotationDuration=SwanUltRotation)
    # Epiphany does not apply to detonations, so bump this buff til after the rotation cone

    #%% Print Statements
    for character in team:
        character.print()

    #%% Asta Guinaifen BlackSwan Luocha Rotations
    # Napkin Math for stacks applied
    
    numDots = 2
    adjacentStackRate = 2 * (BlackSwanCharacter.numEnemies - 1) / BlackSwanCharacter.numEnemies
    dotStackRate = numDots * AstaCharacter.numEnemies
    
    # Guinaifen applies 1 stack every ult, 4 turn rotation
    GuinaifenStackRate = GuinaifenCharacter.numEnemies / 4
    
    # Swan alternates applying basic and skill stacks
    swanBasicStacks = 1 + numDots
    swanSkillStacks = (1 + numDots) * min(3.0,BlackSwanCharacter.numEnemies)
    
    SwanStackRate = (swanBasicStacks + swanSkillStacks) / 2
    
    netStackRate = adjacentStackRate * AstaCharacter.enemySpeed
    netStackRate += dotStackRate * AstaCharacter.enemySpeed
    netStackRate += GuinaifenStackRate * GuinaifenCharacter.getTotalStat('SPD')
    netStackRate += SwanStackRate * BlackSwanCharacter.getTotalStat('SPD')
    netStackRate = netStackRate / AstaCharacter.enemySpeed / AstaCharacter.numEnemies
    netStackRate *= 1.0 + 1.0 / SwanUltRotation # swan ult effectively applies 1 extra rotation of dots every N turns
    print(f'net Stack Rate per Enemy {netStackRate}')
    
    BlackSwanCharacter.setSacramentStacks(netStackRate)

    numBasicAsta = 1.5
    numSkillAsta = 1.5
    AstaRotation = [AstaCharacter.useBasic() * numBasicAsta,
                    AstaCharacter.useSkill() * numSkillAsta,
                    AstaCharacter.useUltimate() * 1,]

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


    #%% Asta Guinaifen BlackSwan Luocha Rotation Math
    numDotGuinaifen = DotEstimator(GuinaifenRotation, GuinaifenCharacter, config, dotMode='alwaysBlast')
    numDotGuinaifen = min(numDotGuinaifen, 2.0 * numSkillGuinaifen * min(3.0, GuinaifenCharacter.numEnemies))
    numDotBlackSwan = DotEstimator(BlackSwanRotation, BlackSwanCharacter, config, dotMode='alwaysAll')
    numDotBlackSwan = min(numDotBlackSwan, 3.0 * (numSkillBlackSwan + numUltBlackSwan) * BlackSwanCharacter.numEnemies)

    totalAstaEffect = sumEffects(AstaRotation)
    totalGuinaifenEffect = sumEffects(GuinaifenRotation)
    totalBlackSwanEffect = sumEffects(BlackSwanRotation)
    totalLuochaEffect = sumEffects(LuochaRotation)

    AstaRotationDuration = totalAstaEffect.actionvalue * 100.0 / AstaCharacter.getTotalStat('SPD')
    GuinaifenRotationDuration = totalGuinaifenEffect.actionvalue * 100.0 / GuinaifenCharacter.getTotalStat('SPD')
    BlackSwanRotationDuration = totalBlackSwanEffect.actionvalue * 100.0 / BlackSwanCharacter.getTotalStat('SPD')
    LuochaRotationDuration = totalLuochaEffect.actionvalue * 100.0 / LuochaCharacter.getTotalStat('SPD')

    # scale other character's character's rotation
    GuinaifenRotation = [x * AstaRotationDuration / GuinaifenRotationDuration for x in GuinaifenRotation]
    BlackSwanRotation = [x * AstaRotationDuration / BlackSwanRotationDuration for x in BlackSwanRotation]
    LuochaRotation = [x * AstaRotationDuration / LuochaRotationDuration for x in LuochaRotation]
    numDotGuinaifen *= AstaRotationDuration / GuinaifenRotationDuration
    numDotBlackSwan *= AstaRotationDuration / BlackSwanRotationDuration

    AstaEstimate = DefaultEstimator(f'Asta: {numBasicAsta:.1f}N {numSkillAsta:.1f}E 1Q, S{AstaCharacter.lightcone.superposition:d} {AstaCharacter.lightcone.name}', 
                                    AstaRotation, AstaCharacter, config)
    GuinaifenEstimate = DefaultEstimator('E6 Guinaifen S{:.0f} {} {:.0f}N {:.0f}E {:.0f}Q {:.1f}Dot'.format(GuinaifenCharacter.lightcone.superposition, GuinaifenCharacter.lightcone.name,
                                                                                                            numBasicGuinaifen, numSkillGuinaifen, numUltGuinaifen, numDotGuinaifen),
                                                                                                            GuinaifenRotation, GuinaifenCharacter, config, numDot=numDotGuinaifen)
    BlackSwanEstimate = DefaultEstimator(f'BlackSwan S{BlackSwanCharacter.lightcone.superposition:.0f} {BlackSwanCharacter.lightcone.name} {numBasicBlackSwan:.0f}N {numSkillBlackSwan:.0f}E {numUltBlackSwan:.0f}Q {numDotBlackSwan:.1f}Dot {BlackSwanCharacter.sacramentStacks:.1f}Sacrament', 
                                                                                                BlackSwanRotation, BlackSwanCharacter, config, numDot=numDotBlackSwan)
    LuochaEstimate = DefaultEstimator('Luocha: 3N 1E 1Q, S{:.0f} {}'.format(LuochaCharacter.lightcone.superposition, LuochaCharacter.lightcone.name), 
                                    LuochaRotation, LuochaCharacter, config)

    return([AstaEstimate, GuinaifenEstimate, BlackSwanEstimate, LuochaEstimate])