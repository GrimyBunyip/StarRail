Configuration = {
    'numEnemies': 2, # number of enemies we are
    'numRounds': 8, # number of rounds simulated, not currently used
    'enemyLevel': 90, # level of enemies
    'enemySpeed': 132, # lvl 86+ enemies have 1.32 speed multiplier. Used for calculating Dot Damage
    'enemyType': 'elite', # options are elite or basic

    'enemyMaxHP': 250000, # used for calculation of break effects exclusively, it's roughly the HP of an elite
    'enemyToughness': 300, # used for calculation of break effects exclusively, most elites used to have 300
    'breakLevelMultiplier': 3767.5533, # base level multiplier for break effects

    'enemyRes': 0.0, # assume you aren't fighting enemies that are resistant to you
    'weaknessBrokenUptime': 0.5, # percentage of time enemies spent with their weakness broken, affects 0.9 vs 1.0 toughness broken multiplier, and characters like sushang

    'fivestarEidolons': 0, #number of eidolons on fivestar characters
    'fourstarEidolons': 6, #number of eidolons on fourstar characters

    'hertaSuperpositions': 5, #number of superpositions on herta light cones
    'eventSuperpositions': 5, #number of superpositions on herta light cones
    'forgottenHallSuperpositions': 5, #number of superpositions on forgotten hall
    'battlePassSuperpositions': 5, #number of superpositions on battlepass lightcones
    'fivestarSuperpositions': 1, #number of superpositions on fivestar light cones
    'fourstarSuperpositions': 5, #number of superpositions on fourstar light cones
    'threestarSuperpositions': 5, #number of superpositions on threestar light cones
}