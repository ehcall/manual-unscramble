import json
import os
import re
import shutil
import random
import string
from natsort import os_sorted
"""
 Takes downloaded files from DocumentAI export and saves them in this project, renaming them in the process
"""
def save_files(style):
    source_path = "C:\\Users\elena\Documents\Manuals\Google Labeled\\" + style + "\\"
    dest_path = "labeled_files\\" + style
    origin_files = {}
    name_files = []
    for root, dirs, files in os.walk(source_path):
        for name in files:
            if name.endswith(".json"):
                origin = os.path.join(root, name)
                origin_files[name] = origin
                name_files.append(name)
               # print(name)
    for i, edited in enumerate(os_sorted(name_files)):
       # print(i, edited, origin_files[edited])
        new_name = dest_path + "\\" + edited[0:10] + str(i+1) + ".json"
       # print(new_name)
        shutil.copy(origin_files[edited], new_name)

"""
 From the file json, pull the essentials from each block
 - block id
 - text
 - type (inset, graphics_caption, body_text, heading)
 - page number
 - vertices
 
 returns the simplified dictionary
"""
def parse_json(filename, style):
   # print(filename)
   # print("parsing json...")
    lesson = {}
    with open("labeled_files\\" + style + "\\" + filename, encoding="utf-8") as f:
        lesson_json = json.load(f)
        page_blocks = lesson_json["entities"]
        #print(page_blocks)
        lesson[filename] = {}
        for block in page_blocks:
           # print(block["id"])
           try:
                 block_text = block["mentionText"]
           except:
               block_test = ""
           block_type = block["type"]
           if block_type in ["a-2-flowing-columns","a-2-columns","a-1-column"]:
               block_text = block_type
           elif block_type not in ["heading","inset","body-text","body_text","graphics_caption","graphics-caption"]:
                 print(block_type)
                 continue

           if "page" in block["pageAnchor"]["pageRefs"][0]:
                block_page = block["pageAnchor"]["pageRefs"][0]["page"]
           else:
                block_page = 0
           block_vertices = block["pageAnchor"]["pageRefs"][0]["boundingPoly"]["normalizedVertices"]

           lesson[filename][block["id"]] = {
                "text": block_text,
                "page": block_page,
                "vertices": block_vertices,
                "type": block_type,
            }
    return (lesson)


def save_json(filename, lesson, style):
    new_filepath = "lesson_blocks\\" + style + "\\" + filename
    with open(new_filepath, 'w') as file:
        json.dump(lesson, file, indent=4)

# save_files("style_07")

style = "other-teaching"
save_files(style)
for file in os.listdir("labeled_files\\" + style + "\\"):
    if re.search('_S', file):
        print(file)
        pass
    else:
        # print("looping...")
        lesson = parse_json(file, style)
       # print(lesson)
        save_json(file, lesson, style)

#filename = "BM_2023_A-10-273-1-5.json"
#lesson = parse_json(filename)
#rename_file_random(filename)

#print(lesson)

