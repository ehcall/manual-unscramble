"""

"""
import os
import shutil

for root, dirs, files in os.walk("C:\\Users\elena\Documents\Manuals\Google Labeled\style_10\\"):
    for name in files:
        if name.endswith(".json"):
            origin = os.path.join(root, name)
            shutil.copy(origin, "labeled_files\style_10")