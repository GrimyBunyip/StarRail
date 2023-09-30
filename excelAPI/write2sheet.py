import json

from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter
from baseClasses.BaseCharacter import BaseCharacter, getStatComments
from baseClasses.BaseEffect import BaseEffect
from estimator.DefaultEstimator import VisualizationInfo

from visualizer.visualizer import COLOR_DICT
import matplotlib.colors as mcolors

hex_dict = {
        'wind': '2ecc71',
        'fire': 'e74c3c',
        'ice': '3498db',
        'lightning': 'bc81df',
        'physical': 'bdc3c7',
        'quantum': '767bd4',
        'imaginary': 'f1c40f',
    }

DEBUG_COLUMN_NAMES = [
    'ability',
    'damage',
    'energy',
    'gauge',
    'action value',
    'SPD', 'ATK', 'HP', 'DEF',
    'DMG', 'CR', 'CD',
    'Vulnerability',
    'ResPen', 'DefShred',
]

def writeVisualizationList(visualizationList:list,path:str):
    workbook:Workbook = Workbook()
    sheet:Worksheet = workbook.active

    current_row = 1
    left_align = Alignment(horizontal='left')
    
    # set column widths
    sheet.column_dimensions[get_column_letter(1)].width = 30
    sheet.column_dimensions[get_column_letter(2)].width = 60
    sheet.column_dimensions[get_column_letter(4)].width = 30
    
    for info in visualizationList:
        info:VisualizationInfo
        
        rotationName:str = info.name
        character:BaseCharacter = info.character
        totalEffect:BaseEffect = info.effect
        breakEffect:BaseEffect = info.breakEffect
        dotEffect:BaseEffect = info.dotEffect
        
        # write character info and header info
        color = hex_dict[character.element]
        current_cell = sheet.cell(row=current_row,column=1,value=character.name)
        current_cell.font = Font(bold=True)
        current_cell.fill = PatternFill(start_color=color,end_color=color,fill_type='solid')
        current_cell.alignment = left_align
        
        for i, column_name in enumerate(DEBUG_COLUMN_NAMES):
            current_cell = sheet.cell(row=current_row, column=4+i, value=column_name)
            current_cell.fill = PatternFill(start_color=color,end_color=color,fill_type='solid')
            current_cell.alignment = left_align
        
        current_row += 1
        
        # fill out character base stats
        stats = ['SPD','ATK','HP','DEF','CR','CD','DMG']
        for i, stat in enumerate(stats):
            current_cell = sheet.cell(row=current_row+i,column=1,value=stat)
            current_cell.fill = PatternFill(start_color=color,end_color=color,fill_type='solid')
            current_cell.alignment = left_align
            
            current_cell = sheet.cell(row=current_row+i,column=2,value=character.getTotalStat(stat))
            current_cell.comment = Comment(getStatComments(character,stat),'')
            current_cell.fill = PatternFill(start_color=color,end_color=color,fill_type='solid')
            current_cell.alignment = left_align
            
        # fill out character equipment
        equipment = [('Light Cone',character.lightcone.name),
                     ('Relic Set One',character.relicsetone.shortname),
                     ('Relic Set Two',character.relicsettwo.shortname),
                     ('Planar Set',character.planarset.shortname),
                     ('Mainstats',json.dumps(character.relicstats.mainstats)),
                     ('Substats',json.dumps(character.relicstats.substats))]
        
        for j, entry in enumerate(equipment):
            name, value = entry
            current_cell = sheet.cell(row=current_row+i+j,column=1,value=name)
            current_cell.fill = PatternFill(start_color=color,end_color=color,fill_type='solid')
            current_cell.alignment = left_align
            
            current_cell = sheet.cell(row=current_row+i+j,column=2,value=value)
            current_cell.fill = PatternFill(start_color=color,end_color=color,fill_type='solid')
            current_cell.alignment = left_align
        
        # fill out rotation details
        for i, info in enumerate(totalEffect.debuginfo):
            for j, entry in enumerate(info):
                if isinstance(entry,list):
                    current_cell = sheet.cell(row=current_row+i,column=4+j,value=entry[0])
                    current_cell.comment = Comment(entry[1],'')               
                    current_cell.alignment = left_align
                else:
                    current_cell = sheet.cell(row=current_row+i,column=4+j,value=entry)
                current_cell.fill = PatternFill(start_color=color,end_color=color,fill_type='solid')
                current_cell.alignment = left_align
        
        current_row += max(i,len(stats)+len(equipment))+1
    
    workbook.save(path)
    workbook.close()