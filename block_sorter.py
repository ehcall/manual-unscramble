import json
import os
from functools import cmp_to_key
"""
 Different styles will need different sorting methods, although some might overlap
"""

def compare_09(block1, block2):
    ## works for style 9
    ## check style 1 and 8?
    vertex1 = block1["vertices"][2]
    vertex2 = block2["vertices"][2]

    if abs(float(vertex1['y']) - float(vertex2['y'])) < .01:
        ## same row
        if vertex1['x'] < vertex2['x']:
         ## block 1, block 2
            return -1
        else:
         ## block 2, block 1
            return 1
    else:
        ## different row
        if vertex1['y'] < vertex2['y']:
        ## block 1, block 2
            return -1
        else:
            return 1



def compare_07(block1, block2):
    vertex1 = block1["vertices"][2]
    vertex2 = block2["vertices"][2]
    # works for styles 7 and 10
    # check styles 2 and 6

    if abs(float(vertex1['y']) - float(vertex2['y'])) < 0.01:
        '''
            if the blocks are on the same row, prioritize columns
        '''
        if vertex1['x'] < vertex2['x']:
            return -1
        elif vertex1['x'] > vertex2['x']:
            return 1
        else:
            return 0
    elif abs(float(vertex1['x']) - float(vertex2['x'])) < 0.1:
        '''
            if the blocks are in the same column, prioritize rows
        '''
        if vertex1['y'] > vertex2['y']:
            return 1
        elif vertex1['y'] < vertex2['y']:
            return -1
    else:
        if vertex1['x'] < vertex2['x']:
            return -1
        elif vertex1['x'] > vertex2['x']:
            return 1


def process(filename, style):
    pages = {}
    with open("lesson_blocks\\" + style + "\\" + filename, encoding="utf-8") as f:
        lesson_json = json.load(f)
    for block in lesson_json[filename]:
        pages.setdefault(lesson_json[filename][block]['page'], []).append(lesson_json[filename][block])

    all_lesson_blocks = []
    for page in pages:
        if style in ["style_07", "style_10"]:
            sorted_text = sorted(pages[page], key=cmp_to_key(compare_07))
        elif style in ["style_09"]:
            sorted_text = sorted(pages[page], key=cmp_to_key(compare_09))
        for text in sorted_text:
            print(text['text'])
        all_lesson_blocks.extend(sorted_text)
    return all_lesson_blocks

style = "style_09"
for file in os.listdir("labeled_files\\" + style + "\\"):
    lesson = process(file, style)
    wait = input("wait here")
    #print(lesson)