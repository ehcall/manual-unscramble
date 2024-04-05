import json
import os
from functools import cmp_to_key

"""
 Different styles will need different sorting methods, although some might overlap
"""



def compare_09(block1, block2):
    ## works for style 1, 1.5, 9
    vertex1 = block1["vertices"][2]
    vertex2 = block2["vertices"][2]
    try:
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
    except:
        return 0


def section_08(page_text):
    sections = {}
    section_headings = ["Additional\nInformation", "Information\nfor the\n Teacher", "Information\nfor the\nTeacher",
                        "Lesson\nPresentation", "Assignment\nfor the\nComing Lesson"]
    i = 0
    sections[i] = {'blocks': []}
    section_coords = [0]
    for block in page_text:
        #   print(block)
        if block["text"] in section_headings:
            i += 1
            sections[i] = {
                'heading': block,
                'blocks': []
            }
            section_coords.append(block['vertices'][2]['y'])

    sorted_coords = sorted(section_coords)
    #  print(sorted_coords)
    for block in page_text:
        if block["text"] not in section_headings:
            block_vertex = block['vertices'][2]['y']
            if len(sorted_coords) == 1:
                sections[0]['blocks'].append(block)
            else:
                for j, heading_vertex in enumerate(sorted_coords):

                    if abs(block_vertex - heading_vertex) < .05:
                        sections[j]['blocks'].append(block)
                        break
                    elif block_vertex < heading_vertex:
                        sections[j - 1]['blocks'].append(block)
                        break
                    elif len(sorted_coords) == j + 1:
                        sections[j]['blocks'].append(block)
                        break
                    # else:
                    #   print("\t\t\t",block['text'])
        else:
            pass
    return sections


def compare_07(block1, block2):
    vertex1 = block1["vertices"][2]
    vertex2 = block2["vertices"][2]
    # works for styles 2, 6, 7 and 10
    try:
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
    except:
        return 0


def process(filename, style):
    pages = {}
    with open("lesson_blocks\\" + style + "\\" + filename, encoding="utf-8") as f:
        lesson_json = json.load(f)
    for block in lesson_json[filename]:
        pages.setdefault(lesson_json[filename][block]['page'], []).append(lesson_json[filename][block])

    all_lesson_blocks = []
    for page in pages:
        if style in ["style_07", "style_10", "style_02", "style_06"]:
            sorted_text = sorted(pages[page], key=cmp_to_key(compare_07))
        elif style in ["style_09", "style_01", "style_01-5"]:
            sorted_text = sorted(pages[page], key=cmp_to_key(compare_09))
        elif style in ["style_08"]:
            sorted_text = []
            sections = section_08(pages[page])
            for section in sections:
                if 'heading' in sections[section]:
                    sorted_text.append(sections[section]['heading'])
                sorted_section = sorted(sections[section]['blocks'], key=cmp_to_key(compare_07))
                sorted_text.extend(sorted_section)
        # for text in sorted_text:
        # print(text["text"])
        all_lesson_blocks.extend(sorted_text)
    return all_lesson_blocks


def process_other(filename):
    pages = {}
    with open("lesson_blocks\\other-teaching\\" + filename, encoding="utf-8") as f:
        lesson_json = json.load(f)
    for block in lesson_json[filename]:
        pages.setdefault(lesson_json[filename][block]['page'], []).append(lesson_json[filename][block])

    all_lesson_blocks = []
    for page in pages:
        sorted_actually = False
        ## TODO: Go through and see which tag (like 'a-2-column') the doc has, and then use the compare function
        for block in pages[page]:
            if block['text'] == 'a-1-column':
                sorted_text = sorted(pages[page], key=cmp_to_key(compare_09))
                sorted_actually =True
                break
            elif block['text'] == 'a-2-columns':
                sorted_text = sorted(pages[page], key=cmp_to_key(compare_09))
                sorted_actually = True
                break
            elif block['text'] == 'a-2-flowing-columns':
                sorted_text = sorted(pages[page], key=cmp_to_key(compare_07))
                sorted_actually = True
                break

        if sorted_actually == False:
            sorted_text = sorted(pages[page], key=cmp_to_key(compare_09))

        for text in sorted_text:
            if text["type"] not in ['a-1-column','a-2-columns','a-2-flowing-columns']:
                all_lesson_blocks.append(text)


    return all_lesson_blocks


def XMLize(lesson_blocks, style, filename):
    filename = 'simple_XML_lessons\\' + style + "\\" + filename + ".xml"
    with open(filename, 'w', encoding='utf-8') as xml_file:
        for lesson_block in lesson_blocks:
            A_tag = "<" + lesson_block["type"] + ">"
            Z_tag = "</" + lesson_block["type"] + ">\n"
            file_line = " ".join([A_tag, lesson_block['text'], Z_tag])
            xml_file.write(file_line)


"""

styles = ['style_01', 'style_01-5', 'style_02', 'style_06', 'style_07', 'style_08', 'style_09']
for style in styles:
    for file in os.listdir("labeled_files\\" + style + "\\"):
        lesson = process(file, style)
        XMLize(lesson, style, file[:-5])
"""

for file in os.listdir("labeled_files\other-teaching\\"):
    lesson = process_other(file)
    XMLize(lesson, "other-manuals", file[:-5])