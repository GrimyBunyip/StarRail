from baseClasses.BaseEffect import sumEffects
from baseClasses.RelicStats import RelicStats
from characters.preservation.Fuxuan import Fuxuan
from characters.hunt.DrRatio import DrRatio
from characters.harmony.Robin import Robin
from characters.hunt.Topaz import Topaz
from estimator.DefaultEstimator import DefaultEstimator
from lightCones.harmony.ForTomorrowsJourney import ForTomorrowsJourney
from lightCones.harmony.PoisedToBloom import PoisedToBloom
from lightCones.hunt.CruisingInTheStellarSea import CruisingInTheStellarSea
from lightCones.hunt.Swordplay import Swordplay
from lightCones.preservation.DayOneOfMyNewLife import DayOneOfMyNewLife
from relicSets.planarSets.BrokenKeel import BrokenKeel
from relicSets.planarSets.IzumoGenseiAndTakamaDivineRealm import IzumoGenseiAndTakamaDivineRealm
from relicSets.relicSets.AshblazingGrandDuke import GrandDuke2pc, GrandDuke4pc
from relicSets.relicSets.LongevousDisciple import LongevousDisciple2pc
from relicSets.relicSets.MessengerTraversingHackerspace import MessengerTraversingHackerspace2pc
from relicSets.relicSets.MusketeerOfWildWheat import MusketeerOfWildWheat2pc
from relicSets.relicSets.PioneerDiverOfDeadWaters import Pioneer2pc, Pioneer4pc
from relicSets.relicSets.PrisonerInDeepConfinement import Prisoner2pc

