import io
import multiprocessing

from urllib.request import urlopen

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.colors import to_rgba

from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseEffect import BaseEffect
from estimator.DefaultEstimator import VisualizationInfo

def visualize(visInfo:VisualizationInfo, visualizerPath:str='visualizer\\visual.png',  **config):
    color_dict = {
        'wind': 'green',
        'fire': 'red',
        'ice': 'blue',
        'lightning': 'purple',
        'physical': 'grey',
        'quantum': 'darkslateblue',
        'imaginary': 'darkgoldenrod',
    }
    
    # convert the colors to different opacities for the stacked bar plot
    for key, value in color_dict.items():
        rgba1 = list(to_rgba(value))
        rgba2 = list(to_rgba(value))
        rgba3 = list(to_rgba(value))
        rgba1[3] = 1.0 # base damage
        rgba2[3] = 0.5 # base damage + dot
        rgba3[3] = 0.25 # total damage
        color_dict[key] = [rgba1, rgba2, rgba3]

    # Sample data
    rotationNames = []
    values = []
    characters = []
    colors = []
    totalEffects = []
    extraImages = []
    for info in visInfo:
        info:VisualizationInfo
        rotationName:str = info.name
        actionEffect:BaseEffect = info.effect
        breakEffect:BaseEffect = info.breakEffect
        dotEffect:BaseEffect = info.dotEffect
        char:BaseCharacter = info.character
        extraImage:str = info.extraImage
        
        speed = char.getTotalSpd()
        cycles = actionEffect.actionvalue * 100.0 / speed
        values.append([(actionEffect.damage) / cycles, 
                       (actionEffect.damage + dotEffect.damage) / cycles, 
                       (actionEffect.damage + dotEffect.damage + breakEffect.damage) / cycles])
        totalEffects.append(actionEffect + dotEffect + breakEffect)
        rotationNames.append(rotationName)
        characters.append(char)
        colors.append(color_dict[char.element])
        extraImages.append(extraImage)

    # sort the data from highest at the top
    combined_data = list(zip(rotationNames, values, characters, colors, totalEffects, extraImages))
    sorted_data = sorted(combined_data, key=lambda x:x[1][2])
    rotationNames, values, characters, colors, totalEffects, extraImages = zip(*sorted_data)

    fig, ax = plt.subplots(figsize=(22,2*len(characters)))

    # Create the bar chart
    bars = ax.barh([x for x in range(len(rotationNames))], [x[0] for x in values], color = [x[0] for x in colors])
    bars = ax.barh([x for x in range(len(rotationNames))], [x[1] for x in values], color = [x[1] for x in colors])
    bars = ax.barh([x for x in range(len(rotationNames))], [x[2] for x in values], color = [x[2] for x in colors])

    # define left and right offsets
    PICTURE_SIZE = 9000
    LEFT_OFFSET = 1000
    RIGHT_OFFSET = 2500

    # Download images and inlay them on the bars as annotations
    for bar, char, rotationName, totalEffect, extraImage in zip(bars, characters, rotationNames, totalEffects, extraImages):
        totalEffect:BaseEffect
        img_data = urlopen(char.graphic).read()
        img = plt.imread(io.BytesIO(img_data), format='png')  # You might need to adjust the format based on the image type
        img = OffsetImage(img, zoom=0.5)  # Adjust the zoom factor as needed
        ab1 = AnnotationBbox(img, (bar.get_width() - RIGHT_OFFSET, bar.get_y() + bar.get_height()/2), frameon=False)
        ax.add_artist(ab1)
        
        if extraImage is not None:
            img_data = urlopen(extraImage).read()
            img = plt.imread(io.BytesIO(img_data), format='png')  # You might need to adjust the format based on the image type
            img = OffsetImage(img, zoom=0.5)  # Adjust the zoom factor as needed
            ab2 = AnnotationBbox(img, (bar.get_width() - RIGHT_OFFSET + PICTURE_SIZE, bar.get_y() + bar.get_height()/2), frameon=False)
            ax.add_artist(ab2)
            
        speed = char.getTotalSpd()
        effectHitRate = char.EHR
        cycles = totalEffect.actionvalue * 100.0 / speed # action value = # of turns kafka took, cycles = # of cycles that passed during this rotation

        ax.text(x = LEFT_OFFSET,
                y = bar.get_y() + bar.get_height() * 2 / 4,
                s = char.longName + 
                    '\nSpd: ' + str(round(speed, 2)) + '    EHR: ' + str(round(effectHitRate, 2)) + 
                    '\nRotation Cycles: ' + str(round(cycles, 2)),
                va = 'center', 
                color = 'white')

        energySurplus = totalEffect.energy - char.maxEnergy
        ax.text(x = bar.get_x() + bar.get_width() * 1 / 2,
                y = bar.get_y() + bar.get_height() * 2 / 4,
                s = rotationName + 
                    '\nDamage per Cycle: ' + str(int((totalEffect.damage) / cycles)) + 
                    '\nGauge per Cycle: ' + str(round(totalEffect.gauge / cycles, 1)) + 
                    '\nSP per Cycle: ' + str(round(totalEffect.skillpoints / cycles, 2)) + 
                    '\nEnergy Surplus per Rotation: ' + str(round(energySurplus, 2)),
                va = 'center', 
                color = 'white')

    plt.xlabel('Build')
    plt.ylabel('Damage')
    plt.axis("off")
    plt.xticks([])
    plt.yticks([])
    plt.title('Star Rail Damage per Cycle Calculator | 20 substats\n no techniques, everything at max stacks\n{} targets: {} with {} HP, {} Toughness, {:.2f} speed'.format(config['numEnemies'], config['enemyType'], config['enemyMaxHP'], config['enemyToughness'], config['enemySpeed']))
    plt.tight_layout()
    plt.savefig(visualizerPath)
    plt.show()