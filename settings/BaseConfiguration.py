Configuration = {
    'numEnemies': 2, # number of enemies we are
    'numRounds': 8, # number of rounds simulated
    'enemyLevel': 90, # level of enemies
    'enemySpeed': 132, # lvl 86+ enemies have 1.32 speed multiplier. They can have varying base speeds, but let's assume 100
    'enemyType': 'elite', # options are elite or basic
    
    'bonusEnergyFlat': 30, # about 3 kills worth over the course of 8 turns
    'bonusEnergyPerEnemyAttack': 12, # amount of energy each time enemies attack the character
    
    'numberEnemyAttacksPerTurn': 0.5, # number of enemy attacks on this character for each turn the enemy takes
    # I do not factor in character abilities that affect number of enemy attacks
    # number of enemy attacks is multiplied by taunt / 100

    'enemyMaxHP': 250000, # used for calculation of break effects exclusively, it's roughly the HP of an elite
    'enemyToughness': 300, # used for calculation of break effects exclusively, most elites have 300
    'breakLevelMultiplier': 3767.5533, # base level multiplier for break effects

    'enemyRes': 0.0, # assume you aren't fighting enemies that are resistant to you
    'brokenMultiplier': 0.95, # enemies take 1.0 damage if toughness is broken, 0.9 otehrwise. I like to assume 0.95 here

    'fivestarEidolons': 0, #number of eidolons on fivestar characters
    'fourstarEidolons': 6, #number of eidolons on fourstar characters

    'fivestarSuperpositions': 1, #number of superpositions on fivestar light cones
    'hertaSuperpositions': 5, #number of superpositions on herta light cones, ignores 'fivestarSuperposition
    'fourstarSuperpositions': 5, #number of superpositions on fourstar light cones
}