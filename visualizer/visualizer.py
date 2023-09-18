import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.colors import to_rgba
from urllib.request import urlopen
import io

from baseClasses.BaseEffect import BaseEffect

def visualize(VisualizationDict:dict, visualizerPath:str='visualizer\\visual.png',  **config):
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
    categories = []
    values = []
    characters = []
    colors = []
    for rotationName, value in VisualizationDict['EffectDict'].items():
        value:BaseEffect
        breakValue:BaseEffect = VisualizationDict['BreakDict'][rotationName]
        dotValue:BaseEffect = VisualizationDict['DotDict'][rotationName]
        
        speed = VisualizationDict['CharacterDict'][rotationName].getTotalSpd()
        cycles = value.actionvalue * 100.0 / speed
        values.append([(value.damage) / cycles, 
                       (value.damage + dotValue.damage) / cycles, 
                       (value.damage + dotValue.damage + breakValue.damage) / cycles])
        categories.append(rotationName)
        characters.append(VisualizationDict['CharacterDict'][rotationName])
        colors.append(color_dict[VisualizationDict['CharacterDict'][rotationName].element])

    # sort the data from highest at the top
    combined_data = list(zip(categories, values, characters, colors))
    sorted_data = sorted(combined_data, key=lambda x:x[1][2])
    categories, values, characters, colors = zip(*sorted_data)

    fig, ax = plt.subplots(figsize=(22,2*len(characters)))

    # Create the bar chart
    bars = ax.barh(categories, [x[0] for x in values], color = [x[0] for x in colors])
    bars = ax.barh(categories, [x[1] for x in values], color = [x[1] for x in colors])
    bars = ax.barh(categories, [x[2] for x in values], color = [x[2] for x in colors])

    # define left and right offsets
    LEFT_OFFSET = 1000
    RIGHT_OFFSET = 2500

    # Download images and inlay them on the bars as annotations
    for bar, character, rotationName in zip(bars, characters, categories):
        img_data = urlopen(character.graphic).read()
        img = plt.imread(io.BytesIO(img_data), format='png')  # You might need to adjust the format based on the image type
        img = OffsetImage(img, zoom=0.5)  # Adjust the zoom factor as needed
        ab1 = AnnotationBbox(img, (bar.get_width() - RIGHT_OFFSET, bar.get_y() + bar.get_height()/2), frameon=False)

        effect = VisualizationDict['EffectDict'][rotationName]
        speed = VisualizationDict['CharacterDict'][rotationName].getTotalSpd()
        effectHitRate = VisualizationDict['CharacterDict'][rotationName].EHR
        cycles = effect.actionvalue * 100.0 / speed # action value = # of turns kafka took, cycles = # of cycles that passed during this rotation

        ax.add_artist(ab1)
        ax.text(x = LEFT_OFFSET,
                y = bar.get_y() + bar.get_height() * 2 / 4,
                s = character.longName + 
                    '\nSpd: ' + str(round(speed, 2)) + '    EHR: ' + str(round(effectHitRate, 2)) + 
                    '\nRotation Cycles: ' + str(round(cycles, 2)),
                va = 'center', 
                color = 'white')

        energySurplus = VisualizationDict['EffectDict'][rotationName].energy - character.maxEnergy
        ax.text(x = bar.get_x() + bar.get_width() * 1 / 2,
                y = bar.get_y() + bar.get_height() * 2 / 4,
                s = rotationName + 
                    '\nDamage per Cycle: ' + str(int(effect.damage / cycles)) + 
                    '\nGauge per Cycle: ' + str(round(effect.gauge / cycles, 1)) + 
                    '\nSP per Cycle: ' + str(round(-effect.skillpoints / cycles, 2)) + 
                    '\nEnergy Surplus per Rotation: ' + str(round(energySurplus, 2)),
                va = 'center', 
                color = 'white')

    plt.xlabel('Build')
    plt.ylabel('Damage')
    plt.axis("off")
    plt.xticks([])
    plt.yticks([])
    plt.title('Star Rail Damage per Cycle Calculator | 20 substats\n {} targets: {} with {} HP, {} Toughness, {:.2f} speed'.format(config['numEnemies'], config['enemyType'], config['enemyMaxHP'], config['enemyToughness'], config['enemySpeed']))
    plt.tight_layout()
    plt.savefig(visualizerPath)
    plt.show()