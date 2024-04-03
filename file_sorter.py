import json
import os
import shutil

"""
 Takes downloaded files from DocumentAI export and saves them in this project
"""
def save_files(style_folder):
    for root, dirs, files in os.walk("C:\\Users\elena\Documents\Manuals\Google Labeled\\" + style_folder + "\\"):
        for name in files:
            if name.endswith(".json"):
                origin = os.path.join(root, name)
                shutil.copy(origin, "labeled_files\\" + style_folder)

## TODO: idk if I need to rename files?
def rename_files(style_folder):
    files = {}
    """
        Split filenames, saving them in a dict with the original filename as key, with values of manual and the page nums as a list
    """
    for filename in os.listdir("labeled_files\\" + style_folder):
        files[filename] = {"manual":"","pages":[]}
        files[filename]["manual"] = filename[0:9]
        files[filename]["pages"] = filename[10:-5].split('-')

    """
        Sort the files by page number
    """
   # for file in files:
   #     print(file)
   #     print(files[file])

"""
 From the file json, pull the essentials from each block
 - block id
 - text
 - type (inset, graphics_caption, body_text, heading)
 - page number
 - vertices
 
 returns the simplified dictionary
"""
def parse_json(filename):
    lesson = {}
    # TODO: adjust this to be dynamic
    with open("labeled_files\style_07\\" + filename, encoding="utf-8") as f:
        lesson_json = json.load(f)
    page_blocks = lesson_json["entities"]
    for block in page_blocks:
        block_text = block["mentionText"]
        block_type = block["type"]
        if "page" in block["pageAnchor"]["pageRefs"][0]:
            block_page = block["pageAnchor"]["pageRefs"][0]["page"]
        else:
            block_page = 0
        block_vertices = block["pageAnchor"]["pageRefs"][0]["boundingPoly"]["normalizedVertices"]

        lesson[filename] = {
            "id": block["id"],
            "text": block_text,
            "page": block_page,
            "vertices": block_vertices,
            "type": block_type,
        }
    return (lesson)


filename = "BM_2023_A-10-273-1-5.json"
lesson = parse_json(filename)
print(lesson)