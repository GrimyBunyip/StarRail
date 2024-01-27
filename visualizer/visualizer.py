import io

from urllib.request import urlopen

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.colors import to_rgba
from matplotlib.patches import Rectangle

from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseEffect import BaseEffect
from estimator.DefaultEstimator import VisualizationInfo

COLOR_DICT = {
    'wind': 'forestgreen',
    'fire': 'firebrick',
    'ice': 'royalblue',
    'lightning': 'purple',
    'physical': 'grey',
    'quantum': 'darkslateblue',
    'imaginary': 'darkgoldenrod',
}

def visualize(visInfoList:list, visualizerPath:str='visualizer\\visual.png',  **config):
    for i, visInfo in enumerate(visInfoList):
        if isinstance(visInfo,VisualizationInfo):
            visInfoList[i] = [visInfo]
    
    # convert the colors to different opacities for the stacked bar plot
    rgba_dict = {}
    for key, value in COLOR_DICT.items():
        rgba1 = list(to_rgba(value))
        rgba2 = list(to_rgba(value))
        rgba3 = list(to_rgba(value))
        rgba1[3] = 1.0 # base damage
        rgba2[3] = 0.5 # base damage + dot
        rgba3[3] = 0.25 # total damage
        rgba_dict[key] = [rgba1, rgba2, rgba3]

    teamsize = max([len(visInfo) for visInfo in visInfoList])

    # Sample data
    rotationNames = []
    values = []
    colors = []
    characters = []
    totalEffects = []
    bottoms = []
    for visInfo in visInfoList: #visInfo for each rotation
        teamName = '\n'.join([info.name for info in visInfo])
        rotationNames.append(teamName)
        
        teamValue = []
        teamColor = []
        teamCharacters = []
        teamBottom = []
        teamEffect:BaseEffect = BaseEffect()
        for i, info in enumerate(visInfo): #info for each character in each rotation
            info:VisualizationInfo
            actionEffect:BaseEffect = info.effect
            breakEffect:BaseEffect = info.breakEffect
            dotEffect:BaseEffect = info.dotEffect
            char:BaseCharacter = info.character
            
            speed = char.getTotalStat('SPD')
            cycles = actionEffect.actionvalue * 100.0 / speed
            
            teamBottom.append(sum(teamValue))
            teamValue.append(actionEffect.damage / cycles)
            teamBottom.append(sum(teamValue))
            teamValue.append(dotEffect.damage / cycles)
            teamBottom.append(sum(teamValue))
            teamValue.append(breakEffect.damage / cycles)
            teamColor.append(rgba_dict[char.element][0])
            teamColor.append(rgba_dict[char.element][1])
            teamColor.append(rgba_dict[char.element][2])
            teamCharacters.append(char)
            
            if i > 0: # only track the energy and action values of the lead character
                for e in [actionEffect, dotEffect, breakEffect]:
                    e.energy = 0.0
                    e.actionvalue = 0.0
            
            teamEffect += actionEffect + dotEffect + breakEffect
            
        #assert abs(sum(teamValue)*cycles - teamEffect.damage) < 0.0000001, 'mismatching total effect damage and bar length'
        
        values.append(teamValue)
        colors.append(teamColor)
        characters.append(teamCharacters)
        bottoms.append(teamBottom)
        totalEffects.append(teamEffect)

    # sort the data from highest at the top
    combined_data = list(zip(rotationNames, values, characters, colors, bottoms, totalEffects,))
    sorted_data = sorted(combined_data, key=lambda x:sum(x[1])) # x[1] is values, x[1][-1] is the largest damage entry in values
    rotationNames, values, characters, colors, bottoms, totalEffects = zip(*sorted_data)

    fig, ax = plt.subplots(figsize=(20,1.5+len(characters)))

    # Create the bar chart
    for i in range(teamsize*3):
        bars = ax.barh([x for x in range(len(rotationNames))], [x[i] for x in values], 
                       left = [x[i] for x in bottoms],
                       color = [x[i] for x in colors],)

    # define left and right offsets
    PICTURE_SIZE = 9000
    LEFT_OFFSET = 1000

    # Download images and inlay them on the bars as annotations
    for bar, teamChars, rotationName, totalEffect in zip(bars, characters, rotationNames, totalEffects):
        bar:Rectangle
        for i, char in enumerate(teamChars):
            img_data = urlopen(char.graphic).read()
            img = plt.imread(io.BytesIO(img_data), format='png')  # You might need to adjust the format based on the image type
            img = OffsetImage(img, zoom=0.35)  # Adjust the zoom factor as needed
            ab = AnnotationBbox(img, (bar.get_width() + bar.get_x() - PICTURE_SIZE * (len(teamChars) - i - 1), bar.get_y() + bar.get_height()/2), frameon=False)
            ax.add_artist(ab)

        totalEffect:BaseEffect
        leadChar:BaseCharacter = teamChars[0]
        speed = leadChar.getTotalStat('SPD')
        effectHitRate = leadChar.getTotalStat('EHR')
        cycles = totalEffect.actionvalue * 100.0 / speed # action value = # of turns kafka took, cycles = # of cycles that passed during this rotation

        ax.text(x = LEFT_OFFSET,
                y = bar.get_y() + bar.get_height() / 2,
                s = leadChar.longName + 
                    '\nSpd: ' + str(round(speed, 2)) + '    EHR: ' + str(round(effectHitRate, 2)) + 
                    '\nRotation Cycles: ' + str(round(cycles, 2)) + '\n' + 
                    ('' if leadChar.relicsettwo is None else leadChar.relicsettwo.shortname) + 
                    ('' if (leadChar.relicsetone is None or '4pc' in leadChar.relicsettwo.shortname) else (' + ' + leadChar.relicsetone.shortname)) + 
                    ('' if leadChar.planarset is None else (' + ' + leadChar.planarset.shortname)),
                va = 'center', 
                color = 'white')

        ax.text(x = (bar.get_x() + bar.get_width()) / 3,
                y = bar.get_y() + bar.get_height() / 2,
                s = rotationName,
                va = 'center', 
                color = 'white')
        
        energySurplus = totalEffect.energy - leadChar.maxEnergy
        ax.text(x = (bar.get_x() + bar.get_width()) * 2 / 3,
                y = bar.get_y() + bar.get_height() / 2,
                s = 'Damage per Cycle: ' + str(int((totalEffect.damage) / cycles)) + 
                    '\nGauge per Cycle: ' + str(round(totalEffect.gauge / cycles, 1)) + 
                    '\nSP per Cycle: ' + str(round(totalEffect.skillpoints / cycles, 2)) + 
                    '\nEnergy Surplus per Rotation: ' + str(round(energySurplus, 2)),
                va = 'center', 
                color = 'white')
        
        print(int((totalEffect.damage) / cycles))

    plt.xlabel('Build')
    plt.ylabel('Damage')
    plt.axis("off")
    plt.xticks([])
    plt.yticks([])
    plt.title('Star Rail Damage per Cycle Calculator | 12 8 5 3 relic substat split | no techniques\nDoTs, including break dots, already at max stacks where possible. Also many copies of GNSW may be assumed. So nihility numbers may look very big!\nDark Left Bar is damage from abilities, including dot explosions. Middle bar is dot ticks. Light right bar is break damage and break dot ticks.\n{} targets: {} with {} HP, {} Toughness, {:.2f} speed'.format(config['numEnemies'], config['enemyType'], config['enemyMaxHP'], config['enemyToughness'], config['enemySpeed']))
    plt.tight_layout()
    plt.savefig(visualizerPath)