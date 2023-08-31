import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from urllib.request import urlopen
import io

def visualize(CharacterDict:dict, EffectDict:dict, Configuration):
    color_dict = {
        'wind': 'green',
        'fire': 'red',
        'ice': 'blue',
        'lightning': 'purple',
        'physical': 'grey',
        'quantum': 'magenta',
        'imaginary': 'yellow',
    }

    # Sample data
    categories = []
    values = []
    characters = []
    colors = []
    for name, value in EffectDict.items():
        categories.append(name)
        values.append(value.damage)
        characters.append(CharacterDict[name])
        colors.append(color_dict[CharacterDict[name].element])

    # sort the data from highest at the top
    combined_data = list(zip(categories, values, characters, colors))
    sorted_data = sorted(combined_data, key=lambda x:x[1])
    categories, values, characters, colors = zip(*sorted_data)

    fig, ax = plt.subplots(figsize=(15,2*len(characters)))

    # Create the bar chart
    bars = ax.barh(categories, values, color = colors)

    # define left and right offsets
    LEFT_OFFSET = 10000
    RIGHT_OFFSET = 20000

    # Download images and inlay them on the bars as annotations
    for bar, character in zip(bars, characters):
        img_data = urlopen(character.graphic).read()
        img = plt.imread(io.BytesIO(img_data), format='png')  # You might need to adjust the format based on the image type
        img = OffsetImage(img, zoom=0.2)  # Adjust the zoom factor as needed
        ab1 = AnnotationBbox(img, (bar.get_width() - RIGHT_OFFSET, bar.get_y() + bar.get_height()/2), frameon=False)

        ax.add_artist(ab1)
        ax.text(x = LEFT_OFFSET,
                y = bar.get_y() + bar.get_height() * 2 / 4,
                s = character.name, 
                va = 'center', 
                color = 'white')

        ax.text(x = bar.get_x() + bar.get_width() * 1 / 2,
                y = bar.get_y() + bar.get_height() * 2 / 4,
                s = 'Damage: ' + str(int(EffectDict[character.name].damage)) + '\nGauge: ' + str(int(EffectDict[character.name].gauge)) + '\nSP: ' + str(round(-EffectDict[character.name].skillpoints,2)) + '\nSpd: ' + str(round(CharacterDict[character.name].getTotalSpd(),2)), 
                va = 'center', 
                color = 'white')

    plt.xlabel('Build')
    plt.ylabel('Damage')
    plt.axis("off")
    plt.xticks([])
    plt.yticks([])
    plt.title('Star Rail DPS Rankings | {} targets | {} rounds | 20 substats'.format(Configuration['numEnemies'], Configuration['numRounds']))
    plt.tight_layout()
    plt.show()