def DrRatioTopazRobinFuxuan(config):
    #%% DrRatio Topaz Robin Fuxuan Characters
    DrRatioCharacter = DrRatio(RelicStats(mainstats = ['ATK.percent', 'SPD.flat', 'CD', 'DMG.imaginary'],
                                    substats = {'CD': 5, 'CR': 8, 'ATK.percent': 3, 'SPD.flat': 12}),
                                    lightcone = CruisingInTheStellarSea(**config),
                                    relicsetone = Pioneer2pc(),
                                    relicsettwo = Pioneer4pc(stacks=2),
                                    planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    debuffStacks=3.0, # assume a bit more than 2 average with no third consistent 3rd debuff
                                    **config)

    TopazCharacter = Topaz(RelicStats(mainstats = ['DMG.fire', 'SPD.flat', 'CR', 'ATK.percent'],
                                    substats = {'CR': 7, 'CD': 9, 'ATK.percent': 3, 'SPD.flat': 9}),
                                    lightcone = Swordplay(**config),
                                    relicsetone = GrandDuke2pc(), relicsettwo = GrandDuke4pc(), planarset = IzumoGenseiAndTakamaDivineRealm(),
                                    **config)

    RobinCharacter = Robin(RelicStats(mainstats = ['ER', 'ATK.percent', 'ATK.percent', 'ATK.percent'],
                                    substats = {'ATK.percent': 8, 'SPD.flat': 12, 'RES': 3, 'ATK.flat': 5}),
                                    lightcone = PoisedToBloom(**config),
                                    relicsetone = Prisoner2pc(), relicsettwo = MusketeerOfWildWheat2pc(), planarset = BrokenKeel(),
                                    **config)

    FuxuanCharacter = Fuxuan(RelicStats(mainstats = ['ER', 'SPD.flat', 'HP.percent', 'HP.percent'],
                            substats = {'HP.percent': 7, 'SPD.flat': 12, 'DEF.percent': 3, 'RES': 6}),
                            lightcone = DayOneOfMyNewLife(**config),
                            relicsetone = LongevousDisciple2pc(), relicsettwo = MessengerTraversingHackerspace2pc(), planarset = BrokenKeel(),
                            **config)
    
    team = [DrRatioCharacter, TopazCharacter, RobinCharacter, FuxuanCharacter]

    #%% DrRatio Topaz Robin Fuxuan Team Buffs
    for character in [TopazCharacter, DrRatioCharacter, RobinCharacter]:
        character.addStat('CD',description='Broken Keel from Fuxuan',amount=0.1)
    for character in [TopazCharacter, DrRatioCharacter, FuxuanCharacter]:
        character.addStat('CD',description='Broken Keel from Robin',amount=0.1)
    for character in [TopazCharacter, DrRatioCharacter]:
        character.addStat('CD',description='Poised to Bloom',amount=0.12+0.04*RobinCharacter.lightcone.superposition)

    # Topaz Vulnerability Buff
    TopazCharacter.applyVulnerabilityDebuff(team,uptime=1.0)
    
    # Dr Ratio Buff
    DrRatioCharacter.applyTalentBuff(team)
    
    # Fu Xuan Buffs
    FuxuanCharacter.applySkillBuff(team)

    # Robin Buffs
    RobinCharacter.applyTalentBuff(team)
    RobinCharacter.applySkillBuff(team)
    RobinUltUptime = 0.5 # assume about half of our attacks get robin buff
    RobinCharacter.applyUltBuff([DrRatioCharacter,TopazCharacter,FuxuanCharacter],uptime=RobinUltUptime)

    #%% Print Statements
    for character in team:
        character.print()

    #%% DrRatio Topaz Robin Fuxuan Rotations
    # assume 154 ish spd ratio and topaz, ratio slower than Topaz, and 134 ish spd robin
    # this optimizes use of robin's advance forward, while keeping numby math good-ish
    # we'll look at what a 4 turn rotation looks like for ratio and topaz here

    # Turn 1 (based on the 154 spd characters)
    # Robin Ult
    # Topaz Ult -> Ratio Ult -> Fuxuan Ult -> Ratio Followup -> Numby attack
    # Topaz Skill -> Numby Attack
    # Ratio Skill -> Ratio followup -> Numby half turn
    # Fuxuan Basic
    
    # Turn 2 
    # Numby Attack -> Topaz Skill -> Numby half turn
    # Ratio Skill -> Ratio followup -> Numby attack
    # Fuxuan Basic
    
    # Turn 3 - Concerto Expired
    # Topaz Basic -> Numby Attack
    # Ratio Skill -> Ratio followup -> Numby half turn
    # Fuxuan Basic
    
    # Turn 4
    # Numby Attack -> Topaz Basic -> Numby half turn
    # Ratio Skill -> Ratio followup -> Numby attack
    # Fuxuan Basic
    
    numBasicRobin = 2.0
    numSkillRobin = 1.0
    RobinRotation = [RobinCharacter.useBasic() * numBasicRobin,
                    RobinCharacter.useSkill() * numSkillRobin,
                    RobinCharacter.useUltimate() * 1,]
    RobinCharacter.applyUltBuff([RobinCharacter],uptime=1.0) # apply robin buff after we calculate damage for her basics
    
    numSkillRatio = 3.5
    numUltRatio = 1.0
    numTalentRatio = numSkillRatio * 0.8 + 2 * numUltRatio # multiply 0.8 for no extra debuff teams
    
    DrRatioRotation = []
    DrRatioRotation += [DrRatioCharacter.useSkill() * numSkillRatio]
    DrRatioRotation += [DrRatioCharacter.useTalent() * numTalentRatio] 
    DrRatioRotation += [DrRatioCharacter.useUltimate()] 

    RobinRotationRatio = [RobinCharacter.useTalent() * (numSkillRatio + numTalentRatio + 1.0)]
    RobinRotationRatio += [RobinCharacter.useConcertoDamage(['skill']) * numSkillRatio * RobinUltUptime]
    RobinRotationRatio += [RobinCharacter.useConcertoDamage(['ultimate']) * RobinUltUptime]
    RobinRotationRatio += [RobinCharacter.useConcertoDamage(['followup']) * (numTalentRatio - 2.0) * RobinUltUptime]
    DrRatioRotation += [RobinCharacter.useAdvanceForward()] 

    numBasicTopaz = 2.0
    numSkillTopaz = 2.0
    numTalentTopaz = 5.0 # rough estimate
    TopazRotation = []
    TopazRotation += [TopazCharacter.useBasic() * numBasicTopaz]
    TopazRotation += [TopazCharacter.useSkill() * numSkillTopaz]
    TopazRotation += [TopazCharacter.useUltimate()]
    TopazRotation += [TopazCharacter.useTalent(windfall=True) * 2.0] # two talents from windfall
    TopazRotation += [TopazCharacter.useTalent(windfall=False) * numTalentTopaz]
    
    RobinRotationTopaz = [RobinCharacter.useTalent() * (numBasicTopaz + numSkillTopaz + numTalentTopaz + 2.0)]
    RobinRotationTopaz += [RobinCharacter.useConcertoDamage(['basic','followup']) * numBasicTopaz * RobinUltUptime]
    RobinRotationTopaz += [RobinCharacter.useConcertoDamage(['skill','followup']) * numSkillTopaz * RobinUltUptime]
    RobinRotationTopaz += [RobinCharacter.useConcertoDamage(['followup']) * numTalentTopaz * RobinUltUptime]
    TopazRotation += [RobinCharacter.useAdvanceForward()] 

    FuxuanRotation = [FuxuanCharacter.useBasic() * 2,
                    FuxuanCharacter.useSkill() * 1,
                    FuxuanCharacter.useUltimate() * 1,]
    
    RobinRotationFuxuan = [RobinCharacter.useTalent() * 2]
    RobinRotationFuxuan += [RobinCharacter.useConcertoDamage(['basic']) * 2 * RobinUltUptime]

    #%% DrRatio Topaz Robin Fuxuan Rotation Math

    totalDrRatioEffect = sumEffects(DrRatioRotation)
    totalTopazEffect = sumEffects(TopazRotation)
    totalRobinEffect = sumEffects(RobinRotation)
    totalFuxuanEffect = sumEffects(FuxuanRotation)

    DrRatioRotationDuration = totalDrRatioEffect.actionvalue * 100.0 / DrRatioCharacter.getTotalStat('SPD')
    TopazRotationDuration = totalTopazEffect.actionvalue * 100.0 / TopazCharacter.getTotalStat('SPD')
    RobinRotationDuration = totalRobinEffect.actionvalue * 100.0 / RobinCharacter.getTotalStat('SPD')
    FuxuanRotationDuration = totalFuxuanEffect.actionvalue * 100.0 / FuxuanCharacter.getTotalStat('SPD')
    

    print('##### Rotation Durations #####')
    print('DrRatio: ',DrRatioRotationDuration)
    print('Topaz: ',TopazRotationDuration)
    print('Robin: ',RobinRotationDuration)
    print('Fuxuan: ',FuxuanRotationDuration)

    # Scale other character's rotation
    TopazRotation = [x * DrRatioRotationDuration / TopazRotationDuration for x in TopazRotation]
    RobinRotationTopaz = [x * DrRatioRotationDuration / TopazRotationDuration for x in RobinRotationTopaz]
    RobinRotation = [x * DrRatioRotationDuration / RobinRotationDuration for x in RobinRotation]
    FuxuanRotation = [x * DrRatioRotationDuration / FuxuanRotationDuration for x in FuxuanRotation]
    RobinRotationFuxuan = [x * DrRatioRotationDuration / FuxuanRotationDuration for x in RobinRotationFuxuan]
    
    RobinRotation += RobinRotationRatio
    RobinRotation += RobinRotationTopaz
    RobinRotation += RobinRotationFuxuan
    totalRobinEffect = sumEffects(RobinRotation)

    DrRatioEstimate = DefaultEstimator(f'DrRatio: {numSkillRatio:.1f}E {numTalentRatio:.1f}T {numUltRatio:.0f}Q, max debuffs on target', DrRatioRotation, DrRatioCharacter, config)
    TopazEstimate = DefaultEstimator(f'Topaz: {TopazCharacter.lightcone.name} {numSkillTopaz:.0f}E {numBasicTopaz:.0f}N {numTalentTopaz:.1f}T Q Windfall(2T)', TopazRotation, TopazCharacter, config)
    RobinEstimate = DefaultEstimator(f'Robin: {numBasicRobin:.1f}N {numSkillRobin:.1f}E 1Q, S{RobinCharacter.lightcone.superposition:d} {RobinCharacter.lightcone.name}', 
                                    RobinRotation, RobinCharacter, config)
    FuxuanEstimate = DefaultEstimator('Fuxuan: 2N 1E 1Q, S{:.0f} {}'.format(FuxuanCharacter.lightcone.superposition, FuxuanCharacter.lightcone.name),
                                    FuxuanRotation, FuxuanCharacter, config)

    return([DrRatioEstimate, TopazEstimate, FuxuanEstimate, RobinEstimate])

